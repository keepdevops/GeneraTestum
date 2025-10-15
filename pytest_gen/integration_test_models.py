"""
Integration testing models and data structures.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set, Tuple


@dataclass
class APIRelationship:
    """Represents a relationship between API endpoints."""
    source_endpoint: str
    target_endpoint: str
    relationship_type: str  # 'dependency', 'sequence', 'data_flow'
    data_flow: Optional[Dict[str, str]] = None  # field mappings
    conditions: List[str] = None


@dataclass
class IntegrationTest:
    """Generated integration test."""
    test_name: str
    test_description: str
    test_code: str
    endpoints: List[str]
    test_type: str  # 'workflow', 'data_flow', 'dependency'


@dataclass
class APIEndpoint:
    """Represents an API endpoint."""
    method: str  # GET, POST, PUT, DELETE, etc.
    path: str
    parameters: List[str]
    response_fields: List[str]
    dependencies: List[str]


@dataclass
class WorkflowStep:
    """Represents a step in an integration workflow."""
    step_number: int
    endpoint: APIEndpoint
    expected_status: int
    data_extraction: Dict[str, str]  # field mappings for data flow
    assertions: List[str]


@dataclass
class IntegrationTestSuite:
    """Complete integration test suite."""
    tests: List[IntegrationTest]
    total_tests: int
    endpoints_covered: List[str]
    test_file_content: str
    coverage_percentage: float


@dataclass
class APIAnalysisResult:
    """Result of API analysis."""
    endpoints: List[APIEndpoint]
    relationships: List[APIRelationship]
    workflows: List[List[WorkflowStep]]
    coverage_analysis: Dict[str, float]
