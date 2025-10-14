"""
Coverage report generation functionality.
"""

from pathlib import Path
from typing import List
from .coverage_models import CoverageReport, CoverageGap


class CoverageReporter:
    """Generates comprehensive coverage reports."""

    def __init__(self, min_coverage: int = 80):
        self.min_coverage = min_coverage

    def generate_coverage_report(self, report: CoverageReport) -> str:
        """Generate a comprehensive coverage report."""
        report_lines = []
        
        # Header
        report_lines.append("=" * 60)
        report_lines.append("📊 AUTOMATED COVERAGE ANALYSIS REPORT")
        report_lines.append("=" * 60)
        
        # Summary
        coverage_status = "✅" if report.total_coverage >= self.min_coverage else "⚠️"
        report_lines.append(f"\n📈 OVERALL COVERAGE: {report.total_coverage:.1f}% {coverage_status}")
        report_lines.append(f"📋 Coverage Target: {self.min_coverage}%")
        report_lines.append(f"🔍 Coverage Gaps Found: {len(report.gaps)}")
        
        # File coverage
        if report.file_coverage:
            report_lines.append(f"\n📁 FILE COVERAGE:")
            for file_path, coverage in sorted(report.file_coverage.items(), key=lambda x: x[1]):
                status = "✅" if coverage >= self.min_coverage else "❌"
                report_lines.append(f"  {file_path}: {coverage:.1f}% {status}")
        
        # High priority gaps
        high_priority_gaps = [gap for gap in report.gaps if gap.priority == "high"]
        if high_priority_gaps:
            report_lines.append(f"\n🚨 HIGH PRIORITY GAPS ({len(high_priority_gaps)}):")
            for gap in high_priority_gaps[:10]:  # Show top 10
                report_lines.append(f"  • {gap.file_path}:{gap.line_number} - {gap.code_line[:50]}...")
                if gap.test_suggestion:
                    report_lines.append(f"    💡 {gap.test_suggestion}")
        
        # Critical paths
        if report.critical_paths:
            report_lines.append(f"\n🎯 CRITICAL PATHS:")
            for path in report.critical_paths:
                report_lines.append(f"  • {path}")
        
        # Recommendations
        if report.recommendations:
            report_lines.append(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(report.recommendations, 1):
                report_lines.append(f"  {i}. {rec}")
        
        return "\n".join(report_lines)

    def auto_generate_missing_tests(self, gaps: List[CoverageGap]) -> List[str]:
        """Automatically generate test suggestions for missing coverage."""
        test_suggestions = []
        
        # Group gaps by file and function
        gaps_by_function = {}
        for gap in gaps:
            key = f"{gap.file_path}:{gap.function_name or 'module'}"
            if key not in gaps_by_function:
                gaps_by_function[key] = []
            gaps_by_function[key].append(gap)
        
        for key, function_gaps in gaps_by_function.items():
            file_path, function_name = key.split(':', 1)
            
            if function_name != 'module' and function_name:
                # Generate function test
                test_suggestions.append(self._generate_function_test_suggestion(function_gaps[0]))
            else:
                # Generate integration test
                test_suggestions.append(self._generate_integration_test_suggestion(function_gaps))
        
        return test_suggestions

    def _generate_function_test_suggestion(self, gap: CoverageGap) -> str:
        """Generate test suggestion for a function."""
        return f"""
# Test for {gap.function_name} in {gap.file_path}
def test_{gap.function_name}():
    \"\"\"Test {gap.function_name} function coverage.\"\"\"
    # TODO: Add test cases to cover line {gap.line_number}
    # Current gap: {gap.code_line[:50]}...
    pass
"""

    def _generate_integration_test_suggestion(self, gaps: List[CoverageGap]) -> str:
        """Generate integration test suggestion for multiple gaps."""
        file_path = gaps[0].file_path
        return f"""
# Integration tests for {file_path}
def test_{Path(file_path).stem}_integration():
    \"\"\"Integration test for {file_path}.\"\"\"
    # TODO: Add integration tests to cover {len(gaps)} uncovered lines
    pass
"""
