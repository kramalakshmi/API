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
    assert cart.total_items() == 6
    assert cart.items == {1: 3, 2: 3}

def test_add_item_invalid_quantity():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(1, 0)

def test_remove_item_and_clear():
    cart = Cart()
    cart.add_item(1, 2)
    cart.remove_item(1)
    assert cart.items == {}
    with pytest.raises(ValueError):
        cart.remove_item(1)
    cart.add_item(2, 4)
    cart.clear()
    assert cart.items == {}
    assert cart.total_items() == 0
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
import cart
