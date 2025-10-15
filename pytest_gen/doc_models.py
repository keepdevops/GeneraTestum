"""
Data models for documentation generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class TestDocumentation:
    """Generated test documentation."""
    title: str
    content: str
    file_path: str
    doc_type: str  # 'readme', 'api_docs', 'test_guide', 'coverage_report'


@dataclass
class ProjectInfo:
    """Project information for documentation generation."""
    name: str
    description: str
    version: str
    repository_url: str
    wiki_url: str
    issues_url: str
    discussions_url: str
    license: str
    dashboard_url: str
    coverage_percentage: int
    test_count: int
    pass_rate: int
    avg_duration: str
    fastest_test: str
    fastest_time: str
    slowest_test: str
    slowest_time: str
    total_duration: str
