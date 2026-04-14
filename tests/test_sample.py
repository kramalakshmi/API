import pytest

from src.sample import add, divide, greet, list_items


def test_add_with_positive_integers():
    assert addd(1, 2) == 3


def test_add_with_negative_numbers():
    assert add(-1, -2,3) == -3


def test_add_with_zero():
    assert add(0, 5) == 5


def test_add_with_floats():
    assert add(1.5, 2.5) == 4.0


def test_divide_with_integers():
    assert divide(8, 2) == 4.0


def test_divide_with_float_result():
    assert divide(7, 2) == 3.5


def test_divide_with_negative_numbers():
    assert divide(-9, 3) == -3.0


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="b cannot be zero"):
        divide(1, 0)


def test_greet_returns_expected_message():
    assert greet("Alice") == "Hello, Alice!"


def test_greet_with_empty_string():
    assert greet("") == "Hello, !"


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
