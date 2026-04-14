import pytest

from src.products import PRODUCTS, get_product, list_products


@pytest.mark.parametrize(
    "product_id, expected",
    [
        (1, {"name": "Laptop", "price": 1200.0}),
        (2, {"name": "Mouse", "price": 25.0}),
        (3, {"name": "Keyboard", "price": 45.0}),
    ],
)
def test_get_product_returns_expected_product_for_valid_ids(product_id, expected):
    assert get_product(product_id) == expected


@pytest.mark.parametrize("product_id", [0, 4, -1, 999])
def test_get_product_raises_value_error_for_invalid_ids(product_id):
    with pytest.raises(ValueError, match="Product not found"):
        get_product(product_id)


def test_get_product_returns_same_object_as_products_mapping():
    product = get_product(1)
    assert product is PRODUCTS[1]


def test_list_products_returns_all_products_in_insertion_order():
    expected = [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]
    assert list_products() == expected


def test_list_products_matches_products_values():
    assert list_products() == list(PRODUCTS.values())


def test_list_products_returns_new_list_each_call():
    first = list_products()
    second = list_products()
    assert first == second
    assert first is not second


def test_list_products_contains_original_product_objects():
    products_list = list_products()
    assert products_list[0] is PRODUCTS[1]
    assert products_list[1] is PRODUCTS[2]
    assert products_list[2] is PRODUCTS[3]
