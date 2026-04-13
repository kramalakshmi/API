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


def test_add_item_with_default_quantity():
    cart = Cart()
    cart.add_item(1)
    assert cart.items == {1: 1}
    assert cart.total_items() == 1


def test_add_item_with_explicit_quantity():
    cart = Cart()
    cart.add_item(2, 3)
    assert cart.items == {2: 3}
    assert cart.total_items() == 3


def test_add_item_accumulates_quantity_for_same_product():
    cart = Cart()
    cart.add_item(5, 2)
    cart.add_item(5, 4)
    assert cart.items == {5: 6}
    assert cart.total_items() == 6


def test_add_item_multiple_products_total_items():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)
    cart.add_item(3, 1)
    assert cart.items == {1: 2, 2: 3, 3: 1}
    assert cart.total_items() == 6


@pytest.mark.parametrize("qty", [0, -1, -5])
def test_add_item_raises_for_non_positive_quantity(qty):
    cart = Cart()
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(1, qty)
    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_existing_product():
    cart = Cart()
    cart.add_item(10, 2)
    cart.add_item(20, 1)

    cart.remove_item(10)

    assert cart.items == {20: 1}
    assert cart.total_items() == 1


def test_remove_item_raises_when_product_not_in_cart():
    cart = Cart()
    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(999)


def test_remove_item_raises_for_missing_product_after_other_items_added():
    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(2)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2


def test_total_items_empty_cart():
    cart = Cart()
    assert cart.total_items() == 0


def test_clear_empties_cart():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_on_empty_cart_is_safe():
    cart = Cart()
    cart.clear()
    assert cart.items == {}
    assert cart.total_items() == 0