"""
Coverage report templates and content generators.
"""

from typing import Dict, Any
from .coverage_report_formatter import CoverageReportFormatter


class CoverageReportTemplates:
    """Templates for coverage report content."""
    
    def __init__(self):
        self.formatter = CoverageReportFormatter()
    
    def generate_overview_section(self, coverage_info: Dict[str, Any]) -> str:
        """Generate overview section."""
        return f"""## 📊 Overview

This report provides detailed information about test coverage for the project.

## 📈 Summary

| Metric | Value |
|--------|-------|
| **Total Coverage** | {coverage_info.get('total_coverage', '85.5')}% |
| **Lines Covered** | {coverage_info.get('lines_covered', '180')} / {coverage_info.get('lines_total', '200')} |
| **Branches Covered** | {coverage_info.get('branches_covered', '45')} / {coverage_info.get('branches_total', '50')} |
| **Functions Covered** | {coverage_info.get('functions_covered', '25')} / {coverage_info.get('functions_total', '28')} |
| **Classes Covered** | {coverage_info.get('classes_covered', '8')} / {coverage_info.get('classes_total', '10')} |"""
    
    def generate_file_coverage_section(self, coverage_info: Dict[str, Any]) -> str:
        """Generate file coverage section."""
        return f"""## 📁 File Coverage

### High Coverage Files (>90%)

{self.formatter.format_high_coverage_files(coverage_info.get('high_coverage_files', []))}

### Medium Coverage Files (70-90%)

{self.formatter.format_medium_coverage_files(coverage_info.get('medium_coverage_files', []))}

### Low Coverage Files (<70%)

{self.formatter.format_low_coverage_files(coverage_info.get('low_coverage_files', []))}"""
    
    def generate_targets_section(self, coverage_info: Dict[str, Any]) -> str:
        """Generate coverage targets section."""
        total_coverage = coverage_info.get('total_coverage', 0)
        
        return f"""## 🎯 Coverage Targets

### Current Status

- **Minimum Target (80%)**: {'✅ Achieved' if total_coverage >= 80 else '❌ Not Achieved'}
- **Recommended Target (90%)**: {'✅ Achieved' if total_coverage >= 90 else '❌ Not Achieved'}
- **Excellent Target (95%)**: {'✅ Achieved' if total_coverage >= 95 else '❌ Not Achieved'}

### Recommendations

{self.formatter.format_recommendations(coverage_info)}"""
    
    def generate_missing_coverage_section(self, coverage_info: Dict[str, Any]) -> str:
        """Generate missing coverage analysis section."""
        return f"""## 🔍 Missing Coverage Analysis

### Critical Missing Lines

{self.formatter.format_missing_lines(coverage_info.get('missing_lines', []))}

### Edge Cases Not Covered

{self.formatter.format_uncovered_edge_cases(coverage_info.get('uncovered_cases', []))}"""
    
    def generate_trends_section(self, coverage_info: Dict[str, Any]) -> str:
        """Generate coverage trends section."""
        return f"""## 📊 Coverage Trends

### Historical Coverage

| Date | Coverage | Change |
|------|----------|--------|
| {coverage_info.get('last_updated', '2024-01-01')} | {coverage_info.get('total_coverage', '85.5')}% | +1.0% |
| {coverage_info.get('previous_date', '2023-12-25')} | 84.5% | +0.5% |
| {coverage_info.get('earlier_date', '2023-12-18')} | 84.0% | +2.0% |

### Coverage Goals

- **Next Sprint**: 90% coverage
- **Next Month**: 95% coverage
- **Long Term**: 98% coverage"""
    
    def generate_test_recommendations_section(self, coverage_info: Dict[str, Any]) -> str:
        """Generate test recommendations section."""
        return f"""## 🧪 Test Recommendations

### Missing Tests

{self.formatter.format_missing_tests(coverage_info.get('missing_tests', []))}

### Test Quality Improvements

1. **Parameterized Tests**: Use `@pytest.mark.parametrize` for multiple test cases
2. **Fixtures**: Create reusable test fixtures for common setup
3. **Mocking**: Use mocks for external dependencies
4. **Assertions**: Use specific assertions with descriptive messages"""
    
    def generate_tools_section(self) -> str:
        """Generate coverage tools section."""
        return """## 📈 Coverage Tools

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
```"""
    
    def generate_improvement_section(self) -> str:
        """Generate coverage improvement section."""
        return """## 🚀 Improving Coverage

### Quick Wins

1. **Add simple unit tests** for uncovered functions
2. **Test error paths** with exception handling
3. **Add boundary tests** for edge cases
4. **Test configuration options** and default values

### Advanced Techniques

1. **Property-based testing** with hypothesis
2. **Mutation testing** to verify test quality
3. **Integration testing** for end-to-end coverage
4. **Performance testing** for critical paths"""
    
    def generate_footer(self, coverage_info: Dict[str, Any]) -> str:
        """Generate report footer."""
        return f"""---

**Last Updated**: {coverage_info.get('last_updated', '2024-01-01')}
**Generated by**: pytest-gen coverage analyzer"""
