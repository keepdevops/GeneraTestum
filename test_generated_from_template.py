"""
Basic function test template.
Use this template for simple functions with clear inputs and outputs.
"""

import pytest
from math_utils import add_numbers

class Test{FunctionName}:
    """Test cases for add_numbers function."""

    def test_add_numbers_happy_path(self):
        """Test add_numbers with normal inputs."""
        # Arrange
        {arrange_code}
        
        # Act
        result = add_numbers({test_args})
        
        # Assert
        assert result == {expected_result}

    def test_add_numbers_edge_cases(self):
        """Test add_numbers with edge cases."""
        # Test edge cases
        {edge_case_tests}

    def test_add_numbers_error_cases(self):
        """Test add_numbers error conditions."""
        # Test error conditions
        {error_case_tests}

    @pytest.mark.parametrize("input_val,expected", [
        {parametrize_cases}
    ])
    def test_add_numbers_parametrized(self, input_val, expected):
        """Test add_numbers with multiple inputs."""
        result = add_numbers(input_val)
        assert result == expected

    def test_add_numbers_type_validation(self):
        """Test add_numbers type validation."""
        # Test type validation if applicable
        {type_validation_tests}
