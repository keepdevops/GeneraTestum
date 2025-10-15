"""
Test method generators for enhanced test building.
"""

from typing import List, Dict, Any
from .code_analyzer import FunctionInfo, ClassInfo


class TestMethodGenerator:
    """Generates specific test methods for functions and classes."""
    
    def __init__(self):
        self.templates = self._get_test_templates()

    def _get_test_templates(self) -> Dict[str, str]:
        return {
            'happy_path': """
        result = {function_call}
        assert result == expected_result""",
            'edge_cases': """
        # Test edge cases
        edge_inputs = [None, '', 0, [], {{}}]
        for edge_input in edge_inputs:
            try:
                result = {function_call_with_edge}
                # Handle expected behavior for edge cases
            except (ValueError, TypeError) as e:
                # Expected for invalid inputs
                pass""",
            'error_handling': """
        with pytest.raises({expected_exception}):
            {function_call_with_invalid}""",
            'parametrized': """
        # Parametrized test with multiple scenarios
        pass  # Will be expanded with @pytest.mark.parametrize"""
        }

    def generate_happy_path_test(self, func_info: FunctionInfo) -> List[str]:
        """Generate happy path test for a function."""
        lines = []
        method_name = f"test_{func_info.name}_happy_path"
        
        lines.append(f"    def {method_name}(self):")
        lines.append('        """Test happy path scenario."""')
        
        # Generate test parameters
        test_params = self._generate_test_parameters(func_info)
        
        # Generate function call
        if func_info.parameters:
            param_names = [param['name'] for param in func_info.parameters]
            param_values = [test_params.get(name, 'test_value') for name in param_names]
            function_call = f"{func_info.name}({', '.join(param_values)})"
        else:
            function_call = f"{func_info.name}()"
        
        # Add assertion
        if func_info.return_type and func_info.return_type != 'None':
            lines.append("        expected_result = 'expected_value'")
            lines.append(f"        result = {function_call}")
            lines.append("        assert result == expected_result")
        else:
            lines.append(f"        result = {function_call}")
            lines.append("        assert result is not None")
        
        return lines

    def generate_edge_case_test(self, func_info: FunctionInfo) -> List[str]:
        """Generate edge case test for a function."""
        lines = []
        method_name = f"test_{func_info.name}_edge_cases"
        
        lines.append(f"    def {method_name}(self):")
        lines.append('        """Test edge cases."""')
        
        if func_info.parameters:
            lines.append("        # Test with edge case inputs")
            lines.append("        edge_cases = [None, '', 0, [], {}]")
            lines.append("        for edge_input in edge_cases:")
            lines.append("            try:")
            param_names = [param['name'] for param in func_info.parameters]
            if len(param_names) == 1:
                lines.append(f"                result = {func_info.name}(edge_input)")
            else:
                lines.append(f"                result = {func_info.name}(edge_input, *{param_names[1:]})")
            lines.append("                # Handle expected behavior")
            lines.append("            except (ValueError, TypeError):")
            lines.append("                # Expected for invalid inputs")
            lines.append("                pass")
        else:
            lines.append("        # No parameters to test edge cases")
            lines.append("        pass")
        
        return lines

    def generate_error_case_test(self, func_info: FunctionInfo) -> List[str]:
        """Generate error handling test for a function."""
        lines = []
        method_name = f"test_{func_info.name}_error_handling"
        
        lines.append(f"    def {method_name}(self):")
        lines.append('        """Test error handling."""')
        
        if func_info.parameters:
            lines.append("        # Test with invalid input")
            lines.append("        with pytest.raises((ValueError, TypeError)):")
            param_names = [param['name'] for param in func_info.parameters]
            invalid_params = ['invalid_input' for _ in param_names]
            lines.append(f"            {func_info.name}({', '.join(invalid_params)})")
        else:
            lines.append("        # Function has no parameters to cause errors")
            lines.append("        pass")
        
        return lines

    def generate_parametrized_test(self, func_info: FunctionInfo) -> List[str]:
        """Generate parametrized test for a function."""
        lines = []
        method_name = f"test_{func_info.name}_parametrized"
        
        lines.append(f"    @pytest.mark.parametrize('input_val,expected', [")
        lines.append("        ('test1', 'expected1'),")
        lines.append("        ('test2', 'expected2'),")
        lines.append("        ('test3', 'expected3')")
        lines.append("    ])")
        lines.append(f"    def {method_name}(self, input_val, expected):")
        lines.append('        """Test with multiple input scenarios."""')
        
        if func_info.parameters:
            param_names = [param['name'] for param in func_info.parameters]
            if len(param_names) == 1:
                lines.append(f"        result = {func_info.name}(input_val)")
            else:
                lines.append(f"        result = {func_info.name}(input_val, *{param_names[1:]})")
            lines.append("        assert result == expected")
        else:
            lines.append(f"        result = {func_info.name}()")
            lines.append("        assert result == expected")
        
        return lines

    def generate_class_initialization_test(self, class_info: ClassInfo) -> List[str]:
        """Generate initialization test for a class."""
        lines = []
        method_name = f"test_{class_info.name.lower()}_initialization"
        
        lines.append(f"    def {method_name}(self):")
        lines.append('        """Test class initialization."""')
        
        lines.append(f"        instance = {class_info.name}()")
        lines.append("        assert instance is not None")
        
        # Test with parameters if constructor has them
        if class_info.methods:
            for method in class_info.methods:
                if method.name == '__init__' and method.parameters:
                    lines.append(f"        # Test initialization with parameters")
                    param_values = [f"test_{param['name']}" for param in method.parameters]
                    lines.append(f"        instance_with_params = {class_info.name}({', '.join(param_values)})")
                    lines.append("        assert instance_with_params is not None")
                    break
        
        return lines

    def generate_method_test(self, method_info: FunctionInfo, class_name: str) -> List[str]:
        """Generate test for a class method."""
        lines = []
        method_name = f"test_{method_info.name}"
        
        lines.append(f"    def {method_name}(self):")
        lines.append(f'        """Test {method_info.name} method."""')
        
        lines.append(f"        instance = {class_name}()")
        
        if method_info.parameters and method_info.parameters[0].get('name') == 'self':
            # Remove self parameter
            params = method_info.parameters[1:]
        else:
            params = method_info.parameters
        
        if params:
            param_values = [f"test_{param['name']}" for param in params]
            lines.append(f"        result = instance.{method_info.name}({', '.join(param_values)})")
        else:
            lines.append(f"        result = instance.{method_info.name}()")
        
        if method_info.return_type and method_info.return_type != 'None':
            lines.append("        assert result is not None")
        else:
            lines.append("        # Method returns None, just check it doesn't raise")
            lines.append("        pass")
        
        return lines

    def _generate_test_parameters(self, func_info: FunctionInfo) -> Dict[str, str]:
        """Generate test parameter values for a function."""
        test_params = {}
        
        for param in func_info.parameters:
            param_name = param['name']
            param_type = param.get('type', 'str')
            
            if param_type == 'int':
                test_params[param_name] = '42'
            elif param_type == 'float':
                test_params[param_name] = '3.14'
            elif param_type == 'bool':
                test_params[param_name] = 'True'
            elif param_type == 'list':
                test_params[param_name] = '[]'
            elif param_type == 'dict':
                test_params[param_name] = '{}'
            else:
                test_params[param_name] = f'"{param_name}_test"'
        
        return test_params
