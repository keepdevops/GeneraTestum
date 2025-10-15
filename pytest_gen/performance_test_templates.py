"""
Performance test templates and code generation.
"""

from typing import Optional
from .performance_test_models import PerformanceTest, PerformanceRequirement


class PerformanceTestTemplates:
    """Templates for generating different types of performance tests."""
    
    @staticmethod
    def generate_execution_time_test(requirement: PerformanceRequirement) -> PerformanceTest:
        """Generate execution time test."""
        test_code = f'''def test_{requirement.function_name}_execution_time():
    """Test execution time for {requirement.function_name}"""
    import time
    
    # Test data
    test_input = generate_test_data()
    
    # Measure execution time
    start_time = time.time()
    result = {requirement.function_name}(test_input)
    execution_time = time.time() - start_time
    
    # Assertions
    assert execution_time <= {requirement.max_execution_time}, \\
        f"Execution time {{execution_time:.4f}}s exceeds limit of {requirement.max_execution_time}s"
    
    assert result is not None, "Function should return a result"
    
    # Log performance
    print(f"Execution time: {{execution_time:.4f}}s")'''
        
        benchmarks = [
            f"Execution time <= {requirement.max_execution_time}s"
        ]
        
        assertions = [
            f"execution_time <= {requirement.max_execution_time}",
            "result is not None"
        ]
        
        return PerformanceTest(
            function_name=requirement.function_name,
            test_code=test_code,
            benchmarks=benchmarks,
            assertions=assertions
        )
    
    @staticmethod
    def generate_memory_test(requirement: PerformanceRequirement) -> PerformanceTest:
        """Generate memory usage test."""
        test_code = f'''def test_{requirement.function_name}_memory_usage():
    """Test memory usage for {requirement.function_name}"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Test data
    test_input = generate_test_data()
    
    # Execute function
    result = {requirement.function_name}(test_input)
    
    # Check memory usage
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = final_memory - initial_memory
    
    # Assertions
    assert memory_used <= {requirement.memory_limit}, \\
        f"Memory usage {{memory_used:.2f}}MB exceeds limit of {requirement.memory_limit}MB"
    
    print(f"Memory used: {{memory_used:.2f}}MB")'''
        
        benchmarks = [
            f"Memory usage <= {requirement.memory_limit}MB"
        ]
        
        assertions = [
            f"memory_used <= {requirement.memory_limit}"
        ]
        
        return PerformanceTest(
            function_name=requirement.function_name,
            test_code=test_code,
            benchmarks=benchmarks,
            assertions=assertions
        )
    
    @staticmethod
    def generate_complexity_test(requirement: PerformanceRequirement) -> Optional[PerformanceTest]:
        """Generate complexity test."""
        if not requirement.complexity_threshold:
            return None
        
        test_code = f'''def test_{requirement.function_name}_complexity():
    """Test algorithmic complexity for {requirement.function_name}"""
    import time
    
    # Test with different input sizes
    sizes = [10, 100, 1000]
    execution_times = []
    
    for size in sizes:
        test_input = generate_test_data(size)
        
        start_time = time.time()
        result = {requirement.function_name}(test_input)
        execution_time = time.time() - start_time
        
        execution_times.append(execution_time)
    
    # Verify complexity pattern
    # For O(n), time should roughly scale linearly
    if "{requirement.complexity_threshold}" == "O(n)":
        ratio = execution_times[-1] / execution_times[0]
        assert ratio <= 1000, f"Complexity doesn't match O(n): ratio {{ratio}}"
    elif "{requirement.complexity_threshold}" == "O(1)":
        # Execution time should be roughly constant
        max_time = max(execution_times)
        min_time = min(execution_times)
        assert max_time / min_time <= 10, f"Complexity doesn't match O(1)"
    
    print(f"Complexity test passed for {requirement.complexity_threshold}")'''
        
        benchmarks = [
            f"Complexity matches {requirement.complexity_threshold}"
        ]
        
        assertions = [
            f"Complexity verification for {requirement.complexity_threshold}"
        ]
        
        return PerformanceTest(
            function_name=requirement.function_name,
            test_code=test_code,
            benchmarks=benchmarks,
            assertions=assertions
        )
    
    @staticmethod
    def generate_benchmark_test(requirement: PerformanceRequirement) -> PerformanceTest:
        """Generate benchmark test."""
        test_code = f'''def test_{requirement.function_name}_benchmark():
    """Benchmark test for {requirement.function_name}"""
    import time
    import statistics
    
    # Run multiple iterations
    iterations = 100
    execution_times = []
    
    for _ in range(iterations):
        test_input = generate_test_data()
        
        start_time = time.time()
        result = {requirement.function_name}(test_input)
        execution_time = time.time() - start_time
        
        execution_times.append(execution_time)
    
    # Calculate statistics
    avg_time = statistics.mean(execution_times)
    median_time = statistics.median(execution_times)
    max_time = max(execution_times)
    min_time = min(execution_times)
    
    # Assertions
    assert avg_time <= {requirement.max_execution_time}, \\
        f"Average execution time {{avg_time:.4f}}s exceeds limit"
    
    assert max_time <= {requirement.max_execution_time * 2}, \\
        f"Maximum execution time {{max_time:.4f}}s exceeds tolerance"
    
    print(f"Benchmark results:")
    print(f"  Average: {{avg_time:.4f}}s")
    print(f"  Median: {{median_time:.4f}}s")
    print(f"  Min: {{min_time:.4f}}s")
    print(f"  Max: {{max_time:.4f}}s")'''
        
        benchmarks = [
            f"Average time <= {requirement.max_execution_time}s",
            f"Max time <= {requirement.max_execution_time * 2}s"
        ]
        
        assertions = [
            "avg_time <= max_execution_time",
            "max_time <= max_execution_time * 2"
        ]
        
        return PerformanceTest(
            function_name=requirement.function_name,
            test_code=test_code,
            benchmarks=benchmarks,
            assertions=assertions
        )
