"""
Test optimizer models and data structures.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set, Tuple


@dataclass
class TestPerformanceMetrics:
    """Test performance metrics."""
    test_name: str
    execution_time: float
    memory_usage: float
    complexity_score: int
    dependency_count: int
    mock_count: int
    assertion_count: int


@dataclass
class OptimizationSuggestion:
    """Test optimization suggestion."""
    test_name: str
    suggestion_type: str  # 'parallelize', 'mock_optimization', 'fixture_optimization', 'assertion_optimization'
    description: str
    potential_improvement: float  # percentage improvement
    implementation: str


@dataclass
class TestSuiteReport:
    """Test suite performance report."""
    total_tests: int
    total_execution_time: float
    average_execution_time: float
    slowest_tests: List[TestPerformanceMetrics]
    optimization_suggestions: List[OptimizationSuggestion]
    parallelization_potential: float


@dataclass
class PerformanceThresholds:
    """Performance thresholds for optimization."""
    slow_test_threshold: float = 1.0  # seconds
    memory_threshold: float = 100.0  # MB
    complexity_threshold: int = 10
    dependency_threshold: int = 5
    mock_threshold: int = 3


@dataclass
class OptimizationResult:
    """Result of test optimization analysis."""
    metrics: List[TestPerformanceMetrics]
    suggestions: List[OptimizationSuggestion]
    report: TestSuiteReport
    improvement_potential: float
    critical_tests: List[str]
