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
import shutil
import json
import textwrap

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5.4"
TOKEN = os.getenv("PAT")
auth = Auth.Token(TOKEN)
AGENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(AGENT_DIR, ".."))
max_attempts=5



ERROR_PATTERNS = {
    # 1. Syntax Errors
    "syntax_error": [
        r"SyntaxError",
        r"unexpected EOF",
        r"invalid syntax",
        r"unterminated string",
        r"indentation error",
    ],

    # 2. Import Errors
    "import_error": [
        r"ImportError",
        r"ModuleNotFoundError",
        r"cannot import name",
        r"No module named",
    ],

    # 3. Wrong sys.path Manipulation
    "sys_path_error": [
        r"sys\.path",
        r"ImportError: attempted relative import",
    ],

    # 4. Name Errors
    "name_error": [
        r"NameError",
        r"is not defined",
    ],

    # 5. Wrong Function Signatures
    "signature_mismatch": [
        r"TypeError: .* takes .* arguments? .* given",
        r"TypeError: missing .* required positional argument",
        r"TypeError: .* got an unexpected keyword argument",
    ],

    # 6. Wrong Expected Values
    "wrong_expected_value": [
        r"AssertionError",
        r"assert .* == .*",
        r"Expected .* but got .*",
    ],

    # 7. Missing Exception Tests
    "missing_exception_test": [
        r"did not raise",
        r"Expected .* to raise",
    ],

    # 8. Wrong Use of pytest Fixtures
    "fixture_error": [
        r"fixture .* not found",
        r"fixture '.*' not found",
        r"ScopeMismatch",
    ],

    # 9. Tests That Never Execute Source Code
    "no_execution": [
        r"collected 0 items",
        r"no tests ran",
    ],

    # 10. Tests That Crash Before Running
    "test_crash": [
        r"ERROR at setup",
        r"Failed: DID NOT RAISE",
        r"AttributeError",
    ],

    # 11. Duplicate or Conflicting sys.path Logic
    "duplicate_sys_path": [
        r"sys\.path\.insert",
        r"sys\.path\.append",
    ],

    # 12. Tests for Non‑Existent Files
    "file_not_found": [
        r"FileNotFoundError",
        r"No such file or directory",
    ],

    # 13. Tests That Depend on Global State
    "global_state_error": [
        r"global variable",
        r"stateful",
        r"depends on global",
    ],

    # 14. Incorrect Testing of __main__
    "main_block_error": [
        r"__main__",
        r"if __name__ ==",
    ],
}



def llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

def extract_missing_functions(cov_json_path):
    """
    Returns a list of (file_path, function_name) tuples for all functions
    that have missing coverage across the entire project.

    Example return:
        [
            ("src/cart.py", "add_item"),
            ("src/orders.py", "calculate_total")
        ]
    """

    if not os.path.exists(cov_json_path):
        return []

    try:
        with open(cov_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    missing = []

    # Iterate through all files in coverage.json
    for file_path, file_data in data.get("files", {}).items():
        missing_lines = set(file_data.get("missing_lines", []))
        if not missing_lines:
            continue

        # Function-level coverage info
        functions = file_data.get("functions", {})

        for fn_name, fn_info in functions.items():
            start = fn_info.get("lineno")
            end = fn_info.get("end_lineno")

            if start is None or end is None:
                continue

            fn_lines = set(range(start, end + 1))

            # If any missing line overlaps this function → function is missing coverage
            if fn_lines & missing_lines:
                missing.append((file_path, fn_name))

    return missing

def get_test_file_path(source_file):
    base = os.path.splitext(os.path.basename(source_file))[0]
    test_file = f"tests/test_{base}.py"
    return test_file if os.path.exists(test_file) else None



    



def log_iteration(i, category, stdout, stderr, coverage):
    print(f"\n===== ITERATION {i} =====")
    print("Error Category:", category)
    print("Coverage:", coverage)
    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)

def copy_project_to_tmp(project_root, tmp_root):
    """
    Copies all .py files from project_root into tmp_root,
    preserving folder structure.
    """
    for root, dirs, files in os.walk(project_root):
        # Compute relative path from project root
        rel_path = os.path.relpath(root, project_root)
        dest_dir = os.path.join(tmp_root, rel_path)
        if not rel_path.startswith(".") and not rel_path.startswith("_"):
                # Create destination directory
                os.makedirs(dest_dir, exist_ok=True)
        
                # Copy only .py files
                for f in files:
                    if f.endswith(".py"):
                        src_file = os.path.join(root, f)
                        dest_file = os.path.join(dest_dir, f)
                        shutil.copy2(src_file, dest_file)
                        print(f"Copying {str(src_file)} to {str(dest_file)}...")

    return tmp_root

def extract_module_error(stderr, stdout, module_name):
    text = stderr + "\n" + stdout
    lines = [line for line in text.splitlines() if module_name in line or "ERROR" in line]
    return "\n".join(lines)

def run_pytest(tmp):
     # Run pytest with coverage on the specific source file
    result = subprocess.run(
        ["pytest", "--maxfail=1", "--disable-warnings", "-q",
            "--cov=src", "--cov-report=term-missing", "--cov-report=json:coverage.json"],
        cwd=tmp,
        capture_output=True,
        text=True
    )
    print("Pytest completed with return code:", result.stdout+" \n"+result.stderr+"\n "+str(result.returncode))
    if result.returncode != 0:
        print("Pytest failed. STDOUT:\n", result.stdout)
        print("Pytest failed. STDERR:\n", result.stderr)
        error_categories = classify_errors(result.stderr, result.stdout)


    return result.stdout, result.stderr, result.returncode



import ast

def extract_function_signatures(source: str) -> dict:
    """
    Extracts function signatures from module source code.
    Returns:
        { function_name: [arg1, arg2, ...] }
    """
    tree = ast.parse(source)
    signatures = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            args = []
            for a in node.args.args:
                args.append(a.arg)

            # Ignore self for class methods
            if args and args[0] == "self":
                args = args[1:]

            signatures[node.name] = args

    return signatures


def detect_signature_mismatches(module_source: str, test_source: str):
    """
    Detects incorrect function calls in test code by comparing them
    to the real function signatures extracted from the module.

    Returns a list of:
    {
        "function": "get_product",
        "expected": ["product_id"],
        "actual": ["x", "y"]
    }
    """
    mismatches = []

    # Extract real signatures
    real_sigs = extract_function_signatures(module_source)

    # Parse test file
    try:
        tree = ast.parse(test_source)
    except Exception:
        # If test file is broken, skip signature detection
        return mismatches

    # Walk through all function calls
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        # Identify function name
        fn_name = None

        # Case: direct call → get_product(...)
        if isinstance(node.func, ast.Name):
            fn_name = node.func.id

        # Case: attribute call → module.get_product(...)
        elif isinstance(node.func, ast.Attribute):
            fn_name = node.func.attr

        if fn_name not in real_sigs:
            continue

        expected = real_sigs[fn_name]

        # Extract actual arguments
        actual = []

        # Positional args
        for arg in node.args:
            if isinstance(arg, ast.Name):
                actual.append(arg.id)
            else:
                actual.append("<value>")

        # Keyword args
        for kw in node.keywords:
            actual.append(kw.arg)

        # Compare lengths
        if len(actual) != len(expected):
            mismatches.append({
                "function": fn_name,
                "expected": expected,
                "actual": actual
            })
            continue

        # Compare keyword names (if used)
        kw_names = [kw.arg for kw in node.keywords]
        if kw_names and kw_names != expected:
            mismatches.append({
                "function": fn_name,
                "expected": expected,
                "actual": actual
            })

    return mismatches



def classify_errors(stderr: str, stdout: str) -> list:
    """
    Returns a list of detected error categories based on regex patterns.
    """
    text = stderr + "\n" + stdout
    detected = []

    for category, patterns in ERROR_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(category)
                break

    return detected


def read_coverage(tmp_root):
    """
    Reads coverage.json generated by pytest-cov and returns the total
    percent_covered as a float. Returns 0.0 if the file is missing or invalid.
    """
    cov_path = os.path.join(tmp_root, "coverage.json")

    if not os.path.exists(cov_path):
        return 0.0

    try:
        with open(cov_path) as f:
            data = json.load(f)

        # pytest-cov stores totals under data["totals"]["percent_covered"]
        return float(data.get("totals", {}).get("percent_covered", 0.0))

    except Exception:
        # If JSON is malformed or missing fields
        return 0.0


def missing_functions_for_module(cov_json_path, module_name):
    """
    Returns a list of function names that have missing coverage
    for the given module (e.g., 'cart', 'orders', etc.).

    Example return:
        ["add_item", "remove_item"]
    """
    if not os.path.exists(cov_json_path):
        return []

    try:
        with open(cov_json_path) as f:
            data = json.load(f)
    except Exception:
        return []

    missing_fns = []

    # Iterate through all files in coverage.json
    for file_path, file_data in data.get("files", {}).items():
        # Only consider this module
       
        if not file_path.endswith(f"{module_name}.py"):
            continue
        
        print("Missing lines:", file_data.get("missing_lines"))
        missing_lines = set(file_data.get("missing_lines", []))
        if not missing_lines:
            continue

        # Function-level coverage info
        functions = file_data.get("functions", {})

        # Extract function names + start lines
        fn_list = []
        for fn_name, fn_info in functions.items():
            start = fn_info.get("start_line") or fn_info.get("lineno")
            if start is not None:
                fn_list.append((fn_name, start))

        # Sort by start line
        fn_list.sort(key=lambda x: x[1])

        # Infer end lines
        inferred = []
        for i, (fn_name, start) in enumerate(fn_list):
            if i < len(fn_list) - 1:
                end = fn_list[i + 1][1] - 1
            else:
                end = start + 2000  # safe upper bound
            inferred.append((fn_name, start, end))

        # Check overlap with missing lines
        for fn_name, start, end in inferred:
            fn_lines = set(range(start, end + 1))
            if fn_lines & missing_lines:
                missing_fns.append(fn_name)

    

    print(f"Missing functions for module '{module_name}': {missing_fns}")
    return missing_fns

import os
import json

def coverage_for_module(cov_json_path, module_name):
    """
    Returns the percent coverage (0–100 float) for a specific module
    based on pytest-cov's coverage.json.

    Example:
        coverage_for_module("coverage.json", "cart")
        → 87.5
    """

    if not os.path.exists(cov_json_path):
        return 0.0

    try:
        with open(cov_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return 0.0

    # Look for the module file inside coverage.json
    target_file = None
    for file_path, file_data in data.get("files", {}).items():
        if file_path.endswith(f"{module_name}.py"):
            target_file = file_data
            break

    if not target_file:
        return 0.0

    # Extract coverage numbers
    summary = target_file.get("summary", {})
    covered = summary.get("covered_lines")
    total = summary.get("num_statements")

    if covered is None or total in (None, 0):
        return 0.0

    return round((covered / total) * 100, 2)



def refinement_loop(tmp_root,llm,project_root: str, max_iter: int = 10, min_cov: float = 85.0) -> bool:
    """
    Multi-module refinement loop:
    - Copies project to a temp dir
    - For each module in src/:
        - Ensure test file exists
        - If missing → create tests
        - If exists → check module coverage
        - If coverage < threshold → refine tests
    - Repeats until all modules reach coverage or max_iter is hit
    - On success, copies tests back to real project
    """


    copy_project_to_tmp(project_root, tmp_root)
    for iteration in range(1, max_iter + 1):
        print(f"\n===== ITERATION {iteration} =====")

        stdout, stderr, code = run_pytest(tmp_root)
        cov_json_path = os.path.join(tmp_root, "coverage.json")

        total_cov = read_coverage(tmp_root)
        print(f"Total coverage: {total_cov}%")

        src_dir = os.path.join(tmp_root, "src")
        all_modules_done = True

        for module_file in os.listdir(src_dir):
            if not module_file.endswith(".py") and not module_file.startswith("__"):
                continue

            module_name = module_file[:-3]
            test_path = os.path.join(tmp_root, "tests", f"test_{module_name}.py")

            module_cov = coverage_for_module(cov_json_path, module_name)
            print(f"Module {module_name}: {module_cov}%")

            # Extract module-specific error output (you can refine this if you want)
            module_error_output = stderr

            missing_fns = missing_functions_for_module(cov_json_path, module_name)

            # CASE 1: No test file → create new tests
            if not os.path.exists(test_path):
                print(f"[CREATE] No tests for {module_name}. Generating new tests.")
                generate_tests_for_module(
                    tmp_root=tmp_root,
                    module_name=module_name,
                    llm=llm,
                    error_output=module_error_output,
                    missing_functions=missing_fns,
                )
                all_modules_done = False
                continue

            # CASE 2: Test file exists but coverage < threshold → refine
            if module_cov < min_cov:
                print(f"[REFINE] {module_name} coverage {module_cov}% < {min_cov}%. Refining tests.")
                generate_tests_for_module(
                    tmp_root=tmp_root,
                    module_name=module_name,
                    llm=llm,
                    error_output=module_error_output,
                    missing_functions=missing_fns,
                )
                all_modules_done = False
                continue

            print(f"[OK] {module_name} meets coverage threshold ({module_cov}%).")

        if all_modules_done:
            print("All modules meet coverage threshold. Copying tests back to project.")
            copy_tests_from_tmp(tmp_root, project_root)
            return True

    print("Max iterations reached. Some modules did not reach coverage threshold.")
    copy_tests_from_tmp(tmp_root, project_root)
    return False


def refinement_loop_old(tmp_root,project_root, llm, max_iter=5, min_cov=85):
    
    copy_project_to_tmp(project_root, tmp_root)

    for i in range(1, max_iter + 1):
        stdout, stderr, code = run_pytest(tmp_root)
        coverage = read_coverage(tmp_root)
        cov_json = os.path.join(tmp_root, "coverage.json")

        print(f"\n===== ITERATION {i} =====")
        print("Coverage:", coverage)

        if code == 0 and coverage >= min_cov:
            print("Coverage threshold met." + str(coverage))
            return True

        # Extract missing functions per module
        missing = extract_missing_functions(cov_json)

        # For each module in src/
        for module_file in os.listdir(os.path.join(tmp_root, "src")):
            if not module_file.endswith(".py"):
                continue

            module_name = module_file.replace(".py", "")

            # Missing functions for this module
            print(f"\nAnalyzing module '{module_name}'...")
            missing_fns = missing_functions_for_module(cov_json, module_name)

            # Extract module-specific errors
            module_error = extract_module_error(stderr, stdout, module_name)

            # Generate or refine tests for this module
            generate_tests_for_module(
                tmp_root,
                module_name,
                llm,
                module_error,
                missing_fns
            )


    print("Failed to reach coverage threshold.")
    return False


def load_module_source(tmp_root, module_name):
    """
    Loads and returns the full source code of a module inside tmp_root/src/.

    Example:
        load_module_source("/tmp/refine_abc123", "cart")
        → returns contents of /tmp/refine_abc123/src/cart.py
    """
    module_path = os.path.join(tmp_root, "src", f"{module_name}.py")

    if not os.path.exists(module_path):
        return ""  # Safe fallback for missing modules

    with open(module_path, "r", encoding="utf-8") as f:
        return f.read()
    


def generate_tests_for_module(
    tmp_root: str,
    module_name: str,
    llm,
    error_output: str,
    missing_functions: list[str],
):
    """
    Generate or refine tests for a single module using the refinement prompt.
    Writes test_{module_name}.py into tmp_root/tests.
    """

    src_path = os.path.join(tmp_root, "src", f"{module_name}.py")
    tests_dir = os.path.join(tmp_root, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    test_path = os.path.join(tests_dir, f"test_{module_name}.py")

    with open(src_path, "r", encoding="utf-8") as f:
        module_source = f.read()

    if os.path.exists(test_path):
        with open(test_path, "r", encoding="utf-8") as f:
            test_source = f.read()
    else:
        test_source = ""

    # Pre‑pytest signature mismatch detection (optional but powerful)
    try:
        signature_mismatches = detect_signature_mismatches(module_source, test_source) if test_source else []
    except Exception:
        signature_mismatches = []

    # Classify error categories from pytest output
    error_categories = classify_errors(error_output, "")
    print(f"Detected error categories for module '{module_name}': {error_categories}")
    print(f"Detected missing_functions '{missing_functions}': {signature_mismatches}")
    prompt = MODULE_REFINEMENT_PROMPT.format(
        module_name=module_name,
        module_source=module_source,
        test_file=test_source or "# No tests yet. Create a new pytest file.",
        error_output=error_output or "No error output available.",
        error_categories=error_categories or "[]",
        missing_functions=missing_functions or "[]",
        signature_mismatches=signature_mismatches or "[]",
    )

    new_tests = llm(prompt)
    new_tests = textwrap.dedent(new_tests).strip()

    with open(test_path, "w", encoding="utf-8") as f:
        f.write(new_tests + "\n")


MODULE_PROMPT = """
You are generating or fixing pytest tests for a single module.

==========================
MODULE NAME
==========================
{module_name}

==========================
MODULE SOURCE CODE
==========================
{module_source}

==========================
CURRENT TEST FILE (if exists)
==========================
{test_file}

==========================
PYTEST ERROR OUTPUT (for this module)
==========================
{error_output}

==========================
MISSING FUNCTIONS (from coverage)
==========================
{missing_functions}

==========================
MANDATORY RULES
==========================

1. Output MUST be valid Python ONLY.
   - No Markdown.
   - No backticks.
   - No code fences.

2. The test file MUST begin with this exact header:

import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

3. All imports MUST use:
   from src.{module_name} import <symbol>

4. NEVER use:
   import {module_name}
   from {module_name} import X
   import src
   import src.{module_name}
   sys.path.append("src")

5. Generate tests for ALL functions and methods in this module.
6. Include normal cases, edge cases, and exception cases.
7. Tests must be deterministic and minimal.
8. Output MUST be a single complete pytest file for this module.

Now regenerate the full corrected test file for this module.
"""

def copy_tests_from_tmp(tmp_root, real_project_root):
    """
    Copies all test_*.py files from tmp_root/tests/ into
    real_project_root/tests/, preserving filenames.
    """
    try:
        tmp_tests = os.path.join(tmp_root, "tests")
        real_tests = os.path.join(real_project_root, "tests")
        
        for root, dirs, files in os.walk(tmp_tests):
                print("ROOT:", root)
                print("DIRS:", dirs)
                print("FILES:", files)
                print("-" * 40)

        if not os.path.exists(tmp_tests):
            print("[WARN] No tests directory found in tmp project.")
            return

        os.makedirs(real_tests, exist_ok=True)

        test_dir = os.path.join(tmp_root, "tests")
        os.makedirs(test_dir, exist_ok=True)

        g = Github(auth=auth)
        repo = g.get_repo("kramalakshmi/API")
        
        for file in os.listdir(tmp_tests):
            if file.endswith(".py"):
                src = str(os.path.join(tmp_tests, file))
                dst = str(os.path.join("tests", file))
                print(f"Copying {src} to {dst}...")
                with open(src) as f:
                    test_code = f.read()
                
                try:
            
                    existing = repo.get_contents(dst,ref="syntax_error_refine")
                    
                    repo.update_file(
                        dst, "Update generated tests", test_code, existing.sha, branch= "syntax_error_refine"
                    )
                except Exception as ex:
                    repo.create_file(
                        dst, "Add generated tests", test_code , branch= "syntax_error_refine"
                    )
                
                
                print(f"[COPIED] {file} → {real_tests}")
    except Exception as e:
        print(f"[ERROR] Failed to copy tests: {e}")


MODULE_REFINEMENT_PROMPT = """
You are a test‑generation and test‑refinement engine.

Your job is to FIX and REWRITE the test file for the module "{module_name}" so that:
- all syntax errors are removed
- imports are correct
- function signatures match the module source
- missing functions are tested
- wrong expected values are corrected
- exception tests are added when appropriate
- tests are deterministic and isolated
- coverage improves for this module
- the final output is a COMPLETE, VALID pytest file

You MUST follow all rules below.

============================================================
### 1. MODULE SOURCE CODE (Ground Truth)
============================================================
This is the exact source code for the module you are testing:

{module_source}

Extract the real function signatures from this source and use them EXACTLY.

============================================================
### 2. CURRENT TEST FILE (Rewrite This)
============================================================
Here is the current test file (may contain errors):

{test_file}

Rewrite this ENTIRE file. Do NOT leave any broken code behind.

============================================================
### 3. PYTEST ERROR OUTPUT (What Went Wrong)
============================================================
These are the errors from pytest:

{error_output}

Use these errors to fix the test file.

============================================================
### 4. DETECTED ERROR CATEGORIES
============================================================
These error categories were detected:

{error_categories}

Fix ALL of them.

============================================================
### 5. MISSING FUNCTIONS (Coverage Gaps)
============================================================
These functions in the module have missing coverage:

{missing_functions}

You MUST add tests for these functions.

============================================================
### 6. SIGNATURE MISMATCHES (Detected Before Pytest)
============================================================
These incorrect function calls were detected:

{signature_mismatches}

Fix ALL of them by matching the real function signatures from the module.

============================================================
### 7. RULES FOR REFINEMENT
============================================================

#### A. Syntax Rules
- The output MUST be valid Python.
- No syntax errors, no indentation errors, no stray characters.

#### B. Import Rules
- Import the module using: `from src.{module_name} import *` OR explicit imports.
- Do NOT modify sys.path.
- Do NOT use relative imports.

#### C. Function Signature Rules
- Match the EXACT signature from the module.
- Do NOT invent parameters.
- Do NOT remove required parameters.
- Use keyword arguments when helpful.

#### D. Expected Value Rules
- Infer correct expected values from the module source.
- Do NOT hallucinate behavior not present in the code.

#### E. Exception Rules
- If the module raises exceptions, add `pytest.raises`.

#### F. Coverage Rules
- Add tests for missing functions.
- Add edge‑case tests.
- Add negative tests where appropriate.

#### G. Test Quality Rules
- Tests must be deterministic.
- No randomness.
- No external files.
- No global state.
- No mocking unless absolutely necessary.

#### H. Output Rules
- Output ONLY the final test file.
- Do NOT include explanations.
- Do NOT include markdown.
- Do NOT include comments outside the test code.

============================================================
### 8. EXAMPLE OF FIXING A WRONG SIGNATURE
============================================================

Source:
    def add_item(cart, item_id, qty):

Wrong:
    result = add_item(1)

Correct:
    result = add_item(cart={{}}, item_id=1, qty=1)

============================================================
### 9. NOW REWRITE THE TEST FILE
============================================================

Rewrite the ENTIRE test file for module "{module_name}" so that:
- all errors are fixed
- all signatures are correct
- all missing functions are tested
- coverage improves
- the file is valid pytest code

Output ONLY the final test file.
"""


if __name__ == "__main__":
    tmp_root = tempfile.mkdtemp(prefix="refine_")
    
    refinement_loop(tmp_root,llm, PROJECT_ROOT)
    copy_tests_from_tmp(tmp_root, PROJECT_ROOT)
