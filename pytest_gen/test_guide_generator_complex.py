"""
Complex test guide documentation generator.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation
from .test_guide_templates_complex import TestGuideTemplatesComplex


class TestGuideGeneratorComplex:
    """Generates comprehensive test guide documentation."""

    def __init__(self):
        self.templates = TestGuideTemplatesComplex()

    def generate_test_guide(self, test_info: Dict[str, Any]) -> TestDocumentation:
        """Generate comprehensive test guide."""
        content = self._build_guide_content(test_info)
        
        return TestDocumentation(
            title="Comprehensive Test Guide",
            content=content,
            file_path="docs/TEST_GUIDE.md",
            doc_type="test_guide"
        )

    def _build_guide_content(self, test_info: Dict[str, Any]) -> str:
        """Build the complete guide content."""
        sections = [
            self._get_overview_section(test_info),
            self._get_framework_section(test_info),
            self.templates.get_test_structure_template(),
            self.templates.get_test_types_template(),
            self.templates.get_test_patterns_template(),
            self.templates.get_mocking_guide_template(),
            self.templates.get_testing_best_practices_template(),
            self.templates.get_debugging_guide_template(),
            self.templates.get_ci_cd_integration_template(),
            self.templates.get_advanced_testing_template(),
            self._get_appendices_section()
        ]
        
        return "\n\n".join(sections)

    def _get_overview_section(self, test_info: Dict[str, Any]) -> str:
        """Get overview section."""
        return f"""# Comprehensive Test Guide

## 📋 Overview

This guide provides comprehensive information about testing in the {test_info.get('project_name', 'Test Generator')} project.

**Project**: {test_info.get('project_name', 'Test Generator')}
**Framework**: {test_info.get('framework', 'pytest')}
**Version**: {test_info.get('framework_version', '7.0.0')}

## 🎯 Testing Philosophy

Our testing approach follows these principles:
- **Comprehensive Coverage**: Test all critical paths and edge cases
- **Fast Feedback**: Quick test execution for rapid development
- **Reliable Tests**: Stable, non-flaky tests that provide consistent results
- **Maintainable**: Clear, readable tests that are easy to understand and modify
- **Isolated**: Tests don't depend on each other and can run in any order
"""

    def _get_framework_section(self, test_info: Dict[str, Any]) -> str:
        """Get framework section."""
        return f"""## 🧪 Test Framework

**Framework**: {test_info.get('framework', 'pytest')}
**Version**: {test_info.get('framework_version', '7.0.0')}

### Key Features
- Automatic test discovery
- Fixture support for setup/teardown
- Parametrized testing
- Rich assertion introspection
- Plugin ecosystem
- Coverage reporting
- Parallel test execution

### Installation
```bash
pip install pytest pytest-cov pytest-xdist
```

### Configuration
Create `pytest.ini` or `pyproject.toml`:
```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests"
]
```
"""

    def _get_appendices_section(self) -> str:
        """Get appendices section."""
        return """## 📚 Appendices

### A. Test Commands Reference
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_module.py

# Run specific test
pytest tests/test_module.py::test_function

# Run with coverage
pytest --cov=src

# Run in parallel
pytest -n auto

# Run only fast tests
pytest -m "not slow"

# Generate HTML report
pytest --html=report.html
```

### B. Common pytest Fixtures
```python
@pytest.fixture(scope="session")
def db_connection():
    # Session-scoped database connection
    pass

@pytest.fixture(scope="function")
def clean_database():
    # Function-scoped database cleanup
    pass

@pytest.fixture(autouse=True)
def setup_test_environment():
    # Auto-used fixture for every test
    pass
```

### C. Testing Checklist
- [ ] All public methods have tests
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Mock external dependencies
- [ ] Tests are fast and isolated
- [ ] Test names are descriptive
- [ ] Coverage is above threshold
- [ ] CI/CD integration is working

### D. Troubleshooting
- **Slow tests**: Use mocking for external calls
- **Flaky tests**: Check for race conditions or timing issues
- **Test failures**: Use `pytest --pdb` for debugging
- **Import errors**: Check PYTHONPATH and virtual environment
- **Coverage issues**: Verify test paths and exclusions
"""