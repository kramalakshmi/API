import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.products import PRODUCTS, get_product, list_products


def test_get_product_returns_expected_product_for_valid_ids():
    assert get_product(1) == {"name": "Laptop", "price": 1200.0}
    assert get_product(2) == {"name": "Mouse", "price": 25.0}
    assert get_product(3) == {"name": "Keyboard", "price": 45.0}

