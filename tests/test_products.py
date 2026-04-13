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


def test_get_product_raises_value_error_for_missing_product_ids():
    for invalid_id in (0, 4, -1, 999):
        with pytest.raises(ValueError, match="Product not found"):
            get_product(invalid_id)


def test_list_products_returns_all_products_in_insertion_order():
    expected = [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]
    assert list_products() == expected


def test_list_products_matches_products_values_snapshot():
    assert list_products() == list(PRODUCTS.values())