class Cart:
    def __init__(self):
        self.items = {}  # product_id → quantity

    def add_item(self, product_id: int, qty: int = 1):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        self.items[product_id] = self.items.get(product_id, 0) + qty

    def remove_item(self, product_id: int):
        if product_id not in self.items:
            raise ValueError("Item not in cart")
        del self.items[product_id]

    def total_items(self):
        return sum(self.items.values())

    def clear(self):
        self.items.clear()
