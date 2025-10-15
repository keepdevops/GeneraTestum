"""
Coverage report generator - refactored for 200LOC limit.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation
from .coverage_report_templates import CoverageReportTemplates


class CoverageReportGenerator:
    """Generates detailed coverage report documentation."""

    def __init__(self):
        self.templates = CoverageReportTemplates()

    def generate_coverage_report(self, coverage_info: Dict[str, Any]) -> TestDocumentation:
        """Generate detailed coverage report."""
        content = f"""# Coverage Report

{self.templates.generate_overview_section(coverage_info)}

{self.templates.generate_file_coverage_section(coverage_info)}

{self.templates.generate_targets_section(coverage_info)}

{self.templates.generate_missing_coverage_section(coverage_info)}

{self.templates.generate_trends_section(coverage_info)}

{self.templates.generate_test_recommendations_section(coverage_info)}

{self.templates.generate_tools_section()}

{self.templates.generate_improvement_section()}

{self.templates.generate_footer(coverage_info)}
"""

        return TestDocumentation(
            title="Coverage Report",
            content=content,
            file_path="docs/COVERAGE_REPORT.md",
            doc_type="coverage_report"
        )

    def generate_summary_report(self, coverage_info: Dict[str, Any]) -> str:
        """Generate a concise summary report."""
        total_coverage = coverage_info.get('total_coverage', 0)
        lines_covered = coverage_info.get('lines_covered', 0)
        lines_total = coverage_info.get('lines_total', 0)
        
        summary = f"""Coverage Summary:
- Total Coverage: {total_coverage}%
- Lines Covered: {lines_covered}/{lines_total}
- Status: {'✅ Good' if total_coverage >= 80 else '⚠️ Needs Improvement'}
"""
        
        if total_coverage < 80:
            summary += "\nRecommendations:\n"
            summary += "- Focus on low coverage files\n"
            summary += "- Add edge case tests\n"
            summary += "- Test error handling paths\n"
        
        return summary

    def generate_coverage_metrics(self, coverage_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate coverage metrics."""
        return {
            "total_coverage": coverage_info.get('total_coverage', 0),
            "lines_coverage": {
                "covered": coverage_info.get('lines_covered', 0),
                "total": coverage_info.get('lines_total', 0),
                "percentage": (coverage_info.get('lines_covered', 0) / coverage_info.get('lines_total', 1)) * 100
            },
            "branches_coverage": {
                "covered": coverage_info.get('branches_covered', 0),
                "total": coverage_info.get('branches_total', 0),
                "percentage": (coverage_info.get('branches_covered', 0) / coverage_info.get('branches_total', 1)) * 100
            },
            "functions_coverage": {
                "covered": coverage_info.get('functions_covered', 0),
                "total": coverage_info.get('functions_total', 0),
                "percentage": (coverage_info.get('functions_covered', 0) / coverage_info.get('functions_total', 1)) * 100
            },
            "classes_coverage": {
                "covered": coverage_info.get('classes_covered', 0),
                "total": coverage_info.get('classes_total', 0),
                "percentage": (coverage_info.get('classes_covered', 0) / coverage_info.get('classes_total', 1)) * 100
            }
        }

    def generate_coverage_recommendations(self, coverage_info: Dict[str, Any]) -> list:
        """Generate specific coverage improvement recommendations."""
        recommendations = []
        total_coverage = coverage_info.get('total_coverage', 0)
        
        if total_coverage < 80:
            recommendations.append({
                "priority": "high",
                "action": "Improve overall coverage",
                "description": f"Current coverage is {total_coverage}%, below the 80% minimum target"
            })
        
        low_coverage_files = coverage_info.get('low_coverage_files', [])
        if low_coverage_files:
            recommendations.append({
                "priority": "high",
                "action": "Focus on low coverage files",
                "description": f"{len(low_coverage_files)} files have coverage below 70%"
            })
        
        missing_lines = coverage_info.get('missing_lines', [])
        if missing_lines:
            recommendations.append({
                "priority": "medium",
                "action": "Add tests for critical missing lines",
                "description": f"{len(missing_lines)} critical lines are not covered"
            })
        
        uncovered_cases = coverage_info.get('uncovered_cases', [])
        if uncovered_cases:
            recommendations.append({
                "priority": "medium",
                "action": "Add edge case tests",
                "description": f"{len(uncovered_cases)} edge cases are not covered"
            })
        
        return recommendations

    def export_coverage_data(self, coverage_info: Dict[str, Any]) -> Dict[str, Any]:
        """Export coverage data in structured format."""
        return {
            "coverage_summary": {
                "total_coverage": coverage_info.get('total_coverage', 0),
                "last_updated": coverage_info.get('last_updated', '2024-01-01'),
                "lines_covered": coverage_info.get('lines_covered', 0),
                "lines_total": coverage_info.get('lines_total', 0),
                "branches_covered": coverage_info.get('branches_covered', 0),
                "branches_total": coverage_info.get('branches_total', 0),
                "functions_covered": coverage_info.get('functions_covered', 0),
                "functions_total": coverage_info.get('functions_total', 0),
                "classes_covered": coverage_info.get('classes_covered', 0),
                "classes_total": coverage_info.get('classes_total', 0)
            },
            "file_coverage": {
                "high_coverage": coverage_info.get('high_coverage_files', []),
                "medium_coverage": coverage_info.get('medium_coverage_files', []),
                "low_coverage": coverage_info.get('low_coverage_files', [])
            },
            "issues": {
                "missing_lines": coverage_info.get('missing_lines', []),
                "uncovered_cases": coverage_info.get('uncovered_cases', []),
                "missing_tests": coverage_info.get('missing_tests', [])
            },
            "recommendations": self.generate_coverage_recommendations(coverage_info)
        }