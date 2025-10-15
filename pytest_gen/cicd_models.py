"""
CI/CD configuration models and data structures.
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
    """Project information for CI/CD configuration generation."""
    name: str
    description: str
    python_version: str = "3.9"
    java_version: str = "11"
    node_version: str = "16"
    test_framework: str = "pytest"
    has_java: bool = False
    has_javascript: bool = False
    has_docker: bool = False
    has_database: bool = False
    has_api: bool = False
    dependencies: List[str] = None
    test_directories: List[str] = None
    source_directories: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.test_directories is None:
            self.test_directories = ["tests"]
        if self.source_directories is None:
            self.source_directories = ["src"]


@dataclass
class CIConfigTemplate:
    """Template for CI/CD configuration generation."""
    name: str
    config_type: str
    template_content: str
    variables: List[str] = None
    requirements: List[str] = None
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = []
        if self.requirements is None:
            self.requirements = []