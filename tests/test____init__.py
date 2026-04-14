import importlib
import sys
import types

import pytest
from src.___init__ import *  # noqa: F401,F403

MODULE_NAME = "src.___init__"


@pytest.fixture
def module():
    return importlib.import_module(MODULE_NAME)


def test_module_can_be_imported(module):
    assert module is not None
    assert isinstance(module, types.ModuleType)


def test_module_has_expected_name(module):
    assert module.__name__ == MODULE_NAME


def test_multiple_imports_return_same_module_object(module):
    module2 = importlib.import_module(MODULE_NAME)
    assert module2 is module


def test_reimport_is_deterministic(module):
    reloaded = importlib.reload(module)
    assert reloaded is module
    assert reloaded.__name__ == MODULE_NAME


def test_star_import_executes_without_error():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    assert isinstance(namespace, dict)
    assert "__builtins__" in namespace


def test_module_dict_contains_standard_attributes(module):
    assert hasattr(module, "__name__")
    assert hasattr(module, "__doc__")
    assert hasattr(module, "__package__")
    assert hasattr(module, "__loader__")
    assert hasattr(module, "__spec__")


def test_module_file_attribute_if_present_is_string(module):
    if hasattr(module, "__file__"):
        assert isinstance(module.__file__, str)


def test_module_cached_attribute_if_present_is_string_or_none(module):
    if hasattr(module, "__cached__"):
        assert module.__cached__ is None or isinstance(module.__cached__, str)


def test_module_all_attribute_shape_if_present(module):
    if hasattr(module, "__all__"):
        assert isinstance(module.__all__, (list, tuple))
        assert all(isinstance(name, str) for name in module.__all__)


def test_importing_unknown_attribute_raises_attribute_error(module):
    with pytest.raises(AttributeError):
        getattr(module, "__definitely_not_a_real_attribute__")


def test_module_spec_matches_module_name(module):
    assert module.__spec__ is not None
    assert module.__spec__.name == MODULE_NAME


def test_module_package_is_src(module):
    assert module.__package__ == "src"


def test_module_doc_is_none_or_string(module):
    assert module.__doc__ is None or isinstance(module.__doc__, str)


def test_dir_returns_sequence_of_strings(module):
    names = dir(module)
    assert isinstance(names, list)
    assert all(isinstance(name, str) for name in names)


def test_module_is_present_in_sys_modules_via_importlib(module):
    assert MODULE_NAME in sys.modules
    assert sys.modules[MODULE_NAME] is module


def test_module_repr_contains_module_name(module):
    representation = repr(module)
    assert "module" in representation.lower()
    assert MODULE_NAME in representation


def test_module_loader_if_present_has_expected_interface(module):
    if module.__loader__ is not None:
        assert hasattr(module.__loader__, "__class__")


def test_module_spec_parent_matches_package(module):
    if module.__spec__ is not None:
        assert module.__spec__.parent == "src"


def test_module_name_present_in_dir(module):
    assert "__name__" in dir(module)


def test_module_globals_accessible_via_dict(module):
    module_dict = vars(module)
    assert isinstance(module_dict, dict)
    assert module_dict["__name__"] == MODULE_NAME


def test_import_module_returns_same_object_after_reload(module):
    importlib.reload(module)
    module_again = importlib.import_module(MODULE_NAME)
    assert module_again is module


def test_module_has_dunder_package_consistent_with_name(module):
    assert module.__name__.startswith(module.__package__ + ".")


def test_module_spec_origin_if_present_is_string_or_none(module):
    if module.__spec__ is not None:
        assert module.__spec__.origin is None or isinstance(module.__spec__.origin, str)


def test_module_has_builtins_in_globals(module):
    assert "__builtins__" in vars(module)


def test_module_attributes_accessible_via_getattr(module):
    assert getattr(module, "__name__") == MODULE_NAME
    assert getattr(module, "__package__") == "src"


def test_module_spec_has_loader_or_origin(module):
    assert module.__spec__ is not None
    assert module.__spec__.loader is not None or module.__spec__.origin is not None


def test_module_file_matches_spec_origin_when_both_present(module):
    if (
        hasattr(module, "__file__")
        and module.__spec__ is not None
        and module.__spec__.origin is not None
    ):
        assert module.__file__ == module.__spec__.origin


def test_module_is_regular_module_type(module):
    assert isinstance(module, types.ModuleType)


def test_module_vars_contains_package_and_spec(module):
    module_dict = vars(module)
    assert "__package__" in module_dict
    assert "__spec__" in module_dict


def test_reloading_twice_keeps_same_identity(module):
    first = importlib.reload(importlib.import_module(MODULE_NAME))
    second = importlib.reload(first)
    assert first is second


def test_importlib_import_after_star_import_still_returns_module():
    namespace = {}
    exec("from src.___init__ import *", namespace)
    imported = importlib.import_module(MODULE_NAME)
    assert imported.__name__ == MODULE_NAME


def test_module_doc_attribute_access_is_stable(module):
    first = module.__doc__
    second = getattr(module, "__doc__")
    assert first == second


def test_module_package_matches_name_prefix(module):
    package, _, _ = module.__name__.rpartition(".")
    assert module.__package__ == package


def test_module_spec_name_matches_module_name_after_reload(module):
    reloaded = importlib.reload(module)
    assert reloaded.__spec__ is not None
    assert reloaded.__spec__.name == reloaded.__name__


def test_module_has_expected_dunder_attributes_types(module):
    assert isinstance(module.__name__, str)
    assert isinstance(module.__package__, str)
    assert module.__spec__ is not None


def test_module_spec_is_consistent_with_sys_modules_entry(module):
    imported = importlib.import_module(MODULE_NAME)
    assert sys.modules[MODULE_NAME] is imported
    assert imported.__spec__.name == MODULE_NAME


def test_module_origin_or_file_mentions_init(module):
    origin = None
    if module.__spec__ is not None:
        origin = module.__spec__.origin
    file_value = getattr(module, "__file__", None)
    if origin is not None:
        assert "__init__" in origin or "___init__" in origin
    if file_value is not None:
        assert "__init__" in file_value or "___init__" in file_value


def test_module_reload_preserves_basic_metadata(module):
    before_name = module.__name__
    before_package = module.__package__
    reloaded = importlib.reload(module)
    assert reloaded.__name__ == before_name
    assert reloaded.__package__ == before_package


def test_module_namespace_is_dictionary_like(module):
    namespace = vars(module)
    assert isinstance(namespace, dict)
    assert namespace["__name__"] == MODULE_NAME


def test_module_dir_contains_standard_dunders(module):
    names = dir(module)
    assert "__doc__" in names
    assert "__package__" in names
    assert "__spec__" in names


def test_module_has_string_name_and_package(module):
    assert isinstance(module.__name__, str)
    assert isinstance(module.__package__, str)


def test_module_spec_loader_matches_loader_when_both_present(module):
    if module.__spec__ is not None:
        assert module.__spec__.loader is module.__loader__


def test_module_file_basename_if_present_mentions_init(module):
    file_value = getattr(module, "__file__", None)
    if file_value is not None:
        assert file_value.endswith(".py")
        assert "__init__" in file_value or "___init__" in file_value


def test_module_in_sys_modules_after_reload(module):
    reloaded = importlib.reload(module)
    assert sys.modules[MODULE_NAME] is reloaded


def test_module_vars_is_same_as_dunder_dict(module):
    assert vars(module) is module.__dict__


def test_module_getattr_for_existing_dunders(module):
    assert getattr(module, "__spec__") is module.__spec__
    assert getattr(module, "__loader__") is module.__loader__


def test_module_has_no_non_string_names_in_dir(module):
    assert all(isinstance(name, str) for name in dir(module))
