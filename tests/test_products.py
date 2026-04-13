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
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))
import products

def test_get_product_returns_existing_product():
    assert products.get_product(1) == {"name": "Laptop", "price": 1200.0}
    assert products.get_product(2) == {"name": "Mouse", "price": 25.0}
    assert products.get_product(3) == {"name": "Keyboard", "price": 45.0}

def test_get_product_raises_for_missing_product():
    try:
        products.get_product(999)
        assert False
    except ValueError as exc:
        assert str(exc) == "Product not found"

def test_list_products_returns_all_products():
    assert products.list_products() == [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]

import pytest
import products

def test_get_product_returns_expected_product():
    result = products.get_product(1)
    assert result == {"name": "Laptop", "price": 1200.0}

def test_get_product_raises_for_missing_product():
    with pytest.raises(ValueError, match="Product not found"):
        products.get_product(999)

def test_list_products_returns_all_products():
    result = products.list_products()
    assert result == [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]
