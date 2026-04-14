def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("b cannot be zero")
    return a / b

def greet(name):
    return f"Hello, {name}!"

def list_items():
    return ["apple", "banana", "carrot"]

if __name__ == "__main__":
    print("This should not be tested")
