"""
Data models for Java code analysis.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class JavaMethod:
    """Information about a Java method."""
    name: str
    parameters: List[Tuple[str, str]]  # (name, type)
    return_type: str
    access_modifier: str  # public, private, protected
    annotations: List[str]
    docstring: Optional[str]
    line_number: int
    is_static: bool = False
    is_abstract: bool = False


@dataclass
class JavaClass:
    """Information about a Java class."""
    name: str
    package: str
    imports: List[str]
    methods: List[JavaMethod]
    fields: List[Tuple[str, str]]  # (name, type)
    annotations: List[str]
    superclass: Optional[str]
    interfaces: List[str]
    access_modifier: str
    docstring: Optional[str]
    line_number: int
    is_abstract: bool = False
    is_final: bool = False


@dataclass
class JavaAnnotation:
    """Information about a Java annotation."""
    name: str
    parameters: Dict[str, Any]
    line_number: int


@dataclass
class JavaFile:
    """Information about a complete Java file."""
    file_path: str
    package: str
    imports: List[str]
    classes: List[JavaClass]
    annotations: List[JavaAnnotation]
    dependencies: Set[str]
    framework: Optional[str]  # Spring, JUnit, etc.
