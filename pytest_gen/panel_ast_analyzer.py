"""
AST visitor for analyzing Panel code.
"""

import ast
from typing import Dict, List, Set, Optional, Any, Tuple
from .panel_models import PanelWidget, PanelCallback, PanelLayout


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
        # Check for widget creation
        widget = self._extract_panel_widget(node)
        if widget:
            self.widgets.append(widget)
        
        # Check for layout creation
        layout = self._extract_panel_layout(node)
        if layout:
            self.layouts.append(layout)
        
        self.generic_visit(node)
    
    def _extract_panel_callback(self, node: ast.FunctionDef) -> Optional[PanelCallback]:
        """Extract Panel callback information."""
        decorators = [self._get_decorator_name(dec) for dec in node.decorator_list]
        
        # Look for @pn.depends decorator
        has_depends = any('depends' in dec for dec in decorators)
        
        if has_depends or self._has_panel_references(node):
            # Extract parameters
            parameters = []
            for arg in node.args.args:
                param_type = None
                if arg.annotation:
                    param_type = ast.unparse(arg.annotation)
                parameters.append((arg.arg, param_type))
            
            # Extract reactive parameters from decorators
            reactive_params = []
            for decorator in decorators:
                if 'depends' in decorator:
                    # Extract parameter names from @pn.depends
                    params = self._extract_depends_params(decorator)
                    reactive_params.extend(params)
            
            # Extract widget dependencies
            widget_deps = self._extract_widget_dependencies(node)
            
            return PanelCallback(
                name=node.name,
                widget_dependencies=widget_deps,
                reactive_params=reactive_params,
                parameters=parameters,
                return_type=ast.unparse(node.returns) if node.returns else None,
                docstring=ast.get_docstring(node),
                line_number=node.lineno
            )
        
        return None
    
    def _extract_panel_widget(self, node: ast.Assign) -> Optional[PanelWidget]:
        """Extract Panel widget information."""
        if not isinstance(node.value, ast.Call):
            return None
        
        call = node.value
        
        # Check if it's a Panel widget creation
        widget_type = self._get_panel_widget_type(call)
        if not widget_type:
            return None
        
        # Extract widget name
        if isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        else:
            name = f"widget_{node.lineno}"
        
        # Extract parameters
        parameters = []
        for keyword in call.keywords:
            if keyword.value:
                value = ast.unparse(keyword.value)
                parameters.append((keyword.arg, value))
        
        # Extract callbacks
        callbacks = self._extract_widget_callbacks(node)
        
        # Extract reactive parameters
        reactive_params = self._extract_widget_reactive_params(node)
        
        return PanelWidget(
            name=name,
            widget_type=widget_type,
            parameters=parameters,
            callbacks=callbacks,
            reactive_params=reactive_params,
            dependencies=set(),
            line_number=node.lineno,
            docstring=None
        )
    
    def _extract_panel_layout(self, node: ast.Assign) -> Optional[PanelLayout]:
        """Extract Panel layout information."""
        if not isinstance(node.value, ast.Call):
            return None
        
        call = node.value
        
        # Check if it's a Panel layout creation
        layout_type = self._get_panel_layout_type(call)
        if not layout_type:
            return None
        
        # Extract layout name
        if isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        else:
            name = f"layout_{node.lineno}"
        
        # Extract parameters
        parameters = []
        for keyword in call.keywords:
            if keyword.value:
                value = ast.unparse(keyword.value)
                parameters.append((keyword.arg, value))
        
        # Extract children
        children = []
        for arg in call.args:
            if isinstance(arg, ast.Name):
                children.append(arg.id)
        
        return PanelLayout(
            name=name,
            layout_type=layout_type,
            children=children,
            parameters=parameters,
            line_number=node.lineno
        )
    
    def _get_panel_widget_type(self, call: ast.Call) -> Optional[str]:
        """Get Panel widget type from function call."""
        if isinstance(call.func, ast.Attribute):
            full_name = ast.unparse(call.func)
            return self.widget_types.get(full_name)
        return None
    
    def _get_panel_layout_type(self, call: ast.Call) -> Optional[str]:
        """Get Panel layout type from function call."""
        if isinstance(call.func, ast.Attribute):
            full_name = ast.unparse(call.func)
            return self.layout_types.get(full_name)
        return None
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return ast.unparse(decorator)
        return str(decorator)
    
    def _extract_depends_params(self, decorator_str: str) -> List[str]:
        """Extract parameter names from @pn.depends decorator."""
        # Simple regex to extract parameter names from decorator
        # This is a simplified implementation
        params = []
        if '(' in decorator_str and ')' in decorator_str:
            content = decorator_str.split('(')[1].split(')')[0]
            # Split by comma and extract variable names
            for param in content.split(','):
                param = param.strip()
                if param and not param.startswith('pn.'):
                    params.append(param)
        return params
    
    def _extract_widget_dependencies(self, node: ast.FunctionDef) -> List[str]:
        """Extract widget dependencies from callback function."""
        deps = []
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                # Check if it's a widget reference
                if child.id in [w.name for w in self.widgets]:
                    deps.append(child.id)
        return list(set(deps))
    
    def _extract_widget_callbacks(self, node: ast.Assign) -> List[str]:
        """Extract callback functions from widget assignment."""
        callbacks = []
        # Look for .bind() or .param.watch() calls
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr in ['bind', 'watch']:
                        for arg in child.args:
                            if isinstance(arg, ast.Name):
                                callbacks.append(arg.id)
        return callbacks
    
    def _extract_widget_reactive_params(self, node: ast.Assign) -> List[str]:
        """Extract reactive parameters from widget."""
        reactive_params = []
        # Look for parameter assignments that might be reactive
        for child in ast.walk(node):
            if isinstance(child, ast.keyword):
                if child.arg in ['value', 'options', 'disabled']:
                    reactive_params.append(child.arg)
        return reactive_params
    
    def _has_panel_references(self, node: ast.FunctionDef) -> bool:
        """Check if function has Panel-related references."""
        for child in ast.walk(node):
            if isinstance(child, ast.Attribute):
                attr_name = ast.unparse(child)
                if 'pn.' in attr_name or 'panel.' in attr_name:
                    return True
        return False
    
    def _is_entry_point(self, node: ast.FunctionDef) -> bool:
        """Check if function is likely the main app entry point."""
        entry_point_names = ['main', 'create_app', 'app', 'dashboard', 'serve']
        return node.name in entry_point_names or any(
            'app' in node.name.lower() or 'serve' in node.name.lower()
            for _ in [node]
        )
