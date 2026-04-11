import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.cart import Cart

def test_add_and_total_items():
    cart = Cart()
    cart.add_item(1)
    cart.add_item(2, 3)
    cart.add_item(1, 2)
    assert cart.items == {1: 3, 2: 3}
    assert cart.total_items() == 6

def test_add_item_with_non_positive_quantity_raises():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(1, 0)
    with pytest.raises(ValueError):
        cart.add_item(1, -1)

def test_remove_item_and_clear():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)
    cart.remove_item(1)
    assert cart.items == {2: 1}
    cart.clear()
    assert cart.items == {}
    assert cart.total_items() == 0

def test_remove_missing_item_raises():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.remove_item(99)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
import cart

def test_add_item_increases_quantity_and_total():
    c = cart.Cart()
    c.add_item(1)
    c.add_item(1, 2)
    c.add_item(2, 3)
    assert c.items[1] == 3
    assert c.items[2] == 3
    assert c.total_items() == 6

def test_add_item_raises_for_non_positive_quantity():
    c = cart.Cart()
    import pytest
    with pytest.raises(ValueError, match="Quantity must be positive"):
        c.add_item(1, 0)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        c.add_item(1, -2)

def test_remove_item_deletes_existing_item():
    c = cart.Cart()
    c.add_item(10, 2)
    c.remove_item(10)
    assert 10 not in c.items
    assert c.total_items() == 0

def test_remove_item_raises_when_missing():
    c = cart.Cart()
    import pytest
    with pytest.raises(ValueError, match="Item not in cart"):
        c.remove_item(99)

def test_total_items_empty_and_after_clear():
    c = cart.Cart()
    assert c.total_items() == 0
    c.add_item(1, 2)
    c.add_item(2, 4)
    assert c.total_items() == 6
    c.clear()
    assert c.items == {}
    assert c.total_items() == 0
