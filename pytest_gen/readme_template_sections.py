"""
README template sections for different parts of the documentation.
"""


class ReadmeTemplateSections:
    """Template sections for README generation."""
    
    @staticmethod
    def get_header_section(project_info: dict) -> str:
        """Generate header and overview section."""
        return f"""# {project_info.get('name', 'Test Generator Project')}

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
- **CI/CD Integration**: Ready-to-use CI/CD pipeline configurations"""
    
    @staticmethod
    def get_project_structure_section(project_info: dict) -> str:
        """Generate project structure section."""
        return f"""## 📁 Project Structure

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
```"""
    
    @staticmethod
    def get_installation_section(project_info: dict) -> str:
        """Generate installation section."""
        return f"""## 🛠️ Installation

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
   ```"""
    
    @staticmethod
    def get_testing_section() -> str:
        """Generate testing section."""
        return """## 🧪 Running Tests

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
```"""
    
    @staticmethod
    def get_coverage_section() -> str:
        """Generate coverage section."""
        return """## 📊 Coverage Reports

After running tests with coverage, you can view detailed reports:

- **HTML Report**: Open `htmlcov/index.html` in your browser
- **Terminal Report**: Coverage summary displayed in terminal
- **XML Report**: Available for CI/CD integration

### Coverage Targets

- **Minimum**: 80% overall coverage
- **Recommended**: 90% overall coverage
- **Excellent**: 95% overall coverage"""
