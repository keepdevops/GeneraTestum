"""
Data models for test runner functionality.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class TestResult:
    """Test execution result."""
    test_name: str
    status: str  # passed, failed, skipped, error
    duration: float
    error_message: Optional[str] = None
    coverage_percentage: Optional[float] = None


@dataclass
class TestSuiteResult:
    """Complete test suite execution result."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    coverage_percentage: Optional[float] = None
    test_results: List[TestResult] = None
    slow_tests: List[Tuple[str, float]] = None
