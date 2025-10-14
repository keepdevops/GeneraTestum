"""
Helper methods for Panel AST analysis.
"""

import ast
import re
from typing import Dict, List, Set, Optional, Any, Tuple


class PanelASTHelpers:
    """Helper methods for Panel AST analysis."""
    
    def __init__(self, widget_types: Dict[str, str], layout_types: Dict[str, str]):
        self.widget_types = widget_types
        self.layout_types = layout_types
    
    def get_panel_widget_type(self, call: ast.Call) -> Optional[str]:
        """Get Panel widget type from function call."""
        if isinstance(call.func, ast.Name):
            return self.widget_types.get(call.func.id)
        elif isinstance(call.func, ast.Attribute):
            return self.widget_types.get(call.func.attr)
        return None
    
    def get_panel_layout_type(self, call: ast.Call) -> Optional[str]:
        """Get Panel layout type from function call."""
        if isinstance(call.func, ast.Name):
            return self.layout_types.get(call.func.id)
        elif isinstance(call.func, ast.Attribute):
            return self.layout_types.get(call.func.attr)
        return None
    
    def get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self.get_decorator_name(decorator.func)
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        return str(decorator)
    
    def extract_depends_params(self, decorator_str: str) -> List[str]:
        """Extract parameter dependencies from @depends decorator."""
        params = []
        
        # Match @depends('param1', 'param2', ...)
        depends_pattern = r"depends\s*\(\s*['\"]([^'\"]+)['\"]"
        matches = re.findall(depends_pattern, decorator_str)
        params.extend(matches)
        
        # Match @depends(param1, param2, ...)
        depends_pattern2 = r"depends\s*\(\s*([^)]+)\s*\)"
        match = re.search(depends_pattern2, decorator_str)
        if match:
            param_list = match.group(1)
            # Split by comma and clean up
            for param in param_list.split(','):
                param = param.strip().strip('\'"')
                if param:
                    params.append(param)
        
        return params
    
    def extract_widget_dependencies(self, node: ast.FunctionDef) -> List[str]:
        """Extract widget dependencies from function body."""
        dependencies = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id in self.widget_types:
                dependencies.append(child.id)
        
        return dependencies
    
    def extract_widget_callbacks(self, node: ast.Assign) -> List[str]:
        """Extract callback references from widget assignment."""
        callbacks = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and 'callback' in child.id.lower():
                callbacks.append(child.id)
        
        return callbacks
    
    def extract_widget_reactive_params(self, node: ast.Assign) -> List[str]:
        """Extract reactive parameters from widget assignment."""
        reactive_params = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.keyword):
                if child.arg and 'value' in child.arg.lower():
                    reactive_params.append(child.arg)
        
        return reactive_params
    
    def has_panel_references(self, node: ast.FunctionDef) -> bool:
        """Check if function has Panel references."""
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                if child.id in self.widget_types or child.id in self.layout_types:
                    return True
            elif isinstance(child, ast.Attribute):
                if 'panel' in ast.unparse(child).lower():
                    return True
        return False
    
    def is_entry_point(self, node: ast.FunctionDef) -> bool:
        """Check if function is a Panel app entry point."""
        # Check function name patterns
        entry_patterns = ['main', 'app', 'create_app', 'serve', 'launch']
        if any(pattern in node.name.lower() for pattern in entry_patterns):
            return True
        
        # Check for Panel serve calls in function body
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr == 'serve':
                        return True
        
        return False
