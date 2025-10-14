"""
Automatic performance test generation for functions with timing requirements.
"""

import ast
import time
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass


@dataclass
class PerformanceRequirement:
    """Performance requirement for a function."""
    function_name: str
    max_execution_time: float  # in seconds
    min_execution_time: Optional[float] = None
    memory_limit: Optional[int] = None  # in MB
    complexity_threshold: Optional[str] = None  # O(1), O(n), O(n²), etc.


@dataclass
class PerformanceTest:
    """Generated performance test."""
    function_name: str
    test_code: str
    benchmarks: List[str]
    assertions: List[str]


class PerformanceAnalyzer:
    """Analyzes code to identify performance-critical functions."""

    def __init__(self):
        self.performance_indicators = {
            'loops': ['for', 'while', 'range', 'enumerate'],
            'recursion': ['def ', 'return'],
            'data_structures': ['list', 'dict', 'set', 'tuple'],
            'algorithms': ['sort', 'search', 'find', 'filter', 'map'],
            'io_operations': ['open', 'read', 'write', 'request', 'query'],
            'computation': ['math', 'calculate', 'compute', 'process']
        }

    def analyze_function_performance(self, func_ast: ast.FunctionDef) -> Optional[PerformanceRequirement]:
        """Analyze a function to determine if it needs performance testing."""
        function_name = func_ast.name
        
        # Check for performance-critical patterns
        performance_score = 0
        complexity_indicators = []
        
        # Analyze function body
        try:
            for node in ast.walk(func_ast):
                if isinstance(node, ast.For):
                    performance_score += 2
                    complexity_indicators.append("O(n)")
                elif isinstance(node, ast.While):
                    performance_score += 3
                    complexity_indicators.append("O(n)")
                elif isinstance(node, ast.ListComp):
                    performance_score += 1
                    complexity_indicators.append("O(n)")
                elif isinstance(node, ast.DictComp):
                    performance_score += 1
                    complexity_indicators.append("O(n)")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['sorted', 'sort', 'max', 'min']:
                            performance_score += 2
                            complexity_indicators.append("O(n log n)")
        except Exception:
            pass
        
        # Check docstring for performance hints
        try:
            docstring = ast.get_docstring(func_ast)
            if docstring:
                docstring_lower = docstring.lower()
                if any(word in docstring_lower for word in ['performance', 'optimize', 'fast', 'slow', 'efficient']):
                    performance_score += 2
        except Exception:
            pass
        
        # Check function name for performance hints
        name_lower = function_name.lower()
        if any(word in name_lower for word in ['sort', 'search', 'find', 'calculate', 'process', 'compute']):
            performance_score += 1
        
        # Determine if function needs performance testing
        if performance_score >= 3:
            # Estimate performance requirements
            if any("O(n²)" in indicator or "O(n³)" in indicator for indicator in complexity_indicators):
                max_time = 1.0  # 1 second for complex operations
            elif any("O(n log n)" in indicator for indicator in complexity_indicators):
                max_time = 0.5  # 0.5 seconds for moderate complexity
            else:
                max_time = 0.1  # 0.1 seconds for simple operations
            
            return PerformanceRequirement(
                function_name=function_name,
                max_execution_time=max_time,
                complexity_threshold=complexity_indicators[0] if complexity_indicators else None
            )
        
        return None

    def analyze_file_performance(self, file_path: str) -> List[PerformanceRequirement]:
        """Analyze a file to identify functions that need performance testing."""
        requirements = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    try:
                        requirement = self.analyze_function_performance(node)
                        if requirement:
                            requirements.append(requirement)
                    except Exception:
                        pass
        
        except Exception:
            pass
        
        return requirements


class PerformanceTestGenerator:
    """Generates performance tests for functions."""

    def __init__(self):
        self.benchmark_templates = {
            'execution_time': self._generate_execution_time_test,
            'memory_usage': self._generate_memory_usage_test,
            'complexity_verification': self._generate_complexity_test
        }

    def generate_performance_tests(self, requirements: List[PerformanceRequirement], 
                                 source_file: str) -> List[PerformanceTest]:
        """Generate performance tests for the given requirements."""
        tests = []
        
        for requirement in requirements:
            test = PerformanceTest(
                function_name=requirement.function_name,
                test_code="",
                benchmarks=[],
                assertions=[]
            )
            
            # Generate execution time test
            test.test_code += self._generate_execution_time_test(requirement, source_file)
            
            # Generate memory usage test if specified
            if requirement.memory_limit:
                test.test_code += self._generate_memory_usage_test(requirement, source_file)
            
            # Generate complexity verification test
            if requirement.complexity_threshold:
                test.test_code += self._generate_complexity_test(requirement, source_file)
            
            tests.append(test)
        
        return tests

    def _generate_execution_time_test(self, requirement: PerformanceRequirement, source_file: str) -> str:
        """Generate execution time performance test."""
        test_code = f"""
def test_{requirement.function_name}_execution_time():
    \"\"\"Test that {requirement.function_name} executes within performance requirements.\"\"\"
    import time
    import pytest
    
    # Import the function
    from {source_file.replace('.py', '').replace('/', '.')} import {requirement.function_name}
    
    # Test with typical input
    start_time = time.time()
    
    # TODO: Replace with actual function call
    # result = {requirement.function_name}(test_input)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Assert execution time is within limits
    assert execution_time < {requirement.max_execution_time}, \\
        f"Function {requirement.function_name} took {{execution_time:.3f}}s, expected < {requirement.max_execution_time}s"
    
    # Optional: Assert minimum execution time
    {f'assert execution_time > {requirement.min_execution_time}, f"Function {requirement.function_name} completed too quickly: {{execution_time:.3f}}s"' if requirement.min_execution_time else '# No minimum time requirement'}

"""
        return test_code

    def _generate_memory_usage_test(self, requirement: PerformanceRequirement, source_file: str) -> str:
        """Generate memory usage performance test."""
        test_code = f"""
def test_{requirement.function_name}_memory_usage():
    \"\"\"Test that {requirement.function_name} uses memory efficiently.\"\"\"
    import psutil
    import os
    import pytest
    
    # Import the function
    from {source_file.replace('.py', '').replace('/', '.')} import {requirement.function_name}
    
    # Get initial memory usage
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # TODO: Replace with actual function call
    # result = {requirement.function_name}(test_input)
    
    # Get final memory usage
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = final_memory - initial_memory
    
    # Assert memory usage is within limits
    assert memory_used < {requirement.memory_limit}, \\
        f"Function {requirement.function_name} used {{memory_used:.2f}}MB, expected < {requirement.memory_limit}MB"

"""
        return test_code

    def _generate_complexity_test(self, requirement: PerformanceRequirement, source_file: str) -> str:
        """Generate complexity verification test."""
        test_code = f"""
def test_{requirement.function_name}_complexity():
    \"\"\"Test that {requirement.function_name} has expected algorithmic complexity.\"\"\"
    import time
    import pytest
    import numpy as np
    
    # Import the function
    from {source_file.replace('.py', '').replace('/', '.')} import {requirement.function_name}
    
    # Test with increasing input sizes
    input_sizes = [10, 100, 1000]  # Adjust based on function
    execution_times = []
    
    for size in input_sizes:
        # TODO: Generate test input of appropriate size
        # test_input = generate_test_input(size)
        
        start_time = time.time()
        # result = {requirement.function_name}(test_input)
        end_time = time.time()
        
        execution_times.append(end_time - start_time)
    
    # Analyze complexity (simplified)
    if len(execution_times) >= 2:
        # Check if execution time scales as expected
        time_ratio = execution_times[-1] / execution_times[0]
        size_ratio = input_sizes[-1] / input_sizes[0]
        
        # TODO: Add complexity-specific assertions
        # For O(n): time_ratio should be roughly proportional to size_ratio
        # For O(n²): time_ratio should be roughly proportional to size_ratio²
        
        assert time_ratio > 0, f"Execution time should increase with input size"

"""
        return test_code


class AutoPerformanceTesting:
    """Main class for automatic performance test generation."""

    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.generator = PerformanceTestGenerator()

    def analyze_and_generate_tests(self, source_file: str) -> List[PerformanceTest]:
        """Analyze source file and generate performance tests."""
        # Analyze file for performance requirements
        requirements = self.analyzer.analyze_file_performance(source_file)
        
        if not requirements:
            return []
        
        # Generate performance tests
        tests = self.generator.generate_performance_tests(requirements, source_file)
        
        return tests

    def generate_performance_report(self, tests: List[PerformanceTest]) -> str:
        """Generate a report of performance tests."""
        if not tests:
            return "✅ No performance tests needed - no performance-critical functions found."
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("⚡ AUTOMATIC PERFORMANCE TEST GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n🎯 PERFORMANCE TESTS GENERATED: {len(tests)}")
        
        for test in tests:
            report_lines.append(f"\n📊 {test.function_name}:")
            report_lines.append(f"  • Execution time testing")
            if "memory" in test.test_code:
                report_lines.append(f"  • Memory usage testing")
            if "complexity" in test.test_code:
                report_lines.append(f"  • Complexity verification")
        
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        report_lines.append(f"  • Run performance tests regularly in CI/CD")
        report_lines.append(f"  • Monitor performance regression over time")
        report_lines.append(f"  • Adjust thresholds based on actual usage patterns")
        
        return "\n".join(report_lines)
