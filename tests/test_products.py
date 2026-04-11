import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.products import PRODUCTS, get_product, list_products

def test_get_product_returns_expected_product():
    assert get_product(1) == {"name": "Laptop", "price": 1200.0}

def test_get_product_raises_for_missing_product():
    with pytest.raises(ValueError, match="Product not found"):
        get_product(999)

def test_list_products_returns_all_products():
    assert list_products() == list(PRODUCTS.values())