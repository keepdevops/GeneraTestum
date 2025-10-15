"""
README configuration and development sections.
"""


class ReadmeConfigSections:
    """Configuration and development sections for README."""
    
    @staticmethod
    def get_configuration_section() -> str:
        """Generate configuration section."""
        return """## 🔧 Configuration

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
```"""
    
    @staticmethod
    def get_development_section() -> str:
        """Generate development section."""
        return """## 🚀 Development

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

Follow the naming convention: `test_<module_name>.py`"""
    
    @staticmethod
    def get_contributing_section(project_info: dict) -> str:
        """Generate contributing section."""
        return f"""## 🤝 Contributing

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
- Add type hints to new code"""
    
    @staticmethod
    def get_footer_section(project_info: dict) -> str:
        """Generate footer section."""
        return f"""## 📚 API Documentation

For detailed API documentation, see:
- [API Reference](docs/API.md)
- [Test Guide](docs/TEST_GUIDE.md)
- [Coverage Report](docs/COVERAGE_REPORT.md)

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
**Version**: {project_info.get('version', '1.0.0')}"""
