"""
A simple calculator module for testing the test generator.
"""

import math
from typing import Union, List


class Calculator:
    """A basic calculator with mathematical operations."""
    
    def __init__(self):
        self.history: List[str] = []
        self.precision = 2
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Add two numbers."""
        result = float(a + b)
        self.history.append(f"{a} + {b} = {result}")
        return round(result, self.precision)
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Subtract second number from first."""
        result = float(a - b)
        self.history.append(f"{a} - {b} = {result}")
        return round(result, self.precision)
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Multiply two numbers."""
        result = float(a * b)
        self.history.append(f"{a} * {b} = {result}")
        return round(result, self.precision)
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Divide first number by second."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = float(a / b)
        self.history.append(f"{a} / {b} = {result}")
        return round(result, self.precision)
    
    def power(self, base: Union[int, float], exponent: Union[int, float]) -> float:
        """Raise base to the power of exponent."""
        result = float(base ** exponent)
        self.history.append(f"{base} ^ {exponent} = {result}")
        return round(result, self.precision)
    
    def sqrt(self, number: Union[int, float]) -> float:
        """Calculate square root."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(number)
        self.history.append(f"√{number} = {result}")
        return round(result, self.precision)
    
    def clear_history(self) -> None:
        """Clear calculation history."""
        self.history.clear()
    
    def get_history(self) -> List[str]:
        """Get calculation history."""
        return self.history.copy()
    
    def set_precision(self, precision: int) -> None:
        """Set decimal precision for results."""
        if precision < 0:
            raise ValueError("Precision must be non-negative")
        self.precision = precision


def calculate_bmi(weight: float, height: float) -> float:
    """Calculate Body Mass Index."""
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive")
    
    # BMI = weight (kg) / height (m)^2
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms."""
    if n < 0:
        raise ValueError("Number of terms must be non-negative")
    
    if n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib
