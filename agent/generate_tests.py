from pathlib import Path
from github import Github
from github import Auth
import os
from openai import OpenAI
import ast

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



def main():
    src_dir = Path("src")
    test_dir = Path("tests")
    test_dir.mkdir(exist_ok=True)

    for file in src_dir.glob("*.py"):
        if not "___init__" in str(file): 
            print(str(Path(file).stem))
            
            test_code = refine_until_strong(file)
            test_file = test_dir / f"test_{Path(file).stem}.py"
            commit_file(str(test_file), test_code)
            


def commit_file(path, content):
    g = Github(auth=auth)
    repo = g.get_repo("kramalakshmi/API")

    try:
        existing = repo.get_contents(path)
        repo.update_file(
            path, "Update generated tests", content, existing.sha
        )
    except:
        repo.create_file(
            path, "Add generated tests", content , branch= "Agents"
        )



def write_to_github(path, message, content, branch="main"):
    try:
        # Check if the file already exists to update it
        contents = repo.get_contents(path, ref=branch)
        repo.update_file(contents.path, message, content, contents.sha, branch=branch)
        print(f"File '{path}' updated successfully.")
    except Exception:
        # If the file doesn't exist, create it
        repo.create_file(path, message, content, branch=branch)
        print(f"File '{path}' created successfully.")

def generate_tests_file(code, filename, error=None, coverage_feedback=None):
    
    prompt = f"""
    Generate minimal pytest tests for {filename}.
    No comments, no blank lines, no placeholders.
    Ensure valid Python.

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
    with tempfile.TemporaryDirectory() as tmp:
        test_path = f"{tmp}/test_generated.py"
        src_path = f"{tmp}/{source_file}"

        with open(test_path, "w") as f:
            f.write(test_code)

        with open(src_path, "w") as f:
            f.write(open(source_file).read())

        result = subprocess.run(
            ["pytest", "--maxfail=1", "--disable-warnings", "-q", "--cov", tmp],
            capture_output=True,
            text=True
        )

        return result.stdout + "\n" + result.stderr


def refine_until_strong(file_path, max_attempts=5):
    code = Path(file_path).read_text()
    filename = str(Path(file_path).stem)
    test_code = generate_tests_file(code, filename)
    attempt = 0

    while attempt < max_attempts:
        # 1. Syntax check
        try:
            ast.parse(test_code)
        except SyntaxError as e:
            test_code = generate_tests_file(code, filename, error=str(e))
            attempt += 1
            continue

        # 2. Run pytest + coverage
        feedback = run_pytest_and_collect_feedback(test_code, filename)

        # Stop if everything passed
        if "failed" not in feedback and "ERROR" not in feedback:
            return test_code

        # 3. Auto‑fix import errors
        if "ImportError" in feedback or "ModuleNotFoundError" in feedback:
            test_code = generate_tests_file(code, filename, coverage_feedback=feedback)
            attempt += 1
            continue

        # 4. Coverage‑guided refinement
        if "coverage" in feedback.lower() or "missing" in feedback.lower():
            test_code = generate_tests_file(code, filename, coverage_feedback=feedback)
            attempt += 1
            continue

        # 5. Runtime errors
        if "E   " in feedback:
            test_code = generate_tests_file(code, filename, coverage_feedback=feedback)
            attempt += 1
            continue

    raise RuntimeError("Failed to generate strong tests after refinement attempts")
if __name__ == "__main__":
    main()
