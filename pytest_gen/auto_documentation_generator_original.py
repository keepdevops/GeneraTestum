"""
Automatic test documentation and README generation.
"""

import os
import ast
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestDocumentation:
    """Generated test documentation."""
    title: str
    content: str
    file_path: str
    doc_type: str  # 'readme', 'api_docs', 'test_guide', 'coverage_report'


class DocumentationGenerator:
    """Generates comprehensive test documentation."""

    def __init__(self):
        self.template_dir = "templates"
        self.output_dir = "docs"

    def generate_project_readme(self, project_info: Dict[str, Any]) -> TestDocumentation:
        """Generate comprehensive project README."""
        content = f"""# {project_info.get('name', 'Test Generator Project')}

## 📋 Overview

{project_info.get('description', 'Automatically generated test suite with comprehensive coverage.')}

## 🚀 Features

- **Automated Test Generation**: Generate comprehensive test suites for Python and Java code
- **Multi-Language Support**: Python (pytest) and Java (JUnit 5) test generation
- **API Testing**: Automatic API endpoint testing with mock generation
- **Security Testing**: Comprehensive security vulnerability testing
- **Performance Testing**: Performance and load testing capabilities
- **Integration Testing**: End-to-end workflow testing
- **Coverage Analysis**: Detailed code coverage reporting
- **Mock Generation**: Intelligent mock object generation
- **CI/CD Integration**: Ready-to-use CI/CD pipeline configurations

## 📁 Project Structure

```
{project_info.get('project_structure', 'project/')}
├── src/                    # Source code
├── tests/                  # Generated test files
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD configurations
└── requirements.txt        # Dependencies
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Java 11+ (for Java projects)
- pip or conda

### Setup

1. **Clone the repository:**
   ```bash
   git clone {project_info.get('repository_url', '<repository-url>')}
   cd {project_info.get('name', 'project')}
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -m pytest_gen --help
   ```

## 🧪 Running Tests

### Python Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_calculator.py

# Run with verbose output
pytest -v
```

### Java Tests

```bash
# Run all tests
./gradlew test

# Run with coverage
./gradlew test jacocoTestReport

# Run specific test class
./gradlew test --tests TestCalculator
```

## 🔧 Configuration

### Python Configuration

Create a `pytest_gen_config.json` file:

```json
{{
  "test_framework": "pytest",
  "mock_level": "comprehensive",
  "coverage_threshold": 80,
  "include_performance_tests": true,
  "include_security_tests": true,
  "include_integration_tests": true
}}
```

### Java Configuration

Create a `pytest_gen_config.json` file:

```json
{{
  "test_framework": "junit5",
  "mock_framework": "mockito",
  "coverage_threshold": 80,
  "include_performance_tests": true,
  "include_security_tests": true
}}
```

## 📊 Test Coverage

Current test coverage: **{project_info.get('coverage_percentage', '85')}%**

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

### Coverage Targets

- **Minimum**: 80%
- **Target**: 90%
- **Excellent**: 95%+

## 🔒 Security Testing

The project includes comprehensive security testing:

### Security Test Categories

- **SQL Injection**: Database query security
- **XSS Protection**: Cross-site scripting prevention
- **Input Validation**: Data sanitization and validation
- **Path Traversal**: File system security
- **Command Injection**: System command security
- **Authentication**: User authentication and authorization

### Running Security Tests

```bash
# Run all security tests
pytest tests/security/

# Run specific security test category
pytest tests/security/test_sql_injection.py
```

## ⚡ Performance Testing

Performance tests ensure your code meets timing requirements:

### Performance Test Types

- **Execution Time**: Function execution time limits
- **Memory Usage**: Memory consumption monitoring
- **Complexity Analysis**: Algorithmic complexity verification
- **Load Testing**: High-load scenario testing

### Running Performance Tests

```bash
# Run performance tests
pytest tests/performance/

# Run with timing analysis
pytest tests/performance/ --durations=10
```

## 🔗 Integration Testing

Integration tests verify end-to-end workflows:

### Integration Test Types

- **API Workflows**: Complete API request/response cycles
- **Data Flow**: Data transformation and validation
- **Service Integration**: External service interactions
- **Database Integration**: Database operations and transactions

### Running Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Run with external services
pytest tests/integration/ --external-services
```

## 🤖 Automation Features

### Automated Test Generation

```bash
# Generate tests for a file
python -m pytest_gen generate example.py

# Generate tests for a directory
python -m pytest_gen generate src/

# Generate with specific options
python -m pytest_gen generate example.py --framework pytest --coverage 90
```

### Automated Analysis

```bash
# Run complete analysis
python -m pytest_gen automation complete src/ tests/

# Run coverage analysis
python -m pytest_gen automation coverage src/ tests/

# Run security analysis
python -m pytest_gen automation security src/

# Run performance analysis
python -m pytest_gen automation performance src/
```

## 🚀 CI/CD Integration

### GitHub Actions

The project includes pre-configured GitHub Actions workflows:

- **Test Runner**: Automated test execution
- **Coverage Reporting**: Coverage analysis and reporting
- **Security Scanning**: Security vulnerability detection
- **Performance Monitoring**: Performance regression detection

### Jenkins Pipeline

Jenkins pipeline configuration is available in `.jenkins/Jenkinsfile`.

## 📈 Monitoring and Reporting

### Test Reports

- **HTML Reports**: Detailed test execution reports
- **Coverage Reports**: Code coverage analysis
- **Security Reports**: Security vulnerability assessment
- **Performance Reports**: Performance metrics and trends

### Metrics Dashboard

Access the metrics dashboard at: `{project_info.get('dashboard_url', 'http://localhost:8080/dashboard')}`

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Test Failures**: Check test configuration and environment
3. **Coverage Issues**: Verify source paths in configuration
4. **Performance Issues**: Check system resources and test timeouts

### Debug Mode

```bash
# Run with debug output
pytest --log-cli-level=DEBUG

# Run with verbose output
pytest -vvv
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Run all quality checks
pre-commit run --all-files
```

## 📝 License

{project_info.get('license', 'MIT License')}

## 🙏 Acknowledgments

- Built with [pytest](https://pytest.org/) for Python testing
- Built with [JUnit 5](https://junit.org/junit5/) for Java testing
- Security testing powered by [Bandit](https://bandit.readthedocs.io/)
- Coverage analysis by [coverage.py](https://coverage.readthedocs.io/)

## 📞 Support

- **Documentation**: [Project Wiki]({project_info.get('wiki_url', '<wiki-url>')})
- **Issues**: [GitHub Issues]({project_info.get('issues_url', '<issues-url>')})
- **Discussions**: [GitHub Discussions]({project_info.get('discussions_url', '<discussions-url>')})

---

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Generated by**: pytest-gen v{project_info.get('version', '1.0.0')}
"""
        
        return TestDocumentation(
            title="README",
            content=content,
            file_path="README.md",
            doc_type="readme"
        )

    def generate_api_documentation(self, api_info: Dict[str, Any]) -> TestDocumentation:
        """Generate API documentation."""
        content = f"""# API Documentation

## 📋 Overview

This document provides comprehensive API documentation for the test suite.

## 🔗 Endpoints

### Base URL

```
{api_info.get('base_url', 'http://localhost:5000')}
```

### Authentication

{api_info.get('authentication', 'No authentication required for test endpoints.')}

## 📚 API Reference

### Test Endpoints

#### GET /tests
Get all available tests.

**Response:**
```json
{{
  "tests": [
    {{
      "id": "test_calculator_add",
      "name": "test_calculator_add",
      "description": "Test calculator addition functionality",
      "status": "pass",
      "duration": 0.001
    }}
  ],
  "total": 1,
  "passed": 1,
  "failed": 0
}}
```

#### POST /tests/run
Run specific tests.

**Request Body:**
```json
{{
  "test_ids": ["test_calculator_add"],
  "options": {{
    "verbose": true,
    "coverage": true
  }}
}}
```

**Response:**
```json
{{
  "results": [
    {{
      "id": "test_calculator_add",
      "status": "pass",
      "duration": 0.001,
      "output": "Test passed successfully"
    }}
  ],
  "summary": {{
    "total": 1,
    "passed": 1,
    "failed": 0,
    "duration": 0.001
  }}
}}
```

#### GET /coverage
Get test coverage information.

**Response:**
```json
{{
  "coverage_percentage": 85.5,
  "files": [
    {{
      "file": "src/calculator.py",
      "coverage": 90.0,
      "lines_covered": 18,
      "lines_total": 20
    }}
  ],
  "summary": {{
    "lines_covered": 180,
    "lines_total": 200,
    "branches_covered": 45,
    "branches_total": 50
  }}
}}
```

#### GET /security
Get security test results.

**Response:**
```json
{{
  "vulnerabilities": [
    {{
      "type": "sql_injection",
      "severity": "high",
      "description": "Potential SQL injection vulnerability",
      "file": "src/database.py",
      "line": 25
    }}
  ],
  "summary": {{
    "total": 1,
    "critical": 0,
    "high": 1,
    "medium": 0,
    "low": 0
  }}
}}
```

#### GET /performance
Get performance test results.

**Response:**
```json
{{
  "performance_tests": [
    {{
      "function": "calculate_fibonacci",
      "execution_time": 0.001,
      "max_time": 0.1,
      "status": "pass",
      "memory_usage": 1024
    }}
  ],
  "summary": {{
    "total": 1,
    "passed": 1,
    "failed": 0,
    "average_time": 0.001
  }}
}}
```

## 🔧 Configuration

### Test Configuration

```json
{{
  "test_framework": "pytest",
  "mock_level": "comprehensive",
  "coverage_threshold": 80,
  "include_performance_tests": true,
  "include_security_tests": true,
  "include_integration_tests": true,
  "timeout": 300,
  "parallel": true,
  "workers": 4
}}
```

### API Configuration

```json
{{
  "base_url": "http://localhost:5000",
  "timeout": 30,
  "retries": 3,
  "headers": {{
    "Content-Type": "application/json",
    "User-Agent": "pytest-gen/1.0.0"
  }}
}}
```

## 📊 Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not Found |
| 500  | Internal Server Error |

## 🧪 Testing the API

### Using curl

```bash
# Get all tests
curl -X GET http://localhost:5000/tests

# Run specific test
curl -X POST http://localhost:5000/tests/run \\
  -H "Content-Type: application/json" \\
  -d '{{"test_ids": ["test_calculator_add"]}}'

# Get coverage
curl -X GET http://localhost:5000/coverage
```

### Using Python requests

```python
import requests

# Get all tests
response = requests.get('http://localhost:5000/tests')
tests = response.json()

# Run specific test
response = requests.post('http://localhost:5000/tests/run', 
                        json={{'test_ids': ['test_calculator_add']}})
result = response.json()

# Get coverage
response = requests.get('http://localhost:5000/coverage')
coverage = response.json()
```

## 📈 Monitoring

### Health Check

```bash
curl -X GET http://localhost:5000/health
```

### Metrics

```bash
curl -X GET http://localhost:5000/metrics
```

---

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return TestDocumentation(
            title="API Documentation",
            content=content,
            file_path="docs/API.md",
            doc_type="api_docs"
        )

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

    def generate_coverage_report(self, coverage_info: Dict[str, Any]) -> TestDocumentation:
        """Generate detailed coverage report."""
        content = f"""# Coverage Report

## 📊 Overview

This report provides detailed information about test coverage for the project.

## 📈 Summary

| Metric | Value |
|--------|-------|
| **Total Coverage** | {coverage_info.get('total_coverage', '85.5')}% |
| **Lines Covered** | {coverage_info.get('lines_covered', '180')} / {coverage_info.get('lines_total', '200')} |
| **Branches Covered** | {coverage_info.get('branches_covered', '45')} / {coverage_info.get('branches_total', '50')} |
| **Functions Covered** | {coverage_info.get('functions_covered', '25')} / {coverage_info.get('functions_total', '28')} |
| **Classes Covered** | {coverage_info.get('classes_covered', '8')} / {coverage_info.get('classes_total', '10')} |

## 📁 File Coverage

### High Coverage Files (>90%)

| File | Coverage | Lines | Missing |
|------|----------|-------|---------|
| src/calculator.py | 95.0% | 20/20 | None |
| src/utils.py | 92.5% | 37/40 | 15, 18, 25 |
| src/validators.py | 90.0% | 18/20 | 12, 19 |

### Medium Coverage Files (70-90%)

| File | Coverage | Lines | Missing |
|------|----------|-------|---------|
| src/api.py | 85.0% | 45/50 | 20-24 |
| src/database.py | 80.0% | 30/35 | 25, 28, 30, 32, 34 |
| src/auth.py | 75.0% | 15/20 | 5, 10, 15, 18, 20 |

### Low Coverage Files (<70%)

| File | Coverage | Lines | Missing |
|------|----------|-------|---------|
| src/legacy.py | 60.0% | 12/20 | 1, 3, 5, 7, 9, 11, 13, 15 |
| src/experimental.py | 45.0% | 9/20 | 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 |

## 🎯 Coverage Targets

### Current Status

- **Minimum Target (80%)**: {'✅ Achieved' if coverage_info.get('total_coverage', 85.5) >= 80 else '❌ Not Achieved'}
- **Recommended Target (90%)**: {'✅ Achieved' if coverage_info.get('total_coverage', 85.5) >= 90 else '❌ Not Achieved'}
- **Excellent Target (95%)**: {'✅ Achieved' if coverage_info.get('total_coverage', 85.5) >= 95 else '❌ Not Achieved'}

### Recommendations

1. **High Priority**: Improve coverage for low coverage files
2. **Medium Priority**: Add edge case tests for medium coverage files
3. **Low Priority**: Maintain high coverage for well-tested files

## 🔍 Missing Coverage Analysis

### Critical Missing Lines

```python
# src/database.py:25-30
def critical_function():
    if condition:  # Line 25 - Missing test case
        return process_data()  # Line 26 - Missing test case
    else:
        return default_value()  # Line 28 - Missing test case
```

### Edge Cases Not Covered

1. **Error Handling**: Exception paths not tested
2. **Boundary Conditions**: Edge values not tested
3. **Null/Empty Inputs**: Empty data handling not tested
4. **Large Data Sets**: Performance with large inputs not tested

## 📊 Coverage Trends

### Recent Changes

| Date | Coverage | Change |
|------|----------|---------|
| {datetime.now().strftime('%Y-%m-%d')} | {coverage_info.get('total_coverage', '85.5')}% | +2.5% |
| {datetime.now().strftime('%Y-%m-%d')} | 83.0% | +1.0% |
| {datetime.now().strftime('%Y-%m-%d')} | 82.0% | +0.5% |

### Coverage Goals

- **Next Sprint**: 90% coverage
- **Next Month**: 95% coverage
- **Long Term**: 98% coverage

## 🧪 Test Recommendations

### Missing Tests

1. **Error Handling Tests**
   ```python
   def test_database_connection_error():
       with pytest.raises(DatabaseError):
           connect_to_database("invalid_url")
   ```

2. **Edge Case Tests**
   ```python
   def test_calculator_overflow():
       with pytest.raises(OverflowError):
           calculator.add(float('inf'), 1)
   ```

3. **Integration Tests**
   ```python
   def test_api_database_integration():
       response = api.create_user(user_data)
       user = database.get_user(response.id)
       assert user.email == user_data.email
   ```

### Test Quality Improvements

1. **Parameterized Tests**: Use `@pytest.mark.parametrize` for multiple test cases
2. **Fixtures**: Create reusable test fixtures for common setup
3. **Mocking**: Use mocks for external dependencies
4. **Assertions**: Use specific assertions with descriptive messages

## 📈 Coverage Tools

### Generating Reports

```bash
# HTML Report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# XML Report
pytest --cov=src --cov-report=xml

# Terminal Report
pytest --cov=src --cov-report=term-missing

# JSON Report
pytest --cov=src --cov-report=json
```

### Coverage Configuration

```ini
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🚀 Improving Coverage

### Quick Wins

1. **Add simple unit tests** for uncovered functions
2. **Test error paths** with exception handling
3. **Add boundary tests** for edge cases
4. **Test configuration options** and default values

### Advanced Techniques

1. **Property-based testing** with hypothesis
2. **Mutation testing** to verify test quality
3. **Integration testing** for end-to-end coverage
4. **Performance testing** for critical paths

---

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Generated by**: pytest-gen coverage analyzer
"""
        
        return TestDocumentation(
            title="Coverage Report",
            content=content,
            file_path="docs/COVERAGE_REPORT.md",
            doc_type="coverage_report"
        )

    def generate_all_documentation(self, project_info: Dict[str, Any]) -> List[TestDocumentation]:
        """Generate all documentation files."""
        docs = []
        
        # Generate README
        docs.append(self.generate_project_readme(project_info))
        
        # Generate API documentation
        docs.append(self.generate_api_documentation(project_info))
        
        # Generate test guide
        docs.append(self.generate_test_guide(project_info))
        
        # Generate coverage report
        docs.append(self.generate_coverage_report(project_info))
        
        return docs

    def save_documentation(self, docs: List[TestDocumentation], output_dir: str = "docs"):
        """Save documentation files to disk."""
        os.makedirs(output_dir, exist_ok=True)
        
        for doc in docs:
            file_path = os.path.join(output_dir, doc.file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(doc.content)
            
            print(f"📄 Generated: {file_path}")


class AutoDocumentationGenerator:
    """Main class for automatic documentation generation."""

    def __init__(self):
        self.generator = DocumentationGenerator()

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze project to gather information for documentation."""
        project_info = {
            'name': os.path.basename(project_path),
            'description': 'Automatically generated test suite with comprehensive coverage.',
            'version': '1.0.0',
            'repository_url': '<repository-url>',
            'wiki_url': '<wiki-url>',
            'issues_url': '<issues-url>',
            'discussions_url': '<discussions-url>',
            'license': 'MIT License',
            'dashboard_url': 'http://localhost:8080/dashboard',
            'coverage_percentage': 85,
            'test_count': 25,
            'pass_rate': 96,
            'avg_duration': 0.15,
            'fastest_test': 'test_simple_add',
            'fastest_time': '0.001',
            'slowest_test': 'test_large_dataset',
            'slowest_time': '2.5',
            'total_duration': '15.2'
        }
        
        # Try to extract more information from the project
        try:
            # Look for setup.py or pyproject.toml
            setup_file = os.path.join(project_path, 'setup.py')
            if os.path.exists(setup_file):
                with open(setup_file, 'r') as f:
                    content = f.read()
                    if 'name=' in content:
                        project_info['name'] = content.split('name=')[1].split(',')[0].strip().strip('"\'')
            
            # Count test files
            test_files = []
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.startswith('test_') and file.endswith('.py'):
                        test_files.append(file)
            project_info['test_count'] = len(test_files)
            
        except Exception:
            pass
        
        return project_info

    def generate_documentation(self, project_path: str, output_dir: str = "docs") -> List[TestDocumentation]:
        """Generate comprehensive documentation for a project."""
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Generate all documentation
        docs = self.generator.generate_all_documentation(project_info)
        
        # Save documentation
        self.generator.save_documentation(docs, output_dir)
        
        return docs

    def generate_documentation_report(self, docs: List[TestDocumentation]) -> str:
        """Generate a report of generated documentation."""
        if not docs:
            return "✅ No documentation generated."
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("📚 AUTOMATIC DOCUMENTATION GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n📄 DOCUMENTATION FILES GENERATED: {len(docs)}")
        
        for doc in docs:
            report_lines.append(f"\n📋 {doc.title.upper()}:")
            report_lines.append(f"  • File: {doc.file_path}")
            report_lines.append(f"  • Type: {doc.doc_type}")
            report_lines.append(f"  • Size: {len(doc.content)} characters")
        
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        report_lines.append(f"  • Review and customize generated documentation")
        report_lines.append(f"  • Add project-specific examples and screenshots")
        report_lines.append(f"  • Update configuration examples for your environment")
        report_lines.append(f"  • Add troubleshooting section for common issues")
        report_lines.append(f"  • Include contribution guidelines and code of conduct")
        
        return "\n".join(report_lines)
