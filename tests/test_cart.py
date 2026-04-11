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


def test_add_item_invalid_quantity():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(1, 0)


def test_remove_item_and_clear():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)
    cart.remove_item(1)
    assert cart.items == {2: 1}
    cart.clear()
    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_missing_raises():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.remove_item(999)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
import cart

def test_cart_add_item_and_total_items():
    c = cart.Cart()
    c.add_item(1)
    c.add_item(2, 3)
    c.add_item(1, 2)
    assert c.items == {1: 3, 2: 3}
    assert c.total_items() == 6

def test_cart_add_item_raises_for_non_positive_quantity():
    c = cart.Cart()
    import pytest
    with pytest.raises(ValueError, match="Quantity must be positive"):
        c.add_item(1, 0)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        c.add_item(1, -1)

def test_cart_remove_item_success_and_missing_item_error():
    c = cart.Cart()
    c.add_item(10, 2)
    c.remove_item(10)
    assert 10 not in c.items
    import pytest
    with pytest.raises(ValueError, match="Item not in cart"):
        c.remove_item(10)

def test_cart_clear_empties_items_and_total():
    c = cart.Cart()
    c.add_item(1, 2)
    c.add_item(2, 4)
    c.clear()
    assert c.items == {}
    assert c.total_items() == 0
