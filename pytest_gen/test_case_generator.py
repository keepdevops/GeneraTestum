"""
Generates test cases for different scenarios.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .config import TestCoverage


@dataclass
class TestCase:
    """A single test case with parameters and expected behavior."""
    name: str
    parameters: Dict[str, Any]
    expected_result: Optional[Any] = None
    expected_exception: Optional[str] = None
    description: Optional[str] = None


class TestCaseGenerator:
    """Generates test cases for comprehensive coverage."""
    
    def __init__(self, config):
        self.config = config
        self._edge_cases = {
            'int': [0, -1, 1, 999999, -999999],
            'float': [0.0, -1.0, 1.0, 3.14159, float('inf'), float('-inf')],
            'str': ['', ' ', 'a', 'hello', 'very long string' * 100],
            'bool': [True, False],
            'list': [[], [1], [1, 2, 3], ['a', 'b', 'c']],
            'dict': [{}, {'key': 'value'}, {'a': 1, 'b': 2}],
        }
        self._error_cases = {
            'int': [None, 'string', [], {}],
            'float': [None, 'string', [], {}],
            'str': [None, 123, [], {}],
            'bool': [None, 'string', 123, []],
            'list': [None, 'string', 123, {}],
            'dict': [None, 'string', 123, []],
        }
    
    def generate_test_cases_for_type(self, param_name: str, param_type: str, func_info) -> List[TestCase]:
        """Generate test cases for a specific parameter type."""
        test_cases = []
        base_type = self._extract_base_type(param_type)
        
        # Happy path cases
        if self.config.coverage_type in [TestCoverage.HAPPY_PATH, TestCoverage.COMPREHENSIVE, TestCoverage.FULL]:
            test_cases.extend(self._generate_happy_path_cases(param_name, base_type))
        
        # Edge cases
        if self.config.generate_edge_cases and self.config.coverage_type in [TestCoverage.COMPREHENSIVE, TestCoverage.FULL]:
            test_cases.extend(self._generate_edge_cases(param_name, base_type))
        
        # Error cases
        if self.config.generate_error_cases and self.config.coverage_type in [TestCoverage.COMPREHENSIVE, TestCoverage.FULL]:
            test_cases.extend(self._generate_error_cases(param_name, base_type))
        
        # Boundary tests
        if self.config.generate_boundary_tests and self.config.coverage_type == TestCoverage.FULL:
            test_cases.extend(self._generate_boundary_cases(param_name, base_type))
        
        return test_cases
    
    def _generate_happy_path_cases(self, param_name: str, base_type: str) -> List[TestCase]:
        """Generate happy path test cases."""
        cases = []
        
        if base_type == 'int':
            cases = [
                TestCase(f"{param_name}_positive", {param_name: 42}, description="Positive integer"),
                TestCase(f"{param_name}_zero", {param_name: 0}, description="Zero"),
                TestCase(f"{param_name}_negative", {param_name: -42}, description="Negative integer"),
            ]
        elif base_type == 'str':
            cases = [
                TestCase(f"{param_name}_normal", {param_name: "hello"}, description="Normal string"),
                TestCase(f"{param_name}_empty", {param_name: ""}, description="Empty string"),
                TestCase(f"{param_name}_single_char", {param_name: "a"}, description="Single character"),
            ]
        elif base_type == 'bool':
            cases = [
                TestCase(f"{param_name}_true", {param_name: True}, description="True"),
                TestCase(f"{param_name}_false", {param_name: False}, description="False"),
            ]
        elif base_type == 'list':
            cases = [
                TestCase(f"{param_name}_normal", {param_name: [1, 2, 3]}, description="Normal list"),
                TestCase(f"{param_name}_empty", {param_name: []}, description="Empty list"),
                TestCase(f"{param_name}_single_item", {param_name: [1]}, description="Single item list"),
            ]
        elif base_type == 'dict':
            cases = [
                TestCase(f"{param_name}_normal", {param_name: {"key": "value"}}, description="Normal dict"),
                TestCase(f"{param_name}_empty", {param_name: {}}, description="Empty dict"),
                TestCase(f"{param_name}_multiple_keys", {param_name: {"a": 1, "b": 2}}, description="Multiple keys"),
            ]
        
        return cases
    
    def _generate_edge_cases(self, param_name: str, base_type: str) -> List[TestCase]:
        """Generate edge case test cases."""
        cases = []
        
        if base_type in self._edge_cases:
            edge_values = self._edge_cases[base_type]
            for i, value in enumerate(edge_values):
                cases.append(TestCase(
                    f"{param_name}_edge_{i}",
                    {param_name: value},
                    description=f"Edge case: {value}"
                ))
        
        return cases
    
    def _generate_error_cases(self, param_name: str, base_type: str) -> List[TestCase]:
        """Generate error case test cases."""
        cases = []
        
        if base_type in self._error_cases:
            error_values = self._error_cases[base_type]
            for i, value in enumerate(error_values):
                cases.append(TestCase(
                    f"{param_name}_error_{i}",
                    {param_name: value},
                    expected_exception="TypeError",
                    description=f"Error case: {type(value).__name__} -> {base_type}"
                ))
        
        return cases
    
    def _generate_boundary_cases(self, param_name: str, base_type: str) -> List[TestCase]:
        """Generate boundary test cases."""
        cases = []
        
        if base_type == 'int':
            cases = [
                TestCase(f"{param_name}_max_int", {param_name: 2**31-1}, description="Max 32-bit int"),
                TestCase(f"{param_name}_min_int", {param_name: -2**31}, description="Min 32-bit int"),
            ]
        elif base_type == 'float':
            cases = [
                TestCase(f"{param_name}_epsilon", {param_name: 1e-10}, description="Very small float"),
                TestCase(f"{param_name}_large", {param_name: 1e10}, description="Very large float"),
            ]
        elif base_type == 'str':
            cases = [
                TestCase(f"{param_name}_unicode", {param_name: "café"}, description="Unicode string"),
                TestCase(f"{param_name}_special_chars", {param_name: "!@#$%^&*()"}, description="Special characters"),
            ]
        
        return cases
    
    def _extract_base_type(self, type_str: str) -> str:
        """Extract base type from type annotation string."""
        if not type_str:
            return 'str'  # Default
        
        type_str = type_str.lower().strip()
        
        if 'int' in type_str:
            return 'int'
        elif 'float' in type_str:
            return 'float'
        elif 'str' in type_str:
            return 'str'
        elif 'bool' in type_str:
            return 'bool'
        elif 'list' in type_str or '[]' in type_str:
            return 'list'
        elif 'dict' in type_str or '{}' in type_str:
            return 'dict'
        else:
            return 'str'  # Default fallback
