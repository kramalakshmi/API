import pytest


def test_cart_init_starts_empty():
    from src.cart import Cart

    cart = Cart()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_add_item_with_default_quantity():
    from src.cart import Cart

    cart = Cart()
    result = cart.add_item(1)

    assert result is None
    assert cart.items == {1: 1}
    assert cart.total_items() == 1


def test_add_item_with_explicit_quantity_and_accumulates():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(10, 3)
    cart.add_item(10, 4)

    assert cart.items == {10: 7}
    assert cart.total_items() == 7


def test_add_item_multiple_products_updates_total_items():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)
    cart.add_item(3)

    assert cart.items == {1: 2, 2: 3, 3: 1}
    assert cart.total_items() == 6


def test_add_item_accepts_zero_and_negative_product_ids():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(0, 3)
    cart.add_item(-1, 2)

    assert cart.items == {0: 3, -1: 2}
    assert cart.total_items() == 5


@pytest.mark.parametrize("qty", [0, -1, -5])
def test_add_item_raises_for_non_positive_quantity_and_preserves_state(qty):
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(2, qty)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2


def test_remove_item_deletes_existing_product():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)

    result = cart.remove_item(1)

    assert result is None
    assert cart.items == {2: 3}
    assert cart.total_items() == 3


def test_remove_item_raises_when_product_not_in_cart_and_preserves_state():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(999)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2


def test_remove_item_raises_on_empty_cart():
    from src.cart import Cart

    cart = Cart()

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(1)

    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_then_readd_same_product():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(9, 2)
    cart.remove_item(9)
    cart.add_item(9, 5)

    assert cart.items == {9: 5}
    assert cart.total_items() == 5


def test_total_items_returns_sum_after_multiple_operations():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 5)
    cart.add_item(1, 3)
    cart.remove_item(2)

    assert cart.items == {1: 5}
    assert cart.total_items() == 5


def test_clear_empties_cart_and_returns_none():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)

    result = cart.clear()

    assert result is None
    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_on_empty_cart_is_safe_and_idempotent():
    from src.cart import Cart

    cart = Cart()

    cart.clear()
    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_cart_can_be_reused_after_clear():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)
    cart.clear()
    cart.add_item(3, 4)

    assert cart.items == {3: 4}
    assert cart.total_items() == 4


def test_clear_mutates_existing_items_dict_reference():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(11, 1)
    items_ref = cart.items

    cart.clear()

    assert items_ref is cart.items
    assert items_ref == {}
    assert cart.total_items() == 0


def test_sequence_of_operations_produces_expected_final_state():
    from src.cart import Cart

    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)
    cart.add_item(1, 3)
    cart.remove_item(2)
    cart.add_item(3)

    assert cart.items == {1: 5, 3: 1}
    assert cart.total_items() == 6
