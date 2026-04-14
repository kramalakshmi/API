import pytest

from src.cart import Cart


def test_cart_init_starts_empty():
    cart = Cart()
    assert cart.items == {}
    assert cart.total_items() == 0


def test_add_item_with_default_quantity():
    cart = Cart()
    cart.add_item(1)
    assert cart.items == {1: 1}
    assert cart.total_items() == 1


def test_add_item_with_explicit_quantity():
    cart = Cart()
    cart.add_item(10, 3)
    assert cart.items == {10: 3}
    assert cart.total_items() == 3


def test_add_item_accumulates_quantity_for_same_product():
    cart = Cart()
    cart.add_item(5, 2)
    cart.add_item(5, 4)
    assert cart.items == {5: 6}
    assert cart.total_items() == 6


def test_add_item_multiple_products_updates_total_items():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)
    cart.add_item(3)
    assert cart.items == {1: 2, 2: 3, 3: 1}
    assert cart.total_items() == 6


@pytest.mark.parametrize("qty", [0, -1, -5])
def test_add_item_raises_for_non_positive_quantity(qty):
    cart = Cart()
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(1, qty)
    assert cart.items == {}
    assert cart.total_items() == 0


def test_add_item_invalid_quantity_does_not_modify_existing_cart():
    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(2, 0)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2


def test_add_item_with_keyword_arguments():
    cart = Cart()
    cart.add_item(product_id=8, qty=2)
    assert cart.items == {8: 2}
    assert cart.total_items() == 2


def test_add_item_accepts_zero_as_product_id():
    cart = Cart()
    cart.add_item(0, 3)
    assert cart.items == {0: 3}
    assert cart.total_items() == 3


def test_remove_item_deletes_existing_product():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 3)

    cart.remove_item(1)

    assert cart.items == {2: 3}
    assert cart.total_items() == 3


def test_remove_item_removes_only_item_and_cart_can_continue_being_used():
    cart = Cart()
    cart.add_item(1, 1)
    cart.add_item(2, 2)

    cart.remove_item(2)
    cart.add_item(3, 4)

    assert cart.items == {1: 1, 3: 4}
    assert cart.total_items() == 5


def test_remove_item_raises_when_product_not_in_cart():
    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(999)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2


def test_remove_item_raises_on_empty_cart():
    cart = Cart()

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(1)

    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_last_item_results_in_empty_cart():
    cart = Cart()
    cart.add_item(7, 3)

    cart.remove_item(7)

    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_with_keyword_argument():
    cart = Cart()
    cart.add_item(4, 2)

    cart.remove_item(product_id=4)

    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_then_readd_same_product():
    cart = Cart()
    cart.add_item(9, 2)
    cart.remove_item(9)
    cart.add_item(9, 5)

    assert cart.items == {9: 5}
    assert cart.total_items() == 5


def test_total_items_returns_sum_after_multiple_operations():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 5)
    cart.add_item(1, 3)
    cart.remove_item(2)

    assert cart.items == {1: 5}
    assert cart.total_items() == 5


def test_total_items_returns_zero_for_new_cart():
    cart = Cart()
    assert cart.total_items() == 0


def test_total_items_returns_zero_after_clearing_non_empty_cart():
    cart = Cart()
    cart.add_item(1, 4)
    cart.add_item(2, 6)

    cart.clear()

    assert cart.total_items() == 0


def test_clear_empties_cart():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(2, 1)

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_on_empty_cart_is_safe():
    cart = Cart()

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_is_idempotent():
    cart = Cart()
    cart.add_item(1, 2)

    cart.clear()
    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_cart_can_be_reused_after_clear():
    cart = Cart()
    cart.add_item(1, 2)
    cart.clear()

    cart.add_item(3, 4)

    assert cart.items == {3: 4}
    assert cart.total_items() == 4


def test_clear_after_failed_remove_preserves_then_clears_state():
    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(99)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_after_failed_add_preserves_then_clears_state():
    cart = Cart()
    cart.add_item(1, 2)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(2, -3)

    assert cart.items == {1: 2}
    assert cart.total_items() == 2

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_item_after_clear_raises():
    cart = Cart()
    cart.add_item(1, 1)
    cart.clear()

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(1)

    assert cart.items == {}
    assert cart.total_items() == 0


def test_clear_removes_all_products_after_accumulated_adds():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(1, 3)
    cart.add_item(2, 4)

    assert cart.items == {1: 5, 2: 4}
    assert cart.total_items() == 9

    cart.clear()

    assert cart.items == {}
    assert cart.total_items() == 0


def test_remove_one_product_does_not_affect_other_accumulated_product():
    cart = Cart()
    cart.add_item(1, 2)
    cart.add_item(1, 1)
    cart.add_item(2, 5)

    cart.remove_item(2)

    assert cart.items == {1: 3}
    assert cart.total_items() == 3


def test_add_item_after_failed_remove_still_works():
    cart = Cart()

    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(123)

    cart.add_item(123, 2)

    assert cart.items == {123: 2}
    assert cart.total_items() == 2
