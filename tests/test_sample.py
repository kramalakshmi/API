import inspect
import pytest

import src.sample as sample_module
from src.sample import add, divide, greet, list_items


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (-1, -2, -3),
        (0, 5, 5),
        (1.5, 2.5, 4.0),
        (1, 2.5, 3.5),
        ("Hello, ", "world", "Hello, world"),
        ([1, 2], [3], [1, 2, 3]),
        ("", "", ""),
        ([], [], []),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_add_raises_type_error_for_incompatible_types():
    with pytest.raises(TypeError):
        add(1, "2")


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (8, 2, 4.0),
        (7, 2, 3.5),
        (-9, 3, -3.0),
        (0, 5, 0.0),
        (5, -2, -2.5),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="b cannot be zero"):
        divide(1, 0)


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Alice", "Hello, Alice!"),
        ("", "Hello, !"),
        ("Bob Smith", "Hello, Bob Smith!"),
        ("  spaced  ", "Hello,   spaced  !"),
        (123, "Hello, 123!"),
    ],
)
def test_greet(name, expected):
    assert greet(name) == expected


def test_list_items_returns_expected_list():
    assert list_items() == ["apple", "banana", "carrot"]


def test_list_items_returns_new_list_each_time():
    first = list_items()
    second = list_items()
    assert first == second
    assert first is not second


def test_list_items_modifying_return_value_does_not_affect_future_calls():
    items = list_items()
    items.append("dragonfruit")
    assert list_items() == ["apple", "banana", "carrot"]


def test_list_items_contents_and_order():
    items = list_items()
    assert len(items) == 3
    assert items[0] == "apple"
    assert items[1] == "banana"
    assert items[2] == "carrot"


def test_list_items_returns_strings_only():
    items = list_items()
    assert all(isinstance(item, str) for item in items)


def test_module_name_on_import():
    assert sample_module.__name__ == "src.sample"


def test_module_source_contains_main_guard_and_print_statement():
    source = inspect.getsource(sample_module)
    assert 'if __name__ == "__main__":' in source
    assert 'print("This should not be tested")' in source


def test_module_file_can_be_compiled():
    source = inspect.getsource(sample_module)
    compile(source, "sample.py", "exec")
