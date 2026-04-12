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


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src')))

import pytest
from unittest.mock import patch
import orders


def test_create_order_raises_value_error_for_empty_cart():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        orders.create_order({})


def test_create_order_returns_created_order_with_items_total_and_status():
    cart_items = {"p1": 2, "p2": 1}
    with patch("orders.calculate_order_total", return_value=25.5) as mock_calculate:
        result = orders.create_order(cart_items)

    mock_calculate.assert_called_once_with(cart_items)
    assert result == {
        "items": cart_items,
        "total": 25.5,
        "status": "CREATED"
    }
