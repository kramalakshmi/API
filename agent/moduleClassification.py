import ast
import re
import moduleAnalysis

CONFIG_KEYWORDS = {
    "getenv", "environ", "load_dotenv", "ConfigParser",
    "json.load", "yaml.safe_load", "open", "boto3", "redis",
    "psycopg2", "connect", "client"
}

def detect_config_dependencies(source: str) -> dict:
    """
    Returns a dict describing config dependencies found in the module.
    """
    tree = ast.parse(source)
    findings = {
        "env_vars": False,
        "dotenv": False,
        "config_files": False,
        "cloud_clients": False,
        "db_connections": False,
        "hardcoded_paths": False,
        "any": False,
    }

    for node in ast.walk(tree):

        # Environment variables
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute):
            if node.value.attr == "environ":
                findings["env_vars"] = True

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # os.getenv
            if node.func.attr == "getenv":
                findings["env_vars"] = True

            # dotenv.load_dotenv
            if node.func.attr == "load_dotenv":
                findings["dotenv"] = True

            # configparser
            if node.func.attr == "read":
                findings["config_files"] = True

            # cloud clients
            if node.func.attr == "client":
                findings["cloud_clients"] = True

            # DB connections
            if node.func.attr == "connect":
                findings["db_connections"] = True

        # Hardcoded paths
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if re.search(r"\.(json|yaml|yml|ini|cfg|env)$", node.value):
                findings["config_files"] = True
            if "/" in node.value or "\\" in node.value:
                findings["hardcoded_paths"] = True

    findings["any"] = any(findings.values())
    return findings

def classify_module(module_name: str, source: str) -> str:
    """
    Returns one of:
    - SAFE
    - CONFIG_REQUIRED
    - SIDE_EFFECT
    - OPTIONAL_DEP
    - HEAVY
    - SKIP
    """
    if module_name == "__init__":
        return "SKIP"

    info = moduleAnalysis.analyze_module_source(source)

    # skip pure entrypoints / scripts
    if info["has_main_guard"]:
        return "SKIP"

    if info["env_vars"] or info["dotenv"] or info["config_files"] or info["cloud_clients"] or info["db_connections"]:
        return "CONFIG_REQUIRED"

    if info["side_effect_calls"]:
        return "SIDE_EFFECT"

    if info["optional_deps"]:
        return "OPTIONAL_DEP"

    if info["heavy_imports"]:
        return "HEAVY"

    return "SAFE"

CONFIG_FIXTURE_TEMPLATE = """
# Auto-generated config neutralization fixtures

import os
import pytest

@pytest.fixture(autouse=True)
def neutralize_env(monkeypatch):
    # Provide safe defaults for missing environment variables
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setenv("DB_URL", "sqlite:///:memory:")

@pytest.fixture(autouse=True)
def neutralize_config_files(tmp_path, monkeypatch):
    # Create a fake config file if module expects one
    cfg = tmp_path / "config.json"
    cfg.write_text('{"mode": "test"}')

    # Patch open() inside the module to read from our fake file
    import src.{module_name} as m
    monkeypatch.setattr(m, "open", lambda f, mode="r": open(cfg, mode))
"""

