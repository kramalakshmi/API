from src.products import get_product

def calculate_order_total(cart_items: dict):
    total = 0.0
    for product_id, qty in cart_items.items():
        product = get_product(product_id)
        total += product["price"] * qty
    return total

def create_order(cart_items: dict):
    if not cart_items:
        raise ValueError("Cannot create order with empty cart")

    total = calculate_order_total(cart_items)
    return {
        "items": cart_items,
        "total": total,
        "status": "CREATED"
    }
