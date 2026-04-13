import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def test_module_imports_successfully():
    from src.___init__ import __doc__
    assert __doc__ is None or isinstance(__doc__, str)