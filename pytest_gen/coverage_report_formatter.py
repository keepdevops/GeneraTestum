"""
Coverage report formatting utilities.
"""

from typing import Dict, Any, List


class CoverageReportFormatter:
    """Formats different sections of coverage reports."""
    
    @staticmethod
    def format_high_coverage_files(files: List[Dict[str, Any]]) -> str:
        """Format high coverage files."""
        if not files:
            return "No files with high coverage found."
        
        formatted = []
        formatted.append("| File | Coverage | Lines | Missing |")
        formatted.append("|------|----------|-------|---------|")
        
        for file_info in files:
            file_path = file_info.get('path', 'unknown')
            coverage = file_info.get('coverage', '0%')
            lines = file_info.get('lines', '0/0')
            missing = file_info.get('missing', 'None')
            formatted.append(f"| {file_path} | {coverage} | {lines} | {missing} |")
        
        return "\n".join(formatted)
    
    @staticmethod
    def format_medium_coverage_files(files: List[Dict[str, Any]]) -> str:
        """Format medium coverage files."""
        if not files:
            return "No files with medium coverage found."
        
        formatted = []
        formatted.append("| File | Coverage | Lines | Missing |")
        formatted.append("|------|----------|-------|---------|")
        
        for file_info in files:
            file_path = file_info.get('path', 'unknown')
            coverage = file_info.get('coverage', '0%')
            lines = file_info.get('lines', '0/0')
            missing = file_info.get('missing', 'None')
            formatted.append(f"| {file_path} | {coverage} | {lines} | {missing} |")
        
        return "\n".join(formatted)
    
    @staticmethod
    def format_low_coverage_files(files: List[Dict[str, Any]]) -> str:
        """Format low coverage files."""
        if not files:
            return "No files with low coverage found."
        
        formatted = []
        formatted.append("| File | Coverage | Lines | Missing |")
        formatted.append("|------|----------|-------|---------|")
        
        for file_info in files:
            file_path = file_info.get('path', 'unknown')
            coverage = file_info.get('coverage', '0%')
            lines = file_info.get('lines', '0/0')
            missing = file_info.get('missing', 'None')
            formatted.append(f"| {file_path} | {coverage} | {lines} | {missing} |")
        
        return "\n".join(formatted)
    
    @staticmethod
    def format_missing_lines(missing_lines: List[Dict[str, Any]]) -> str:
        """Format missing lines information."""
        if not missing_lines:
            return "No critical missing lines identified."
        
        formatted = []
        formatted.append("```python")
        
        for line_info in missing_lines:
            file_path = line_info.get('file', 'unknown')
            line_number = line_info.get('line', 0)
            code = line_info.get('code', '')
            formatted.append(f"# {file_path}:{line_number}")
            formatted.append(f"# {code}  # Missing test case")
            formatted.append("")
        
        formatted.append("```")
        return "\n".join(formatted)
    
    @staticmethod
    def format_uncovered_edge_cases(cases: List[Dict[str, Any]]) -> str:
        """Format uncovered edge cases."""
        if not cases:
            return "No specific edge cases identified."
        
        formatted = []
        for i, case in enumerate(cases, 1):
            case_type = case.get('type', 'Unknown')
            description = case.get('description', '')
            formatted.append(f"{i}. **{case_type}**: {description}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def format_missing_tests(missing_tests: List[Dict[str, Any]]) -> str:
        """Format missing tests recommendations."""
        if not missing_tests:
            return "No specific missing tests identified."
        
        formatted = []
        for test_info in missing_tests:
            test_type = test_info.get('type', 'Unknown')
            description = test_info.get('description', '')
            code = test_info.get('code', '')
            
            formatted.append(f"""
**{test_type} Tests**
```python
{description}
{code}
```
""")
        
        return "\n".join(formatted)
    
    @staticmethod
    def format_recommendations(coverage_info: Dict[str, Any]) -> str:
        """Format coverage recommendations."""
        total_coverage = coverage_info.get('total_coverage', 0)
        
        recommendations = []
        
        if total_coverage < 80:
            recommendations.append("1. **High Priority**: Improve coverage for low coverage files")
        if total_coverage < 90:
            recommendations.append("2. **Medium Priority**: Add edge case tests for medium coverage files")
        if total_coverage >= 90:
            recommendations.append("3. **Low Priority**: Maintain high coverage for well-tested files")
        
        return "\n".join(recommendations) if recommendations else "Coverage targets have been achieved."
