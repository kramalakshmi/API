import pytest

from src.sample import add, divide, greet, list_items


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (-1, -2, -3),
        (0, 5, 5),
        (1.5, 2.5, 4.0),
        (-3, 3, 0),
        (True, True, 2),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_add_with_strings_concatenates():
    assert add("Hello, ", "world") == "Hello, world"


def test_add_with_lists_concatenates():
    assert add([1, 2], [3]) == [1, 2, 3]


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (8, 2, 4.0),
        (7, 2, 3.5),
        (-9, 3, -3.0),
        (0, 5, 0.0),
        (5, -2, -2.5),
        (1, 4, 0.25),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="b cannot be zero"):
        divide(1, 0)


def test_divide_zero_by_negative_number():
    assert divide(0, -3) == 0.0


def test_greet_returns_expected_message():
    assert greet("Alice") == "Hello, Alice!"


def test_greet_with_empty_string():
    assert greet("") == "Hello, !"


def test_greet_with_whitespace_name():
    assert greet("Bob Smith") == "Hello, Bob Smith!"


def test_greet_preserves_leading_and_trailing_spaces():
    assert greet("  Alice  ") == "Hello,   Alice  !"


def test_list_items_returns_expected_list():
    assert list_items() == ["apple", "banana", "carrot"]


def test_list_items_returns_new_list_each_time():
    first = list_items()
    second = list_items()

    assert first == second
    assert first is not second


def test_list_items_contents_and_order():
    items = list_items()
    assert items[0] == "apple"
    assert items[1] == "banana"
    assert items[2] == "carrot"
    assert len(items) == 3


def test_list_items_mutating_returned_list_does_not_affect_future_calls():
    items = list_items()
    items.append("dragonfruit")

    assert list_items() == ["apple", "banana", "carrot"]


def test_list_items_returns_strings_only():
    items = list_items()
    assert all(isinstance(item, str) for item in items)
