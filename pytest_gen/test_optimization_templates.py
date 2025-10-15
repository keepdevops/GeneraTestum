"""
Test optimization templates for different optimization types.
"""

from typing import List
from .test_optimizer_models import OptimizationSuggestion, TestPerformanceMetrics


class TestOptimizationTemplates:
    """Templates for generating optimized test code."""
    
    @staticmethod
    def generate_parallel_test_template(suggestion: OptimizationSuggestion, 
                                       metrics: List[TestPerformanceMetrics]) -> str:
        """Generate parallel test execution template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''def {suggestion.test_name}():
    """Optimized parallel test for {suggestion.test_name}."""
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
        """Run a single test case."""
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
    """Parametrized version for better parallelization."""
    result = process_data(test_data["input"])
    assert result == test_data["expected"]
'''
    
    @staticmethod
    def generate_mock_optimization_template(suggestion: OptimizationSuggestion, 
                                           metrics: List[TestPerformanceMetrics]) -> str:
        """Generate mock optimization template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''@pytest.fixture
def mock_dependencies():
    """Optimized mock dependencies."""
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
    """Optimized test with efficient mocking."""
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
    """Optimized test data fixture."""
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
    """Optimized mock services."""
    return {{
        "user_service": Mock(),
        "product_service": Mock(),
        "payment_service": Mock()
    }}

def {suggestion.test_name}(test_data, mock_services):
    """Test using optimized fixtures."""
    # Setup mock return values
    mock_services["user_service"].get_user.return_value = test_data["users"][0]
    mock_services["product_service"].get_product.return_value = test_data["products"][0]
    
    # Run test
    result = business_logic(test_data["users"][0]["id"])
    
    # Verify results
    assert result is not None
    mock_services["user_service"].get_user.assert_called_once()
'''
    
    @staticmethod
    def generate_fixture_optimization_template(suggestion: OptimizationSuggestion, 
                                              metrics: List[TestPerformanceMetrics]) -> str:
        """Generate fixture optimization template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''@pytest.fixture(scope="session")
def shared_data():
    """Session-scoped fixture for expensive setup."""
    # Expensive setup that can be shared across tests
    database = setup_test_database()
    yield database
    cleanup_test_database(database)

@pytest.fixture(scope="function")
def test_environment():
    """Function-scoped fixture for test isolation."""
    # Lightweight setup for each test
    config = {{"mode": "test", "debug": True}}
    yield config

@pytest.fixture
def mock_cache():
    """Optimized cache mock."""
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
    """Optimized database mock."""
    mock = Mock()
    mock.query.return_value = []
    mock.execute.return_value = True
    return mock

@pytest.fixture
def mock_requests():
    """Optimized requests mock."""
    mock = Mock()
    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {{"success": True}}
    return mock

def {suggestion.test_name}(mock_cache, mock_db, mock_requests):
    """Optimized test using efficient fixtures."""
    # Test implementation using optimized fixtures
    result = function_under_test()
    assert result is not None
    
    # Verify mock interactions
    mock_cache.get.assert_called()
    mock_db.query.assert_called()
    mock_requests.get.assert_called()
'''
    
    @staticmethod
    def generate_assertion_optimization_template(suggestion: OptimizationSuggestion, 
                                                metrics: List[TestPerformanceMetrics]) -> str:
        """Generate assertion optimization template."""
        metric = next((m for m in metrics if m.test_name == suggestion.test_name), None)
        if not metric:
            return ""
        
        return f'''def {suggestion.test_name}():
    """Optimized test with efficient assertions."""
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
