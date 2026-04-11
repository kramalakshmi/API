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

PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
TEST_FILE = os.path.join(TESTS_DIR, "test_generated.py")
COV_FILE = os.path.join(PROJECT_ROOT, ".coverage")


def run_pytest_with_coverage() -> subprocess.CompletedProcess:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--maxfail=1",
        "--disable-warnings",
        "-q",
        "--cov=src",
        "--cov-report=term-missing",
    ]
    return subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)


def load_coverage_for_file(py_file: str) -> Tuple[str, List[int], List[int]]:
    cov = Coverage(data_file=COV_FILE)
    cov.load()
    filename, executed, missing, _ = cov.analysis2(py_file)[:4]
    return filename, executed, missing

def build_function_regions(source_path: str) -> List[Tuple[str, int, int]]:
    with open(source_path, "r", encoding="utf-8") as f:
        code = f.read()
    tree = ast.parse(code)
    top_level = list(tree.body)

    regions = []
    for i, node in enumerate(top_level):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            if i + 1 < len(top_level):
                end = top_level[i + 1].lineno - 1
            else:
                end = 10**9
            regions.append((node.name, start, end))
    return regions


def map_missing_to_functions(source_path: str, missing_lines: List[int]) -> List[str]:
    regions = build_function_regions(source_path)
    result = []
    for line in missing_lines:
        func_name = "<module>"
        for name, start, end in regions:
            if start <= line <= end:
                func_name = name
                break
        result.append(f"{func_name}:{line}")
    return result

def extract_missing_functions(src_dir: str) -> Set[str]:
    funcs: Set[str] = set()
    for fname in os.listdir(src_dir):
        if not fname.endswith(".py") or fname == "__init__.py":
            continue
        path = os.path.join(src_dir, fname)
        _, _, missing = load_coverage_for_file(path)
        mapped = map_missing_to_functions(path, missing)
        for item in mapped:
            name, _ = item.split(":", 1)
            name = name.strip()
            if name != "<module>":
                funcs.add(name)
    return funcs

def fix_import_header(test_code: str) -> str:
    lines = test_code.splitlines()
    external_imports = []
    body_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            if any(k in stripped for k in ("src", "main", "RequestAPI", "sample_app")):
                continue
            external_imports.append(line)
        else:
            body_lines.append(line)

    src_dir = SRC_DIR
    header = [
        "import sys",
        "import os",
        f"sys.path.append(os.path.abspath(r'{src_dir}'))",
    ]

    for fname in os.listdir(src_dir):
        if fname.endswith(".py") and fname != "__init__.py":
            mod = fname[:-3]
            header.append(f"import {mod}")

    header.append("")
    return "\n".join(header + external_imports + [""] + body_lines).strip() + "\n"

def ensure_test_file_exists() -> None:
    os.makedirs(TESTS_DIR, exist_ok=True)
    if not os.path.exists(TEST_FILE):
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            f.write("")

def refine_once() -> None:
    ensure_test_file_exists()

    result = run_pytest_with_coverage()
    with open(os.path.join(PROJECT_ROOT, "pytest_output.log"), "w", encoding="utf-8") as f:
        f.write(result.stdout)
        f.write("\n=== STDERR ===\n")
        f.write(result.stderr)

    if result.returncode == 0 and "coverage" in result.stdout.lower():
        print("Tests passing; coverage already computed.")
    else:
        print("Pytest failed or coverage incomplete, proceeding with refinement.")

    missing_funcs = extract_missing_functions(SRC_DIR)
    if not missing_funcs:
        print("No missing functions detected.")
        return

    with open(TEST_FILE, "r", encoding="utf-8") as f:
        existing = f.read()

    new_tests = generate_tests_for_functions(missing_funcs)
    combined = existing.rstrip() + "\n\n" + new_tests if existing.strip() else new_tests
    fixed = fix_import_header(combined)

    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write(fixed)

    print(f"Refinement applied. Missing functions: {sorted(missing_funcs)}")


if __name__ == "__main__":
    refine_once()
  


