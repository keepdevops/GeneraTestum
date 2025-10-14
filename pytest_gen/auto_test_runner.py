"""
Automated test runner with intelligent analysis and reporting.
"""

import time
from typing import Dict, List, Any
from .test_runner_models import TestSuiteResult
from .test_runner_executor import TestExecutor
from .test_runner_analyzer import TestResultAnalyzer


class AutoTestRunner:
    """Automated test runner with intelligent analysis."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.default_timeout = self.config.get('timeout', 300)  # 5 minutes
        self.coverage_threshold = self.config.get('coverage_threshold', 80)
        
        # Initialize components
        self.executor = TestExecutor(self.default_timeout)
        self.analyzer = TestResultAnalyzer(self.coverage_threshold)

    def run_tests(self, test_path: str, **kwargs) -> TestSuiteResult:
        """Run tests and return comprehensive results."""
        start_time = time.time()
        
        # Run tests with pytest
        test_results = self.executor.execute_pytest(test_path, **kwargs)
        
        # Run coverage analysis
        coverage_result = self.executor.run_coverage_analysis(test_path)
        
        # Analyze results
        suite_result = self.analyzer.analyze_results(test_results, coverage_result, start_time)
        
        return suite_result

    def generate_report(self, suite_result: TestSuiteResult) -> str:
        """Generate a comprehensive test report."""
        return self.analyzer.generate_report(suite_result)

    def auto_fix_suggestions(self, suite_result: TestSuiteResult) -> List[str]:
        """Generate automatic fix suggestions based on test results."""
        return self.analyzer.auto_fix_suggestions(suite_result)
