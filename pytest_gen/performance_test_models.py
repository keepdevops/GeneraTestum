"""
Performance testing data models.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class PerformanceRequirement:
    """Performance requirement for a function."""
    function_name: str
    max_execution_time: float  # in seconds
    min_execution_time: Optional[float] = None
    memory_limit: Optional[int] = None  # in MB
    complexity_threshold: Optional[str] = None  # O(1), O(n), O(n²), etc.


@dataclass
class PerformanceTest:
    """Generated performance test."""
    function_name: str
    test_code: str
    benchmarks: List[str]
    assertions: List[str]


@dataclass
class PerformanceAnalysis:
    """Performance analysis result."""
    function_name: str
    performance_score: float
    complexity_level: str
    critical_operations: List[str]
    estimated_complexity: str
    recommendations: List[str]


@dataclass
class PerformanceTestSuite:
    """Complete performance test suite."""
    tests: List[PerformanceTest]
    requirements: List[PerformanceRequirement]
    total_tests: int
    coverage_percentage: float
    test_file_content: str
