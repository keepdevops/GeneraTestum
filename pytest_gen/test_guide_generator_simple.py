"""
Simple test guide documentation generator.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation


class TestGuideGenerator:
    """Generates comprehensive test guide documentation."""

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
├── integration/            # Integration tests
├── e2e/                   # End-to-end tests
├── fixtures/              # Test fixtures
└── mocks/                 # Mock objects
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

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## 🏗️ Test Types

### Unit Tests

Unit tests verify individual functions or methods in isolation.

```python
def test_calculator_add():
    calculator = Calculator()
    result = calculator.add(2, 3)
    assert result == 5

def test_calculator_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(ValueError):
        calculator.divide(10, 0)
```

### Integration Tests

Integration tests verify that multiple components work together.

```python
def test_api_workflow():
    response = requests.post("/api/users", json={{"name": "John"}})
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    response = requests.get(f"/api/users/{{user_id}}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"
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
