import importlib
import sys
import types

import pytest
from src.___init__ import *  # noqa: F401,F403

MODULE_NAME = "src.___init__"


def _import_module():
    return importlib.import_module(MODULE_NAME)


def test_module_can_be_imported():
    module = _import_module()
    assert isinstance(module, types.ModuleType)


def test_reimport_returns_same_module_object():
    first = _import_module()
    second = _import_module()
    assert first is second


def test_module_is_registered_in_sys_modules():
    module = _import_module()
    assert MODULE_NAME in sys.modules
    assert sys.modules[MODULE_NAME] is module


def test_module_name_is_correct():
    module = _import_module()
    assert module.__name__ == MODULE_NAME


def test_module_has_standard_attributes():
    module = _import_module()
    for attr in ("__name__", "__package__", "__doc__", "__loader__", "__spec__"):
        assert hasattr(module, attr)


def test_module_package_is_string_or_none():
    module = _import_module()
    assert module.__package__ is None or isinstance(module.__package__, str)


def test_module_doc_is_string_or_none():
    module = _import_module()
    assert module.__doc__ is None or isinstance(module.__doc__, str)


def test_module_file_attribute_if_present_is_string():
    module = _import_module()
    file_attr = getattr(module, "__file__", None)
    if file_attr is not None:
        assert isinstance(file_attr, str)


def test_module_cached_attribute_if_present_is_string_or_none():
    module = _import_module()
    cached = getattr(module, "__cached__", None)
    assert cached is None or isinstance(cached, str)


def test_module_dir_contains_standard_names():
    module = _import_module()
    names = dir(module)
    assert isinstance(names, list)
    assert "__name__" in names
    assert "__package__" in names


def test_module_vars_contains_standard_keys():
    module = _import_module()
    module_vars = vars(module)
    assert isinstance(module_vars, dict)
    for key in ("__name__", "__spec__", "__builtins__"):
        assert key in module_vars


def test_module_vars_name_matches_dunder_name():
    module = _import_module()
    assert vars(module)["__name__"] == module.__name__


def test_module_repr_is_string():
    module = _import_module()
    assert isinstance(repr(module), str)


def test_module_spec_exists_and_matches_name():
    module = _import_module()
    assert module.__spec__ is not None
    assert module.__spec__.name == MODULE_NAME


def test_module_spec_has_loader_attribute():
    module = _import_module()
    assert hasattr(module.__spec__, "loader")


def test_module_spec_origin_if_present_is_string_or_none():
    module = _import_module()
    origin = module.__spec__.origin
    assert origin is None or isinstance(origin, str)


def test_module_loader_attribute_if_present_is_not_primitive_container():
    module = _import_module()
    loader = getattr(module, "__loader__", None)
    assert loader is None or not isinstance(
        loader, (str, int, float, list, tuple, dict, set)
    )


def test_module_package_consistency():
    module = _import_module()
    if module.__package__ is not None:
        assert module.__name__.startswith(module.__package__) or module.__package__ == ""


def test_module_spec_parent_matches_package_when_available():
    module = _import_module()
    if module.__package__ is not None:
        assert module.__spec__.parent == module.__package__


def test_all_exports_exist_if_defined():
    module = _import_module()
    exported = getattr(module, "__all__", None)
    if exported is not None:
        assert isinstance(exported, (list, tuple))
        for name in exported:
            assert isinstance(name, str)
            assert hasattr(module, name)


def test_all_exports_are_non_none_if_defined():
    module = _import_module()
    exported = getattr(module, "__all__", ())
    for name in exported:
        assert getattr(module, name) is not None


def test_all_exports_are_strings_if_defined():
    module = _import_module()
    exported = getattr(module, "__all__", None)
    if exported is not None:
        assert all(isinstance(name, str) for name in exported)


def test_import_is_idempotent_across_multiple_calls():
    modules = [_import_module() for _ in range(3)]
    assert modules[0] is modules[1] is modules[2]


def test_invalid_module_import_raises_module_not_found():
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("src.___init___does_not_exist")
