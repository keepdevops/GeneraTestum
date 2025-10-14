"""
Dependency analysis functionality for smart mock generation.
"""

import ast
from typing import Dict, List, Any, Set
from .mock_models import DependencyInfo


class DependencyVisitor(ast.NodeVisitor):
    """AST visitor to identify dependencies."""
    
    def __init__(self):
        self.dependencies = {}
    
    def visit_Import(self, node):
        for alias in node.names:
            self._analyze_import(alias.name, alias.asname)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self._analyze_import(node.module, None)
    
    def _analyze_import(self, module_name: str, alias: str = None):
        """Analyze import to determine dependency type."""
        name = alias or module_name
        
        if any(api_lib in module_name for api_lib in ['requests', 'urllib', 'httpx']):
            self.dependencies[name] = {'type': 'api'}
        elif any(db_lib in module_name for db_lib in ['sqlite3', 'psycopg2', 'pymongo', 'sqlalchemy']):
            self.dependencies[name] = {'type': 'database'}
        elif any(file_lib in module_name for file_lib in ['os', 'pathlib', 'shutil']):
            self.dependencies[name] = {'type': 'file'}
        else:
            self.dependencies[name] = {'type': 'library'}


class DependencyAnalyzer:
    """Analyzes code to identify external dependencies."""

    def __init__(self):
        self.dependency_cache = {}

    def analyze_dependencies(self, code: str, file_path: str = None) -> List[DependencyInfo]:
        """Analyze code to identify external dependencies."""
        dependencies = []
        
        try:
            tree = ast.parse(code)
            visitor = DependencyVisitor()
            visitor.visit(tree)
            
            for dep_name, dep_info in visitor.dependencies.items():
                dependency = DependencyInfo(
                    name=dep_name,
                    type=dep_info['type'],
                    url=dep_info.get('url'),
                    methods=dep_info.get('methods', [])
                )
                dependencies.append(dependency)
                
                # Cache for reuse
                self.dependency_cache[dep_name] = dependency
                
        except SyntaxError:
            # Fallback to simple string analysis
            dependencies.extend(self._simple_dependency_analysis(code))
        
        return dependencies

    def _simple_dependency_analysis(self, code: str) -> List[DependencyInfo]:
        """Simple string-based dependency analysis fallback."""
        dependencies = []
        
        # Common patterns
        patterns = {
            'requests': 'api',
            'http.client': 'api',
            'urllib': 'api',
            'sqlite3': 'database',
            'psycopg2': 'database',
            'pymongo': 'database',
            'open': 'file',
            'pathlib': 'file',
            'os': 'file'
        }
        
        for pattern, dep_type in patterns.items():
            if pattern in code:
                dependencies.append(DependencyInfo(
                    name=pattern,
                    type=dep_type
                ))
        
        return dependencies
