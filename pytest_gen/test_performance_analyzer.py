"""
Test performance analyzer.
"""

import ast
import os
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from .test_optimizer_models import TestPerformanceMetrics, OptimizationSuggestion, PerformanceThresholds


class TestPerformanceAnalyzer:
    """Analyzes test performance and identifies optimization opportunities."""

    def __init__(self):
        self.complexity_keywords = {
            'loops': ['for', 'while', 'for_each', 'iterate'],
            'conditionals': ['if', 'elif', 'else', 'switch', 'case'],
            'exceptions': ['try', 'except', 'catch', 'finally', 'raise'],
            'async': ['async', 'await', 'asyncio'],
            'nested': ['def ', 'class ', 'lambda'],
            'complex_assertions': ['assert_that', 'expect', 'should', 'must']
        }
        
        self.performance_patterns = {
            'slow_operations': [
                r'sleep\s*\(',
                r'time\.sleep\s*\(',
                r'requests\.get\s*\(',
                r'requests\.post\s*\(',
                r'database\.query\s*\(',
                r'db\.execute\s*\(',
                r'file\.read\s*\(',
                r'open\s*\(',
                r'subprocess\.call\s*\(',
                r'os\.system\s*\('
            ],
            'memory_intensive': [
                r'\.copy\s*\(',
                r'\.clone\s*\(',
                r'deepcopy\s*\(',
                r'pickle\.loads\s*\(',
                r'json\.loads\s*\(',
                r'pandas\.read_csv\s*\(',
                r'numpy\.array\s*\(',
                r'list\s*\(',
                r'dict\s*\(',
                r'set\s*\('
            ],
            'io_operations': [
                r'open\s*\(',
                r'file\s*\(',
                r'\.read\s*\(',
                r'\.write\s*\(',
                r'\.save\s*\(',
                r'\.load\s*\(',
                r'requests\.',
                r'urllib\.',
                r'socket\.',
                r'ftp\.'
            ]
        }

    def analyze_test_file(self, file_path: str) -> List[TestPerformanceMetrics]:
        """Analyze a test file for performance metrics."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception:
            return []
        
        # Parse the code
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []
        
        metrics = []
        
        # Find test functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                metric = self._analyze_test_function(node, source_code, file_path)
                if metric:
                    metrics.append(metric)
        
        return metrics

    def _analyze_test_function(self, node: ast.FunctionDef, source_code: str, file_path: str) -> Optional[TestPerformanceMetrics]:
        """Analyze a single test function."""
        # Extract function body
        lines = source_code.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno - 1 if hasattr(node, 'end_lineno') else start_line + 10
        
        function_code = '\n'.join(lines[start_line:end_line + 1])
        
        # Calculate metrics
        complexity_score = self._calculate_complexity(node)
        dependency_count = self._count_dependencies(node)
        mock_count = self._count_mocks(function_code)
        assertion_count = self._count_assertions(node)
        
        # Estimate execution time (rough approximation)
        execution_time = self._estimate_execution_time(function_code, complexity_score, dependency_count)
        
        # Estimate memory usage
        memory_usage = self._estimate_memory_usage(function_code)
        
        return TestPerformanceMetrics(
            test_name=node.name,
            execution_time=execution_time,
            memory_usage=memory_usage,
            complexity_score=complexity_score,
            dependency_count=dependency_count,
            mock_count=mock_count,
            assertion_count=assertion_count
        )

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
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

    def _count_dependencies(self, node: ast.FunctionDef) -> int:
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

    def _count_mocks(self, function_code: str) -> int:
        """Count mock objects in function code."""
        import re
        
        mock_patterns = [
            r'@mock\.',
            r'@patch\s*\(',
            r'MagicMock\s*\(',
            r'Mock\s*\(',
            r'\.mock_',
            r'patch\s*\(',
            r'unittest\.mock\.',
            r'mockito\.',
            r'sinon\.'
        ]
        
        mock_count = 0
        for pattern in mock_patterns:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            mock_count += len(matches)
        
        return mock_count

    def _count_assertions(self, node: ast.FunctionDef) -> int:
        """Count assertions in a function."""
        assertion_count = 0
        
        for child in ast.walk(node):
            if isinstance(child, ast.Assert):
                assertion_count += 1
            elif isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr.startswith(('assert', 'expect', 'should')):
                        assertion_count += 1
                elif isinstance(child.func, ast.Name):
                    if child.func.id.startswith(('assert', 'expect', 'should')):
                        assertion_count += 1
        
        return assertion_count

    def _estimate_execution_time(self, function_code: str, complexity: int, dependencies: int) -> float:
        """Estimate execution time based on code analysis."""
        import re
        
        base_time = 0.1  # Base execution time
        
        # Add time for complexity
        complexity_time = complexity * 0.05
        
        # Add time for dependencies
        dependency_time = dependencies * 0.02
        
        # Add time for slow operations
        slow_ops_time = 0
        for pattern in self.performance_patterns['slow_operations']:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            slow_ops_time += len(matches) * 0.5
        
        # Add time for IO operations
        io_time = 0
        for pattern in self.performance_patterns['io_operations']:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            io_time += len(matches) * 0.2
        
        total_time = base_time + complexity_time + dependency_time + slow_ops_time + io_time
        
        return round(total_time, 3)

    def _estimate_memory_usage(self, function_code: str) -> float:
        """Estimate memory usage based on code analysis."""
        import re
        
        base_memory = 1.0  # Base memory usage in MB
        
        # Add memory for data structures
        data_structure_patterns = [
            r'list\s*\(',
            r'dict\s*\(',
            r'set\s*\(',
            r'tuple\s*\(',
            r'array\s*\(',
            r'matrix\s*\('
        ]
        
        memory_usage = base_memory
        for pattern in data_structure_patterns:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            memory_usage += len(matches) * 0.5
        
        # Add memory for memory-intensive operations
        for pattern in self.performance_patterns['memory_intensive']:
            matches = re.findall(pattern, function_code, re.IGNORECASE)
            memory_usage += len(matches) * 2.0
        
        return round(memory_usage, 2)

    def analyze_test_directory(self, directory: str) -> List[TestPerformanceMetrics]:
        """Analyze all test files in a directory."""
        all_metrics = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    metrics = self.analyze_test_file(file_path)
                    all_metrics.extend(metrics)
        
        return all_metrics

    def identify_optimization_opportunities(self, metrics: List[TestPerformanceMetrics], 
                                          thresholds: PerformanceThresholds) -> List[OptimizationSuggestion]:
        """Identify optimization opportunities based on metrics."""
        suggestions = []
        
        for metric in metrics:
            # Check for slow tests
            if metric.execution_time > thresholds.slow_test_threshold:
                suggestions.append(OptimizationSuggestion(
                    test_name=metric.test_name,
                    suggestion_type='parallelize',
                    description=f'Test takes {metric.execution_time}s, consider parallelization',
                    potential_improvement=50.0,
                    implementation='Use pytest-xdist for parallel execution'
                ))
            
            # Check for high memory usage
            if metric.memory_usage > thresholds.memory_threshold:
                suggestions.append(OptimizationSuggestion(
                    test_name=metric.test_name,
                    suggestion_type='mock_optimization',
                    description=f'Test uses {metric.memory_usage}MB, optimize memory usage',
                    potential_improvement=30.0,
                    implementation='Use more efficient mocks and data structures'
                ))
            
            # Check for high complexity
            if metric.complexity_score > thresholds.complexity_threshold:
                suggestions.append(OptimizationSuggestion(
                    test_name=metric.test_name,
                    suggestion_type='fixture_optimization',
                    description=f'Test has complexity {metric.complexity_score}, simplify logic',
                    potential_improvement=25.0,
                    implementation='Break down complex tests into smaller, focused tests'
                ))
            
            # Check for too many dependencies
            if metric.dependency_count > thresholds.dependency_threshold:
                suggestions.append(OptimizationSuggestion(
                    test_name=metric.test_name,
                    suggestion_type='mock_optimization',
                    description=f'Test has {metric.dependency_count} dependencies, mock more',
                    potential_improvement=40.0,
                    implementation='Mock external dependencies to reduce coupling'
                ))
        
        return suggestions
