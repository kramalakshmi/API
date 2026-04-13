import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.cart import Cart


def test_cart_init_starts_empty():
    cart = Cart()
    assert cart.items == {}
    assert cart.total_items() == 0


def test_add_item_default_quantity():
    cart = Cart()
    cart.add_item(1)
    assert cart.items == {1: 1}
    assert cart.total_items() == 1


def test_add_item_accumulates_quantity_for_same_product():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(1, 3)
    assert cart.items == {1: 5}
    assert cart.total_items() == 5


def test_add_item_multiple_products_updates_total():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 4)
    assert cart.items == {1: 2, 2: 4}
    assert cart.total_items() == 6


@pytest.mark.parametrize("qty", [0, -1, -5])
def test_add_item_rejects_non_positive_quantity(qty):
    cart = Cart()
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(1, qty)
    assert cart.items == {}


def test_remove_item_existing_product():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)
    cart.remove_item(1)
    assert cart.items == {2: 1}
    assert cart.total_items() == 1


def test_remove_item_missing_product_raises():
    cart = Cart()
    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(999)


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