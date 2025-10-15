"""
Security testing models and data structures.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set, Tuple


@dataclass
class SecurityVulnerability:
    """Represents a potential security vulnerability."""
    vulnerability_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    affected_function: str
    line_number: int
    mitigation: str


@dataclass
class SecurityTest:
    """Generated security test."""
    test_name: str
    test_description: str
    test_code: str
    vulnerability_type: str
    severity: str


@dataclass
class SecurityPattern:
    """Security vulnerability pattern definition."""
    patterns: List[str]
    severity: str
    description: str
    mitigation: str = ""
    test_template: str = ""


@dataclass
class SecurityAnalysisResult:
    """Result of security analysis."""
    vulnerabilities: List[SecurityVulnerability]
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    analysis_summary: str


@dataclass
class SecurityTestSuite:
    """Complete security test suite."""
    tests: List[SecurityTest]
    total_tests: int
    coverage: Dict[str, int]  # vulnerability_type -> test_count
    test_file_content: str
