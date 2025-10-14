"""
Flask-specific API analyzer.
"""

import ast
import re
from typing import Dict, List, Set, Optional
from .api_models import APIEndpoint, APIModuleInfo
from .base_api_analyzer import BaseAPIAnalyzer


class FlaskAnalyzer(BaseAPIAnalyzer):
    """Analyzer for Flask applications."""
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit Flask route functions."""
        decorators = [self._get_decorator_name(dec) for dec in node.decorator_list]
        
        # Look for @app.route decorators
        for decorator in decorators:
            if 'route' in decorator.lower():
                endpoint = self._extract_flask_endpoint(node, decorator)
                if endpoint:
                    self.endpoints.append(endpoint)
        
        self.generic_visit(node)
    
    def _extract_flask_endpoint(self, node: ast.FunctionDef, decorator: str) -> Optional[APIEndpoint]:
        """Extract Flask endpoint information."""
        # Extract route path from decorator (simplified)
        path_match = re.search(r'route\(["\']([^"\']+)["\']', decorator)
        path = path_match.group(1) if path_match else '/'
        
        # Determine HTTP method (simplified)
        method = 'GET'
        if 'methods=' in decorator:
            methods_match = re.search(r'methods=\[["\']([^"\']+)["\']', decorator)
            if methods_match:
                method = methods_match.group(1)
        
        # Extract parameters
        parameters = []
        for arg in node.args.args:
            if arg.arg != 'self':  # Skip self parameter
                param_type = None
                if arg.annotation:
                    param_type = ast.unparse(arg.annotation)
                parameters.append((arg.arg, param_type))
        
        return_annotation = None
        if node.returns:
            return_annotation = ast.unparse(node.returns)
        
        return APIEndpoint(
            name=node.name,
            path=path,
            method=method,
            handler=node.name,
            parameters=parameters,
            return_type=return_annotation,
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            framework='flask',
            dependencies=set(),
            line_number=node.lineno,
            docstring=ast.get_docstring(node)
        )
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        return str(decorator)
