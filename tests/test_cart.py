import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.cart import Cart


def test_cart_initializes_empty():
    cart = Cart()
    assert cart.items == {}
    assert cart.total_items() == 0


def test_add_item_adds_new_product_with_default_quantity():
    cart = Cart()
    cart.add_item(1)
    assert cart.items == {1: 1}
    assert cart.total_items() == 1


def test_add_item_adds_specified_quantity():
    cart = Cart()
    cart.add_item(2, 3)
    assert cart.items == {2: 3}
    assert cart.total_items() == 3


def test_add_item_accumulates_quantity_for_existing_product():
    cart = Cart()
    cart.add_item(5, 2)
    cart.add_item(5, 4)
    assert cart.items == {5: 6}
    assert cart.total_items() == 6


@pytest.mark.parametrize("qty", [0, -1, -5])
def test_add_item_raises_for_non_positive_quantity(qty):
    cart = Cart()
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(1, qty)
    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_removes_existing_product():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)

    cart.remove_item(1)

    assert cart.items == {2: 3}
    assert cart.total_items() == 3


def test_remove_item_raises_for_missing_product():
    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(99)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2


def test_total_items_sums_quantities_across_multiple_products():
    cart = Cart()
    cart.add_item(10, 1)
    cart.add_item(20, 4)
    cart.add_item(30, 2)

    assert cart.total_items() == 7


def test_clear_empties_cart():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_on_empty_cart_is_safe():
    cart = Cart()

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0