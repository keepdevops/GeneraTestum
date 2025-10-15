"""
Performance test generator - refactored for 200LOC limit.
"""

from typing import Dict, List, Any
from .performance_test_models import PerformanceTest, PerformanceTestSuite, PerformanceRequirement
from .performance_test_templates import PerformanceTestTemplates
from .performance_test_file_generator import PerformanceTestFileGenerator
from .performance_test_reporter import PerformanceTestReporter


class PerformanceTestGenerator:
    """Generates performance tests from requirements."""

    def __init__(self):
        self.templates = PerformanceTestTemplates()
        self.file_generator = PerformanceTestFileGenerator()
        self.reporter = PerformanceTestReporter()

    def generate_performance_tests(self, requirements: List[PerformanceRequirement]) -> PerformanceTestSuite:
        """Generate performance tests from requirements."""
        tests = []
        
        for requirement in requirements:
            # Generate execution time test
            execution_test = self.templates.generate_execution_time_test(requirement)
            if execution_test:
                tests.append(execution_test)
            
            # Generate memory test if memory limit specified
            if requirement.memory_limit:
                memory_test = self.templates.generate_memory_test(requirement)
                if memory_test:
                    tests.append(memory_test)
            
            # Generate complexity test
            complexity_test = self.templates.generate_complexity_test(requirement)
            if complexity_test:
                tests.append(complexity_test)
            
            # Generate benchmark test
            benchmark_test = self.templates.generate_benchmark_test(requirement)
            if benchmark_test:
                tests.append(benchmark_test)
        
        # Generate test file content
        test_file_content = self.file_generator.generate_test_file_content(tests)
        
        # Calculate coverage
        coverage_percentage = len(requirements) / len(requirements) * 100 if requirements else 0
        
        return PerformanceTestSuite(
            tests=tests,
            requirements=requirements,
            total_tests=len(tests),
            coverage_percentage=coverage_percentage,
            test_file_content=test_file_content
        )

    def generate_performance_report(self, test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Generate performance test report."""
        return self.reporter.generate_performance_report(test_suite)

    def generate_summary_report(self, test_suite: PerformanceTestSuite) -> str:
        """Generate a human-readable summary report."""
        return self.reporter.generate_summary_report(test_suite)

    def analyze_test_coverage(self, test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Analyze test coverage and identify gaps."""
        return self.reporter.analyze_test_coverage(test_suite)

    def generate_performance_metrics(self, test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Generate performance metrics from test suite."""
        return self.reporter.generate_performance_metrics(test_suite)

    def export_to_json(self, test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Export test suite to JSON format."""
        return self.reporter.export_to_json(test_suite)

    def generate_test_file_with_fixtures(self, tests: List[PerformanceTest]) -> str:
        """Generate test file with pytest fixtures."""
        content = self.file_generator.generate_test_file_header()
        content += self.file_generator.generate_performance_fixtures()
        
        for test in tests:
            content = self.file_generator.add_test_function(content, test)
        
        return content

    def generate_pytest_config(self) -> str:
        """Generate pytest configuration for performance tests."""
        return self.file_generator.generate_pytest_config()

    def get_test_statistics(self, test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Get comprehensive test statistics."""
        metrics = self.generate_performance_metrics(test_suite)
        coverage = self.analyze_test_coverage(test_suite)
        
        return {
            "generation_stats": metrics["test_generation_stats"],
            "requirement_stats": metrics["requirement_stats"],
            "coverage_stats": coverage,
            "recommendations": self._generate_recommendations(test_suite)
        }

    def _generate_recommendations(self, test_suite: PerformanceTestSuite) -> List[str]:
        """Generate recommendations based on test suite analysis."""
        recommendations = []
        
        if test_suite.total_tests == 0:
            recommendations.append("No performance tests generated - check requirements")
        
        if test_suite.coverage_percentage < 100:
            recommendations.append("Consider adding tests for uncovered functions")
        
        # Check for functions without memory tests
        functions_with_memory_limits = [r for r in test_suite.requirements if r.memory_limit]
        memory_tests = [t for t in test_suite.tests if "memory_usage" in t.test_code]
        
        if len(functions_with_memory_limits) > len(memory_tests):
            recommendations.append("Add memory usage tests for functions with memory limits")
        
        # Check for functions without complexity tests
        functions_with_complexity = [r for r in test_suite.requirements if r.complexity_threshold]
        complexity_tests = [t for t in test_suite.tests if "complexity" in t.test_code]
        
        if len(functions_with_complexity) > len(complexity_tests):
            recommendations.append("Add complexity tests for functions with complexity thresholds")
        
        return recommendations