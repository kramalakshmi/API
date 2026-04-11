import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.orders import calculate_order_total, create_order


def test_calculate_order_total(monkeypatch):
    products = {
        "p1": {"price": 10.0},
        "p2": {"price": 2.5},
    }

    def fake_get_product(product_id):
        return products[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    assert calculate_order_total({"p1": 2, "p2": 4}) == 30.0


def test_create_order(monkeypatch):
    def fake_calculate_order_total(cart_items):
        return 42.0

    monkeypatch.setattr("src.orders.calculate_order_total", fake_calculate_order_total)
    cart_items = {"p1": 3}
    result = create_order(cart_items)
    assert result == {"items": cart_items, "total": 42.0, "status": "CREATED"}


def test_create_order_empty_cart_raises():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        create_order({})
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))

import pytest
from unittest.mock import patch
from src.orders import calculate_order_total, create_order

def test_calculate_order_total_sums_prices_times_quantities():
    cart_items = {"p1": 2, "p2": 3}
    with patch("src.orders.get_product") as mock_get_product:
        mock_get_product.side_effect = [
            {"price": 10.0},
            {"price": 5.5},
        ]
        total = calculate_order_total(cart_items)
    assert total == pytest.approx(36.5)

def test_calculate_order_total_returns_zero_for_empty_cart():
    assert calculate_order_total({}) == 0.0

def test_create_order_raises_for_empty_cart():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        create_order({})

def test_create_order_returns_created_order_with_total():
    cart_items = {"p1": 1, "p2": 4}
    with patch("src.orders.calculate_order_total", return_value=42.0) as mock_total:
        order = create_order(cart_items)
    mock_total.assert_called_once_with(cart_items)
    assert order == {
        "items": cart_items,
        "total": 42.0,
        "status": "CREATED"
    }
