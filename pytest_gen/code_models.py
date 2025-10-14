"""
Data models for Python code analysis.
"""

import ast
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    """Information about a Python function."""
    name: str
    parameters: List[Tuple[str, Any]]
    return_annotation: Optional[str]
    docstring: Optional[str]
    is_async: bool
    is_method: bool
    is_classmethod: bool
    is_staticmethod: bool
    decorators: List[str]
    dependencies: Set[str]
    line_number: int


@dataclass
class ClassInfo:
    """Information about a Python class."""
    name: str
    methods: List[FunctionInfo]
    properties: List[str]
    inheritance: List[str]
    docstring: Optional[str]
    decorators: List[str]
    dependencies: Set[str]
    line_number: int


@dataclass
class ModuleInfo:
    """Information about a Python module."""
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: Dict[str, str]  # name -> module
    dependencies: Set[str]
    file_path: str
