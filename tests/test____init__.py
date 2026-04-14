import importlib
import sys
import types

import pytest
from src.___init__ import *


MODULE_NAME = "src.___init__"


def test_module_imports_successfully():
    module = importlib.import_module(MODULE_NAME)
    assert isinstance(module, types.ModuleType)
    assert module.__name__ == MODULE_NAME


def test_module_has_standard_dunder_attributes():
    module = importlib.import_module(MODULE_NAME)
    for attr in ("__name__", "__doc__", "__package__", "__loader__", "__spec__"):
        assert hasattr(module, attr)


def test_reimport_returns_same_module_object():
    module1 = importlib.import_module(MODULE_NAME)
    module2 = importlib.import_module(MODULE_NAME)
    assert module1 is module2


def test_module_dir_is_stable_across_imports():
    module1 = importlib.import_module(MODULE_NAME)
    module2 = importlib.import_module(MODULE_NAME)
    assert dir(module1) == dir(module2)


def test_star_import_exec_populates_namespace_dict():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert isinstance(namespace, dict)


def test_star_import_exec_contains_builtins():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert "__builtins__" in namespace


def test_star_import_namespace_matches_module_public_names():
    module = importlib.import_module(MODULE_NAME)
    namespace = {}
    exec("from src.___init__ import *", namespace)

    if hasattr(module, "__all__"):
        expected_names = set(module.__all__)
    else:
        expected_names = {name for name in dir(module) if not name.startswith("_")}

    imported_names = {name for name in namespace if name != "__builtins__"}
    assert imported_names == expected_names


def test_module_doc_attribute_is_string_or_none():
    module = importlib.import_module(MODULE_NAME)
    assert module.__doc__ is None or isinstance(module.__doc__, str)


def test_module_package_attribute_is_string_or_none():
    module = importlib.import_module(MODULE_NAME)
    assert module.__package__ is None or isinstance(module.__package__, str)


def test_module_spec_name_matches_module_name():
    module = importlib.import_module(MODULE_NAME)
    assert module.__spec__ is not None
    assert module.__spec__.name == MODULE_NAME


def test_module_loader_is_present():
    module = importlib.import_module(MODULE_NAME)
    assert module.__loader__ is not None


def test_module_file_attribute_if_present_is_string():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__file__"):
        assert module.__file__ is None or isinstance(module.__file__, str)


def test_module_cached_attribute_if_present_is_string():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__cached__"):
        assert module.__cached__ is None or isinstance(module.__cached__, str)


def test_module_can_be_accessed_via_importlib_and_direct_import_namespace():
    module = importlib.import_module(MODULE_NAME)
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert module.__name__ == MODULE_NAME
    assert isinstance(namespace, dict)


def test_imported_star_names_are_present_in_module_when_public():
    module = importlib.import_module(MODULE_NAME)
    public_names = [name for name in dir(module) if not name.startswith("_")]
    for name in public_names:
        assert hasattr(module, name)


def test_module_identity_matches_directly_imported_module_object():
    direct_module = importlib.import_module(MODULE_NAME)
    imported_again = importlib.import_module(MODULE_NAME)
    assert direct_module is imported_again


def test_module_package_is_string_or_none():
    module = importlib.import_module(MODULE_NAME)
    assert module.__package__ is None or isinstance(module.__package__, str)


def test_module_has_no_unexpected_public_callables_without_module_membership():
    module = importlib.import_module(MODULE_NAME)
    public_callables = [
        name for name in dir(module) if not name.startswith("_") and callable(getattr(module, name))
    ]
    for name in public_callables:
        obj = getattr(module, name)
        assert hasattr(module, name)
        assert hasattr(obj, "__module__")


def test_module_repr_contains_module_name():
    module = importlib.import_module(MODULE_NAME)
    assert MODULE_NAME in repr(module)


def test_import_module_invalid_name_raises():
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("src.___init___does_not_exist")


def test_module_object_available_in_sys_modules_after_import():
    module = importlib.import_module(MODULE_NAME)
    assert MODULE_NAME in sys.modules
    assert sys.modules[MODULE_NAME] is module


def test_module_all_if_present_is_sequence_of_strings():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__all__"):
        assert isinstance(module.__all__, (list, tuple))
        assert all(isinstance(name, str) for name in module.__all__)


def test_module_dict_contains_expected_core_keys():
    module = importlib.import_module(MODULE_NAME)
    module_dict = module.__dict__
    assert "__name__" in module_dict
    assert "__package__" in module_dict
    assert "__spec__" in module_dict


def test_module_name_matches_imported___name__():
    module = importlib.import_module(MODULE_NAME)
    assert __name__ != MODULE_NAME
    assert module.__name__ == MODULE_NAME


def test_star_import_does_not_import_private_names_when_no___all__():
    module = importlib.import_module(MODULE_NAME)
    if hasattr(module, "__all__"):
        pytest.skip("Module defines __all__; star import behavior is governed by __all__")

    namespace = {}
    exec("from src.___init__ import *", namespace)
    imported_names = {name for name in namespace if name != "__builtins__"}
    assert all(not name.startswith("_") for name in imported_names)


def test_module_spec_origin_if_present_is_string_or_none():
    module = importlib.import_module(MODULE_NAME)
    assert module.__spec__ is not None
    assert module.__spec__.origin is None or isinstance(module.__spec__.origin, str)
