"""
Test metrics calculation utilities.
"""

import ast
import re
from typing import Optional, Set
from .test_optimizer_models import TestPerformanceMetrics


class TestMetricsCalculator:
    """Calculates various test performance metrics."""
    
    def __init__(self, patterns):
        self.patterns = patterns
    
    def calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def count_dependencies(self, node: ast.FunctionDef) -> int:
        """Count external dependencies in a function."""
        dependencies = set()
        
        for child in ast.walk(node):
            if isinstance(child, ast.Import):
                for alias in child.names:
                    dependencies.add(alias.name)
            elif isinstance(child, ast.ImportFrom):
                if child.module:
                    dependencies.add(child.module)
        
        return len(dependencies)
    
    def count_mocks(self, function_code: str) -> int:
        """Count mock objects in function code."""
        mock_count = 0
        for pattern in self.patterns.get_mock_patterns():
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            mock_count += len(matches)
        
        return mock_count
    
    def count_assertions(self, node: ast.FunctionDef) -> int:
        """Count assertions in a function."""
        assertion_count = 0
        
        for child in ast.walk(node):
            if isinstance(child, ast.Assert):
                assertion_count += 1
            elif isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr.startswith(tuple(self.patterns.get_assertion_patterns())):
                        assertion_count += 1
                elif isinstance(child.func, ast.Name):
                    if child.func.id.startswith(tuple(self.patterns.get_assertion_patterns())):
                        assertion_count += 1
        
        return assertion_count
    
    def estimate_execution_time(self, function_code: str, complexity: int, dependencies: int) -> float:
        """Estimate execution time based on code analysis."""
        base_time = 0.1  # Base execution time
        
        # Add time for complexity
        complexity_time = complexity * 0.05
        
        # Add time for dependencies
        dependency_time = dependencies * 0.02
        
        # Add time for slow operations
        slow_ops_time = 0
        for pattern in self.patterns.get_performance_patterns()['slow_operations']:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            slow_ops_time += len(matches) * 0.5
        
        # Add time for IO operations
        io_time = 0
        for pattern in self.patterns.get_performance_patterns()['io_operations']:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            io_time += len(matches) * 0.2
        
        total_time = base_time + complexity_time + dependency_time + slow_ops_time + io_time
        
        return round(total_time, 3)
    
    def estimate_memory_usage(self, function_code: str) -> float:
        """Estimate memory usage based on code analysis."""
        base_memory = 1.0  # Base memory usage in MB
        
        memory_usage = base_memory
        
        # Add memory for data structures
        for pattern in self.patterns.get_data_structure_patterns():
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            memory_usage += len(matches) * 0.5
        
        # Add memory for memory-intensive operations
        for pattern in self.patterns.get_performance_patterns()['memory_intensive']:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            memory_usage += len(matches) * 2.0
        
        return round(memory_usage, 2)
    
    def analyze_test_function(self, node: ast.FunctionDef, source_code: str, file_path: str) -> Optional[TestPerformanceMetrics]:
        """Analyze a single test function and return metrics."""
        # Extract function body
        lines = source_code.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno - 1 if hasattr(node, 'end_lineno') else start_line + 10
        
        function_code = '\n'.join(lines[start_line:end_line + 1])
        
        # Calculate metrics
        complexity_score = self.calculate_complexity(node)
        dependency_count = self.count_dependencies(node)
        mock_count = self.count_mocks(function_code)
        assertion_count = self.count_assertions(node)
        
        # Estimate execution time
        execution_time = self.estimate_execution_time(function_code, complexity_score, dependency_count)
        
        # Estimate memory usage
        memory_usage = self.estimate_memory_usage(function_code)
        
        return TestPerformanceMetrics(
            test_name=node.name,
            execution_time=execution_time,
            memory_usage=memory_usage,
            complexity_score=complexity_score,
            dependency_count=dependency_count,
            mock_count=mock_count,
            assertion_count=assertion_count
        )
