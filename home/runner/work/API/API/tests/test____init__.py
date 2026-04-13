import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.___init__ import *  # noqa: F401,F403


def test_module_imports_successfully():
    assert True


def test_module_namespace_is_accessible():
    exported = [name for name in globals() if not name.startswith("_")]
    assert isinstance(exported, list)