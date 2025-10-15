"""
Data models for CI/CD pipeline generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class CIConfig:
    """Generated CI/CD configuration."""
    name: str
    content: str
    file_path: str
    config_type: str  # 'github_actions', 'jenkins', 'gitlab_ci', 'azure_devops'


@dataclass
class ProjectInfo:
    """Project information for CI/CD configuration."""
    name: str
    python_version: str
    java_version: str
    node_version: str
    has_java: bool
    has_python: bool
    has_node: bool
    has_docker: bool
    has_database: bool
