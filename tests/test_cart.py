import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.cart import Cart

def test_add_item_and_total_items():
    cart = Cart()
    cart.add_item(1)
    cart.add_item(1, 2)
    cart.add_item(2, 3)
    assert cart.items == {1: 3, 2: 3}
    assert cart.total_items() == 6

def test_add_item_with_non_positive_quantity_raises():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(1, 0)
    with pytest.raises(ValueError):
        cart.add_item(1, -1)

def test_remove_item_and_missing_item_raises():
    cart = Cart()
    cart.add_item(1, 2)
    cart.remove_item(1)
    assert cart.items == {}
    with pytest.raises(ValueError):
        cart.remove_item(1)

def test_clear_empties_cart():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)
    cart.clear()
    assert cart.items == {}
    assert cart.total_items() == 0