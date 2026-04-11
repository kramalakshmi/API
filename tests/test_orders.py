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
```python
def test_calculate_order_total(monkeypatch):
    import orders

    products = {
        1: {"price": 10.0},
        2: {"price": 5.5},
    }

    monkeypatch.setattr(orders, "get_product", lambda product_id: products[product_id])

    result = orders.calculate_order_total({1: 2, 2: 3})

    assert result == 36.5


def test_create_order_raises_for_empty_cart():
    import orders
    import pytest

    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        orders.create_order({})


def test_create_order_returns_created_order(monkeypatch):
    import orders

    monkeypatch.setattr(orders, "calculate_order_total", lambda cart_items: 42.0)

    cart = {1: 2}
    result = orders.create_order(cart)

    assert result == {
        "items": cart,
        "total": 42.0,
        "status": "CREATED",
    }
```
