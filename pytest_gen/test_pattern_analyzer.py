"""
Test pattern analysis for enhanced test building.
"""

from typing import List, Dict, Any
from .code_analyzer import FunctionInfo, ClassInfo


class TestPatternAnalyzer:
    """Analyzes code to determine appropriate test patterns."""
    
    def __init__(self):
        self.function_patterns = {
            'utility': ['happy_path', 'edge_cases', 'error_handling'],
            'calculation': ['happy_path', 'edge_cases', 'parametrized'],
            'validation': ['happy_path', 'edge_cases', 'error_handling'],
            'data_processing': ['happy_path', 'parametrized', 'edge_cases'],
            'api_endpoint': ['happy_path', 'error_handling', 'authentication'],
            'database': ['happy_path', 'error_handling', 'mock_dependencies']
        }
        
        self.class_patterns = {
            'service': ['initialization', 'method_tests', 'error_handling'],
            'model': ['initialization', 'property_tests', 'validation'],
            'controller': ['initialization', 'method_tests', 'authentication'],
            'utility': ['initialization', 'method_tests', 'edge_cases']
        }

    def determine_function_type(self, func_info: FunctionInfo) -> str:
        """Determine the type of function for pattern selection."""
        name = func_info.name.lower()
        
        if any(keyword in name for keyword in ['calculate', 'compute', 'math', 'sum', 'add', 'multiply']):
            return 'calculation'
        elif any(keyword in name for keyword in ['validate', 'check', 'verify', 'is_valid']):
            return 'validation'
        elif any(keyword in name for keyword in ['process', 'parse', 'transform', 'convert']):
            return 'data_processing'
        elif any(keyword in name for keyword in ['api', 'endpoint', 'route', 'handler']):
            return 'api_endpoint'
        elif any(keyword in name for keyword in ['db', 'database', 'save', 'load', 'query']):
            return 'database'
        else:
            return 'utility'

    def determine_class_type(self, class_info: ClassInfo) -> str:
        """Determine the type of class for pattern selection."""
        name = class_info.name.lower()
        
        if any(keyword in name for keyword in ['service', 'manager', 'handler']):
            return 'service'
        elif any(keyword in name for keyword in ['model', 'entity', 'data']):
            return 'model'
        elif any(keyword in name for keyword in ['controller', 'api', 'view']):
            return 'controller'
        else:
            return 'utility'

    def get_function_patterns(self, func_info: FunctionInfo) -> List[str]:
        """Get appropriate test patterns for a function."""
        function_type = self.determine_function_type(func_info)
        return self.function_patterns.get(function_type, ['happy_path', 'edge_cases'])

    def get_class_patterns(self, class_info: ClassInfo) -> List[str]:
        """Get appropriate test patterns for a class."""
        class_type = self.determine_class_type(class_info)
        return self.class_patterns.get(class_type, ['initialization', 'method_tests'])

    def analyze_test_complexity(self, func_info: FunctionInfo) -> str:
        """Analyze the complexity of a function to determine test depth."""
        complexity_score = 0
        
        # Parameter count
        complexity_score += len(func_info.parameters)
        
        # Return type complexity
        if func_info.return_type and func_info.return_type != 'None':
            complexity_score += 1
        
        # Docstring presence
        if func_info.docstring:
            complexity_score += 1
        
        # Name length (indicates complexity)
        complexity_score += len(func_info.name) // 10
        
        if complexity_score <= 2:
            return 'simple'
        elif complexity_score <= 5:
            return 'medium'
        else:
            return 'complex'

    def get_enhanced_patterns(self, func_info: FunctionInfo) -> List[Dict[str, Any]]:
        """Get enhanced test patterns based on function analysis."""
        patterns = []
        base_patterns = self.get_function_patterns(func_info)
        complexity = self.analyze_test_complexity(func_info)
        
        for pattern in base_patterns:
            pattern_config = {
                'type': pattern,
                'complexity': complexity,
                'parameters': func_info.parameters,
                'return_type': func_info.return_type
            }
            patterns.append(pattern_config)
        
        return patterns
