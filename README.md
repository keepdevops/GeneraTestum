# Pytest Code Generator

A comprehensive tool for automatically generating pytest test cases from Python code, APIs, and other code types with intelligent mocking, fixtures, and parametrization.

## Features

- **Multi-Language Support**: Python, Java (JUnit 5), and Panel applications
- **Multi-Type Code Analysis**: Supports Python functions/classes, Flask, FastAPI, Django, Tornado, and Panel APIs
- **Interactive Panel GUI**: Modern web-based interface with file browser and live preview
- **Comprehensive Test Generation**: Happy path, edge cases, error handling, and boundary tests
- **Smart Mocking**: Automatic detection and mocking of external dependencies
- **Pytest Fixtures**: Auto-generated fixtures for common test setups
- **Parametrized Tests**: Multiple input scenarios with comprehensive coverage
- **Plugin Architecture**: Extensible system for adding new language support
- **Triple Interface**: CLI, Panel GUI, and programmatic library usage
- **Configurable**: Extensive configuration options for customizing test generation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### CLI Usage

Generate tests for a Python file:
```bash
pytest-gen generate my_module.py
```

Generate tests for a directory:
```bash
pytest-gen generate src/ --output tests/
```

Generate tests for Java files:
```bash
pytest-gen generate MyClass.java
```

Generate tests for Panel applications:
```bash
pytest-gen generate my_dashboard.py
```

Launch the interactive Panel GUI:
```bash
pytest-gen gui --port 5007
```

Analyze code without generating tests:
```bash
pytest-gen analyze my_api.py
```

### Library Usage

```python
from pytest_gen import generate_tests, GeneratorConfig

# Generate tests with default settings
test_files = generate_tests('my_module.py')

# Generate tests with custom configuration
config = GeneratorConfig(
    mock_level=MockLevel.COMPREHENSIVE,
    coverage_type=TestCoverage.FULL,
    output_dir='custom_tests/'
)
test_files = generate_tests('my_module.py', config=config)
```

## Configuration

### Command Line Options

```bash
pytest-gen generate SOURCE [OPTIONS]

Options:
  -o, --output PATH              Output directory for test files
  -c, --config PATH              Configuration file path
  --mock-level [none|basic|comprehensive]  Mock generation level
  --coverage [happy_path|comprehensive|full]  Test coverage level
  --include-private              Include private methods in tests
  --no-fixtures                  Disable fixture generation
  --no-parametrize              Disable parametrized tests
  --max-lines INTEGER            Maximum lines per test file (default: 200)
  --split-files                  Split large test files
  --dry-run                      Show what would be generated
  -v, --verbose                  Verbose output
```

### Configuration File

Create a configuration file:
```bash
pytest-gen init-config --format json
```

Example configuration:
```json
{
  "output_dir": "tests",
  "mock_level": "comprehensive",
  "coverage_type": "comprehensive",
  "generate_fixtures": true,
  "generate_parametrize": true,
  "mock_external_calls": true,
  "mock_database": true,
  "mock_file_io": true,
  "mock_network": true,
  "max_lines_per_file": 200,
  "split_large_tests": true
}
```

## Supported Code Types

### Python Functions and Classes

```python
def calculate_total(items, tax_rate=0.1):
    """Calculate total with tax."""
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)

class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_user(self, user_id):
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

Generated tests include:
- Parameter validation tests
- Return type assertions
- Mock database connections
- Edge case handling (empty lists, None values)
- Error handling tests

### Flask APIs

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = database.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)
```

Generated tests include:
- HTTP status code validation
- Response format validation
- Mock database calls
- Error response handling

### FastAPI APIs

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Generated Test Structure

### Basic Function Test
```python
def test_calculate_total():
    """Test calculate_total function."""
    # Arrange
    items = [Mock(price=10.0), Mock(price=20.0)]
    tax_rate = 0.1
    
    # Act
    result = calculate_total(items, tax_rate)
    
    # Assert
    assert result == 33.0
```

### Mocked Dependencies
```python
@patch('requests.get')
def test_with_mocked_request(mock_get):
    """Test with mocked HTTP request."""
    # Arrange
    mock_get.return_value.json.return_value = {'status': 'success'}
    
    # Act
    result = fetch_data_from_api()
    
    # Assert
    mock_get.assert_called_once()
    assert result['status'] == 'success'
```

### Parametrized Tests
```python
@pytest.mark.parametrize("tax_rate,expected", [
    (0.0, 30.0),
    (0.1, 33.0),
    (0.2, 36.0),
])
def test_calculate_total_parametrized(tax_rate, expected):
    """Test calculate_total with multiple tax rates."""
    items = [Mock(price=10.0), Mock(price=20.0)]
    result = calculate_total(items, tax_rate)
    assert result == expected
```

### Pytest Fixtures
```python
@pytest.fixture(scope='function')
def test_db():
    """Test database fixture."""
    import tempfile
    import sqlite3
    db_file = tempfile.NamedTemporaryFile(delete=False)
    connection = sqlite3.connect(db_file.name)
    yield connection
    connection.close()
    os.unlink(db_file.name)
```

## Advanced Usage

### Custom Mock Configuration

```python
config = GeneratorConfig(
    mock_dependencies={
        'requests', 'urllib', 'sqlite3', 'psycopg2',
        'custom_module', 'another_dependency'
    }
)
```

### API Framework Detection

The generator automatically detects and supports:
- **Flask**: `@app.route` decorators
- **FastAPI**: `@app.get`, `@app.post`, etc.
- **Django**: View classes with HTTP methods
- **Tornado**: Handler classes with HTTP methods

### Edge Case Generation

Automatically generates tests for:
- **Boundary values**: Min/max integers, empty strings, None values
- **Error conditions**: Invalid types, missing parameters
- **Edge cases**: Very large numbers, special characters, Unicode

## Examples

### Example 1: Simple Function
```python
# math_utils.py
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Generated test:
```python
def test_divide():
    """Test divide function."""
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    """Test divide by zero error."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5.0),
    (0, 5, 0.0),
    (-10, 2, -5.0),
])
def test_divide_parametrized(a, b, expected):
    """Test divide with multiple values."""
    assert divide(a, b) == expected
```

### Example 2: API Endpoint
```python
# api.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = database.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'Not found'}), 404
```

Generated test:
```python
@patch('database.get_user')
def test_get_user_success(mock_get_user):
    """Test successful user retrieval."""
    mock_get_user.return_value = {'id': 1, 'name': 'John'}
    
    response = test_client.get('/api/users/1')
    
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'John'}

def test_get_user_not_found():
    """Test user not found."""
    with patch('database.get_user', return_value=None):
        response = test_client.get('/api/users/999')
        
        assert response.status_code == 404
        assert response.json() == {'error': 'Not found'}
```

## File Organization

Generated tests respect the 200 lines per file limit by:
- Splitting large test files automatically
- Organizing tests by functionality
- Creating separate files for fixtures and utilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Changelog

### v1.0.0
- Initial release
- AST-based Python code analysis
- API framework support (Flask, FastAPI, Django, Tornado)
- Comprehensive test generation with mocking and fixtures
- CLI and library interfaces
- Configurable test generation options
