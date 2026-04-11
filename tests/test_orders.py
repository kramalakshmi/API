import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.orders import calculate_order_total, create_order

def test_calculate_order_total(monkeypatch):
    def fake_get_product(product_id):
        products = {
            "a": {"price": 10.0},
            "b": {"price": 2.5},
        }
        return products[product_id]
    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    assert calculate_order_total({"a": 2, "b": 4}) == 30.0

def test_create_order_empty_cart_raises():
    with pytest.raises(ValueError):
        create_order({})

def test_create_order(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 3.0}
    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    result = create_order({"x": 2})
    assert result == {"items": {"x": 2}, "total": 6.0, "status": "CREATED"}
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))

import pytest
from unittest.mock import patch
from src.orders import calculate_order_total, create_order


def test_calculate_order_total_sums_product_prices_times_quantities():
    cart_items = {1: 2, 2: 3}
    products = {
        1: {"price": 10.0},
        2: {"price": 5.5},
    }

    with patch("src.orders.get_product", side_effect=lambda product_id: products[product_id]):
        result = calculate_order_total(cart_items)

    assert result == 36.5


def test_create_order_raises_value_error_for_empty_cart():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        create_order({})


def test_create_order_returns_expected_order_structure():
    cart_items = {1: 1, 2: 2}
    products = {
        1: {"price": 12.0},
        2: {"price": 4.0},
    }

    with patch("src.orders.get_product", side_effect=lambda product_id: products[product_id]):
        result = create_order(cart_items)

    assert result == {
        "items": cart_items,
        "total": 20.0,
        "status": "CREATED",
    }
