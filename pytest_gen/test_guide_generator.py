"""
Test guide documentation generator.
"""

from typing import Dict, Any
from datetime import datetime
from .doc_models import TestDocumentation


class TestGuideGenerator:
    """Generates comprehensive test guide documentation."""

    def generate_test_guide(self, test_info: Dict[str, Any]) -> TestDocumentation:
        """Generate comprehensive test guide."""
        content = f"""# Test Guide

## 📋 Overview

This guide provides comprehensive information about running and understanding the test suite.

## 🧪 Test Types

### Unit Tests

Unit tests verify individual functions and methods in isolation.

**Example:**
```python
def test_calculator_add():
    calculator = Calculator()
    result = calculator.add(2, 3)
    assert result == 5
```

### Integration Tests

Integration tests verify that different components work together correctly.

**Example:**
```python
def test_api_workflow():
    # Create user
    user = create_user("test@example.com")
    
    # Login
    token = login_user(user.email, "password")
    
    # Access protected resource
    response = get_protected_data(token)
    assert response.status_code == 200
```

### Security Tests

Security tests verify that the application is protected against common vulnerabilities.

**Example:**
```python
def test_sql_injection_protection():
    malicious_input = "'; DROP TABLE users; --"
    with pytest.raises(ValueError):
        query_user(malicious_input)
```

### Performance Tests

Performance tests verify that functions meet timing and resource requirements.

**Example:**
```python
def test_fibonacci_performance():
    start_time = time.time()
    result = fibonacci(30)
    execution_time = time.time() - start_time
    assert execution_time < 0.1
```

## 🚀 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator.py

# Run specific test function
pytest tests/test_calculator.py::test_add

# Run tests matching pattern
pytest -k "test_calculator"
```

### Advanced Test Execution

```bash
# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v

# Run in parallel
pytest -n auto

# Run with timing
pytest --durations=10

# Run failed tests only
pytest --lf

# Run last failed test
pytest --ff
```

### Test Markers

```bash
# Run slow tests
pytest -m slow

# Run integration tests
pytest -m integration

# Run security tests
pytest -m security

# Run performance tests
pytest -m performance
```

## 📊 Understanding Test Results

### Test Output

```
========================= test session starts =========================
platform darwin -- Python 3.9.0, pytest-6.2.0, py-1.10.0, pluggy-0.13.1
rootdir: /path/to/project
plugins: cov-2.12.0, xdist-2.3.0
collected 25 items

tests/test_calculator.py ..........                                [ 40%]
tests/test_api.py ................                                 [ 80%]
tests/test_security.py .....                                      [100%]

========================= 25 passed in 0.15s =========================
```

### Coverage Report

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/calculator.py          20      2    90%   15, 18
src/api.py                 45      5    89%   20-24
src/database.py            30      3    90%   25, 28, 30
-----------------------------------------------------
TOTAL                      95     10    89%
```

## 🔧 Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    security: marks tests as security tests
    performance: marks tests as performance tests
```

### conftest.py

```python
import pytest

@pytest.fixture
def calculator():
    return Calculator()

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

@pytest.fixture(scope="session")
def database():
    db = Database()
    yield db
    db.cleanup()
```

## 🐛 Debugging Tests

### Debug Mode

```bash
# Run with debug output
pytest --log-cli-level=DEBUG

# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest --pdb -x
```

### Test Debugging

```python
def test_debug_example():
    result = complex_function()
    
    # Add debug output
    print(f"Result: {{result}}")
    
    # Use debugger
    import pdb; pdb.set_trace()
    
    expected_value = "expected"
    assert result == expected_value
```

## 📈 Test Metrics

### Key Metrics

- **Test Coverage**: {test_info.get('coverage', '85')}%
- **Test Count**: {test_info.get('test_count', '25')}
- **Pass Rate**: {test_info.get('pass_rate', '96')}%
- **Average Duration**: {test_info.get('avg_duration', '0.15')}s

### Performance Metrics

- **Fastest Test**: {test_info.get('fastest_test', 'test_simple_add')} ({test_info.get('fastest_time', '0.001')}s)
- **Slowest Test**: {test_info.get('slowest_test', 'test_large_dataset')} ({test_info.get('slowest_time', '2.5')}s)
- **Total Duration**: {test_info.get('total_duration', '15.2')}s

## 🔍 Test Analysis

### Coverage Analysis

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Generate XML coverage report
pytest --cov=src --cov-report=xml

# Generate coverage report with missing lines
pytest --cov=src --cov-report=term-missing
```

### Performance Analysis

```bash
# Run with timing analysis
pytest --durations=10

# Profile slow tests
pytest --profile

# Memory profiling
pytest --memray
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Install missing dependencies
   pip install -r requirements.txt
   ```

2. **Test Failures**
   ```bash
   # Run with verbose output
   pytest -v
   
   # Run with full traceback
   pytest --tb=long
   
   # Run specific failing test
   pytest tests/test_failing.py::test_specific_function
   ```

3. **Coverage Issues**
   ```bash
   # Check coverage configuration
   pytest --cov=src --cov-report=term-missing
   
   # Verify source paths
   pytest --cov=src --cov-report=html
   ```

### Getting Help

- **Documentation**: Check the project README and API docs
- **Issues**: Report issues on GitHub
- **Discussions**: Join discussions on GitHub Discussions

---

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return TestDocumentation(
            title="Test Guide",
            content=content,
            file_path="docs/TEST_GUIDE.md",
            doc_type="test_guide"
        )
