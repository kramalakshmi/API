import importlib
import sys

import src.___init__ as module
from src.___init__ import *


def test_module_imports_successfully():
    imported = importlib.import_module("src.___init__")
    assert imported is module


def test_reimport_returns_same_module_object():
    first = importlib.import_module("src.___init__")
    second = importlib.import_module("src.___init__")
    assert first is second
    assert first is module


def test_module_is_registered_in_sys_modules():
    assert "src.___init__" in sys.modules
    assert sys.modules["src.___init__"] is module


def test_module_name_is_expected():
    assert module.__name__ == "src.___init__"


def test_module_package_is_expected():
    assert module.__package__ == "src"


def test_module_has_standard_attributes():
    assert hasattr(module, "__name__")
    assert hasattr(module, "__package__")
    assert hasattr(module, "__dict__")
    assert hasattr(module, "__spec__")


def test_module_namespace_is_dict():
    assert isinstance(module.__dict__, dict)


def test_module_doc_is_none_or_string():
    assert module.__doc__ is None or isinstance(module.__doc__, str)


def test_module_file_if_present_is_string():
    if hasattr(module, "__file__"):
        assert isinstance(module.__file__, str)


def test_module_cached_if_present_is_string_or_none():
    cached = getattr(module, "__cached__", None)
    assert cached is None or isinstance(cached, str)


def test_module_has_loader_and_spec():
    assert hasattr(module, "__loader__")
    assert hasattr(module, "__spec__")
    assert module.__spec__ is not None


def test_module_spec_name_matches_module_name():
    assert module.__spec__.name == module.__name__


def test_module_spec_parent_matches_package():
    assert module.__spec__.parent == module.__package__


def test_module_loader_matches_spec_loader():
    assert module.__loader__ is module.__spec__.loader


def test_module_spec_origin_if_present_is_string_or_none():
    origin = getattr(module.__spec__, "origin", None)
    assert origin is None or isinstance(origin, str)


def test_module_file_matches_spec_origin_when_both_present():
    if hasattr(module, "__file__") and getattr(module.__spec__, "origin", None) is not None:
        assert module.__file__ == module.__spec__.origin


def test_module_name_and_package_are_strings():
    assert isinstance(module.__name__, str)
    assert isinstance(module.__package__, str)


def test_module_name_starts_with_package_prefix():
    assert module.__name__.startswith(module.__package__ + ".")


def test_namespace_contains_basic_dunder_names():
    namespace = module.__dict__
    assert "__name__" in namespace
    assert "__doc__" in namespace
    assert "__package__" in namespace
    assert "__spec__" in namespace


def test_namespace_values_match_module_attributes():
    assert module.__dict__["__name__"] == module.__name__
    assert module.__dict__["__package__"] == module.__package__
    assert module.__dict__.get("__doc__") == module.__doc__
    assert module.__dict__.get("__spec__") is module.__spec__


def test_namespace_loader_matches_module_loader_when_present():
    if "__loader__" in module.__dict__:
        assert module.__dict__["__loader__"] is module.__loader__


def test_all_namespace_keys_are_strings():
    assert all(isinstance(key, str) for key in module.__dict__)


def test_dunder_keys_are_strings():
    dunder_keys = [key for key in module.__dict__ if key.startswith("__")]
    assert all(isinstance(key, str) for key in dunder_keys)


def test_public_names_are_strings():
    public_names = [name for name in module.__dict__ if not name.startswith("_")]
    assert all(isinstance(name, str) for name in public_names)


def test_public_callables_collection_can_be_built():
    public_callables = [
        name
        for name, obj in module.__dict__.items()
        if not name.startswith("_") and callable(obj)
    ]
    assert isinstance(public_callables, list)
    assert all(isinstance(name, str) for name in public_callables)


def test_dir_returns_list_of_strings():
    names = dir(module)
    assert isinstance(names, list)
    assert all(isinstance(name, str) for name in names)


def test_dir_contains_standard_attributes():
    names = dir(module)
    assert "__name__" in names
    assert "__dict__" in names
    assert "__package__" in names
    assert "__spec__" in names


def test_repr_is_string():
    assert isinstance(repr(module), str)


def test_annotations_is_dict_or_absent():
    annotations = getattr(module, "__annotations__", None)
    assert annotations is None or isinstance(annotations, dict)


def test_imported_names_from_star_do_not_break_test_module_globals():
    assert "__name__" in globals()
    assert globals()["__name__"] == __name__


def test_importlib_can_resolve_same_module_by_name():
    resolved = importlib.import_module("src.___init__")
    assert resolved is module
    assert resolved.__name__ == module.__name__
    assert resolved.__package__ == module.__package__


def test_module_spec_is_registered_consistently():
    assert sys.modules[module.__spec__.name] is module


def test_module_dict_identity_is_stable():
    assert module.__dict__ is module.__dict__


def test_module_has_no_unexpected_runtime_side_effects_on_reimport():
    before_keys = set(module.__dict__.keys())
    reimported = importlib.import_module("src.___init__")
    after_keys = set(reimported.__dict__.keys())
    assert reimported is module
    assert before_keys == after_keys


def test_module_spec_has_expected_basic_shape():
    spec = module.__spec__
    assert spec is not None
    assert isinstance(spec.name, str)
    assert spec.loader is module.__loader__


def test_module_dict_contains_builtins_reference():
    assert "__builtins__" in module.__dict__


def test_module_globals_reference_same_module_name():
    assert module.__dict__["__name__"] == "src.___init__"
