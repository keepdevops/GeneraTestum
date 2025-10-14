"""
Django-specific analyzer.
"""

import ast
from typing import Dict, List, Set, Optional
from .api_models import APIEndpoint, APIModuleInfo
from .base_api_analyzer import BaseAPIAnalyzer


class DjangoAnalyzer(BaseAPIAnalyzer):
    """Analyzer for Django views."""
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit Django view classes."""
        if self._is_django_view(node):
            for method in node.body:
                if isinstance(method, ast.FunctionDef) and method.name in ['get', 'post', 'put', 'delete']:
                    endpoint = self._extract_django_endpoint(method, node.name)
                    if endpoint:
                        self.endpoints.append(endpoint)
        
        self.generic_visit(node)
    
    def _is_django_view(self, node: ast.ClassDef) -> bool:
        """Check if class is a Django view."""
        for base in node.bases:
            if isinstance(base, ast.Name) and 'View' in base.id:
                return True
        return False
    
    def _extract_django_endpoint(self, method: ast.FunctionDef, class_name: str) -> Optional[APIEndpoint]:
        """Extract Django endpoint information."""
        return APIEndpoint(
            name=f"{class_name}_{method.name}",
            path=f"/{class_name.lower()}/",
            method=method.name.upper(),
            handler=f"{class_name}.{method.name}",
            parameters=[],
            return_type=None,
            decorators=[],
            framework='django',
            dependencies=set(),
            line_number=method.lineno,
            docstring=ast.get_docstring(method)
        )
