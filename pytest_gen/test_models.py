"""
Data models for test generation.
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from .mock_generator import MockInfo
from .fixture_generator import FixtureInfo
from .parametrize_generator import ParametrizeInfo


@dataclass
class GeneratedTest:
    """A generated test with all components."""
    name: str
    content: str
    imports: Set[str]
    fixtures: List[FixtureInfo]
    mocks: List[MockInfo]
    parametrize: List[ParametrizeInfo]
    file_path: str
    line_count: int


@dataclass
class TestFile:
    """A complete test file with multiple tests."""
    file_path: str
    tests: List[GeneratedTest]
    imports: Set[str]
    fixtures: List[FixtureInfo]
    content: str
    line_count: int
