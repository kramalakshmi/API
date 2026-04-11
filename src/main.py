import cart
import orders
import products

def run_demo():
    print("Available products:", list_products())

    cart = Cart()
    cart.add_item(1, 1)
    cart.add_item(2, 2)

    order = create_order(cart.items)
    print("Order created:", order)

if __name__ == "__main__":
    run_demo()
