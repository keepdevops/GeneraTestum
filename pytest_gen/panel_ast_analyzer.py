"""
AST visitor for analyzing Panel code.
"""

import ast
from typing import Dict, List, Set, Optional, Any, Tuple
from .panel_models import PanelWidget, PanelCallback, PanelLayout
from .panel_ast_visitor import PanelASTVisitor
from .panel_ast_extractors import PanelASTExtractors
from .panel_ast_helpers import PanelASTHelpers


class PanelASTAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing Panel code."""
    
    def __init__(self, widget_types: Dict[str, str], layout_types: Dict[str, str]):
        self.widget_types = widget_types
        self.layout_types = layout_types
        self.widgets = []
        self.callbacks = []
        self.layouts = []
        self.imports = {}
        self.dependencies = set()
        self.entry_point = None
        
        # Initialize helper components
        self.visitor = PanelASTVisitor(widget_types, layout_types)
        self.extractors = PanelASTExtractors(widget_types, layout_types)
        self.helpers = PanelASTHelpers(widget_types, layout_types)
        
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        self.visitor.visit_Import(node)
        self.imports.update(self.visitor.imports)
        self.dependencies.update(self.visitor.dependencies)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from import statements."""
        self.visitor.visit_ImportFrom(node)
        self.imports.update(self.visitor.imports)
        self.dependencies.update(self.visitor.dependencies)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        # Check for Panel callbacks
        callback = self.extractors.extract_panel_callback(node)
        if callback:
            self.callbacks.append(callback)
        
        # Check for entry point (app creation)
        if self.helpers.is_entry_point(node):
            self.entry_point = node.name
        
        self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignment statements."""
        # Check for Panel widgets
        widget = self.extractors.extract_panel_widget(node)
        if widget:
            self.widgets.append(widget)
        
        # Check for Panel layouts
        layout = self.extractors.extract_panel_layout(node)
        if layout:
            self.layouts.append(layout)
        
        self.generic_visit(node)