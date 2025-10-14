"""
FastAPI-specific analyzer.
"""

import ast
from typing import Dict, List, Set, Optional
from .api_models import APIEndpoint, APIModuleInfo
from .base_api_analyzer import BaseAPIAnalyzer


class FastAPIAnalyzer(BaseAPIAnalyzer):
    """Analyzer for FastAPI applications."""
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit FastAPI endpoint functions."""
        decorators = [self._get_decorator_name(dec) for dec in node.decorator_list]
        
        # Look for FastAPI decorators (get, post, put, delete, etc.)
        for decorator in decorators:
            if decorator.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                endpoint = self._extract_fastapi_endpoint(node, decorator)
                if endpoint:
                    self.endpoints.append(endpoint)
        
        self.generic_visit(node)
    
    def _extract_fastapi_endpoint(self, node: ast.FunctionDef, decorator: str) -> Optional[APIEndpoint]:
        """Extract FastAPI endpoint information."""
        method = decorator.upper()
        
        # Extract path from decorator arguments (simplified)
        path = '/'  # Default path
        
        # Extract parameters
        parameters = []
        for arg in node.args.args:
            if arg.arg != 'self':
                param_type = None
                if arg.annotation:
                    param_type = ast.unparse(arg.annotation)
                parameters.append((arg.arg, param_type))
        
        return APIEndpoint(
            name=node.name,
            path=path,
            method=method,
            handler=node.name,
            parameters=parameters,
            return_type=ast.unparse(node.returns) if node.returns else None,
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            framework='fastapi',
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
