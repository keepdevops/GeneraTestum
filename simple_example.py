def add_numbers(a, b):
    """Add two numbers."""
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers."""
    return a * b

def divide_numbers(a, b):
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def is_even(n):
    """Check if a number is even."""
    return n % 2 == 0
