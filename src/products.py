PRODUCTS = {
    1: {"name": "Laptop", "price": 1200.0},
    2: {"name": "Mouse", "price": 25.0},
    3: {"name": "Keyboard", "price": 45.0},
}

def get_product(product_id: int):
    if product_id not in PRODUCTS:
        raise ValueError("Product not found")
    return PRODUCTS[product_id]

def list_products():
    return list(PRODUCTS.values())
