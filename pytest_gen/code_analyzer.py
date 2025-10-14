"""
AST-based Python code analysis for test generation.
"""

import ast
from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .code_models import FunctionInfo, ClassInfo, ModuleInfo
from .code_ast_analyzer import ASTAnalyzer
from .code_analysis_helpers import CodeAnalysisHelpers


class CodeAnalyzer:
    """Analyzes Python code using AST parsing."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.helpers = CodeAnalysisHelpers(config)
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
        return self.helpers.get_test_candidates(module_info)