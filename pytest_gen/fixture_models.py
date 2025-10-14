"""
Data models for pytest fixtures.
"""

from typing import List, Optional, Any
from dataclasses import dataclass


@dataclass
class FixtureInfo:
    """Information about a pytest fixture."""
    name: str
    scope: str  # function, class, module, session
    autouse: bool
    params: Optional[List[Any]] = None
    setup_code: List[str] = None
    teardown_code: List[str] = None
    dependencies: List[str] = None
    return_type: Optional[str] = None
