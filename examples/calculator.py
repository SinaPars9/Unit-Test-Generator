def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate_discount(price, discount):
    if price < 0 or discount < 0 or discount > 100:
        raise ValueError("Invalid input")
    return price * (1 - discount / 100)