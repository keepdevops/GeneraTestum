"""
Documentation generation models and data structures.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


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
    version: str = "1.0.0"
    author: str = "Test Generator"
    email: str = "test@example.com"
    license: str = "MIT"
    repository: str = ""
    homepage: str = ""
    keywords: List[str] = None
    classifiers: List[str] = None
    install_requires: List[str] = None
    extras_require: Dict[str, List[str]] = None
    python_requires: str = ">=3.8"
    packages: List[str] = None
    package_dir: Dict[str, str] = None
    package_data: Dict[str, List[str]] = None
    include_package_data: bool = True
    zip_safe: bool = False
    entry_points: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = ["testing", "pytest", "automation"]
        if self.classifiers is None:
            self.classifiers = [
                "Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11",
            ]
        if self.install_requires is None:
            self.install_requires = ["pytest", "pytest-cov"]
        if self.extras_require is None:
            self.extras_require = {
                "dev": ["black", "flake8", "mypy"],
                "docs": ["sphinx", "sphinx-rtd-theme"],
            }
        if self.packages is None:
            self.packages = []
        if self.package_dir is None:
            self.package_dir = {}
        if self.package_data is None:
            self.package_data = {}
        if self.entry_points is None:
            self.entry_points = {}


@dataclass
class APIInfo:
    """API information for documentation generation."""
    name: str
    description: str
    version: str = "1.0.0"
    base_url: str = ""
    endpoints: List[Dict[str, Any]] = None
    authentication: Dict[str, Any] = None
    rate_limiting: Dict[str, Any] = None
    error_codes: Dict[int, str] = None
    examples: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.endpoints is None:
            self.endpoints = []
        if self.authentication is None:
            self.authentication = {}
        if self.rate_limiting is None:
            self.rate_limiting = {}
        if self.error_codes is None:
            self.error_codes = {}
        if self.examples is None:
            self.examples = []


@dataclass
class TestInfo:
    """Test information for documentation generation."""
    framework: str = "pytest"
    test_directories: List[str] = None
    test_files: List[str] = None
    test_functions: List[str] = None
    fixtures: List[str] = None
    coverage_threshold: float = 80.0
    performance_threshold: float = 1.0
    
    def __post_init__(self):
        if self.test_directories is None:
            self.test_directories = ["tests"]
        if self.test_files is None:
            self.test_files = []
        if self.test_functions is None:
            self.test_functions = []
        if self.fixtures is None:
            self.fixtures = []


@dataclass
class CoverageInfo:
    """Coverage information for documentation generation."""
    total_coverage: float = 0.0
    lines_covered: int = 0
    lines_total: int = 0
    branches_covered: int = 0
    branches_total: int = 0
    functions_covered: int = 0
    functions_total: int = 0
    classes_covered: int = 0
    classes_total: int = 0
    missing_lines: List[int] = None
    uncovered_functions: List[str] = None
    uncovered_classes: List[str] = None
    
    def __post_init__(self):
        if self.missing_lines is None:
            self.missing_lines = []
        if self.uncovered_functions is None:
            self.uncovered_functions = []
        if self.uncovered_classes is None:
            self.uncovered_classes = []