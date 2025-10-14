from simple_example import add_numbers, multiply_numbers, divide_numbers, is_even
import pytest

def test_add_numbers():
    """Test for add_numbers function."""
    # Happy path
    assert add_numbers(2, 3) == 5
    assert add_numbers(0, 0) == 0
    assert add_numbers(-1, 1) == 0
    
    # Edge cases
    assert add_numbers(1.5, 2.5) == 4.0
    assert add_numbers(-5, -3) == -8

def test_multiply_numbers():
    """Test for multiply_numbers function."""
    # Happy path
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(0, 5) == 0
    assert multiply_numbers(1, 10) == 10
    
    # Edge cases
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(2.5, 4) == 10.0

def test_divide_numbers():
    """Test for divide_numbers function."""
    # Happy path
    assert divide_numbers(10, 2) == 5.0
    assert divide_numbers(9, 3) == 3.0
    assert divide_numbers(1, 2) == 0.5
    
    # Error case
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(5, 0)

def test_is_even():
    """Test for is_even function."""
    # Happy path
    assert is_even(2) == True
    assert is_even(4) == True
    assert is_even(0) == True
    
    # Edge cases
    assert is_even(1) == False
    assert is_even(3) == False
    assert is_even(-2) == True
    assert is_even(-1) == False
