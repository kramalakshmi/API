import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from src.products import get_product, list_products

def test_get_product_returns_product():
    assert get_product(1) == {"name": "Laptop", "price": 1200.0}

def test_get_product_raises_for_missing_product():
    with pytest.raises(ValueError, match="Product not found"):
        get_product(999)

def test_list_products_returns_all_products():
    assert list_products() == [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]
```python
def test_get_product_returns_expected_product():
    import products
    assert products.get_product(1) == {"name": "Laptop", "price": 1200.0}
    assert products.get_product(2) == {"name": "Mouse", "price": 25.0}
    assert products.get_product(3) == {"name": "Keyboard", "price": 45.0}


def test_get_product_raises_for_missing_product():
    import pytest
    import products
    with pytest.raises(ValueError, match="Product not found"):
        products.get_product(999)


def test_list_products_returns_all_products():
    import products
    assert products.list_products() == [
        {"name": "Laptop", "price": 1200.0},
        {"name": "Mouse", "price": 25.0},
        {"name": "Keyboard", "price": 45.0},
    ]
```
