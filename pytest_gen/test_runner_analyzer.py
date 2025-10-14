"""
Test result analysis functionality for automated test runner.
"""

import time
from typing import Dict, List, Any
from .test_runner_models import TestResult, TestSuiteResult


class TestResultAnalyzer:
    """Analyzes test results and generates insights."""

    def __init__(self, coverage_threshold: int = 80):
        self.coverage_threshold = coverage_threshold

    def analyze_results(self, test_results: Dict[str, Any], coverage_result: Dict[str, Any], start_time: float) -> TestSuiteResult:
        """Analyze test results and create comprehensive report."""
        duration = time.time() - start_time
        summary = test_results.get('summary', {})
        
        # Extract individual test results
        test_result_objects = []
        slow_tests = []
        
        for test in test_results.get('tests', []):
            test_duration = test.get('duration', 0.0)
            test_result = TestResult(
                test_name=test.get('nodeid', 'unknown'),
                status=test.get('outcome', 'unknown'),
                duration=test_duration,
                error_message=test.get('call', {}).get('longrepr', None) if test.get('outcome') == 'failed' else None
            )
            test_result_objects.append(test_result)
            
            # Track slow tests (> 1 second)
            if test_duration > 1.0:
                slow_tests.append((test.get('nodeid', 'unknown'), test_duration))
        
        # Sort slow tests by duration
        slow_tests.sort(key=lambda x: x[1], reverse=True)
        
        return TestSuiteResult(
            total_tests=summary.get('total', 0),
            passed=summary.get('passed', 0),
            failed=summary.get('failed', 0),
            skipped=summary.get('skipped', 0),
            errors=summary.get('errors', 0),
            duration=duration,
            coverage_percentage=coverage_result.get('coverage_percentage'),
            test_results=test_result_objects,
            slow_tests=slow_tests[:10]  # Top 10 slowest tests
        )

    def generate_report(self, suite_result: TestSuiteResult) -> str:
        """Generate a comprehensive test report."""
        report_lines = []
        
        # Header
        report_lines.append("=" * 60)
        report_lines.append("🧪 AUTOMATED TEST EXECUTION REPORT")
        report_lines.append("=" * 60)
        
        # Summary
        report_lines.append(f"\n📊 SUMMARY:")
        report_lines.append(f"  Total Tests: {suite_result.total_tests}")
        report_lines.append(f"  ✅ Passed: {suite_result.passed}")
        report_lines.append(f"  ❌ Failed: {suite_result.failed}")
        report_lines.append(f"  ⏭️  Skipped: {suite_result.skipped}")
        report_lines.append(f"  💥 Errors: {suite_result.errors}")
        report_lines.append(f"  ⏱️  Duration: {suite_result.duration:.2f}s")
        
        if suite_result.coverage_percentage is not None:
            coverage_status = "✅" if suite_result.coverage_percentage >= self.coverage_threshold else "⚠️"
            report_lines.append(f"  📈 Coverage: {suite_result.coverage_percentage:.1f}% {coverage_status}")
        
        # Failed tests
        if suite_result.failed > 0 or suite_result.errors > 0:
            report_lines.append(f"\n❌ FAILED TESTS:")
            for test_result in suite_result.test_results:
                if test_result.status in ['failed', 'error']:
                    report_lines.append(f"  • {test_result.test_name}")
                    if test_result.error_message:
                        report_lines.append(f"    {test_result.error_message[:100]}...")
        
        # Slow tests
        if suite_result.slow_tests:
            report_lines.append(f"\n🐌 SLOW TESTS (>1s):")
            for test_name, duration in suite_result.slow_tests:
                report_lines.append(f"  • {test_name}: {duration:.2f}s")
        
        # Recommendations
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        
        if suite_result.coverage_percentage and suite_result.coverage_percentage < self.coverage_threshold:
            report_lines.append(f"  • Coverage is below {self.coverage_threshold}% - consider adding more tests")
        
        if suite_result.failed > 0:
            report_lines.append(f"  • {suite_result.failed} tests failed - review and fix failing tests")
        
        if suite_result.slow_tests:
            report_lines.append(f"  • Consider optimizing slow tests for better performance")
        
        if suite_result.skipped > 0:
            report_lines.append(f"  • {suite_result.skipped} tests were skipped - review skip conditions")
        
        return "\n".join(report_lines)

    def auto_fix_suggestions(self, suite_result: TestSuiteResult) -> List[str]:
        """Generate automatic fix suggestions based on test results."""
        suggestions = []
        
        # Coverage suggestions
        if suite_result.coverage_percentage and suite_result.coverage_percentage < self.coverage_threshold:
            suggestions.append(f"Generate additional tests to improve coverage from {suite_result.coverage_percentage:.1f}% to {self.coverage_threshold}%")
        
        # Failure suggestions
        if suite_result.failed > 0:
            suggestions.append("Run 'pytest --lf' to re-run only failed tests")
            suggestions.append("Check test dependencies and mock configurations")
        
        # Performance suggestions
        if suite_result.slow_tests:
            suggestions.append("Consider using pytest-xdist for parallel test execution")
            suggestions.append("Review slow tests for optimization opportunities")
        
        # General suggestions
        if suite_result.total_tests > 100:
            suggestions.append("Consider splitting large test suite into smaller modules")
        
        return suggestions
