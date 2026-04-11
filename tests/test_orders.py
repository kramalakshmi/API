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


def test_create_order_returns_created_order(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 3.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)
    assert create_order({1: 2}) == {
        "items": {1: 2},
        "total": 6.0,
        "status": "CREATED",
    }


def test_create_order_empty_cart_raises():
    with pytest.raises(ValueError):
        create_order({})
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
    import pytest
    import orders

    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        orders.create_order({})


def test_create_order_returns_created_order(monkeypatch):
    import orders

    monkeypatch.setattr(orders, "calculate_order_total", lambda cart_items: 42.0)

    cart = {1: 2, 2: 1}
    result = orders.create_order(cart)

    assert result == {
        "items": cart,
        "total": 42.0,
        "status": "CREATED",
    }
```
