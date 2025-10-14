"""
Example test file for Calculator class.
This shows how to test a class with methods, state changes, and error handling.
"""

import pytest
from calculator import Calculator

class TestCalculator:
    """Test cases for Calculator class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()

    def test_calculator_initialization(self):
        """Test Calculator initialization."""
        calc = Calculator()
        assert calc is not None
        assert calc.history == []

    def test_add(self):
        """Test Calculator.add method."""
        result = self.calc.add(2, 3)
        assert result == 5
        assert '2 + 3 = 5' in self.calc.history

    def test_add_float_numbers(self):
        """Test Calculator.add with float numbers."""
        result = self.calc.add(1.5, 2.5)
        assert result == 4.0
        assert '1.5 + 2.5 = 4.0' in self.calc.history

    def test_subtract(self):
        """Test Calculator.subtract method."""
        result = self.calc.subtract(10, 3)
        assert result == 7
        assert '10 - 3 = 7' in self.calc.history

    def test_multiply(self):
        """Test Calculator.multiply method."""
        result = self.calc.multiply(4, 5)
        assert result == 20
        assert '4 * 5 = 20' in self.calc.history

    def test_divide(self):
        """Test Calculator.divide method."""
        result = self.calc.divide(10, 2)
        assert result == 5.0
        assert '10 / 2 = 5.0' in self.calc.history

    def test_divide_by_zero(self):
        """Test Calculator.divide with zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(5, 0)

    def test_power(self):
        """Test Calculator.power method."""
        result = self.calc.power(2, 3)
        assert result == 8
        assert '2 ** 3 = 8' in self.calc.history

    def test_sqrt(self):
        """Test Calculator.sqrt method."""
        result = self.calc.sqrt(16)
        assert result == 4.0
        assert 'sqrt(16) = 4.0' in self.calc.history

    def test_sqrt_negative_number(self):
        """Test Calculator.sqrt with negative number raises error."""
        with pytest.raises(ValueError, match="Cannot calculate square root of a negative number"):
            self.calc.sqrt(-1)

    def test_clear_history(self):
        """Test Calculator.clear_history method."""
        # Add some operations
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        assert len(self.calc.history) == 2
        
        # Clear history
        self.calc.clear_history()
        assert self.calc.history == []

    def test_get_history(self):
        """Test Calculator.get_history method."""
        # Add some operations
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        
        history = self.calc.get_history()
        assert len(history) == 2
        assert '1 + 2 = 3' in history
        assert '3 * 4 = 12' in history

    def test_set_precision(self):
        """Test Calculator.set_precision method."""
        # This is a placeholder method, so we just test it doesn't crash
        self.calc.set_precision(2)
        # No assertion needed as it's a placeholder

    def test_history_state_changes(self):
        """Test that operations modify history state."""
        # Initial state
        assert len(self.calc.history) == 0
        
        # After first operation
        self.calc.add(1, 2)
        assert len(self.calc.history) == 1
        
        # After second operation
        self.calc.multiply(3, 4)
        assert len(self.calc.history) == 2

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (1.5, 2.5, 4.0),
        (-5, -3, -8)
    ])
    def test_add_parametrized(self, a, b, expected):
        """Test Calculator.add with multiple inputs."""
        result = self.calc.add(a, b)
        assert result == expected

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (9, 3, 3.0),
        (1, 2, 0.5),
        (0, 1, 0.0)
    ])
    def test_divide_parametrized(self, a, b, expected):
        """Test Calculator.divide with multiple inputs."""
        result = self.calc.divide(a, b)
        assert result == expected

    def teardown_method(self):
        """Clean up after each test method."""
        # Clean up if needed
        pass
