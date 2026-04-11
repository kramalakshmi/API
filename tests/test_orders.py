import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.orders import calculate_order_total, create_order

def test_calculate_order_total(monkeypatch):
    prices = {1: {"price": 10.0}, 2: {"price": 2.5}}
    monkeypatch.setattr("src.orders.get_product", lambda product_id: prices[product_id])
    assert calculate_order_total({1: 2, 2: 4}) == 30.0

def test_create_order_empty_cart():
    with pytest.raises(ValueError):
        create_order({})

def test_create_order(monkeypatch):
    monkeypatch.setattr("src.orders.get_product", lambda product_id: {"price": 3.0})
    result = create_order({5: 2})
    assert result == {"items": {5: 2}, "total": 6.0, "status": "CREATED"}