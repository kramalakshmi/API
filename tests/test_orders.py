import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.orders import calculate_order_total, create_order


def test_calculate_order_total(monkeypatch):
    products = {1: {"price": 10.0}, 2: {"price": 2.5}}

    def fake_get_product(product_id):
        return products[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    assert calculate_order_total({1: 2, 2: 4}) == 30.0


def test_create_order_empty_cart_raises():
    with pytest.raises(ValueError):
        create_order({})


def test_create_order(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 3.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    result = create_order({5: 2})
    assert result == {"items": {5: 2}, "total": 6.0, "status": "CREATED"}