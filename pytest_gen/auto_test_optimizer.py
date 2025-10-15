"""
Main automatic test optimizer.
"""

import os
from typing import Dict, List, Any
from .test_optimizer_models import TestPerformanceMetrics, OptimizationSuggestion, TestSuiteReport, PerformanceThresholds, OptimizationResult
from .test_performance_analyzer import TestPerformanceAnalyzer
from .test_optimizer import TestOptimizer


class AutoTestOptimizer:
    """Main class for automatic test optimization."""

    def __init__(self):
        self.analyzer = TestPerformanceAnalyzer()
        self.optimizer = TestOptimizer()
        self.thresholds = PerformanceThresholds()

    def analyze_test_directory(self, directory: str) -> List[TestPerformanceMetrics]:
        """Analyze test directory for performance metrics."""
        return self.analyzer.analyze_test_directory(directory)

    def generate_optimization_suggestions(self, metrics: List[TestPerformanceMetrics]) -> List[OptimizationSuggestion]:
        """Generate optimization suggestions based on metrics."""
        return self.analyzer.identify_optimization_opportunities(metrics, self.thresholds)

    def generate_optimized_tests(self, metrics: List[TestPerformanceMetrics], 
                               suggestions: List[OptimizationSuggestion]) -> Dict[str, str]:
        """Generate optimized test code."""
        return self.optimizer.generate_optimized_tests(metrics, suggestions)

    def generate_optimization_report(self, metrics: List[TestPerformanceMetrics], 
                                   suggestions: List[OptimizationSuggestion]) -> TestSuiteReport:
        """Generate optimization report."""
        return self.optimizer.generate_optimization_report(metrics, suggestions)

    def save_optimized_tests(self, optimized_tests: Dict[str, str], output_dir: str = "optimized_tests"):
        """Save optimized tests to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        for test_name, test_code in optimized_tests.items():
            file_path = os.path.join(output_dir, f"{test_name}.py")
            with open(file_path, 'w') as f:
                f.write(test_code)
            print(f"Generated optimized test: {file_path}")

    def run_complete_optimization(self, test_directory: str, output_dir: str = "optimized_tests") -> OptimizationResult:
        """Run complete test optimization analysis."""
        # Analyze performance
        metrics = self.analyze_test_directory(test_directory)
        
        if not metrics:
            return OptimizationResult(
                metrics=[],
                suggestions=[],
                report=TestSuiteReport(
                    total_tests=0,
                    total_execution_time=0.0,
                    average_execution_time=0.0,
                    slowest_tests=[],
                    optimization_suggestions=[],
                    parallelization_potential=0.0
                ),
                improvement_potential=0.0,
                critical_tests=[]
            )
        
        # Generate suggestions
        suggestions = self.generate_optimization_suggestions(metrics)
        
        # Generate optimized tests
        optimized_tests = self.generate_optimized_tests(metrics, suggestions)
        
        # Save optimized tests
        self.save_optimized_tests(optimized_tests, output_dir)
        
        # Generate report
        report = self.generate_optimization_report(metrics, suggestions)
        
        # Calculate improvement potential
        improvement_potential = sum(s.potential_improvement for s in suggestions) / len(suggestions) if suggestions else 0.0
        
        # Identify critical tests
        critical_tests = [m.test_name for m in metrics if m.execution_time > self.thresholds.slow_test_threshold * 2]
        
        return OptimizationResult(
            metrics=metrics,
            suggestions=suggestions,
            report=report,
            improvement_potential=improvement_potential,
            critical_tests=critical_tests
        )

    def generate_optimization_summary(self, result: OptimizationResult) -> str:
        """Generate optimization summary report."""
        report = result.report
        
        summary_lines = []
        summary_lines.append("=" * 60)
        summary_lines.append("⚡ AUTOMATIC TEST OPTIMIZATION REPORT")
        summary_lines.append("=" * 60)
        
        summary_lines.append(f"\n📊 TEST SUITE ANALYSIS:")
        summary_lines.append(f"  • Total Tests: {report.total_tests}")
        summary_lines.append(f"  • Total Execution Time: {report.total_execution_time:.2f}s")
        summary_lines.append(f"  • Average Execution Time: {report.average_execution_time:.3f}s")
        summary_lines.append(f"  • Parallelization Potential: {report.parallelization_potential:.1f}%")
        
        summary_lines.append(f"\n🚨 CRITICAL TESTS ({len(result.critical_tests)}):")
        for test_name in result.critical_tests:
            summary_lines.append(f"  • {test_name}")
        
        summary_lines.append(f"\n🐌 SLOWEST TESTS:")
        for metric in report.slowest_tests[:5]:
            summary_lines.append(f"  • {metric.test_name}: {metric.execution_time:.3f}s")
        
        summary_lines.append(f"\n💡 OPTIMIZATION SUGGESTIONS ({len(result.suggestions)}):")
        suggestion_types = {}
        for suggestion in result.suggestions:
            suggestion_types[suggestion.suggestion_type] = suggestion_types.get(suggestion.suggestion_type, 0) + 1
        
        for suggestion_type, count in suggestion_types.items():
            summary_lines.append(f"  • {suggestion_type}: {count} suggestions")
        
        summary_lines.append(f"\n🎯 IMPROVEMENT POTENTIAL:")
        summary_lines.append(f"  • Overall Improvement: {result.improvement_potential:.1f}%")
        summary_lines.append(f"  • Estimated Time Savings: {report.total_execution_time * result.improvement_potential / 100:.2f}s")
        
        summary_lines.append(f"\n🔧 RECOMMENDED ACTIONS:")
        summary_lines.append(f"  1. Implement parallel test execution with pytest-xdist")
        summary_lines.append(f"  2. Optimize mock usage for memory-intensive tests")
        summary_lines.append(f"  3. Break down complex tests into smaller units")
        summary_lines.append(f"  4. Use session-scoped fixtures for expensive setup")
        summary_lines.append(f"  5. Implement test data factories for better reusability")
        
        summary_lines.append(f"\n📁 GENERATED FILES:")
        summary_lines.append(f"  • Optimized tests saved to: optimized_tests/")
        summary_lines.append(f"  • Total optimized tests: {len(result.suggestions)}")
        
        return "\n".join(summary_lines)