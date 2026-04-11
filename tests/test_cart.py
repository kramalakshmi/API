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

