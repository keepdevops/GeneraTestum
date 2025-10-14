"""
Basic function test template.
Use this template for simple functions with clear inputs and outputs.
"""

import pytest
from {module_name} import {function_name}

class Test{FunctionName}:
    """Test cases for {function_name} function."""

    def test_{function_name}_happy_path(self):
        """Test {function_name} with normal inputs."""
        # Arrange
        {arrange_code}
        
        # Act
        result = {function_name}({test_args})
        
        # Assert
        assert result == {expected_result}

    def test_{function_name}_edge_cases(self):
        """Test {function_name} with edge cases."""
        # Test edge cases
        {edge_case_tests}

    def test_{function_name}_error_cases(self):
        """Test {function_name} error conditions."""
        # Test error conditions
        {error_case_tests}

    @pytest.mark.parametrize("input_val,expected", [
        {parametrize_cases}
    ])
    def test_{function_name}_parametrized(self, input_val, expected):
        """Test {function_name} with multiple inputs."""
        result = {function_name}(input_val)
        assert result == expected

    def test_{function_name}_type_validation(self):
        """Test {function_name} type validation."""
        # Test type validation if applicable
        {type_validation_tests}
