import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
import products

def test_get_product_returns_expected_product():
    assert products.get_product(1) == {"name": "Laptop", "price": 1200.0}

def test_get_product_raises_for_missing_product():
    with pytest.raises(ValueError, match="Product not found"):
        products.get_product(999)

def test_list_products_returns_all_products():
    assert products.list_products() == [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]