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


def test_create_order(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 3.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    order = create_order({"x": 2})
    assert order == {"items": {"x": 2}, "total": 6.0, "status": "CREATED"}


def test_create_order_empty_cart():
    with pytest.raises(ValueError):
        create_order({})