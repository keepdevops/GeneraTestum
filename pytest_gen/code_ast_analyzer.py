"""
AST visitor for analyzing Python code.
"""

import ast
from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .code_models import FunctionInfo, ClassInfo


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing Python code."""
    
    def __init__(self, config: GeneratorConfig, external_deps: Set[str]):
        self.config = config
        self.external_dependencies = external_deps
        self.functions = []
        self.classes = []
        self.imports = {}
        self.dependencies = set()
        self.current_class = None
        
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            self.imports[alias.name] = alias.name
            if alias.name in self.external_dependencies:
                self.dependencies.add(alias.name)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from import statements."""
        if node.module:
            if node.module in self.external_dependencies:
                self.dependencies.add(node.module)
            
            for alias in node.names:
                self.imports[alias.name] = node.module
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        func_info = self._extract_function_info(node, is_async=False)
        
        if self.current_class:
            # This is a method
            func_info.is_method = True
            self.classes[-1].methods.append(func_info)
        else:
            # This is a standalone function
            self.functions.append(func_info)
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definitions."""
        func_info = self._extract_function_info(node, is_async=True)
        
        if self.current_class:
            # This is a method
            func_info.is_method = True
            self.classes[-1].methods.append(func_info)
        else:
            # This is a standalone function
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
            inheritance=[base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
            docstring=ast.get_docstring(node),
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            dependencies=set(),
            line_number=node.lineno
        )
        
        self.classes.append(class_info)
        self.generic_visit(node)
        
        # Extract dependencies from class methods
        for method in class_info.methods:
            class_info.dependencies.update(self._extract_dependencies_from_node(method))
        
        self.current_class = old_class
    
    def _extract_function_info(self, node: ast.FunctionDef, is_async: bool = False) -> FunctionInfo:
        """Extract function information from AST node."""
        parameters = []
        for arg in node.args.args:
            param_name = arg.arg
            param_type = None
            if arg.annotation:
                param_type = ast.unparse(arg.annotation)
            parameters.append((param_name, param_type))
        
        return FunctionInfo(
            name=node.name,
            parameters=parameters,
            return_annotation=ast.unparse(node.returns) if node.returns else None,
            docstring=ast.get_docstring(node),
            is_async=is_async,
            is_method=self.current_class is not None,
            is_classmethod=any(self._get_decorator_name(dec) == 'classmethod' for dec in node.decorator_list),
            is_staticmethod=any(self._get_decorator_name(dec) == 'staticmethod' for dec in node.decorator_list),
            decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
            dependencies=self._extract_dependencies_from_node(node),
            line_number=node.lineno
        )
    
    def _extract_dependencies_from_node(self, node: ast.AST) -> Set[str]:
        """Extract external dependencies from AST node."""
        dependencies = set()
        
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                if child.id in self.external_dependencies:
                    dependencies.add(child.id)
            elif isinstance(child, ast.Attribute):
                if child.value.id in self.external_dependencies:
                    dependencies.add(child.value.id)
        
        return dependencies
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        return str(decorator)
