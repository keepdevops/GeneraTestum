"""
Tornado-specific analyzer.
"""

import ast
from typing import Dict, List, Set, Optional
from .api_models import APIEndpoint, APIModuleInfo
from .base_api_analyzer import BaseAPIAnalyzer


class TornadoAnalyzer(BaseAPIAnalyzer):
    """Analyzer for Tornado handlers."""
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit Tornado handler classes."""
        if self._is_tornado_handler(node):
            for method in node.body:
                if isinstance(method, ast.FunctionDef) and method.name.startswith('_'):
                    continue  # Skip private methods
                
                if isinstance(method, ast.FunctionDef) and method.name in ['get', 'post', 'put', 'delete']:
                    endpoint = self._extract_tornado_endpoint(method, node.name)
                    if endpoint:
                        self.endpoints.append(endpoint)
        
        self.generic_visit(node)
    
    def _is_tornado_handler(self, node: ast.ClassDef) -> bool:
        """Check if class is a Tornado handler."""
        for base in node.bases:
            if isinstance(base, ast.Name) and 'Handler' in base.id:
                return True
        return False
    
    def _extract_tornado_endpoint(self, method: ast.FunctionDef, class_name: str) -> Optional[APIEndpoint]:
        """Extract Tornado endpoint information."""
        return APIEndpoint(
            name=f"{class_name}_{method.name}",
            path=f"/{class_name.lower()}/",
            method=method.name.upper(),
            handler=f"{class_name}.{method.name}",
            parameters=[],
            return_type=None,
            decorators=[],
            framework='tornado',
            dependencies=set(),
            line_number=method.lineno,
            docstring=ast.get_docstring(method)
        )
