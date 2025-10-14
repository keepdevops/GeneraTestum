"""
Data models for template management.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class TestTemplate:
    """Information about a test template."""
    name: str
    content: str
    variables: Dict[str, Any]
