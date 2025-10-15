"""
Test optimizer - refactored for 200LOC limit.
"""

from typing import Dict, List, Any
from .test_optimizer_models import TestPerformanceMetrics, OptimizationSuggestion, TestSuiteReport, OptimizationResult
from .test_optimization_templates import TestOptimizationTemplates
from .test_optimization_analyzer import TestOptimizationAnalyzer


class TestOptimizer:
    """Generates optimized test code based on performance analysis."""

    def __init__(self):
        self.templates = TestOptimizationTemplates()
        self.analyzer = TestOptimizationAnalyzer()
        self.optimization_templates = {
            'parallelize': self.templates.generate_parallel_test_template,
            'mock_optimization': self.templates.generate_mock_optimization_template,
            'fixture_optimization': self.templates.generate_fixture_optimization_template,
            'assertion_optimization': self.templates.generate_assertion_optimization_template
        }

    def generate_optimized_tests(self, metrics: List[TestPerformanceMetrics], 
                               suggestions: List[OptimizationSuggestion]) -> Dict[str, str]:
        """Generate optimized test code for suggestions."""
        optimized_tests = {}
        
        for suggestion in suggestions:
            template_func = self.optimization_templates.get(suggestion.suggestion_type)
            if template_func:
                optimized_code = template_func(suggestion, metrics)
                optimized_tests[suggestion.test_name] = optimized_code
        
        return optimized_tests

    def generate_optimization_report(self, metrics: List[TestPerformanceMetrics], 
                                   suggestions: List[OptimizationSuggestion]) -> TestSuiteReport:
        """Generate comprehensive optimization report."""
        return self.analyzer.generate_optimization_report(metrics, suggestions)

    def analyze_optimization_potential(self, metrics: List[TestPerformanceMetrics]) -> Dict[str, Any]:
        """Analyze optimization potential for test suite."""
        return self.analyzer.analyze_optimization_potential(metrics)

    def generate_optimization_summary(self, metrics: List[TestPerformanceMetrics], 
                                     suggestions: List[OptimizationSuggestion]) -> str:
        """Generate human-readable optimization summary."""
        return self.analyzer.generate_optimization_summary(metrics, suggestions)

    def calculate_optimization_impact(self, suggestions: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """Calculate the potential impact of optimization suggestions."""
        return self.analyzer.calculate_optimization_impact(suggestions)

    def export_optimization_data(self, metrics: List[TestPerformanceMetrics], 
                               suggestions: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """Export optimization data in structured format."""
        return self.analyzer.export_optimization_data(metrics, suggestions)

    def generate_optimized_test_config(self, metrics: List[TestPerformanceMetrics]) -> str:
        """Generate optimized pytest configuration."""
        config_lines = []
        config_lines.append("[tool:pytest]")
        config_lines.append("testpaths = .")
        config_lines.append("python_files = test_*.py")
        config_lines.append("python_classes = Test*")
        config_lines.append("python_functions = test_*")
        config_lines.append("addopts = -v --tb=short --strict-markers")
        config_lines.append("")
        config_lines.append("# Optimization settings")
        
        # Add parallel execution if there are slow tests
        slow_tests = [m for m in metrics if m.execution_time > 1.0]
        if slow_tests:
            config_lines.append("addopts = -v --tb=short --strict-markers -n auto")
            config_lines.append("# Use pytest-xdist for parallel execution")
        
        config_lines.append("")
        config_lines.append("markers =")
        config_lines.append("    slow: marks tests as slow running")
        config_lines.append("    fast: marks tests as fast running")
        config_lines.append("    memory: marks tests as memory intensive")
        config_lines.append("    parallel: marks tests for parallel execution")
        
        return "\n".join(config_lines)

    def get_optimization_priorities(self, suggestions: List[OptimizationSuggestion]) -> List[OptimizationSuggestion]:
        """Get suggestions sorted by priority."""
        def get_priority(suggestion):
            if suggestion.suggestion_type == 'parallelize' and suggestion.potential_improvement > 40:
                return 1
            elif suggestion.suggestion_type == 'mock_optimization' and suggestion.potential_improvement > 30:
                return 2
            elif suggestion.suggestion_type == 'fixture_optimization':
                return 3
            else:
                return 4
        
        return sorted(suggestions, key=get_priority)

    def generate_optimization_plan(self, metrics: List[TestPerformanceMetrics], 
                                 suggestions: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """Generate a comprehensive optimization plan."""
        prioritized_suggestions = self.get_optimization_priorities(suggestions)
        impact_analysis = self.calculate_optimization_impact(suggestions)
        potential_analysis = self.analyze_optimization_potential(metrics)
        
        return {
            "executive_summary": {
                "total_tests": len(metrics),
                "optimization_score": potential_analysis.get("optimization_score", 0),
                "potential_improvement": impact_analysis.get("total_improvement", 0),
                "priority_suggestions": len([s for s in prioritized_suggestions if self._get_priority(s) <= 2])
            },
            "optimization_phases": [
                {
                    "phase": 1,
                    "name": "High Impact Optimizations",
                    "suggestions": [s for s in prioritized_suggestions if self._get_priority(s) == 1],
                    "estimated_improvement": sum(s.potential_improvement for s in prioritized_suggestions if self._get_priority(s) == 1)
                },
                {
                    "phase": 2,
                    "name": "Medium Impact Optimizations", 
                    "suggestions": [s for s in prioritized_suggestions if self._get_priority(s) == 2],
                    "estimated_improvement": sum(s.potential_improvement for s in prioritized_suggestions if self._get_priority(s) == 2)
                },
                {
                    "phase": 3,
                    "name": "Low Impact Optimizations",
                    "suggestions": [s for s in prioritized_suggestions if self._get_priority(s) >= 3],
                    "estimated_improvement": sum(s.potential_improvement for s in prioritized_suggestions if self._get_priority(s) >= 3)
                }
            ],
            "implementation_guidance": {
                "parallelization": "Use pytest-xdist for parallel test execution",
                "mocking": "Implement targeted mocking to reduce dependencies",
                "fixtures": "Optimize fixture scopes and reduce setup overhead",
                "assertions": "Use specific assertions and parametrized tests"
            }
        }
    
    def _get_priority(self, suggestion: OptimizationSuggestion) -> int:
        """Get priority level for a suggestion."""
        if suggestion.suggestion_type == 'parallelize' and suggestion.potential_improvement > 40:
            return 1
        elif suggestion.suggestion_type == 'mock_optimization' and suggestion.potential_improvement > 30:
            return 2
        elif suggestion.suggestion_type == 'fixture_optimization':
            return 3
        else:
            return 4