"""
AST-based Python code analysis for test generation.
"""

import ast
import inspect
from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .code_models import FunctionInfo, ClassInfo, ModuleInfo


class CodeAnalyzer:
    """Analyzes Python code using AST parsing."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self._external_dependencies = {
            'requests', 'urllib', 'sqlite3', 'psycopg2', 'pymongo',
            'open', 'file', 'os', 'pathlib', 'json', 'pickle',
            'datetime', 'time', 'random', 'uuid', 'hashlib'
        }
    
    def analyze_file(self, file_path: str) -> ModuleInfo:
        """Analyze a Python file and extract code information."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        return self._analyze_ast(tree, file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> ModuleInfo:
        """Analyze Python code string."""
        tree = ast.parse(code)
        return self._analyze_ast(tree, file_path)
    
    def _analyze_ast(self, tree: ast.AST, file_path: str) -> ModuleInfo:
        """Analyze AST tree and extract module information."""
        analyzer = ASTAnalyzer(self.config, self._external_dependencies)
        analyzer.visit(tree)
        
        return ModuleInfo(
            functions=analyzer.functions,
            classes=analyzer.classes,
            imports=analyzer.imports,
            dependencies=analyzer.dependencies,
            file_path=file_path
        )
    
    def get_test_candidates(self, module_info: ModuleInfo) -> List[FunctionInfo]:
        """Get functions that should have tests generated."""
        candidates = []
        
        for func in module_info.functions:
            if self._should_test_function(func):
                candidates.append(func)
        
        for cls in module_info.classes:
            for method in cls.methods:
                if self._should_test_method(method):
                    candidates.append(method)
        
        return candidates
    
    def _should_test_function(self, func: FunctionInfo) -> bool:
        """Determine if a function should have tests generated."""
        if not self.config.include_private_methods and func.name.startswith('_'):
            return False
        
        # Skip test functions
        if func.name.startswith('test_'):
            return False
        
        return True
    
    def _should_test_method(self, method: FunctionInfo) -> bool:
        """Determine if a method should have tests generated."""
        if not self.config.include_private_methods and method.name.startswith('_'):
            return False
        
        # Skip magic methods except __init__
        if method.name.startswith('__') and method.name != '__init__':
            return False
        
        return True


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing Python code."""
    
    def __init__(self, config: GeneratorConfig, external_deps: Set[str]):
        self.config = config
        self.external_deps = external_deps
        self.functions = []
        self.classes = []
        self.imports = {}
        self.dependencies = set()
        self.current_class = None
    
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            self.imports[alias.name] = alias.name
            if alias.name in self.external_deps:
                self.dependencies.add(alias.name)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from import statements."""
        if node.module:
            if node.module in self.external_deps:
                self.dependencies.add(node.module)
            
            for alias in node.names:
                self.imports[alias.name] = node.module
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        func_info = self._extract_function_info(node)
        self.functions.append(func_info)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definitions."""
        func_info = self._extract_function_info(node, is_async=True)
        self.functions.append(func_info)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definitions."""
        old_class = self.current_class
        self.current_class = node.name
        
        class_info = ClassInfo(
            name=node.name,
            methods=[],
            properties=[],
            inheritance=[base.id for base in node.bases if isinstance(base, ast.Name)],
            docstring=ast.get_docstring(node),
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            dependencies=set(),
            line_number=node.lineno
        )
        
        self.generic_visit(node)
        
        # Collect methods
        for func in self.functions[:]:
            if self._is_method(func.name, node):
                func.is_method = True
                if func.name == '__init__':
                    func.is_staticmethod = False
                class_info.methods.append(func)
                self.functions.remove(func)
        
        self.classes.append(class_info)
        self.current_class = old_class
    
    def _extract_function_info(self, node: ast.FunctionDef, is_async: bool = False) -> FunctionInfo:
        """Extract function information from AST node."""
        parameters = []
        for arg in node.args.args:
            param_type = None
            if arg.annotation:
                param_type = ast.unparse(arg.annotation)
            parameters.append((arg.arg, param_type))
        
        return_annotation = None
        if node.returns:
            return_annotation = ast.unparse(node.returns)
        
        # Extract dependencies from function body
        deps = self._extract_dependencies_from_node(node)
        
        return FunctionInfo(
            name=node.name,
            parameters=parameters,
            return_annotation=return_annotation,
            docstring=ast.get_docstring(node),
            is_async=is_async,
            is_method=self.current_class is not None,
            is_classmethod=any('classmethod' in self._get_decorator_name(dec) for dec in node.decorator_list),
            is_staticmethod=any('staticmethod' in self._get_decorator_name(dec) for dec in node.decorator_list),
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            dependencies=deps,
            line_number=node.lineno
        )
    
    def _extract_dependencies_from_node(self, node: ast.AST) -> Set[str]:
        """Extract external dependencies from an AST node."""
        deps = set()
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    if child.func.id in self.external_deps:
                        deps.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    if hasattr(child.func.value, 'id') and child.func.value.id in self.external_deps:
                        deps.add(child.func.value.id)
        
        return deps
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        return str(decorator)
    
    def _is_method(self, func_name: str, class_node: ast.ClassDef) -> bool:
        """Check if function is a method of the class."""
        # This is a simplified check - in reality, we'd need to track
        # which functions are defined inside which classes
        return True  # For now, assume all functions can be methods