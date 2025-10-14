"""
Panel-specific extraction methods for AST analysis.
"""

import ast
import re
from typing import Dict, List, Set, Optional, Any, Tuple
from .panel_models import PanelWidget, PanelCallback, PanelLayout


class PanelASTExtractors:
    """Panel-specific extraction methods for AST analysis."""
    
    def __init__(self, widget_types: Dict[str, str], layout_types: Dict[str, str]):
        self.widget_types = widget_types
        self.layout_types = layout_types
    
    def extract_panel_callback(self, node: ast.FunctionDef) -> Optional[PanelCallback]:
        """Extract Panel callback information from function definition."""
        if not self._has_panel_references(node):
            return None
        
        callback = PanelCallback(
            name=node.name,
            parameters=[arg.arg for arg in node.args.args],
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            docstring=ast.get_docstring(node),
            line_number=node.lineno
        )
        
        # Extract dependencies from decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                decorator_str = ast.unparse(decorator)
                callback.dependencies.extend(self._extract_depends_params(decorator_str))
        
        # Extract widget dependencies from function body
        callback.dependencies.extend(self._extract_widget_dependencies(node))
        
        return callback
    
    def extract_panel_widget(self, node: ast.Assign) -> Optional[PanelWidget]:
        """Extract Panel widget information from assignment."""
        if not isinstance(node.value, ast.Call):
            return None
        
        widget_type = self._get_panel_widget_type(node.value)
        if not widget_type:
            return None
        
        widget = PanelWidget(
            name=node.targets[0].id if isinstance(node.targets[0], ast.Name) else str(node.targets[0]),
            widget_type=widget_type,
            parameters=self._extract_call_parameters(node.value),
            callbacks=self._extract_widget_callbacks(node),
            reactive_params=self._extract_widget_reactive_params(node),
            line_number=node.lineno
        )
        
        return widget
    
    def extract_panel_layout(self, node: ast.Assign) -> Optional[PanelLayout]:
        """Extract Panel layout information from assignment."""
        if not isinstance(node.value, ast.Call):
            return None
        
        layout_type = self._get_panel_layout_type(node.value)
        if not layout_type:
            return None
        
        layout = PanelLayout(
            name=node.targets[0].id if isinstance(node.targets[0], ast.Name) else str(node.targets[0]),
            layout_type=layout_type,
            parameters=self._extract_call_parameters(node.value),
            children=self._extract_layout_children(node.value),
            line_number=node.lineno
        )
        
        return layout
    
    def _extract_call_parameters(self, call_node: ast.Call) -> Dict[str, Any]:
        """Extract parameters from function call."""
        parameters = {}
        
        # Positional arguments
        for i, arg in enumerate(call_node.args):
            parameters[f"arg_{i}"] = ast.unparse(arg)
        
        # Keyword arguments
        for keyword in call_node.keywords:
            if keyword.arg:
                parameters[keyword.arg] = ast.unparse(keyword.value)
        
        return parameters
    
    def _extract_layout_children(self, call_node: ast.Call) -> List[str]:
        """Extract children from layout call."""
        children = []
        
        # Look for children in arguments
        for arg in call_node.args:
            if isinstance(arg, ast.List):
                for child in arg.elts:
                    if isinstance(child, ast.Name):
                        children.append(child.id)
            elif isinstance(arg, ast.Name):
                children.append(arg.id)
        
        return children
