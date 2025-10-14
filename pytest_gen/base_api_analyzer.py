"""
Base class for API analyzers.
"""

import ast
from typing import Dict, List, Set, Optional
from .api_models import APIEndpoint


class BaseAPIAnalyzer(ast.NodeVisitor):
    """Base class for API analyzers."""
    
    def __init__(self):
        self.endpoints = []
        self.imports = {}
        self.dependencies = set()
    
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            self.imports[alias.name] = alias.name
            if alias.name in ['requests', 'urllib', 'sqlite3']:
                self.dependencies.add(alias.name)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from import statements."""
        if node.module:
            if node.module in ['requests', 'urllib', 'sqlite3']:
                self.dependencies.add(node.module)
            
            for alias in node.names:
                self.imports[alias.name] = node.module
