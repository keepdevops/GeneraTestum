"""
Core AST visitor methods for Panel code analysis.
"""

import ast
from typing import Dict, List, Set, Optional, Any, Tuple
from .panel_models import PanelWidget, PanelCallback, PanelLayout


class PanelASTVisitor:
    """Core AST visitor methods for Panel code analysis."""
    
    def __init__(self, widget_types: Dict[str, str], layout_types: Dict[str, str]):
        self.widget_types = widget_types
        self.layout_types = layout_types
        self.widgets = []
        self.callbacks = []
        self.layouts = []
        self.imports = {}
        self.dependencies = set()
        self.entry_point = None
        
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            self.imports[alias.name] = alias.name
            if 'panel' in alias.name:
                self.dependencies.add('panel')
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from import statements."""
        if node.module:
            if 'panel' in node.module:
                self.dependencies.add('panel')
            
            for alias in node.names:
                self.imports[alias.name] = node.module
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        # Check for Panel callbacks
        callback = self._extract_panel_callback(node)
        if callback:
            self.callbacks.append(callback)
        
        # Check for entry point (app creation)
        if self._is_entry_point(node):
            self.entry_point = node.name
        
        self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignment statements."""
        # Check for Panel widgets
        widget = self._extract_panel_widget(node)
        if widget:
            self.widgets.append(widget)
        
        # Check for Panel layouts
        layout = self._extract_panel_layout(node)
        if layout:
            self.layouts.append(layout)
        
        self.generic_visit(node)
    
    def generic_visit(self, node: ast.AST) -> None:
        """Generic visitor for AST nodes."""
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(item)
    
    def visit(self, node: ast.AST) -> None:
        """Visit a single AST node."""
        method = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
