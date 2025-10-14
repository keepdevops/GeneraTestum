"""
Data models for API analysis.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class APIEndpoint:
    """Information about an API endpoint."""
    name: str
    path: str
    method: str
    handler: str  # Function/method name
    parameters: List[Tuple[str, str]]  # (name, type)
    return_type: Optional[str]
    decorators: List[str]
    framework: str
    dependencies: Set[str]
    line_number: int
    docstring: Optional[str]


@dataclass
class APIModuleInfo:
    """Information about an API module."""
    endpoints: List[APIEndpoint]
    framework: str
    imports: Dict[str, str]
    dependencies: Set[str]
    file_path: str
