"""
Basic test guide templates.
"""


class TestGuideBasicTemplates:
    """Basic test guide templates."""
    
    @staticmethod
    def get_test_structure_template() -> str:
        """Get test structure template."""
        return """
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
"""

    @staticmethod
    def get_test_types_template() -> str:
        """Get test types template."""
        return """
## 🧪 Test Types

### Unit Tests
- **Purpose**: Test individual functions, methods, or classes in isolation
- **Scope**: Single component
- **Speed**: Fast (< 1ms per test)
- **Dependencies**: Mocked or stubbed

### Integration Tests
- **Purpose**: Test interaction between components
- **Scope**: Multiple components
- **Speed**: Medium (1-100ms per test)
- **Dependencies**: Real services, test databases

### End-to-End Tests
- **Purpose**: Test complete user workflows
- **Scope**: Entire application
- **Speed**: Slow (> 100ms per test)
- **Dependencies**: Full environment

### Performance Tests
- **Purpose**: Test system performance under load
- **Scope**: Critical paths
- **Speed**: Variable
- **Dependencies**: Load testing tools
"""

    @staticmethod
    def get_test_patterns_template() -> str:
        """Get test patterns template."""
        return """
## 🔧 Test Patterns

### AAA Pattern (Arrange, Act, Assert)
```python
def test_calculate_total():
    # Arrange
    items = [10, 20, 30]
    expected = 60
    
    # Act
    result = calculate_total(items)
    
    # Assert
    assert result == expected
```

### Given-When-Then Pattern
```python
def test_user_login():
    # Given
    user = create_test_user()
    
    # When
    result = login_user(user.email, "password")
    
    # Then
    assert result.success is True
    assert result.token is not None
```

### Test Fixtures
```python
@pytest.fixture
def sample_data():
    return {
        "users": [{"id": 1, "name": "John"}],
        "products": [{"id": 1, "name": "Product1"}]
    }

def test_process_data(sample_data):
    result = process_users(sample_data["users"])
    assert len(result) == 1
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("test", "TEST")
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```
"""

    @staticmethod
    def get_mocking_guide_template() -> str:
        """Get mocking guide template."""
        return """
## 🎭 Mocking Guide

### Basic Mocking
```python
from unittest.mock import Mock, patch

def test_api_call():
    # Mock external API
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"data": "test"}
        
        result = fetch_data()
        
        assert result == {"data": "test"}
        mock_get.assert_called_once()
```

### Mock Objects
```python
def test_service_interaction():
    # Create mock service
    mock_service = Mock()
    mock_service.process.return_value = "processed"
    
    result = business_logic(mock_service)
    
    assert result == "processed"
    mock_service.process.assert_called_once()
```

### Mock Database
```python
@pytest.fixture
def mock_db():
    db = Mock()
    db.query.return_value = [{"id": 1, "name": "test"}]
    return db

def test_database_operation(mock_db):
    result = get_users(mock_db)
    assert len(result) == 1
    mock_db.query.assert_called_once()
```
"""
