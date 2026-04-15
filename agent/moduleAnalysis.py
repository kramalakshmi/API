import ast
import re

HEAVY_IMPORTS = {"pandas", "tensorflow", "torch", "sklearn"}
OPTIONAL_DEP_PATTERNS = ("ImportError", "find_spec", "HAS_", "optional")

class ModuleAnalysis(ast.NodeVisitor):
    def __init__(self):
        self.env_vars = False
        self.dotenv = False
        self.config_files = False
        self.cloud_clients = False
        self.db_connections = False
        self.hardcoded_paths = False
        self.side_effect_calls = False
        self.optional_deps = False
        self.heavy_imports = False

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.name.split(".")[0]
            if name in HEAVY_IMPORTS:
                self.heavy_imports = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            root = node.module.split(".")[0]
            if root in HEAVY_IMPORTS:
                self.heavy_imports = True
        self.generic_visit(node)

    def visit_Call(self, node):
        # os.getenv / os.environ[...] / load_dotenv
        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr

            if attr == "getenv":
                self.env_vars = True
            if attr == "load_dotenv":
                self.dotenv = True
            if attr == "client":  # boto3.client, redis.client, etc.
                self.cloud_clients = True
            if attr == "connect":  # db connections
                self.db_connections = True

            # side-effect-ish calls at top level
            if attr in {"get", "post", "put", "delete", "run", "sleep"}:
                self.side_effect_calls = True

        self.generic_visit(node)

    def visit_Subscript(self, node):
        # os.environ["KEY"]
        if isinstance(node.value, ast.Attribute) and node.value.attr == "environ":
            self.env_vars = True
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            s = node.value
            if re.search(r"\.(json|yaml|yml|ini|cfg|env)$", s):
                self.config_files = True
            if "/" in s or "\\" in s:
                self.hardcoded_paths = True
            if any(p in s for p in OPTIONAL_DEP_PATTERNS):
                self.optional_deps = True
        self.generic_visit(node)


def analyze_module_source(source: str) -> dict:
    tree = ast.parse(source)
    analyzer = ModuleAnalysis()
    analyzer.visit(tree)

    return {
        "env_vars": analyzer.env_vars,
        "dotenv": analyzer.dotenv,
        "config_files": analyzer.config_files,
        "cloud_clients": analyzer.cloud_clients,
        "db_connections": analyzer.db_connections,
        "hardcoded_paths": analyzer.hardcoded_paths,
        "side_effect_calls": analyzer.side_effect_calls,
        "optional_deps": analyzer.optional_deps,
        "heavy_imports": analyzer.heavy_imports,
        "has_main_guard": "if __name__ == '__main__'" in source,
    }
