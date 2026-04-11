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

def generate_tests_for_missing_functions(source_code, missing_funcs,source_name):
    prompt = f"""
You are analyzing coverage results for a Python module.

Rules:

1. Missing lines that map to "<module>" represent top‑level code such as:
   - the `if __name__ == "__main__":` block
   - print statements
   - example usage
   - any code outside functions

2. You must NOT generate tests for "<module>" lines.
   - Do NOT create tests for the main block.
   - Do NOT import any module named "main" or "main_module".
   - Do NOT attempt to execute or validate example usage code.

3. Only generate tests for REAL functions:
   - Functions with actual names (e.g., get_data, post_data, put_data)
   - Ignore any missing lines belonging to "<module>"

4. Never guess or invent imports.
   - Use ONLY the provided import header for project modules.
   - Do NOT import "main", "main_module", or anything related to the main block.

5. Output ONLY pytest test functions for the missing real functions.

Inputs:
- Missing items: {missing_funcs}
- Source code: {source_code}
- Import header to use at the top of the test file:

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
- Include import {source_name}

Your task:
- Identify which missing items correspond to real functions.
- Ignore all "<module>" entries.
- Generate pytest tests ONLY for the real functions.
- Do not include comments or explanations.
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
    
    missing = get_missing_functions(
    source_path=os.path.join(tmp,"src", source_file),
    coverage_file=os.path.join(tmp, ".coverage")
    )
    
    print("Missing:", ", ".join(missing))
    missingList = ", ".join(missing)

    parts = missingList.split("Missing")[-1].strip(": ").split(",")
    funcs = {
    p.split(":")[0].strip()
    for p in parts
    if p.split(":")[0].strip() != "<module>"
}

    print("List of functions "+str( list(funcs)))
    return list(funcs)




def get_missing_functions(source_path, coverage_file):
    cov = Coverage(data_file=coverage_file)
    cov.load()

    analysis = cov.analysis2(source_path)
    missing_lines = analysis[3]  # list of missing line numbers
    print("Missing lines:", missing_lines)

    print(str(source_path))
    with open(source_path) as f:
        tree = ast.parse(f.read())

    top_level = [node for node in tree.body]

    regions  = []
    for i, node in enumerate(top_level):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            # end is just before the next top-level node, or large number
            if i + 1 < len(top_level):
                end = top_level[i + 1].lineno - 1
            else:
                end = 10**9
            regions.append((node.name, start, end))

    # Map line numbers → function names
    result = []
    for line in missing_lines:
        func_name = None
        for name, start, end in regions:
            if start <= line <= end:
                func_name = name
                break
        if func_name:
            result.append(f"{func_name}:{line}")
        else:
            # line is not inside any function (e.g., main block)
            result.append(f"<module>:{line}")

    

    return result
    


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
        #cov_output = run_coverage_for_module(module_name, cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
        test_code = Path(test_file).read_text()
        #cov_output= run_pytest_and_collect_feedback(test_code, source_file)
        feedback, coverage_percentage, missing_funcs= run_pytest_and_collect_feedback(test_code, source_file)
        

        if not missing_funcs:
            print("All functions already covered.")
            return

        print("Missing coverage for:", missing_funcs)

        new_tests = generate_tests_for_missing_functions(source_code, missing_funcs,module_name)
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
        existing = repo.get_contents(path,ref="e_commerce")
        print("Path "+ path)
        
        repo.update_file(
            path, "Update generated tests", content, existing.sha, branch= "e_commerce"
        )
    except:
        repo.create_file(
            path, "Add generated tests", content , branch= "e_commerce"
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
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)   

    


- Do not include comments or explanations in the output.
- Do NOT guess filenames; use only the filenames provided to you.

- Do NOT invent modules.

IMPORT RULES (MANDATORY — DO NOT VIOLATE):

1. All imports in test files MUST use the full module path:
   from src.<module> import <symbol>

2. NEVER use bare imports such as:
   import cart
   from cart import Cart
   import src
   import src.cart

3. NEVER shorten or rewrite module paths.
   The test must mirror the source code’s import path exactly.

4. The only valid import pattern is:
   from src.<module> import <symbol>

5. If the source file imports from "src.cart", the test MUST import:
   from src.cart import Cart

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
        for root, dirs, files in os.walk(tmp):
            print("ROOT:", root)
            print("DIRS:", dirs)
            print("FILES:", files)
            print("-" * 40)


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
                missing_funcs = get_uncovered_functions(cov_output,os.path.basename(source_file),tmp)
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
                    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
                    
                    
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
                    new_tests = generate_tests_for_missing_functions(source_code, missing_funcs,Path(filename).stem)
                    print(new_tests)
                    #print(get_import_statements(new_tests))
                    content = test_code + "\n" + new_tests + "\n"
                    test_file = str(Path("tests")) +"/" + f"test_{Path(filename).stem}.py"
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
