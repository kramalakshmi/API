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


@pytest.mark.parametrize("product_id", [0, 4, -1, 999, "1", None, (1,), [1]])
def test_get_product_raises_for_missing_or_non_matching_keys(product_id):
    if isinstance(product_id, list):
        with pytest.raises(TypeError):
            get_product(product_id)
    else:
        with pytest.raises(ValueError, match="Product not found"):
            get_product(product_id)


def test_get_product_raises_type_error_for_unhashable_dict_key():
    with pytest.raises(TypeError):
        get_product({1: "a"})


def test_get_product_accepts_bool_true_as_key_equivalent_to_1():
    assert get_product(True) is PRODUCTS[1]


def test_get_product_accepts_float_one_as_key_equivalent_to_1():
    assert get_product(1.0) is PRODUCTS[1]


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


def test_modifying_returned_list_does_not_change_products_mapping():
    products_list = list_products()
    removed = products_list.pop()
    assert removed is PRODUCTS[3]
    assert len(products_list) == 2
    assert len(PRODUCTS) == 3
    assert PRODUCTS[3] == {"name": "Keyboard", "price": 45.0}


def test_products_mapping_has_expected_structure():
    assert set(PRODUCTS.keys()) == {1, 2, 3}
    for product in PRODUCTS.values():
        assert set(product.keys()) == {"name", "price"}
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], float)


def test_modifying_product_from_get_product_reflects_in_products_mapping():
    original_name = PRODUCTS[1]["name"]
    try:
        product = get_product(1)
        product["name"] = "Updated Laptop"
        assert PRODUCTS[1]["name"] == "Updated Laptop"
    finally:
        PRODUCTS[1]["name"] = original_name


def test_modifying_product_from_list_products_reflects_in_products_mapping():
    original_price = PRODUCTS[2]["price"]
    try:
        products_list = list_products()
        products_list[1]["price"] = 30.0
        assert PRODUCTS[2]["price"] == 30.0
    finally:
        PRODUCTS[2]["price"] = original_price


def test_list_products_on_empty_products_returns_empty_list():
    original_products = PRODUCTS.copy()
    try:
        PRODUCTS.clear()
        assert list_products() == []
    finally:
        PRODUCTS.clear()
        PRODUCTS.update(original_products)


def test_get_product_on_empty_products_raises_value_error():
    original_products = PRODUCTS.copy()
    try:
        PRODUCTS.clear()
        with pytest.raises(ValueError, match="Product not found"):
            get_product(1)
    finally:
        PRODUCTS.clear()
        PRODUCTS.update(original_products)
