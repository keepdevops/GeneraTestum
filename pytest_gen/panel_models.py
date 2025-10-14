"""
Data models for Panel application analysis.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class PanelWidget:
    """Information about a Panel widget."""
    name: str
    widget_type: str  # Button, Slider, TextInput, etc.
    parameters: List[Tuple[str, Any]]
    callbacks: List[str]
    reactive_params: List[str]
    dependencies: Set[str]
    line_number: int
    docstring: Optional[str]


@dataclass
class PanelCallback:
    """Information about a Panel callback function."""
    name: str
    widget_dependencies: List[str]  # Widgets that trigger this callback
    reactive_params: List[str]  # @pn.depends parameters
    parameters: List[Tuple[str, str]]
    return_type: Optional[str]
    docstring: Optional[str]
    line_number: int


@dataclass
class PanelLayout:
    """Information about Panel layout components."""
    name: str
    layout_type: str  # Row, Column, Tabs, etc.
    children: List[str]  # Child widget names
    parameters: List[Tuple[str, Any]]
    line_number: int


@dataclass
class PanelApp:
    """Information about a complete Panel application."""
    name: str
    widgets: List[PanelWidget]
    callbacks: List[PanelCallback]
    layouts: List[PanelLayout]
    imports: Dict[str, str]
    dependencies: Set[str]
    file_path: str
    entry_point: Optional[str]  # Main app creation function
