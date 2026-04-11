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