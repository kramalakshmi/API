import importlib
import sys
import types

import pytest
from src.___init__ import *

MODULE_NAME = "src.___init__"


@pytest.fixture
def module():
    return importlib.import_module(MODULE_NAME)


def test_module_imports_as_module_type(module):
    assert isinstance(module, types.ModuleType)
    assert module.__name__ == MODULE_NAME


def test_reimport_returns_same_module_object(module):
    module2 = importlib.import_module(MODULE_NAME)
    assert module2 is module


def test_reload_returns_same_module_object(module):
    reloaded = importlib.reload(module)
    assert reloaded is module


def test_module_has_standard_attributes(module):
    assert hasattr(module, "__name__")
    assert hasattr(module, "__package__")
    assert hasattr(module, "__doc__")
    assert hasattr(module, "__spec__")
    assert hasattr(module, "__dict__")


def test_module_standard_attribute_types(module):
    assert isinstance(module.__name__, str)
    assert module.__package__ is None or isinstance(module.__package__, str)
    assert module.__doc__ is None or isinstance(module.__doc__, str)
    assert module.__spec__ is not None
    assert module.__spec__.name == module.__name__
    assert isinstance(module.__dict__, dict)


def test_module_dict_contains_expected_keys(module):
    module_dict = module.__dict__
    assert "__name__" in module_dict
    assert "__package__" in module_dict
    assert "__spec__" in module_dict


def test_module_file_attribute_if_present_is_non_empty_string(module):
    if getattr(module, "__file__", None) is not None:
        assert isinstance(module.__file__, str)
        assert module.__file__


def test_dir_is_deterministic(module):
    attrs1 = dir(module)
    attrs2 = dir(module)
    assert isinstance(attrs1, list)
    assert attrs1 == attrs2


def test_import_by_module_name_returns_same_object(module):
    reimported = importlib.import_module(module.__name__)
    assert reimported is module


def test_star_import_executes_without_error():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert isinstance(namespace, dict)
    assert "__builtins__" in namespace


def test_all_attribute_if_present_is_valid(module):
    if hasattr(module, "__all__"):
        assert isinstance(module.__all__, (list, tuple))
        for name in module.__all__:
            assert isinstance(name, str)
            assert hasattr(module, name)


def test_module_object_exposed_by_star_import_matches_importlib_module(module):
    namespace = {}
    exec("from src.___init__ import *", namespace)
    imported_names = {k for k in namespace if k != "__builtins__"}

    if hasattr(module, "__all__"):
        assert imported_names == set(module.__all__)
    else:
        expected = {name for name in module.__dict__ if not name.startswith("_")}
        assert imported_names == expected


def test_module_repr_is_string_and_contains_name(module):
    representation = repr(module)
    assert isinstance(representation, str)
    assert module.__name__ in representation


def test_module_package_name_is_consistent_with_module_name(module):
    expected_package = MODULE_NAME.rpartition(".")[0]
    assert module.__package__ == expected_package


def test_module_spec_origin_matches_file_when_file_present(module):
    if getattr(module, "__file__", None) is not None:
        assert module.__spec__.origin == module.__file__


def test_module_is_present_in_sys_modules_via_importlib(module):
    assert MODULE_NAME in sys.modules
    assert sys.modules[MODULE_NAME] is module


def test_module_doc_attribute_is_stable_across_accesses(module):
    assert module.__doc__ == module.__doc__


def test_module_name_parts_are_consistent(module):
    assert module.__name__.endswith(".___init__")
    assert module.__name__.split(".")[0] == "src"


def test_module_spec_has_loader(module):
    assert module.__spec__.loader is not None


def test_module_cached_attribute_if_present_is_string_or_none(module):
    if hasattr(module, "__cached__"):
        assert module.__cached__ is None or isinstance(module.__cached__, str)


def test_module_loader_attribute_if_present(module):
    if hasattr(module, "__loader__"):
        assert module.__loader__ is not None


def test_importing_unknown_attribute_from_module_raises_import_error():
    with pytest.raises(ImportError):
        exec("from src.___init__ import definitely_missing_name")


def test_module_dict_identity_is_stable(module):
    assert module.__dict__ is module.__dict__


def test_module_spec_parent_matches_package(module):
    assert module.__spec__.parent == module.__package__


def test_module_name_matches_fixture_import(module):
    imported = importlib.import_module(MODULE_NAME)
    assert imported.__name__ == MODULE_NAME


def test_module_has_no_invalid_all_entries_if_present(module):
    if hasattr(module, "__all__"):
        assert all(name and isinstance(name, str) for name in module.__all__)


def test_star_import_namespace_values_match_module_attributes(module):
    namespace = {}
    exec("from src.___init__ import *", namespace)

    imported_module = importlib.import_module(MODULE_NAME)
    for name, value in namespace.items():
        if name == "__builtins__":
            continue
        assert hasattr(imported_module, name)
        assert getattr(imported_module, name) is value


def test_module_can_be_accessed_from_sys_modules_after_import(module):
    assert sys.modules.get(MODULE_NAME) is module


def test_module_spec_name_matches_module_name(module):
    assert module.__spec__.name == module.__name__


def test_module_package_is_prefix_of_module_name(module):
    if module.__package__:
        assert module.__name__.startswith(module.__package__ + ".")


def test_module_dict_contains_dunder_name_value(module):
    assert module.__dict__["__name__"] == MODULE_NAME


def test_module_has_no_duplicate_all_entries_if_present(module):
    if hasattr(module, "__all__"):
        assert len(module.__all__) == len(set(module.__all__))
