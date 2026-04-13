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
        "a": {"price": 2.5},
        "b": {"price": 4.0},
        "c": {"price": 1.25},
    }

    def fake_get_product(product_id):
        return products[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"a": 2, "b": 1, "c": 4})

    assert result == 2.5 * 2 + 4.0 * 1 + 1.25 * 4


def test_calculate_order_total_empty_cart_returns_zero_and_does_not_call_get_product(monkeypatch):
    def fake_get_product(product_id):
        raise AssertionError("get_product should not be called for empty cart")

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({})

    assert result == 0.0


def test_create_order_returns_expected_structure(monkeypatch):
    def fake_get_product(product_id):
        prices = {
            "x": {"price": 3.0},
            "y": {"price": 7.5},
        }
        return prices[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    cart = {"x": 2, "y": 1}
    result = create_order(cart)

    assert result == {
        "items": cart,
        "total": 13.5,
        "status": "CREATED",
    }


def test_create_order_raises_for_empty_cart():
    with pytest.raises(ValueError, match="Cannot create order with empty cart"):
        create_order({})


def test_create_order_propagates_get_product_exception(monkeypatch):
    def fake_get_product(product_id):
        raise KeyError(product_id)

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    with pytest.raises(KeyError, match="missing"):
        create_order({"missing": 1})