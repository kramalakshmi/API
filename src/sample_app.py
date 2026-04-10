import math

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b

def normalize(values):
    total = sum(values)
    if total == 0:
        return [0 for _ in values]
    return [v / total for v in values]

def compute_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main():
    print("Addition:", add(2, 3))
    print("Division:", divide(10, 2))
    print("Normalized:", normalize([1, 1, 2]))
    print("Distance:", compute_distance(0, 0, 3, 4))

if __name__ == "__main__":
    main()
