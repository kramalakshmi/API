import pathlib
from github import Github
import os




def main():
    TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(TOKEN)

    repo = g.get_repo("kramalakshmi/API")

    src_dir = pathlib.Path("src")
    test_dir = pathlib.Path("tests")
    test_dir.mkdir(exist_ok=True)

    test_file = test_dir / "test_file.py"

    repo.create_file(
    path="folder/new_file.txt",      # Path and name of the file
    message="Initial commit",       # Commit message
    content="Hello, GitHub!")

# Close connection
g.close()
    #commit_file(str(test_file), "Hello GitHub! This file was written using PyGithub.")

    '''src_dir = pathlib.Path("src")
    test_dir = pathlib.Path("tests")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "te_create.py"
    test_file.write_text("test")
    print("test "+str(test_dir))
    #commit_file(str(test_file), "Test")
    file_path = "tests/test_create.txt"
    commit_msg = "Automated commit from Python"
    file_content = "Hello GitHub! This file was written using PyGithub."
    '''
    #write_to_github(file_path, commit_msg, file_content)
def commit_file(path, content):
    TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(TOKEN)
    repo = g.get_repo("kramalakshmi/API")
    #repo = g.get_repo(REPO)

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
