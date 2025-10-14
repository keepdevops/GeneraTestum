"""
Source code analysis and file processing utilities.
"""

import os
from typing import Dict, List, Set, Optional, Any, Tuple, Union
from .config import GeneratorConfig, CodeType
from .code_analyzer import CodeAnalyzer, ModuleInfo
from .api_analyzer import APIAnalyzer, APIModuleInfo


class SourceAnalyzer:
    """Analyzes source code and determines what tests should be generated."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.code_analyzer = CodeAnalyzer(config)
        self.api_analyzer = APIAnalyzer(config)
    
    def analyze_source(self, source_path: str) -> Dict[str, Any]:
        """Analyze source code and return information about what tests would be generated."""
        if os.path.isfile(source_path):
            return self._analyze_file(source_path)
        elif os.path.isdir(source_path):
            return self._analyze_directory(source_path)
        else:
            raise ValueError(f"Source path '{source_path}' does not exist")
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file."""
        analysis = {
            'file_path': file_path,
            'file_type': 'unknown',
            'functions': [],
            'classes': [],
            'endpoints': [],
            'dependencies': set(),
            'estimated_tests': 0
        }
        
        # Try Python analysis
        try:
            module_info = self.code_analyzer.analyze_file(file_path)
            analysis['file_type'] = 'python'
            analysis['functions'] = [{'name': f.name, 'parameters': len(f.parameters)} for f in module_info.functions]
            analysis['classes'] = [{'name': c.name, 'methods': len(c.methods)} for c in module_info.classes]
            analysis['dependencies'] = module_info.dependencies
            analysis['estimated_tests'] = len(module_info.functions) + sum(len(c.methods) for c in module_info.classes)
        except Exception:
            pass
        
        # Try API analysis
        try:
            api_info = self.api_analyzer.analyze_file(file_path)
            if api_info:
                analysis['file_type'] = 'api'
                analysis['endpoints'] = [{'name': e.name, 'method': e.method, 'path': e.path} for e in api_info.endpoints]
                analysis['dependencies'] = api_info.dependencies
                analysis['estimated_tests'] = len(api_info.endpoints)
        except Exception:
            pass
        
        return analysis
    
    def _analyze_directory(self, dir_path: str) -> Dict[str, Any]:
        """Analyze a directory."""
        analysis = {
            'directory_path': dir_path,
            'files': [],
            'total_estimated_tests': 0
        }
        
        for root, dirs, files in os.walk(dir_path):
            if any(skip_dir in root for skip_dir in ['test', 'tests', '__pycache__']):
                continue
            
            for file in files:
                if self._should_process_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        file_analysis = self._analyze_file(file_path)
                        analysis['files'].append(file_analysis)
                        analysis['total_estimated_tests'] += file_analysis['estimated_tests']
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
        
        return analysis
    
    def detect_file_type(self, file_path: str) -> CodeType:
        """Detect the type of code in a file."""
        if not file_path.endswith('.py'):
            return CodeType.PYTHON  # Default to Python
        
        # Read first few lines to detect framework
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read first 1000 chars
                
            if self._has_api_indicators(content):
                return CodeType.API
            else:
                return CodeType.PYTHON
        except Exception:
            return CodeType.PYTHON
    
    def detect_code_type(self, code: str) -> CodeType:
        """Detect the type of code from content."""
        if self._has_api_indicators(code):
            return CodeType.API
        else:
            return CodeType.PYTHON
    
    def _has_api_indicators(self, content: str) -> bool:
        """Check if content has API framework indicators."""
        api_indicators = [
            'from flask import',
            'import flask',
            'from fastapi import',
            'import fastapi',
            'from django',
            'import django',
            'from tornado',
            'import tornado',
            '@app.route',
            '@router.',
            'class.*View',
            'class.*Handler'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in api_indicators)
    
    def _should_process_file(self, filename: str) -> bool:
        """Check if a file should be processed."""
        # Only process Python files
        if not filename.endswith('.py'):
            return False
        
        # Skip test files
        if filename.startswith('test_') or filename.endswith('_test.py'):
            return False
        
        # Skip __init__.py
        if filename == '__init__.py':
            return False
        
        return True
