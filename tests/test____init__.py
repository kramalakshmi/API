import importlib
import types

import pytest
from src.___init__ import *


MODULE_NAME = "src.___init__"


@pytest.fixture
def module():
    return importlib.import_module(MODULE_NAME)


def test_module_imports_successfully(module):
    assert isinstance(module, types.ModuleType)
    assert module.__name__ == MODULE_NAME


def test_module_has_standard_dunder_attributes(module):
    assert hasattr(module, "__name__")
    assert hasattr(module, "__doc__")
    assert hasattr(module, "__package__")
    assert hasattr(module, "__dict__")


def test_reimport_returns_same_module_object(module):
    second = importlib.import_module(MODULE_NAME)
    assert module is second


def test_module_dict_is_accessible(module):
    assert isinstance(module.__dict__, dict)


def test_module_file_and_spec_attributes_are_consistent_if_present(module):
    spec = getattr(module, "__spec__", None)
    if spec is not None:
        assert spec.name == MODULE_NAME
    if hasattr(module, "__file__"):
        assert isinstance(module.__file__, str)
        assert module.__file__


def test_module_package_is_string_or_none(module):
    assert module.__package__ is None or isinstance(module.__package__, str)


def test_module_doc_is_string_or_none(module):
    assert module.__doc__ is None or isinstance(module.__doc__, str)


def test_module_is_present_in_sys_modules_via_importlib(module):
    reloaded = importlib.import_module(MODULE_NAME)
    assert module is reloaded


def test_star_import_namespace_is_deterministic_across_runs():
    namespace_one = {}
    namespace_two = {}
    exec("from src.___init__ import *", namespace_one)
    exec("from src.___init__ import *", namespace_two)
    assert set(namespace_one.keys()) == set(namespace_two.keys())


def test_star_import_executes_and_produces_namespace_dict():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert isinstance(namespace, dict)


def test_star_import_populates_builtin_dunder_in_namespace():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert "__builtins__" in namespace


def test_module_namespace_contains_expected_name(module):
    assert module.__name__ == MODULE_NAME


def test_module_all_attribute_is_valid_if_present(module):
    if hasattr(module, "__all__"):
        assert isinstance(module.__all__, (list, tuple))
        for item in module.__all__:
            assert isinstance(item, str)


def test_reload_preserves_module_identity(module):
    reloaded = importlib.reload(module)
    assert reloaded is module
    assert reloaded.__name__ == MODULE_NAME


def test_module_repr_contains_module_name(module):
    assert MODULE_NAME in repr(module)


def test_module_dict_contains_name_key(module):
    assert "__name__" in module.__dict__
    assert module.__dict__["__name__"] == MODULE_NAME


def test_module_loader_matches_spec_loader_when_spec_present(module):
    spec = getattr(module, "__spec__", None)
    if spec is not None:
        assert module.__loader__ is spec.loader


def test_module_cached_attribute_is_string_or_none_if_present(module):
    if hasattr(module, "__cached__"):
        assert module.__cached__ is None or isinstance(module.__cached__, str)


def test_module_has_no_unexpected_callable_exports_assumption(module):
    exported = getattr(module, "__all__", None)
    if exported is not None:
        for name in exported:
            assert hasattr(module, name)


def test_importing_nonexistent_attribute_from_module_raises():
    with pytest.raises(ImportError):
        exec("from src.___init__ import definitely_not_a_real_name")


def test_module_object_from_direct_import_matches_importlib(module):
    assert module is importlib.import_module(MODULE_NAME)


def test_module_has_string_name_and_dict(module):
    assert isinstance(module.__name__, str)
    assert isinstance(vars(module), dict)


def test_module_spec_parent_matches_package_when_spec_present(module):
    spec = getattr(module, "__spec__", None)
    if spec is not None:
        assert spec.parent == module.__package__


def test_module_name_ends_with_expected_leaf(module):
    assert module.__name__.split(".")[-1] == "___init__"


def test_module_dir_contains_standard_name(module):
    assert "__name__" in dir(module) or "__name__" in module.__dict__
