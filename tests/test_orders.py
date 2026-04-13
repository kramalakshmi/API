import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.orders import calculate_order_total, create_order


def test_calculate_order_total_single_item(monkeypatch):
    def fake_get_product(product_id):
        assert product_id == "p1"
        return {"price": 10.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"p1": 3})

    assert result == 30.0


def test_calculate_order_total_multiple_items(monkeypatch):
    products = {
        "a": {"price": 2.5},
        "b": {"price": 4.0},
        "c": {"price": 1.25},
    }

    def fake_get_product(product_id):
        return products[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"a": 2, "b": 1, "c": 4})

    assert result == 14.0


def test_calculate_order_total_empty_cart(monkeypatch):
    calls = []

    def fake_get_product(product_id):
        calls.append(product_id)
        return {"price": 999.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({})

    assert result == 0.0
    assert calls == []


def test_create_order_returns_expected_structure(monkeypatch):
    cart = {"x": 2, "y": 1}

    def fake_calculate_order_total(cart_items):
        assert cart_items is cart
        return 42.5

    monkeypatch.setattr("src.orders.calculate_order_total", fake_calculate_order_total)

    result = create_order(cart)

    assert result == {
        "items": cart,
        "total": 42.5,
        "status": "CREATED",
    }


def test_create_order_raises_for_empty_cart():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        create_order({})


def test_create_order_uses_calculate_order_total(monkeypatch):
    called = {"count": 0}

    def fake_calculate_order_total(cart_items):
        called["count"] += 1
        assert cart_items == {"p1": 1}
        return 9.99

    monkeypatch.setattr("src.orders.calculate_order_total", fake_calculate_order_total)

    result = create_order({"p1": 1})

    assert called["count"] == 1
    assert result["total"] == 9.99
    assert result["status"] == "CREATED"
    assert result["items"] == {"p1": 1}