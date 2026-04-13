import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.orders import calculate_order_total
from src.orders import create_order


def test_calculate_order_total_single_item(monkeypatch):
    def fake_get_product(product_id):
        assert product_id == "p1"
        return {"price": 10.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"p1": 3})

    assert result == 30.0


def test_calculate_order_total_multiple_items(monkeypatch):
    products = {
        "p1": {"price": 5.5},
        "p2": {"price": 2.0},
        "p3": {"price": 1.25},
    }

    def fake_get_product(product_id):
        return products[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"p1": 2, "p2": 4, "p3": 3})

    assert result == 5.5 * 2 + 2.0 * 4 + 1.25 * 3


def test_calculate_order_total_empty_cart(monkeypatch):
    calls = []

    def fake_get_product(product_id):
        calls.append(product_id)
        return {"price": 1.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({})

    assert result == 0.0
    assert calls == []


def test_create_order_returns_expected_structure(monkeypatch):
    def fake_calculate_order_total(cart_items):
        assert cart_items == {"p1": 2, "p2": 1}
        return 42.5

    monkeypatch.setattr("src.orders.calculate_order_total", fake_calculate_order_total)

    cart = {"p1": 2, "p2": 1}
    result = create_order(cart)

    assert result == {
        "items": cart,
        "total": 42.5,
        "status": "CREATED",
    }


def test_create_order_raises_for_empty_cart():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        create_order({})


def test_create_order_uses_calculated_total(monkeypatch):
    def fake_get_product(product_id):
        prices = {
            "a": {"price": 3.0},
            "b": {"price": 4.5},
        }
        return prices[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = create_order({"a": 2, "b": 2})

    assert result["items"] == {"a": 2, "b": 2}
    assert result["total"] == 15.0
    assert result["status"] == "CREATED"