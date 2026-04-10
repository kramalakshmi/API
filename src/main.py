from src.cart import Cart
from src.orders import create_order
from src.products import list_products

def run_demo():
    print("Available products:", list_products())

    cart = Cart()
    cart.add_item(1, 1)
    cart.add_item(2, 2)

    order = create_order(cart.items)
    print("Order created:", order)

if __name__ == "__main__":
    run_demo()
