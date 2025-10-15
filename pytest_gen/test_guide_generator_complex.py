"""
Test guide documentation generator.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation


class TestGuideGenerator:
    """Generates comprehensive test guide documentation."""

    def __init__(self):
        from .test_guide_helpers import TestGuideHelpers
        self.helpers = TestGuideHelpers()

    def generate_test_guide(self, test_info: Dict[str, Any]) -> TestDocumentation:
        """Generate comprehensive test guide."""
        content = f"""# Test Guide

## 📋 Overview

This guide provides comprehensive information about testing in the {test_info.get('project_name', 'Test Generator')} project.

## 🧪 Test Framework

**Framework**: {test_info.get('framework', 'pytest')}
**Version**: {test_info.get('framework_version', '7.0.0')}

## 📁 Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_models.py
│   ├── test_utils.py
│   └── test_validators.py
├── integration/            # Integration tests
│   ├── test_api.py
│   ├── test_database.py
│   └── test_workflows.py
├── e2e/                   # End-to-end tests
│   ├── test_user_journey.py
│   └── test_complete_flow.py
├── fixtures/              # Test fixtures
│   ├── conftest.py
│   └── fixtures.py
└── mocks/                 # Mock objects
    ├── mock_services.py
    └── mock_data.py
```

## 🚀 Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests in a specific directory
pytest tests/unit/

# Run tests matching a pattern
pytest -k "test_calculator"

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### Advanced Commands

```bash
# Run tests in parallel
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run tests and stop on first failure
pytest -x

# Run tests with custom markers
pytest -m "not slow"

# Run tests with specific Python version
pytest --python-version=3.9
```

## 🏗️ Test Types

### Unit Tests

Unit tests verify individual functions or methods in isolation.

```python
{self.helpers.get_basic_test_examples()}
```

### Integration Tests

Integration tests verify that multiple components work together.

```python
def test_api_workflow():
    # Create user
    response = requests.post("/api/users", json={{"name": "John"}})
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Get user
    response = requests.get(f"/api/users/{{user_id}}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    
    # Update user
    response = requests.put(f"/api/users/{{user_id}}", json={{"name": "Jane"}})
    assert response.status_code == 200
    
    # Delete user
    response = requests.delete(f"/api/users/{{user_id}}")
    assert response.status_code == 204
```

### End-to-End Tests

E2E tests verify complete user workflows.

```python
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
```

## 🔧 Test Configuration

### pytest.ini

```ini
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
```

### conftest.py

```python
import pytest
import tempfile
import os

@pytest.fixture(scope="session")
def test_data_dir():
    """Provide test data directory."""
    return os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture
def temp_file():
    """Provide temporary file."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_database():
    """Provide mock database."""
    from unittest.mock import MagicMock
    db = MagicMock()
    db.query.return_value = []
    return db
```

## 🎭 Mocking and Fixtures

### Using Fixtures

```python
@pytest.fixture
def sample_user():
    return {{
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "active": True
    }}

def test_user_creation(sample_user):
    user = User(**sample_user)
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
```

### Using Mocks

```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_external_api_call(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {{"data": "test"}}
    mock_get.return_value = mock_response
    
    result = call_external_api()
    assert result == {{"data": "test"}}
    mock_get.assert_called_once_with("https://api.example.com/data")
```

## 📊 Coverage Testing

### Coverage Goals

- **Minimum**: 80% overall coverage
- **Recommended**: 90% overall coverage
- **Critical Functions**: 100% coverage

### Coverage Commands

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# Coverage with missing lines
pytest --cov=src --cov-report=term-missing

# Coverage threshold
pytest --cov=src --cov-fail-under=80

# Coverage for specific modules
pytest --cov=src.models --cov=src.utils
```

### Coverage Configuration

```ini
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

## 🔒 Security Testing

### Input Validation Tests

```python
def test_sql_injection_protection():
    malicious_input = "'; DROP TABLE users; --"
    with pytest.raises(ValidationError):
        validate_user_input(malicious_input)

def test_xss_protection():
    malicious_script = "<script>alert('xss')</script>"
    result = sanitize_input(malicious_script)
    assert "<script>" not in result
    assert "alert" not in result
```

### Authentication Tests

```python
def test_authentication_required():
    response = client.get("/protected")
    assert response.status_code == 401

def test_valid_token():
    headers = {{"Authorization": "Bearer valid-token"}}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200

def test_invalid_token():
    headers = {{"Authorization": "Bearer invalid-token"}}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
```

## ⚡ Performance Testing

### Response Time Tests

```python
import time

def test_api_response_time():
    start_time = time.time()
    response = client.get("/api/data")
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response.status_code == 200
    assert response_time < 1.0  # Should respond within 1 second
```

### Load Testing

```python
def test_concurrent_requests():
    import concurrent.futures
    
    def make_request():
        return client.get("/api/data")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [future.result() for future in futures]
    
    for response in results:
        assert response.status_code == 200
```

## 🐛 Debugging Tests

### Debug Mode

```bash
# Run tests with debugging
pytest --pdb

# Drop into debugger on failure
pytest --pdb-trace

# Show local variables in tracebacks
pytest -l
```

### Debug Example

```python
def test_debug_example():
    result = complex_function()
    
    # Add debugging
    print(f"Result: {{result}}")
    assert result is not None
    
    # Use debugger
    import pdb; pdb.set_trace()
    assert result > 0
```

## 📈 Test Reporting

### HTML Reports

```bash
# Generate HTML test report
pytest --html=report.html --self-contained-html

# Generate JUnit XML report
pytest --junitxml=report.xml
```

### Custom Reporting

```python
def pytest_html_report_title(report):
    report.title = "Test Generator Test Report"

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("Custom summary information")])
```

## 🚀 Continuous Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

---

**Last Updated**: {test_info.get('last_updated', '2024-01-01')}
**Test Framework**: {test_info.get('framework', 'pytest')} {test_info.get('framework_version', '7.0.0')}
"""

        return TestDocumentation(
            title="Test Guide",
            content=content,
            file_path="docs/TEST_GUIDE.md",
            doc_type="test_guide"
        )
