from pathlib import Path
from github import Github
from github import Auth
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def generate_tests_for_file(file_path):
    code = Path(file_path).read_text()

    prompt = f"""
    Generate pytest unit tests for the following Python code.
    Use clear, deterministic test cases.

    Code:
    {code}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content



def main():
    src_dir = Path("src")
    test_dir = Path("tests")
    test_dir.mkdir(exist_ok=True)

    for file in src_dir.glob("*.py"):
        print(str(Path(file).stem))
        
        test_code = generate_tests_for_file(file)
        test_file = test_dir / f"test_{Path(file).stem}.py"
        commit_file(str(test_file), test_code)
        


def commit_file(path, content):
    g = Github(TOKEN)
    repo = g.get_repo(REPO)

    try:
        existing = repo.get_contents(path)
        repo.update_file(
            path, "Update generated tests", content, existing.sha
        )
    except:
        repo.create_file(
            path, "Add generated tests", content
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


if __name__ == "__main__":
    main()
