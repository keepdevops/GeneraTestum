"""
Test optimizer for generating optimized test code.
"""

from typing import Dict, List, Any, Optional
from .test_optimizer_models import TestPerformanceMetrics, OptimizationSuggestion, TestSuiteReport, OptimizationResult


class TestOptimizer:
    """Generates optimized test code based on performance analysis."""

    def __init__(self):
        self.optimization_templates = {
            'parallelize': self._generate_parallel_test_template,
            'mock_optimization': self._generate_mock_optimization_template,
            'fixture_optimization': self._generate_fixture_optimization_template,
            'assertion_optimization': self._generate_assertion_optimization_template
        }

    def generate_optimized_tests(self, metrics: List[TestPerformanceMetrics], 
                               suggestions: List[OptimizationSuggestion]) -> Dict[str, str]:
        """Generate optimized test code for suggestions."""
        optimized_tests = {}
        
        for suggestion in suggestions:
            template_func = self.optimization_templates.get(suggestion.suggestion_type)
            if template_func:
                optimized_code = template_func(suggestion, metrics)
                optimized_tests[suggestion.test_name] = optimized_code
        
        return optimized_tests

    def _generate_parallel_test_template(self, suggestion: OptimizationSuggestion, 
                                       metrics: List[TestPerformanceMetrics]) -> str:
        """Generate parallel test execution template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''def {suggestion.test_name}():
    \"\"\"Optimized parallel test for {suggestion.test_name}.\"\"\"
    import pytest
    import concurrent.futures
    import threading
    
    # Test data setup
    test_data = [
        {{"input": "test1", "expected": "result1"}},
        {{"input": "test2", "expected": "result2"}},
        {{"input": "test3", "expected": "result3"}}
    ]
    
    def run_single_test(data):
        \"\"\"Run a single test case.\"\"\"
        result = process_data(data["input"])
        assert result == data["expected"]
        return True
    
    # Parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_single_test, data) for data in test_data]
        results = [future.result() for future in futures]
    
    # Verify all tests passed
    assert all(results)

@pytest.mark.parametrize("test_data", [
    {{"input": "test1", "expected": "result1"}},
    {{"input": "test2", "expected": "result2"}},
    {{"input": "test3", "expected": "result3"}}
])
def {suggestion.test_name}_parametrized(test_data):
    \"\"\"Parametrized version for better parallelization.\"\"\"
    result = process_data(test_data["input"])
    assert result == test_data["expected"]
'''

    def _generate_mock_optimization_template(self, suggestion: OptimizationSuggestion, 
                                           metrics: List[TestPerformanceMetrics]) -> str:
        """Generate mock optimization template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''@pytest.fixture
def mock_dependencies():
    \"\"\"Optimized mock dependencies.\"\"\"
    from unittest.mock import Mock, patch
    
    # Create lightweight mocks
    mock_db = Mock()
    mock_db.query.return_value = []
    mock_db.execute.return_value = True
    
    mock_api = Mock()
    mock_api.get.return_value.status_code = 200
    mock_api.get.return_value.json.return_value = {{"data": "test"}}
    
    return {{
        "database": mock_db,
        "api": mock_api
    }}

def {suggestion.test_name}():
    \"\"\"Optimized test with efficient mocking.\"\"\"
    import pytest
    from unittest.mock import patch, Mock
    
    # Use context managers for targeted mocking
    with patch('module.external_service') as mock_service:
        mock_service.return_value = Mock(data="test_data")
        
        result = function_under_test()
        
        # Verify mock was called correctly
        mock_service.assert_called_once()
        assert result is not None

def test_data():
    \"\"\"Optimized test data fixture.\"\"\"
    return {{
        "users": [
            {{"id": 1, "name": "John"}},
            {{"id": 2, "name": "Jane"}}
        ],
        "products": [
            {{"id": 1, "name": "Product1"}},
            {{"id": 2, "name": "Product2"}}
        ]
    }}

def mock_services():
    \"\"\"Optimized mock services.\"\"\"
    return {{
        "user_service": Mock(),
        "product_service": Mock(),
        "payment_service": Mock()
    }}

def {suggestion.test_name}(test_data, mock_services):
    \"\"\"Test using optimized fixtures.\"\"\"
    # Setup mock return values
    mock_services["user_service"].get_user.return_value = test_data["users"][0]
    mock_services["product_service"].get_product.return_value = test_data["products"][0]
    
    # Run test
    result = business_logic(test_data["users"][0]["id"])
    
    # Verify results
    assert result is not None
    mock_services["user_service"].get_user.assert_called_once()
'''

    def _generate_fixture_optimization_template(self, suggestion: OptimizationSuggestion, 
                                              metrics: List[TestPerformanceMetrics]) -> str:
        """Generate fixture optimization template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''@pytest.fixture(scope="session")
def shared_data():
    \"\"\"Session-scoped fixture for expensive setup.\"\"\"
    # Expensive setup that can be shared across tests
    database = setup_test_database()
    yield database
    cleanup_test_database(database)

@pytest.fixture(scope="function")
def test_environment():
    \"\"\"Function-scoped fixture for test isolation.\"\"\"
    # Lightweight setup for each test
    config = {{"mode": "test", "debug": True}}
    yield config

@pytest.fixture
def mock_cache():
    \"\"\"Optimized cache mock.\"\"\"
    cache = {{}}
    
    def get(key):
        return cache.get(key)
    
    def set(key, value):
        cache[key] = value
    
    mock = Mock()
    mock.get = get
    mock.set = set
    return mock

@pytest.fixture
def mock_db():
    \"\"\"Optimized database mock.\"\"\"
    mock = Mock()
    mock.query.return_value = []
    mock.execute.return_value = True
    return mock

@pytest.fixture
def mock_requests():
    \"\"\"Optimized requests mock.\"\"\"
    mock = Mock()
    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {{"success": True}}
    return mock

def {suggestion.test_name}(mock_cache, mock_db, mock_requests):
    \"\"\"Optimized test using efficient fixtures.\"\"\"
    # Test implementation using optimized fixtures
    result = function_under_test()
    assert result is not None
    
    # Verify mock interactions
    mock_cache.get.assert_called()
    mock_db.query.assert_called()
    mock_requests.get.assert_called()
'''

    def _generate_assertion_optimization_template(self, suggestion: OptimizationSuggestion, 
                                                metrics: List[TestPerformanceMetrics]) -> str:
        """Generate assertion optimization template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''def {suggestion.test_name}():
    \"\"\"Optimized test with efficient assertions.\"\"\"
    import pytest
    
    # Use specific assertions instead of generic ones
    result = function_under_test()
    
    # Optimized assertions
    assert result is not None
    assert isinstance(result, dict)
    assert "expected_key" in result
    assert result["expected_key"] == "expected_value"
    
    # Use pytest.raises for exception testing
    with pytest.raises(ValueError, match="Expected error message"):
        function_that_should_fail("invalid_input")
    
    # Use pytest.approx for floating point comparisons
    float_result = calculate_float_value()
    assert float_result == pytest.approx(3.14159, abs=1e-5)
    
    # Use pytest.parametrize for multiple test cases
    @pytest.mark.parametrize("input_val,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
        ("input3", "output3")
    ])
    def test_multiple_cases(input_val, expected):
        result = process_input(input_val)
        assert result == expected
'''

    def generate_optimization_report(self, metrics: List[TestPerformanceMetrics], 
                                   suggestions: List[OptimizationSuggestion]) -> TestSuiteReport:
        """Generate comprehensive optimization report."""
        total_tests = len(metrics)
        total_execution_time = sum(m.execution_time for m in metrics)
        average_execution_time = total_execution_time / total_tests if total_tests > 0 else 0
        
        # Find slowest tests
        slowest_tests = sorted(metrics, key=lambda x: x.execution_time, reverse=True)[:5]
        
        # Calculate parallelization potential
        parallelizable_tests = sum(1 for m in metrics if m.execution_time > 0.5)
        parallelization_potential = (parallelizable_tests / total_tests * 100) if total_tests > 0 else 0
        
        return TestSuiteReport(
            total_tests=total_tests,
            total_execution_time=total_execution_time,
            average_execution_time=average_execution_time,
            slowest_tests=slowest_tests,
            optimization_suggestions=suggestions,
            parallelization_potential=parallelization_potential
        )
