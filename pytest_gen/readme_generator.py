"""
README documentation generator.
"""

from typing import Dict, Any
from datetime import datetime
from .doc_models import TestDocumentation


class ReadmeGenerator:
    """Generates comprehensive project README documentation."""

    def generate_readme(self, project_info: Dict[str, Any]) -> TestDocumentation:
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
