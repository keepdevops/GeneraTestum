"""
Data models for smart mock generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set


@dataclass
class DependencyInfo:
    """Information about a code dependency."""
    name: str
    type: str  # 'api', 'database', 'file', 'service', 'library'
    url: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    methods: List[str] = None


@dataclass
class MockConfig:
    """Configuration for mock generation."""
    mock_type: str  # 'simple', 'realistic', 'intelligent'
    include_responses: bool = True
    include_error_cases: bool = True
    data_source: Optional[str] = None  # 'api', 'file', 'generated'
