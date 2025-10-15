"""
README documentation generator.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation


class ReadmeGenerator:
    """Generates comprehensive project README documentation."""

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
{project_info.get('name', 'project')}/
├── src/                    # Source code
├── tests/                  # Test files
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── docs/                  # Documentation
├── scripts/               # Build and deployment scripts
├── requirements.txt       # Python dependencies
├── setup.py              # Package configuration
├── README.md             # This file
└── .github/              # GitHub workflows
    └── workflows/
        └── ci.yml        # CI/CD pipeline
```

## 🛠️ Installation

### Prerequisites

- Python {project_info.get('python_version', '3.9')}+
- pip
- Git

### Setup

1. **Clone the repository**:
   ```bash
   git clone {project_info.get('repository', 'https://github.com/your-org/your-project.git')}
   cd {project_info.get('name', 'project')}
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Run Specific Test Types
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# End-to-end tests only
pytest tests/e2e/
```

### Run Tests with Different Verbosity
```bash
# Verbose output
pytest -v

# Extra verbose with print statements
pytest -s

# Show local variables in tracebacks
pytest -l
```

## 📊 Coverage Reports

After running tests with coverage, you can view detailed reports:

- **HTML Report**: Open `htmlcov/index.html` in your browser
- **Terminal Report**: Coverage summary displayed in terminal
- **XML Report**: Available for CI/CD integration

### Coverage Targets

- **Minimum**: 80% overall coverage
- **Recommended**: 90% overall coverage
- **Excellent**: 95% overall coverage

## 🔧 Configuration

### pytest Configuration

Create `pytest.ini` in your project root:

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
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
```

### Coverage Configuration

Create `.coveragerc`:

```ini
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

## 🚀 Development

### Code Style

This project follows PEP 8 style guidelines. Use the provided tools:

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

### Adding New Tests

1. **Unit Tests**: Add to `tests/unit/`
2. **Integration Tests**: Add to `tests/integration/`
3. **End-to-End Tests**: Add to `tests/e2e/`

Follow the naming convention: `test_<module_name>.py`

## 📚 API Documentation

For detailed API documentation, see:
- [API Reference](docs/API.md)
- [Test Guide](docs/TEST_GUIDE.md)
- [Coverage Report](docs/COVERAGE_REPORT.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Write tests for all new functionality
- Maintain test coverage above 80%
- Follow PEP 8 style guidelines
- Update documentation as needed
- Add type hints to new code

## 📄 License

This project is licensed under the {project_info.get('license', 'MIT')} License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **{project_info.get('author', 'Your Name')}** - *Initial work* - [{project_info.get('email', 'your.email@example.com')}](mailto:{project_info.get('email', 'your.email@example.com')})

## 🙏 Acknowledgments

- Thanks to the pytest community for the excellent testing framework
- Thanks to all contributors who help improve this project
- Inspired by modern testing practices and CI/CD best practices

## 📞 Support

- **Issues**: [GitHub Issues]({project_info.get('repository', 'https://github.com/your-org/your-project')}/issues)
- **Discussions**: [GitHub Discussions]({project_info.get('repository', 'https://github.com/your-org/your-project')}/discussions)
- **Email**: {project_info.get('email', 'support@example.com')}

---

**Last Updated**: {project_info.get('last_updated', '2024-01-01')}
**Version**: {project_info.get('version', '1.0.0')}
"""

        return TestDocumentation(
            title="README",
            content=content,
            file_path="README.md",
            doc_type="readme"
        )