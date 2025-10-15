"""
Performance test file generation and reporting utilities.
"""

from typing import Dict, List, Any
from .performance_test_models import PerformanceTest, PerformanceTestSuite


class PerformanceTestFileGenerator:
    """Generates complete performance test files."""
    
    @staticmethod
    def generate_test_file_content(tests: List[PerformanceTest]) -> str:
        """Generate complete test file content."""
        if not tests:
            return "# No performance tests generated"
        
        # File header
        content = '''"""Performance tests for critical functions."""
import pytest
import time
import psutil
import os
import statistics
from unittest.mock import patch, MagicMock

def generate_test_data(size=100):
    """Generate test data for performance testing."""
    return [i for i in range(size)]

'''
        
        # Add test functions
        for test in tests:
            content += test.test_code + "\n\n"
        
        return content
    
    @staticmethod
    def generate_test_file_header() -> str:
        """Generate test file header with imports and utilities."""
        return '''"""Performance tests for critical functions."""
import pytest
import time
import psutil
import os
import statistics
from unittest.mock import patch, MagicMock

def generate_test_data(size=100):
    """Generate test data for performance testing."""
    return [i for i in range(size)]

def measure_execution_time(func, *args, **kwargs):
    """Helper function to measure execution time."""
    start_time = time.time()
    result = func(*args, **kwargs)
    execution_time = time.time() - start_time
    return result, execution_time

def measure_memory_usage(func, *args, **kwargs):
    """Helper function to measure memory usage."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    result = func(*args, **kwargs)
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = final_memory - initial_memory
    
    return result, memory_used

'''
    
    @staticmethod
    def add_test_function(content: str, test: PerformanceTest) -> str:
        """Add a test function to the file content."""
        return content + test.test_code + "\n\n"
    
    @staticmethod
    def generate_pytest_config() -> str:
        """Generate pytest configuration for performance tests."""
        return '''[tool:pytest]
testpaths = .
python_files = test_performance_*.py
python_classes = TestPerformance*
python_functions = test_*_performance*
addopts = -v --tb=short --strict-markers
markers =
    performance: marks tests as performance tests
    slow: marks tests as slow running
    memory: marks tests as memory intensive
    benchmark: marks tests as benchmark tests
'''
    
    @staticmethod
    def generate_performance_fixtures() -> str:
        """Generate pytest fixtures for performance testing."""
        return '''
@pytest.fixture
def performance_data():
    """Fixture providing test data for performance tests."""
    return {
        'small': [i for i in range(10)],
        'medium': [i for i in range(100)],
        'large': [i for i in range(1000)],
        'xlarge': [i for i in range(10000)]
    }

@pytest.fixture
def performance_timer():
    """Fixture providing a performance timer."""
    class PerformanceTimer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
            return self.end_time - self.start_time
        
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return PerformanceTimer()

'''
