"""
Advanced test guide templates.
"""


class TestGuideAdvancedTemplates:
    """Advanced test guide templates."""
    
    @staticmethod
    def get_testing_best_practices_template() -> str:
        """Get testing best practices template."""
        return """
## ✅ Testing Best Practices

### Test Naming
- Use descriptive names that explain what is being tested
- Follow pattern: `test_<function>_<scenario>_<expected_result>`
- Examples:
  - `test_calculate_total_with_valid_inputs_returns_correct_sum`
  - `test_login_with_invalid_credentials_raises_authentication_error`

### Test Organization
- Group related tests in classes
- Use fixtures for common setup
- Keep tests independent and isolated
- One assertion per test when possible

### Test Data
- Use realistic test data
- Avoid hardcoded values
- Use factories for complex objects
- Clean up test data after tests

### Assertions
- Use specific assertions
- Test both positive and negative cases
- Verify side effects
- Check error messages and exceptions

### Performance
- Keep unit tests fast (< 1ms)
- Use mocking for slow operations
- Run tests in parallel when possible
- Monitor test execution time
"""

    @staticmethod
    def get_debugging_guide_template() -> str:
        """Get debugging guide template."""
        return """
## 🐛 Debugging Tests

### Common Issues

#### Test Failures
```python
# Use pytest -v for verbose output
pytest -v test_file.py

# Use pytest -s to see print statements
pytest -s test_file.py

# Use --tb=short for shorter tracebacks
pytest --tb=short test_file.py
```

#### Mock Issues
```python
# Check if mock was called
mock_obj.assert_called()

# Check call arguments
mock_obj.assert_called_with(expected_args)

# Check call count
assert mock_obj.call_count == 2

# Reset mock state
mock_obj.reset_mock()
```

#### Database Issues
```python
# Use transactions for isolation
@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()
```

### Debugging Tools
- `pytest --pdb` - Drop into debugger on failure
- `pytest -x` - Stop on first failure
- `pytest --lf` - Run last failed tests only
- `pytest --ff` - Run failed tests first
"""

    @staticmethod
    def get_ci_cd_integration_template() -> str:
        """Get CI/CD integration template."""
        return """
## 🚀 CI/CD Integration

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

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --junitxml=test-results.xml'
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'test-results.xml'
                }
            }
        }
    }
}
```

### Coverage Reports
```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# Set coverage threshold
pytest --cov=src --cov-fail-under=80
```
"""

    @staticmethod
    def get_advanced_testing_template() -> str:
        """Get advanced testing template."""
        return """
## 🎯 Advanced Testing

### Property-Based Testing
```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=100))
def test_fibonacci_properties(n):
    result = fibonacci(n)
    assert result >= 0
    if n > 1:
        assert fibonacci(n) == fibonacci(n-1) + fibonacci(n-2)
```

### Mutation Testing
```bash
# Install mutmut
pip install mutmut

# Run mutation testing
mutmut run

# Generate report
mutmut junitxml > mutation-report.xml
```

### Contract Testing
```python
from pact import Consumer, Provider

def test_api_contract():
    pact = Consumer('frontend').has_pact_with(Provider('backend'))
    pact.given('user exists').upon_receiving('get user request').with_request(
        'GET', '/users/1'
    ).will_respond_with(200, body={
        'id': 1,
        'name': 'John Doe'
    })
    
    with pact:
        result = get_user(1)
        assert result['name'] == 'John Doe'
```

### Test Data Management
```python
@pytest.fixture
def test_data():
    return {
        'users': load_test_data('users.json'),
        'products': load_test_data('products.json')
    }

def load_test_data(filename):
    with open(f'test_data/{filename}') as f:
        return json.load(f)
```
"""
