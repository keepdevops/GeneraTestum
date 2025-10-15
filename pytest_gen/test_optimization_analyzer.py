"""
Test optimization analysis and reporting utilities.
"""

from typing import Dict, List, Any
from .test_optimizer_models import TestPerformanceMetrics, OptimizationSuggestion, TestSuiteReport


class TestOptimizationAnalyzer:
    """Analyzes test performance and generates optimization reports."""
    
    @staticmethod
    def generate_optimization_report(metrics: List[TestPerformanceMetrics], 
                                   suggestions: List[OptimizationSuggestion]) -> TestSuiteReport:
        """Generate comprehensive optimization report."""
        total_tests = len(metrics)
        total_execution_time = sum(m.execution_time for m in metrics)
        average_execution_time = total_execution_time / total_tests if total_tests > 0 else 0
        
        # Find slowest tests
        slowest_tests = sorted(metrics, key=lambda x: x.execution_time, reverse=True)[:5]
        
        # Calculate parallelization potential
        parallelizable_tests = sum(1 for m in metrics if m.execution_time > 0.5)
        parallelization_potential = (parallelizable_tests / total_tests * 100) if total_tests > 0 else 0
        
        return TestSuiteReport(
            total_tests=total_tests,
            total_execution_time=total_execution_time,
            average_execution_time=average_execution_time,
            slowest_tests=slowest_tests,
            optimization_suggestions=suggestions,
            parallelization_potential=parallelization_potential
        )
    
    @staticmethod
    def analyze_optimization_potential(metrics: List[TestPerformanceMetrics]) -> Dict[str, Any]:
        """Analyze optimization potential for test suite."""
        if not metrics:
            return {"potential": 0, "recommendations": []}
        
        total_tests = len(metrics)
        slow_tests = [m for m in metrics if m.execution_time > 1.0]
        memory_intensive_tests = [m for m in metrics if m.memory_usage > 10.0]
        complex_tests = [m for m in metrics if m.complexity_score > 10]
        high_dependency_tests = [m for m in metrics if m.dependency_count > 5]
        
        optimization_score = 0
        recommendations = []
        
        # Parallelization potential
        parallelizable = len(slow_tests)
        if parallelizable > 0:
            optimization_score += 30
            recommendations.append(f"Parallelize {parallelizable} slow tests for ~50% speed improvement")
        
        # Memory optimization potential
        if memory_intensive_tests:
            optimization_score += 25
            recommendations.append(f"Optimize memory usage in {len(memory_intensive_tests)} tests")
        
        # Complexity reduction potential
        if complex_tests:
            optimization_score += 20
            recommendations.append(f"Simplify {len(complex_tests)} complex tests")
        
        # Mock optimization potential
        if high_dependency_tests:
            optimization_score += 25
            recommendations.append(f"Add mocking for {len(high_dependency_tests)} high-dependency tests")
        
        return {
            "optimization_score": min(optimization_score, 100),
            "potential_improvement": optimization_score,
            "recommendations": recommendations,
            "statistics": {
                "total_tests": total_tests,
                "slow_tests": len(slow_tests),
                "memory_intensive_tests": len(memory_intensive_tests),
                "complex_tests": len(complex_tests),
                "high_dependency_tests": len(high_dependency_tests)
            }
        }
    
    @staticmethod
    def generate_optimization_summary(metrics: List[TestPerformanceMetrics], 
                                     suggestions: List[OptimizationSuggestion]) -> str:
        """Generate human-readable optimization summary."""
        if not metrics:
            return "No test metrics available for optimization analysis."
        
        total_tests = len(metrics)
        total_time = sum(m.execution_time for m in metrics)
        avg_time = total_time / total_tests
        
        summary_lines = []
        summary_lines.append("=== TEST OPTIMIZATION SUMMARY ===")
        summary_lines.append("")
        summary_lines.append(f"Total Tests: {total_tests}")
        summary_lines.append(f"Total Execution Time: {total_time:.2f}s")
        summary_lines.append(f"Average Execution Time: {avg_time:.3f}s")
        summary_lines.append("")
        
        # Slowest tests
        slowest = sorted(metrics, key=lambda x: x.execution_time, reverse=True)[:3]
        summary_lines.append("Slowest Tests:")
        for i, test in enumerate(slowest, 1):
            summary_lines.append(f"  {i}. {test.test_name}: {test.execution_time:.3f}s")
        summary_lines.append("")
        
        # Optimization suggestions
        if suggestions:
            summary_lines.append("Optimization Suggestions:")
            for i, suggestion in enumerate(suggestions[:5], 1):
                summary_lines.append(f"  {i}. {suggestion.test_name}: {suggestion.description}")
                summary_lines.append(f"     Potential improvement: {suggestion.potential_improvement}%")
        else:
            summary_lines.append("No optimization suggestions generated.")
        
        return "\n".join(summary_lines)
    
    @staticmethod
    def calculate_optimization_impact(suggestions: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """Calculate the potential impact of optimization suggestions."""
        if not suggestions:
            return {"total_improvement": 0, "impact_by_type": {}}
        
        total_improvement = sum(s.potential_improvement for s in suggestions)
        
        # Group by suggestion type
        impact_by_type = {}
        for suggestion in suggestions:
            suggestion_type = suggestion.suggestion_type
            if suggestion_type not in impact_by_type:
                impact_by_type[suggestion_type] = {
                    "count": 0,
                    "total_improvement": 0,
                    "avg_improvement": 0
                }
            
            impact_by_type[suggestion_type]["count"] += 1
            impact_by_type[suggestion_type]["total_improvement"] += suggestion.potential_improvement
        
        # Calculate averages
        for suggestion_type in impact_by_type:
            count = impact_by_type[suggestion_type]["count"]
            total = impact_by_type[suggestion_type]["total_improvement"]
            impact_by_type[suggestion_type]["avg_improvement"] = total / count if count > 0 else 0
        
        return {
            "total_improvement": total_improvement,
            "avg_improvement": total_improvement / len(suggestions) if suggestions else 0,
            "impact_by_type": impact_by_type,
            "total_suggestions": len(suggestions)
        }
    
    @staticmethod
    def export_optimization_data(metrics: List[TestPerformanceMetrics], 
                               suggestions: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """Export optimization data in structured format."""
        return {
            "metrics_summary": {
                "total_tests": len(metrics),
                "total_execution_time": sum(m.execution_time for m in metrics),
                "average_execution_time": sum(m.execution_time for m in metrics) / len(metrics) if metrics else 0,
                "total_memory_usage": sum(m.memory_usage for m in metrics),
                "average_complexity": sum(m.complexity_score for m in metrics) / len(metrics) if metrics else 0
            },
            "optimization_analysis": TestOptimizationAnalyzer.analyze_optimization_potential(metrics),
            "suggestions": [
                {
                    "test_name": s.test_name,
                    "suggestion_type": s.suggestion_type,
                    "description": s.description,
                    "potential_improvement": s.potential_improvement,
                    "implementation": s.implementation
                }
                for s in suggestions
            ],
            "impact_analysis": TestOptimizationAnalyzer.calculate_optimization_impact(suggestions)
        }