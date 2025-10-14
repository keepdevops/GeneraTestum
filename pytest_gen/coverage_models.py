"""
Data models for coverage analysis functionality.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class CoverageGap:
    """Represents a coverage gap in the code."""
    file_path: str
    line_number: int
    code_line: str
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    test_suggestion: Optional[str] = None


@dataclass
class CoverageReport:
    """Comprehensive coverage analysis report."""
    total_coverage: float
    file_coverage: Dict[str, float]
    gaps: List[CoverageGap]
    recommendations: List[str]
    critical_paths: List[str]
