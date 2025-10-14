"""
Parametrized test case generation for multiple input scenarios.
"""

from typing import Dict, List, Set, Optional, Any, Tuple, Union
from dataclasses import dataclass
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ClassInfo, ModuleInfo
from .test_case_generator import TestCase, TestCaseGenerator


@dataclass
class ParametrizeInfo:
    """Information about a parametrized test."""
    parameter_name: str
    test_cases: List[TestCase]
    ids: Optional[List[str]] = None


class ParametrizeGenerator:
    """Generates parametrized test cases for comprehensive coverage."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.test_case_generator = TestCaseGenerator(config)
    
    def generate_parametrize_for_function(self, func_info: FunctionInfo) -> List[ParametrizeInfo]:
        """Generate parametrized tests for a specific function."""
        if not self.config.generate_parametrize:
            return []
        
        parametrize_list = []
        
        # Generate parametrized tests for each parameter
        for param_name, param_type in func_info.parameters:
            if param_type:
                test_cases = self.test_case_generator.generate_test_cases_for_type(param_name, param_type, func_info)
                if test_cases:
                    parametrize_info = ParametrizeInfo(
                        parameter_name=param_name,
                        test_cases=test_cases,
                        ids=[f"test_{param_name}_{i}" for i in range(len(test_cases))]
                    )
                    parametrize_list.append(parametrize_info)
        
        # Generate combined parametrize tests for multiple parameters
        if len(func_info.parameters) > 1:
            combined_parametrize = self._generate_combined_parametrize(func_info)
            parametrize_list.extend(combined_parametrize)
        
        return parametrize_list
    
    def _generate_combined_parametrize(self, func_info: FunctionInfo) -> List[ParametrizeInfo]:
        """Generate combined parametrize tests for multiple parameters."""
        if len(func_info.parameters) < 2:
            return []
        
        parametrize_list = []
        
        # Generate a few combinations of parameters
        param_combinations = self._get_parameter_combinations(func_info.parameters)
        
        test_cases = []
        for i, combination in enumerate(param_combinations):
            test_cases.append(TestCase(
                f"combined_{i}",
                combination,
                description=f"Combined parameters: {combination}"
            ))
        
        if test_cases:
            parametrize_info = ParametrizeInfo(
                parameter_name="params",
                test_cases=test_cases,
                ids=[f"combined_{i}" for i in range(len(test_cases))]
            )
            parametrize_list.append(parametrize_info)
        
        return parametrize_list
    
    def _get_parameter_combinations(self, parameters: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """Get combinations of parameter values."""
        combinations = []
        
        # Simple combinations for demonstration
        if len(parameters) == 2:
            param1_name, param1_type = parameters[0]
            param2_name, param2_type = parameters[1]
            
            combinations = [
                {param1_name: self._get_sample_value(param1_type), param2_name: self._get_sample_value(param2_type)},
                {param1_name: self._get_sample_value(param1_type), param2_name: self._get_edge_value(param2_type)},
                {param1_name: self._get_edge_value(param1_type), param2_name: self._get_sample_value(param2_type)},
            ]
        else:
            # For more than 2 parameters, use a simpler approach
            combination = {}
            for param_name, param_type in parameters:
                combination[param_name] = self._get_sample_value(param_type)
            combinations = [combination]
        
        return combinations
    
    def _get_sample_value(self, param_type: str) -> Any:
        """Get a sample value for a parameter type."""
        base_type = self.test_case_generator._extract_base_type(param_type)
        
        if base_type == 'int':
            return 42
        elif base_type == 'str':
            return "test"
        elif base_type == 'bool':
            return True
        elif base_type == 'list':
            return [1, 2, 3]
        elif base_type == 'dict':
            return {"key": "value"}
        elif base_type == 'float':
            return 3.14
        else:
            return None
    
    def _get_edge_value(self, param_type: str) -> Any:
        """Get an edge value for a parameter type."""
        base_type = self.test_case_generator._extract_base_type(param_type)
        
        if base_type == 'int':
            return 0
        elif base_type == 'str':
            return ""
        elif base_type == 'bool':
            return False
        elif base_type == 'list':
            return []
        elif base_type == 'dict':
            return {}
        elif base_type == 'float':
            return 0.0
        else:
            return None
    
    def generate_parametrize_code(self, parametrize_info: ParametrizeInfo) -> List[str]:
        """Generate Python code for parametrized tests."""
        if not parametrize_info.test_cases:
            return []
        
        code_lines = []
        
        # Generate the parametrize decorator
        param_names = list(parametrize_info.test_cases[0].parameters.keys())
        param_values = []
        ids = []
        
        for test_case in parametrize_info.test_cases:
            values = tuple(test_case.parameters[name] for name in param_names)
            param_values.append(values)
            ids.append(test_case.name)
        
        # Format the decorator
        if len(param_names) == 1:
            decorator = f"@pytest.mark.parametrize('{param_names[0]}', {param_values})"
        else:
            decorator = f"@pytest.mark.parametrize('{','.join(param_names)}', {param_values})"
        
        code_lines.append(decorator)
        code_lines.append("def test_parametrized():")
        code_lines.append("    # Test implementation here")
        code_lines.append("    pass")
        code_lines.append("")
        
        return code_lines
    
    def get_parametrize_imports(self) -> Set[str]:
        """Get import statements needed for parametrized tests."""
        return {"import pytest"}