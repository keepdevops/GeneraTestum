"""
Test performance analyzer - refactored for 200LOC limit.
"""

import ast
import os
from typing import Dict, List, Any, Optional
from .test_optimizer_models import TestPerformanceMetrics, OptimizationSuggestion, PerformanceThresholds
from .test_performance_patterns import TestPerformancePatterns
from .test_metrics_calculator import TestMetricsCalculator
from .test_optimization_analyzer import TestOptimizationAnalyzer


class TestPerformanceAnalyzer:
    """Analyzes test performance and identifies optimization opportunities."""

    def __init__(self):
        self.patterns = TestPerformancePatterns()
        self.calculator = TestMetricsCalculator(self.patterns)
        self.optimizer = TestOptimizationAnalyzer()

    def analyze_test_file(self, file_path: str) -> List[TestPerformanceMetrics]:
        """Analyze a test file for performance metrics."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception:
            return []
        
        # Parse the code
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []
        
        metrics = []
        
        # Find test functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                metric = self.calculator.analyze_test_function(node, source_code, file_path)
                if metric:
                    metrics.append(metric)
        
        return metrics

    def analyze_test_directory(self, directory: str) -> List[TestPerformanceMetrics]:
        """Analyze all test files in a directory."""
        all_metrics = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    metrics = self.analyze_test_file(file_path)
                    all_metrics.extend(metrics)
        
        return all_metrics

    def identify_optimization_opportunities(self, metrics: List[TestPerformanceMetrics], 
                                          thresholds: PerformanceThresholds = None) -> List[OptimizationSuggestion]:
        """Identify optimization opportunities based on metrics."""
        return self.optimizer.identify_optimization_opportunities(metrics, thresholds)

    def analyze_performance_trends(self, metrics: List[TestPerformanceMetrics]) -> dict:
        """Analyze performance trends across tests."""
        return self.optimizer.analyze_performance_trends(metrics)

    def generate_optimization_report(self, metrics: List[TestPerformanceMetrics]) -> str:
        """Generate a comprehensive optimization report."""
        return self.optimizer.generate_optimization_report(metrics)

    def get_performance_summary(self, metrics: List[TestPerformanceMetrics]) -> Dict[str, Any]:
        """Get a summary of performance metrics."""
        if not metrics:
            return {
                'total_tests': 0,
                'average_execution_time': 0.0,
                'average_memory_usage': 0.0,
                'average_complexity': 0,
                'optimization_opportunities': 0
            }
        
        total_tests = len(metrics)
        avg_execution_time = sum(m.execution_time for m in metrics) / total_tests
        avg_memory_usage = sum(m.memory_usage for m in metrics) / total_tests
        avg_complexity = sum(m.complexity_score for m in metrics) / total_tests
        
        # Count optimization opportunities
        suggestions = self.identify_optimization_opportunities(metrics)
        
        return {
            'total_tests': total_tests,
            'average_execution_time': round(avg_execution_time, 3),
            'average_memory_usage': round(avg_memory_usage, 2),
            'average_complexity': round(avg_complexity, 1),
            'optimization_opportunities': len(suggestions),
            'slowest_test': max(metrics, key=lambda m: m.execution_time).test_name,
            'most_memory_intensive': max(metrics, key=lambda m: m.memory_usage).test_name,
            'most_complex': max(metrics, key=lambda m: m.complexity_score).test_name
        }

    def find_slowest_tests(self, metrics: List[TestPerformanceMetrics], limit: int = 10) -> List[TestPerformanceMetrics]:
        """Find the slowest tests."""
        return sorted(metrics, key=lambda m: m.execution_time, reverse=True)[:limit]

    def find_most_memory_intensive_tests(self, metrics: List[TestPerformanceMetrics], limit: int = 10) -> List[TestPerformanceMetrics]:
        """Find the most memory intensive tests."""
        return sorted(metrics, key=lambda m: m.memory_usage, reverse=True)[:limit]

    def find_most_complex_tests(self, metrics: List[TestPerformanceMetrics], limit: int = 10) -> List[TestPerformanceMetrics]:
        """Find the most complex tests."""
        return sorted(metrics, key=lambda m: m.complexity_score, reverse=True)[:limit]

    def export_metrics_to_dict(self, metrics: List[TestPerformanceMetrics]) -> List[Dict[str, Any]]:
        """Export metrics to dictionary format."""
        return [
            {
                'test_name': m.test_name,
                'execution_time': m.execution_time,
                'memory_usage': m.memory_usage,
                'complexity_score': m.complexity_score,
                'dependency_count': m.dependency_count,
                'mock_count': m.mock_count,
                'assertion_count': m.assertion_count
            }
            for m in metrics
        ]