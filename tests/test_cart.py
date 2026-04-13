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

