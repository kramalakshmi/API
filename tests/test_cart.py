import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))

import pytest
import cart

def test_add_and_total_items():
    c = cart.Cart()
    c.add_item(1)
    c.add_item(2, 3)
    c.add_item(1, 2)
    assert c.items == {1: 3, 2: 3}
    assert c.total_items() == 6

def test_add_item_invalid_quantity():
    c = cart.Cart()
    with pytest.raises(ValueError):
        c.add_item(1, 0)

def test_remove_item():
    c = cart.Cart()
    c.add_item(1, 2)
    c.remove_item(1)
    assert c.items == {}
    assert c.total_items() == 0

def test_remove_item_missing():
    c = cart.Cart()
    with pytest.raises(ValueError):
        c.remove_item(1)

def test_clear():
    c = cart.Cart()
    c.add_item(1, 2)
    c.add_item(2, 1)
    c.clear()
    assert c.items == {}
    assert c.total_items() == 0