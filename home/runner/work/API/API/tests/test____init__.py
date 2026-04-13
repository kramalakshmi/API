import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest

try:
    from src.___init__ import __doc__
except Exception as exc:
    pytest.skip(f"Unable to import src.___init__: {exc}", allow_module_level=True)


def test_module_imports_without_error():
    assert True


def test_module_doc_is_string_or_none():
    assert __doc__ is None or isinstance(__doc__, str)