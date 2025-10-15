"""
Test guide documentation templates.
"""


def get_basic_test_examples() -> str:
    """Get basic test examples."""
    return """
def test_calculator_add():
    calculator = Calculator()
    result = calculator.add(2, 3)
    assert result == 5

def test_calculator_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(ValueError):
        calculator.divide(10, 0)
"""


def get_integration_test_examples() -> str:
    """Get integration test examples."""
    return """
def test_api_workflow():
    # Create user
    response = requests.post("/api/users", json={"name": "John"})
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Get user
    response = requests.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    
    # Update user
    response = requests.put(f"/api/users/{user_id}", json={"name": "Jane"})
    assert response.status_code == 200
    
    # Delete user
    response = requests.delete(f"/api/users/{user_id}")
    assert response.status_code == 204
"""


def get_e2e_test_examples() -> str:
    """Get end-to-end test examples."""
    return """
def test_user_registration_flow():
    # Navigate to registration page
    driver.get("/register")
    
    # Fill registration form
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "confirm_password").send_keys("password123")
    
    # Submit form
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Verify success
    assert "Registration successful" in driver.page_source
    assert driver.current_url == "/dashboard"
"""


def get_pytest_config() -> str:
    """Get pytest configuration."""
    return """
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
    unit: marks tests as unit tests
"""


def get_conftest_example() -> str:
    """Get conftest.py example."""
    return """
import pytest
import tempfile
import os

@pytest.fixture(scope="session")
def test_data_dir():
    \"\"\"Provide test data directory.\"\"\"
    return os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture
def temp_file():
    \"\"\"Provide temporary file.\"\"\"
    with tempfile.NamedTemporaryFile(delete=False) as f:
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_database():
    \"\"\"Provide mock database.\"\"\"
    from unittest.mock import MagicMock
    db = MagicMock()
    db.query.return_value = []
    return db
"""


def get_fixture_examples() -> str:
    """Get fixture examples."""
    return """
@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "active": True
    }

def test_user_creation(sample_user):
    user = User(**sample_user)
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
"""


def get_mock_examples() -> str:
    """Get mock examples."""
    return """
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_external_api_call(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response
    
    result = call_external_api()
    assert result == {"data": "test"}
    mock_get.assert_called_once_with("https://api.example.com/data")
"""


def get_security_test_examples() -> str:
    """Get security test examples."""
    return """
def test_sql_injection_protection():
    malicious_input = "'; DROP TABLE users; --"
    with pytest.raises(ValidationError):
        validate_user_input(malicious_input)

def test_xss_protection():
    malicious_script = "<script>alert('xss')</script>"
    result = sanitize_input(malicious_script)
    assert "<script>" not in result
    assert "alert" not in result
"""


def get_performance_test_examples() -> str:
    """Get performance test examples."""
    return """
import time

def test_api_response_time():
    start_time = time.time()
    response = client.get("/api/data")
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response.status_code == 200
    assert response_time < 1.0  # Should respond within 1 second
"""
