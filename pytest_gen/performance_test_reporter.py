"""
Performance test reporting and analysis utilities.
"""

from typing import Dict, List, Any
from .performance_test_models import PerformanceTestSuite


class PerformanceTestReporter:
    """Generates reports and analysis for performance tests."""
    
    @staticmethod
    def generate_performance_report(test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Generate performance test report."""
        return {
            "total_tests": test_suite.total_tests,
            "coverage_percentage": test_suite.coverage_percentage,
            "functions_tested": len(test_suite.requirements),
            "test_types": {
                "execution_time": len([t for t in test_suite.tests if "execution_time" in t.test_code]),
                "memory_usage": len([t for t in test_suite.tests if "memory_usage" in t.test_code]),
                "complexity": len([t for t in test_suite.tests if "complexity" in t.test_code]),
                "benchmark": len([t for t in test_suite.tests if "benchmark" in t.test_code])
            },
            "requirements": [
                {
                    "function_name": req.function_name,
                    "max_execution_time": req.max_execution_time,
                    "memory_limit": req.memory_limit,
                    "complexity_threshold": req.complexity_threshold
                }
                for req in test_suite.requirements
            ]
        }
    
    @staticmethod
    def generate_summary_report(test_suite: PerformanceTestSuite) -> str:
        """Generate a human-readable summary report."""
        report_lines = []
        report_lines.append("=== PERFORMANCE TEST GENERATION REPORT ===")
        report_lines.append("")
        
        # Summary statistics
        report_lines.append("SUMMARY:")
        report_lines.append(f"  Total Tests Generated: {test_suite.total_tests}")
        report_lines.append(f"  Functions Tested: {len(test_suite.requirements)}")
        report_lines.append(f"  Coverage: {test_suite.coverage_percentage:.1f}%")
        report_lines.append("")
        
        # Test type breakdown
        test_types = {
            "execution_time": len([t for t in test_suite.tests if "execution_time" in t.test_code]),
            "memory_usage": len([t for t in test_suite.tests if "memory_usage" in t.test_code]),
            "complexity": len([t for t in test_suite.tests if "complexity" in t.test_code]),
            "benchmark": len([t for t in test_suite.tests if "benchmark" in t.test_code])
        }
        
        report_lines.append("TEST TYPES GENERATED:")
        for test_type, count in test_types.items():
            report_lines.append(f"  {test_type.replace('_', ' ').title()}: {count}")
        report_lines.append("")
        
        # Requirements details
        report_lines.append("REQUIREMENTS COVERED:")
        for req in test_suite.requirements:
            report_lines.append(f"  • {req.function_name}")
            report_lines.append(f"    - Max execution time: {req.max_execution_time}s")
            if req.memory_limit:
                report_lines.append(f"    - Memory limit: {req.memory_limit}MB")
            if req.complexity_threshold:
                report_lines.append(f"    - Complexity: {req.complexity_threshold}")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS:")
        if test_suite.total_tests == 0:
            report_lines.append("  • No performance requirements found")
        else:
            report_lines.append("  • Run tests with: pytest test_performance_*.py -v")
            report_lines.append("  • Monitor execution times during CI/CD")
            report_lines.append("  • Set up performance regression alerts")
            report_lines.append("  • Consider adding load testing for critical functions")
        
        return "\n".join(report_lines)
    
    @staticmethod
    def analyze_test_coverage(test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Analyze test coverage and identify gaps."""
        total_requirements = len(test_suite.requirements)
        covered_requirements = len(set(test.function_name for test in test_suite.tests))
        
        coverage_percentage = (covered_requirements / total_requirements * 100) if total_requirements > 0 else 0
        
        # Identify uncovered functions
        all_functions = set(req.function_name for req in test_suite.requirements)
        covered_functions = set(test.function_name for test in test_suite.tests)
        uncovered_functions = all_functions - covered_functions
        
        return {
            "total_requirements": total_requirements,
            "covered_requirements": covered_requirements,
            "coverage_percentage": coverage_percentage,
            "uncovered_functions": list(uncovered_functions),
            "coverage_gaps": len(uncovered_functions)
        }
    
    @staticmethod
    def generate_performance_metrics(test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Generate performance metrics from test suite."""
        metrics = {
            "test_generation_stats": {
                "total_tests": test_suite.total_tests,
                "avg_tests_per_function": test_suite.total_tests / len(test_suite.requirements) if test_suite.requirements else 0,
                "test_types_count": {
                    "execution_time": len([t for t in test_suite.tests if "execution_time" in t.test_code]),
                    "memory_usage": len([t for t in test_suite.tests if "memory_usage" in t.test_code]),
                    "complexity": len([t for t in test_suite.tests if "complexity" in t.test_code]),
                    "benchmark": len([t for t in test_suite.tests if "benchmark" in t.test_code])
                }
            },
            "requirement_stats": {
                "total_functions": len(test_suite.requirements),
                "functions_with_memory_limits": len([r for r in test_suite.requirements if r.memory_limit]),
                "functions_with_complexity_thresholds": len([r for r in test_suite.requirements if r.complexity_threshold]),
                "avg_execution_time_limit": sum(r.max_execution_time for r in test_suite.requirements) / len(test_suite.requirements) if test_suite.requirements else 0
            }
        }
        
        return metrics
    
    @staticmethod
    def export_to_json(test_suite: PerformanceTestSuite) -> Dict[str, Any]:
        """Export test suite to JSON format."""
        return {
            "test_suite": {
                "total_tests": test_suite.total_tests,
                "coverage_percentage": test_suite.coverage_percentage,
                "requirements": [
                    {
                        "function_name": req.function_name,
                        "max_execution_time": req.max_execution_time,
                        "memory_limit": req.memory_limit,
                        "complexity_threshold": req.complexity_threshold
                    }
                    for req in test_suite.requirements
                ],
                "tests": [
                    {
                        "function_name": test.function_name,
                        "test_code": test.test_code,
                        "benchmarks": test.benchmarks,
                        "assertions": test.assertions
                    }
                    for test in test_suite.tests
                ]
            },
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",  # Would be actual timestamp
                "generator_version": "1.0.0",
                "test_framework": "pytest"
            }
        }
