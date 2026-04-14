import pytest

from src.orders import calculate_order_total, create_order


def test_calculate_order_total_single_item(monkeypatch):
    def fake_get_product(product_id):
        assert product_id == "p1"
        return {"price": 10.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    assert calculate_order_total({"p1": 3}) == 30.0


def test_calculate_order_total_multiple_items(monkeypatch):
    products = {
        "a": {"price": 2.5},
        "b": {"price": 4.0},
        "c": {"price": 1.25},
    }

    def fake_get_product(product_id):
        return products[product_id]

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    assert calculate_order_total({"a": 2, "b": 1, "c": 4}) == 14.0


def test_calculate_order_total_empty_cart_returns_zero_and_does_not_call_get_product(monkeypatch):
    def fake_get_product(product_id):
        raise AssertionError("get_product should not be called for empty cart")

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    assert calculate_order_total({}) == 0.0


def test_calculate_order_total_calls_get_product_for_each_cart_item(monkeypatch):
    calls = []

    def fake_get_product(product_id):
        calls.append(product_id)
        return {"price": {"a": 1.0, "b": 2.0}[product_id]}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"a": 3, "b": 2})

    assert result == 7.0
    assert calls == ["a", "b"]


def test_calculate_order_total_propagates_get_product_exception(monkeypatch):
    def fake_get_product(product_id):
        raise KeyError(product_id)

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    with pytest.raises(KeyError, match="missing"):
        calculate_order_total({"missing": 1})


def test_calculate_order_total_allows_zero_quantity(monkeypatch):
    calls = []

    def fake_get_product(product_id):
        calls.append(product_id)
        return {"price": 9.99}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = calculate_order_total({"p1": 0})

    assert result == 0.0
    assert calls == ["p1"]


def test_calculate_order_total_allows_negative_quantity(monkeypatch):
    def fake_get_product(product_id):
        assert product_id == "p1"
        return {"price": 5.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    assert calculate_order_total({"p1": -2}) == -10.0


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


def test_create_order_uses_calculated_total(monkeypatch):
    def fake_get_product(product_id):
        return {"price": {"p1": 5.0, "p2": 1.5}[product_id]}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    cart = {"p1": 2, "p2": 4}
    result = create_order(cart)

    assert result["items"] == cart
    assert result["total"] == 16.0
    assert result["status"] == "CREATED"


def test_create_order_preserves_same_cart_object_reference(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 2.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    cart = {"item": 3}
    result = create_order(cart)

    assert result["items"] is cart


def test_create_order_calls_get_product_for_each_item_via_total_calculation(monkeypatch):
    calls = []

    def fake_get_product(product_id):
        calls.append(product_id)
        return {"price": {"a": 2.0, "b": 3.0}[product_id]}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    result = create_order({"a": 1, "b": 2})

    assert result["total"] == 8.0
    assert calls == ["a", "b"]


def test_create_order_with_zero_quantity_item_still_creates_order(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 4.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    cart = {"item": 0}
    result = create_order(cart)

    assert result == {
        "items": cart,
        "total": 0.0,
        "status": "CREATED",
    }


def test_create_order_with_negative_quantity_uses_calculated_negative_total(monkeypatch):
    def fake_get_product(product_id):
        return {"price": 4.0}

    monkeypatch.setattr("src.orders.get_product", fake_get_product)

    cart = {"item": -2}
    result = create_order(cart)

    assert result == {
        "items": cart,
        "total": -8.0,
        "status": "CREATED",
    }
