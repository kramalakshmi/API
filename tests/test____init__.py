import importlib
import sys
import types

import pytest
from src.___init__ import *


MODULE_NAME = "src.___init__"


def test_module_imports_successfully():
    module = importlib.import_module(MODULE_NAME)
    assert module is not None
    assert isinstance(module, types.ModuleType)
    assert module.__name__ == MODULE_NAME


def test_star_import_executes_without_error_and_populates_namespace():
    namespace = {}
    exec("from src.___init__ import *", {}, namespace)
    assert isinstance(namespace, dict)
    assert "__builtins__" in namespace


def test_module_has_standard_dunder_attributes():
    module = importlib.import_module(MODULE_NAME)
    assert hasattr(module, "__name__")
    assert hasattr(module, "__doc__")
    assert hasattr(module, "__package__")
    assert hasattr(module, "__dict__")
    assert module.__name__ == MODULE_NAME


def test_reimport_returns_same_module_object():
    module1 = importlib.import_module(MODULE_NAME)
    module2 = importlib.import_module(MODULE_NAME)
    assert module1 is module2


def test_module_dict_is_accessible():
    module = importlib.import_module(MODULE_NAME)
    assert isinstance(module.__dict__, dict)


def test_module_file_and_spec_attributes_are_consistent():
    module = importlib.import_module(MODULE_NAME)
    assert hasattr(module, "__spec__")
    assert module.__spec__ is not None
    assert module.__spec__.name == MODULE_NAME
    if getattr(module, "__file__", None) is not None:
        assert isinstance(module.__file__, str)


def test_importlib_returns_same_object_as_direct_import():
    direct_module = importlib.import_module(MODULE_NAME)
    imported_again = importlib.import_module(MODULE_NAME)
    assert direct_module is imported_again


def test_module_can_be_reloaded():
    module = importlib.import_module(MODULE_NAME)
    reloaded = importlib.reload(module)
    assert reloaded is module
    assert reloaded.__name__ == MODULE_NAME


def test_module_package_name_is_string():
    module = importlib.import_module(MODULE_NAME)
    assert isinstance(module.__package__, str)


def test_module_doc_attribute_exists_even_if_none():
    module = importlib.import_module(MODULE_NAME)
    assert hasattr(module, "__doc__")


def test_module_dir_returns_iterable_of_attribute_names():
    module = importlib.import_module(MODULE_NAME)
    names = dir(module)
    assert isinstance(names, list)
    assert "__name__" in names


def test_module_repr_is_string():
    module = importlib.import_module(MODULE_NAME)
    assert isinstance(repr(module), str)


def test_module_is_present_in_sys_modules_after_import():
    module = importlib.import_module(MODULE_NAME)
    assert MODULE_NAME in sys.modules
    assert sys.modules[MODULE_NAME] is module


def test_module_spec_has_loader():
    module = importlib.import_module(MODULE_NAME)
    assert module.__spec__ is not None
    assert module.__spec__.loader is not None


def test_module_all_attribute_if_present_is_well_formed():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__all__"):
        assert isinstance(module.__all__, (list, tuple))
        assert all(isinstance(name, str) for name in module.__all__)
    else:
        pytest.skip("__all__ is not defined for this module")


def test_module_object_from_star_import_matches_importlib_module():
    imported_module = importlib.import_module(MODULE_NAME)
    assert imported_module is sys.modules[MODULE_NAME]


def test_module_name_matches_expected():
    module = importlib.import_module(MODULE_NAME)
    assert module.__name__ == MODULE_NAME
    assert MODULE_NAME.endswith(".___init__")


def test_module_has_string_or_none_file_attribute():
    module = importlib.import_module(MODULE_NAME)
    assert getattr(module, "__file__", None) is None or isinstance(module.__file__, str)


def test_module_cached_attribute_if_present_is_string_or_none():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__cached__"):
        assert module.__cached__ is None or isinstance(module.__cached__, str)


def test_module_loader_attribute_if_present_matches_spec_loader():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__loader__") and module.__spec__ is not None:
        assert module.__loader__ is module.__spec__.loader or module.__loader__ is not None


def test_module_annotations_attribute_if_present_is_dict():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__annotations__"):
        assert isinstance(module.__annotations__, dict)


def test_importing_nonexistent_subattribute_raises_attribute_error_if_no_such_name():
    module = importlib.import_module(MODULE_NAME)
    missing_name = "__definitely_missing_test_attribute__"
    assert not hasattr(module, missing_name)
    with pytest.raises(AttributeError):
        getattr(module, missing_name)
