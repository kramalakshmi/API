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
    assert isinstance(module, types.ModuleType)


def test_module_name_matches_expected(module):
    assert module.__name__ == MODULE_NAME


def test_reimport_returns_same_module_object():
    first = importlib.import_module(MODULE_NAME)
    second = importlib.import_module(MODULE_NAME)
    assert first is second


def test_module_has_dictionary_namespace(module):
    assert isinstance(module.__dict__, dict)


def test_module_has_file_attribute(module):
    assert hasattr(module, "__file__")
    assert isinstance(module.__file__, str)
    assert module.__file__
    assert module.__file__.endswith(".py")


def test_module_has_package_attribute(module):
    assert hasattr(module, "__package__")
    assert isinstance(module.__package__, str)
    assert module.__package__ == "src"


def test_module_has_spec_attribute(module):
    assert hasattr(module, "__spec__")
    assert module.__spec__ is not None
    assert module.__spec__.name == MODULE_NAME


def test_module_dict_contains_core_dunder_names(module):
    namespace = module.__dict__
    for name in ("__name__", "__package__", "__doc__"):
        assert name in namespace


def test_importlib_import_reference_same_module():
    direct_module = importlib.import_module(MODULE_NAME)
    imported_module = importlib.import_module(MODULE_NAME)
    assert imported_module is direct_module


def test_public_callables_collection_is_well_formed(module):
    public_callables = [
        name
        for name, obj in vars(module).items()
        if not name.startswith("_") and callable(obj)
    ]
    assert isinstance(public_callables, list)
    assert all(isinstance(name, str) for name in public_callables)


def test_public_non_dunder_names_collection_is_well_formed(module):
    public_names = [name for name in vars(module) if not name.startswith("_")]
    assert isinstance(public_names, list)
    assert all(isinstance(name, str) for name in public_names)


def test_star_import_executes_and_provides_namespace_dict():
    namespace = {}
    exec("from src.___init__ import *", {}, namespace)
    assert isinstance(namespace, dict)
    assert "__builtins__" in namespace


def test_module_attributes_are_accessible(module):
    assert getattr(module, "__name__") == MODULE_NAME
    assert isinstance(getattr(module, "__dict__"), dict)


def test_reload_returns_module_object(module):
    reloaded = importlib.reload(module)
    assert isinstance(reloaded, types.ModuleType)
    assert reloaded is module


def test_module_doc_attribute_exists(module):
    assert hasattr(module, "__doc__")


def test_module_has_loader_attribute(module):
    assert hasattr(module, "__loader__")


def test_module_cached_attribute_if_present_is_string_or_none(module):
    if hasattr(module, "__cached__"):
        assert module.__cached__ is None or isinstance(module.__cached__, str)


def test_vars_returns_same_namespace_object(module):
    assert vars(module) is module.__dict__


def test_module_dir_returns_list_of_strings(module):
    names = dir(module)
    assert isinstance(names, list)
    assert all(isinstance(name, str) for name in names)


def test_module_is_present_in_sys_modules_after_import(module):
    assert MODULE_NAME in sys.modules
    assert sys.modules[MODULE_NAME] is module


def test_reloading_multiple_times_keeps_same_identity(module):
    reloaded_once = importlib.reload(module)
    reloaded_twice = importlib.reload(module)
    assert reloaded_once is module
    assert reloaded_twice is module


def test_accessing_missing_attribute_raises_attribute_error(module):
    with pytest.raises(AttributeError):
        getattr(module, "__definitely_missing_attribute__")


def test_module_doc_is_none_or_string(module):
    assert module.__doc__ is None or isinstance(module.__doc__, str)


def test_module_has_standard_dunder_attributes(module):
    for attr in ("__name__", "__package__", "__spec__", "__loader__", "__dict__"):
        assert hasattr(module, attr)


def test_module_repr_contains_module_name(module):
    assert MODULE_NAME in repr(module)


def test_module_all_if_present_is_sequence_of_strings(module):
    if hasattr(module, "__all__"):
        assert isinstance(module.__all__, (list, tuple))
        assert all(isinstance(name, str) for name in module.__all__)


def test_module_file_matches_spec_origin_when_available(module):
    if getattr(module, "__spec__", None) is not None and module.__spec__.origin:
        assert module.__file__ == module.__spec__.origin


def test_module_loader_matches_spec_loader_when_available(module):
    if getattr(module, "__spec__", None) is not None:
        assert module.__loader__ is module.__spec__.loader


def test_module_package_is_prefix_of_module_name(module):
    assert module.__name__.startswith(f"{module.__package__}.")


def test_module_dict_identity_stable_across_reload(module):
    namespace_before = module.__dict__
    importlib.reload(module)
    namespace_after = module.__dict__
    assert isinstance(namespace_before, dict)
    assert isinstance(namespace_after, dict)
    assert namespace_before is namespace_after


def test_getattr_existing_dunder_file_matches_attribute_access():
    imported = importlib.import_module(MODULE_NAME)
    assert getattr(imported, "__file__") == imported.__file__


def test_hasattr_for_missing_attribute_is_false(module):
    assert hasattr(module, "__definitely_missing_attribute__") is False


def test_module_spec_has_expected_parent(module):
    if getattr(module, "__spec__", None) is not None:
        assert module.__spec__.parent == "src"


def test_module_name_available_in_sys_modules_mapping():
    imported = importlib.import_module(MODULE_NAME)
    assert sys.modules.get(MODULE_NAME) is imported


def test_module_dir_includes_standard_names(module):
    names = dir(module)
    assert "__name__" in names
    assert "__doc__" in names
    assert "__package__" in names


def test_module_file_exists_in_namespace(module):
    assert "__file__" in module.__dict__
    assert module.__dict__["__file__"] == module.__file__


def test_module_spec_origin_is_string_when_present(module):
    if module.__spec__ is not None and module.__spec__.origin is not None:
        assert isinstance(module.__spec__.origin, str)


def test_module_loader_and_spec_loader_are_consistent_types(module):
    if module.__spec__ is not None:
        assert (
            type(module.__loader__) is type(module.__spec__.loader)
            or module.__loader__ is module.__spec__.loader
        )


def test_module_has_no_missing_standard_identity_fields(module):
    assert module.__name__
    assert module.__package__ == "src"
    assert module.__spec__ is not None


def test_import_via_sys_modules_returns_same_object(module):
    assert sys.modules[MODULE_NAME] is module


def test_module_namespace_contains_standard_keys_after_reload(module):
    importlib.reload(module)
    for key in ("__name__", "__package__", "__loader__", "__spec__"):
        assert key in module.__dict__


def test_module_repr_is_string(module):
    assert isinstance(repr(module), str)


def test_module_file_points_to_init_file(module):
    assert module.__file__.rsplit("/", 1)[-1] == "___init__.py" or module.__file__.rsplit("\\", 1)[-1] == "___init__.py"


def test_module_spec_origin_matches_file_basename(module):
    if module.__spec__ is not None and module.__spec__.origin:
        origin_name = module.__spec__.origin.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        assert origin_name == "___init__.py"


def test_module_namespace_is_mutable(module):
    sentinel_name = "__test_sentinel__"
    module.__dict__[sentinel_name] = 123
    try:
        assert getattr(module, sentinel_name) == 123
    finally:
        module.__dict__.pop(sentinel_name, None)
        if hasattr(module, sentinel_name):
            delattr(module, sentinel_name)


def test_module_getattribute_for_existing_name(module):
    assert module.__getattribute__("__name__") == MODULE_NAME


def test_module_missing_key_not_in_namespace(module):
    assert "__definitely_missing_attribute__" not in module.__dict__


def test_module_all_names_exist_when_all_present(module):
    if hasattr(module, "__all__"):
        for name in module.__all__:
            assert hasattr(module, name) or name in module.__dict__


def test_module_docstring_consistency(module):
    assert module.__doc__ == module.__dict__.get("__doc__")


def test_module_spec_name_consistency(module):
    assert module.__spec__.name == module.__name__


def test_module_loader_is_not_missing(module):
    assert module.__loader__ is not None


def test_module_package_matches_name_prefix_exactly(module):
    package_prefix = module.__name__.split(".", 1)[0]
    assert module.__package__ == package_prefix


def test_imported_star_names_are_subset_of_public_names(module):
    namespace = {}
    exec("from src.___init__ import *", {}, namespace)
    imported_names = {k for k in namespace if k != "__builtins__"}
    public_names = {name for name in vars(importlib.import_module(MODULE_NAME)) if not name.startswith("_")}
    if hasattr(importlib.import_module(MODULE_NAME), "__all__"):
        expected = set(importlib.import_module(MODULE_NAME).__all__)
        assert imported_names == expected
    else:
        assert imported_names.issubset(public_names)
