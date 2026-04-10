from pathlib import Path
from github import Github
from git import Repo
from github import Auth
import os
from openai import OpenAI
import ast
import subprocess
import tempfile
import re
from coverage import Coverage

repo_structure = """
        project/
            src/
                __init__.py
                RequestAPI.py
            tests/
                test_RequestAPI.py
        """


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5.4"
TOKEN = os.getenv("PAT")
auth = Auth.Token(TOKEN)


def generate_tests_for_file(file_path):
    code = Path(file_path).read_text()
    
    prompt = f"""
    Generate pytest unit tests for the following Python code.
    Use clear, deterministic test cases.
    Return only the Python code. Do not include explanations,Do not include comments and Do not include docstrings
    I want pytest tests without any extra lines, no chatter, no comments, no unnecessary whitespace, no print statements, no example usage.
Just clean, minimal test code.


    Code:
    {code}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert Python developer. Write only the code, no explanations ,  comments, or docstrings. I want pytest tests without any extra lines, no chatter, no comments, no unnecessary whitespace, no print statements, no example usage.Just clean, minimal test code."},
        {"role": "user", "content": prompt}]
            
    )

    return response.choices[0].message.content

def get_import_statements(code: str):
    tree = ast.parse(code)
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else ""))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(
                alias.name + (f" as {alias.asname}" if alias.asname else "")
                for alias in node.names
            )
            imports.append(f"from {module} import {names}")

    return imports


def get_function_names(source_code):
    tree = ast.parse(source_code)
    return [
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]

def generate_tests_for_missing_functions(source_code, missing_funcs):
    prompt = f"""
Generate pytest tests ONLY for these functions:
{missing_funcs}

Source code:
{source_code}

Rules:
- No comments
- No blank lines
- Return only code for missing functions
- 
- External imports must be returned exactly as they appear.
- Project imports must NOT be returned; use the provided header instead.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    
- Then import all filenames under src folder
- Do not guess or invent imports.
- Do not include comments or explanations in the output.
-Do NOT invent modules.
    
"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

def get_test_file_path(source_file):
    base = os.path.splitext(os.path.basename(source_file))[0]
    test_file = f"tests/test_{base}.py"
    return test_file if os.path.exists(test_file) else None



def run_coverage_for_module(module_name, cwd):
    result = subprocess.run(
        [
            "pytest",
            "-q",
            f"--cov={module_name}",
            "--cov-report=term-missing",
        ],
        cwd=cwd,
        capture_output=True,
        text=True
    )



    
    print(str(result.stdout) + "\n" + str(result.stderr))
    return result.stdout + "\n" + result.stderr
    
def get_uncovered_functions(coverage_output,source_file,tmp):
    #print(coverage_output)
    missing_line = None
    
    lines = coverage_output.splitlines()
    for i in range(1,len(lines)):
        current_line = lines[i]
        if "%" in current_line:
            missing_line = current_line
            break
   
    if not missing_line:
        return []
    print("missing_line "+missing_line)
    # Example: "Missing: func_a:5, func_c:12"
    with open(os.path.join(tmp, ".coverage")) as f:
        coverage_file = f.read()
        print(coverage_file)
    missing = get_missing_functions(
    source_path=os.path.join(tmp, source_file),
    coverage_file=os.path.join(tmp, ".coverage")
    )
    
    print("Missing:", ", ".join(missing))
    missingList = ", ".join(missing)

    parts = missingList.split("Missing")[-1].strip(": ").split(",")
    funcs = {p.split(":")[0].strip() for p in parts}
    print("List of functions "+str( list(funcs)))
    return list(funcs)




def get_missing_functions(source_path, coverage_file):
    cov = Coverage(data_file=coverage_file)
    cov.load()

    analysis = cov.analysis2(source_path)
    missing_lines = analysis[3]  # list of missing line numbers

    with open(source_path) as f:
        tree = ast.parse(f.read())

    # Map line numbers → function names
    func_map = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for lineno in range(node.lineno, node.end_lineno + 1):
                func_map[lineno] = node.name

    # Build output
    missing = []
    for line in missing_lines:
        func = func_map.get(line, None)
        if func:
            missing.append(f"{func}:{line}")

    return missing
    


def incremental_test_generation(source_file):
    with open(source_file) as f:
        source_code = f.read()

    funcs = get_function_names(source_code)
    test_file = get_test_file_path(source_file)

    # If no test file exists → generate full test suite
    if not test_file:
        print("No test file found. Generating full test suite.")
        test_code = refine_until_strong(source_file)
        test_file_name = Path("tests") / f"test_{Path(source_file).stem}.py"
        commit_file(str(test_file_name), test_code)

    # Test file exists → run coverage
    else:
        print("Test file exists. Running coverage... for "+test_file)
        module_name = os.path.splitext(os.path.basename(source_file))[0]
        print(os.path.basename(source_file))
        print(module_name )
        #cov_output = run_coverage_for_module(module_name, cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        test_code = Path(test_file).read_text()
        #cov_output= run_pytest_and_collect_feedback(test_code, source_file)
        feedback, coverage_percentage, missing_funcs= run_pytest_and_collect_feedback(test_code, source_file)
        #missing_funcs = get_uncovered_functions(cov_output,os.path.basename(source_file),tmp)

        if not missing_funcs:
            print("All functions already covered.")
            return

        print("Missing coverage for:", missing_funcs)

        new_tests = generate_tests_for_missing_functions(source_code, missing_funcs)
        print(new_tests)
        #print(get_import_statements(new_tests))
        content = test_code + "\n" + new_tests + "\n"
        commit_file(test_file, content)
        print("New tests added.")
            
def main():
    
    src_dir = Path("src")
    test_dir = Path("tests")
    test_dir.mkdir(exist_ok=True)

    for file in src_dir.glob("*.py"):
        if not "___init__" in str(file): 
            print(str(Path(file).stem))
            incremental_test_generation(file)
            '''
            test_code = refine_until_strong(file)
            
            test_file = test_dir / f"test_{Path(file).stem}.py"
            commit_file(str(test_file), test_code)
            '''
            


def commit_file(path, content):
    
    g = Github(auth=auth)
    repo = g.get_repo("kramalakshmi/API")
    print("Path "+ path)
   
    
    try:
        '''
        #repo = git.Repo(os.getcwd())
        local_repo=Repo(search_parent_directories=True)
        if local_repo.head.is_detached:
            # Handle the detached state (e.g., use the commit hash)
            current_commit = local_repo.head.object.hexsha
            print(f"Detached at: {current_commit}")
        else:
            # Safe to access active_branch
            print(f"On branch: {local_repo.active_branch.name}")
        branch_name=local_repo.active_branch.name
        remote_url= local_repo.remotes.origin.url
        print(remote_url)
        print(branch_name , repo.default_branch)
        # Get the name of the active branch
        current_branch = repo.active_branch.name
        print(f"Current branch: {current_branch}")
        '''
        existing = repo.get_contents(path,ref="GenAItestCase")
        print("Path "+ path)
        
        repo.update_file(
            path, "Update generated tests", content, existing.sha, branch= "GenAItestCase"
        )
    except:
        repo.create_file(
            path, "Add generated tests", content , branch= "GenAItestCase"
        )



def write_to_github(path, message, content, branch="main"):
    try:
        # Check if the file already exists to update it
        contents = repo.get_contents(path, ref=branch)
        repo.update_file(contents.path, message, content, existing.sha, branch=branch)
        print(f"File '{path}' updated successfully.")
    except Exception:
        # If the file doesn't exist, create it
        repo.create_file(path, message, content, branch=branch)
        print(f"File '{path}' created successfully.")

def generate_tests_file(code, filename, error=None, coverage_feedback=None):
    print("In generate_tests_file")
    source_name = str(Path(filename).stem)
    
    prompt = f"""
    Generate minimal pytest tests for {filename}.
    Ensure valid Python.
Rules:
  - No comments, no explanations, no extra text.
- External imports must be returned exactly as they appear.
- For Project imports use only the provided header instead.
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    
- Include import {source_name}
- Do not include any other Project imports
- Do not guess or invent imports.
- Do not include comments or explanations in the output.
- Do NOT guess filenames; use only the filenames provided to you.

- Do NOT invent modules.
    Source code:
    {code}
    """

    if error:
        prompt += f"\nFix this syntax error:\n{error}\nRegenerate corrected tests only."

    if coverage_feedback:
        prompt += f"\nImprove coverage based on this pytest feedback:\n{coverage_feedback}\nRegenerate improved tests only."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content



def run_pytest_and_collect_feedback(test_code, source_file):
    filename = str(Path(source_file).stem)
    print("Running pytest and collecting feedback")
    print ("Code generated" )
    with tempfile.TemporaryDirectory() as tmp:
        test_path = f"{tmp}/tests"
        src_path = f"{tmp}/src"
            
        Path(test_path).mkdir(exist_ok=True)
        Path(src_path).mkdir(exist_ok=True)

        test_path = f"{test_path}/test_generated.py"
        src_path = f"{src_path}/{filename}.py"
            
        with open(test_path, "w") as f:
            f.write(test_code)

        with open(src_path, "w") as f:
            code = Path(source_file).read_text()
            f.write(code)

        with open(test_path, "r") as f:
            print("#######################   TESTING ccode ######################")
            #print(test_path)
            context = f.read()
            print(context)

        
        print("Sanity check import:")
        try:
            import sys, os
            print(os.listdir(tmp))
            print(test_path)
            print(src_path)
            print(os.getcwd())
            sys.path.append(os.getcwd())

            sys.path.append(tmp)  # tmp is your TemporaryDirectory path
            import RequestAPI
            print("SUCCESS: RequestAPI imported")
        except Exception as e:
            print("FAILED:", e)

        # Run pytest with coverage on the specific source file
        result = subprocess.run(
            ["pytest", "--maxfail=1", "--disable-warnings", "-q",
             "--cov", filename, "--cov-report=term-missing"],
            cwd=tmp,
            capture_output=True,
            text=True
        )

        '''
        result = subprocess.run(["pytest", "--maxfail=1", "--disable-warnings", "-q", "--cov", src_path],
            capture_output=True,
            text=True
        )
        '''
        
        cov_output= result.stdout + "\n" + result.stderr
        print( "Coverage generated "+ cov_output)
        match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", cov_output)
        covePer= int(match.group(1))
        if match:
            print("COverage percentage "+str(covePer ))
            if covePer == 100:
                return result.stdout + "\n" + result.stderr, covePer,[]
            else:
                missing_funcs = get_uncovered_functions(cov_output,os.path.basename(source_file),tmp+"/src")
                return result.stdout + "\n" + result.stderr,covePer,missing_funcs
            
                 

def refine_until_strong(file_path, max_attempts=5):
    
    source_code = Path(file_path).read_text()
    filename = str(Path(file_path))
    test_code = generate_tests_file(source_code, filename)
    attempt = 0
    print("Attempt "+str(attempt))
    while attempt < max_attempts:
        # 1. Syntax check
        try:
            ast.parse(test_code)
            print("Parsed code")
        except SyntaxError as e:
            test_code = generate_tests_file(source_code, filename, error=str(e))
            attempt += 1
            continue

        # 2. Run pytest + coverage
        feedback, coverage_percentage, missing_funcs = run_pytest_and_collect_feedback(test_code, filename)

        print("Feedback after pytest "+str(feedback))

        # 3. Auto‑fix import errors
        if "ImportError" in feedback or "ModuleNotFoundError" in feedback:
            print("Import error")
            test_code = generate_tests_file(source_code, filename, coverage_feedback=f"""
        
                    Fix the import errors shown below.
            
                    Replace the import with EXACTLY this block:
            
                    import sys
                    import os
                    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
                    
                    import RequestAPI

            
                    Do NOT use 'import src.RequestAPI'.
                    Do NOT invent modules.
                    {feedback}
                    
                    """
            )
            attempt += 1
            continue
        print("No import error found.. MOving on")
        # 4. Coverage‑guided refinement
        try:
            if coverage_percentage == 100:
                print("No coverage missing .. MOving on")
                return test_code
            else:
                if not missing_funcs:
                    print("All functions already covered.")
                    return
                else:
                    print("Missing coverage for:", missing_funcs)
                    new_tests = generate_tests_for_missing_functions(source_code, missing_funcs)
                    print(new_tests)
                    #print(get_import_statements(new_tests))
                    content = test_code + "\n" + new_tests + "\n"
                    test_file = str(Path("tests")) / f"test_{Path(filename).stem}.py"
                    commit_file(test_file, content)
                    print("New tests added.")
                    attempt += 1
                    print("Attempt "+str(attempt))
                    feedback, coverage_percentage, missing_funcs = run_pytest_and_collect_feedback(test_code, filename)
        except Exception as e:
            print("Error during coverage refinement:", e)
            #test_code = generate_tests_file(source_code, filename, coverage_feedback=str(e))
            #attempt += 1
            #continue
        
        # 5. Runtime errors
        if "E   " in feedback:
            print("Runtime errors found")
            test_code = generate_tests_file(source_code, filename, coverage_feedback=feedback)
            attempt += 1
            continue
        # Stop if everything passed
        if "failed" not in feedback and "ERROR" not in feedback:
            return test_code

    raise RuntimeError("Failed to generate strong tests after refinement attempts")
if __name__ == "__main__":
    main()
