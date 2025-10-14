"""
Core test generation operations.
"""

import os
from typing import List, Dict, Any, Optional
from .code_analyzer import CodeAnalyzer, ModuleInfo
from .api_analyzer import APIAnalyzer
from .api_models import APIModuleInfo
from .test_builder import TestBuilder, TestFile
from .source_analyzer import SourceAnalyzer


class GeneratorCoreOperations:
    """Core test generation operations."""
    
    def __init__(self, config):
        self.config = config
        self.code_analyzer = CodeAnalyzer(self.config)
        self.api_analyzer = APIAnalyzer(self.config)
        self.test_builder = TestBuilder(self.config)
        self.source_analyzer = SourceAnalyzer(self.config)
    
    def generate_tests_for_file(self, file_path: str) -> List[str]:
        """Generate tests for a single file."""
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Detect file type
        code_type = self.source_analyzer.detect_file_type(file_path)
        
        if code_type == "python":
            return self._generate_python_tests(file_path)
        elif code_type == "api":
            return self._generate_api_tests(file_path)
        else:
            return []
    
    def generate_tests_for_directory(self, dir_path: str) -> List[str]:
        """Generate tests for all files in a directory."""
        generated_files = []
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    file_path = os.path.join(root, file)
                    file_tests = self.generate_tests_for_file(file_path)
                    generated_files.extend(file_tests)
        
        return generated_files
    
    def generate_tests_from_code_string(self, code: str, file_path: str = "<string>") -> List[str]:
        """Generate tests from code string."""
        # Detect code type
        code_type = self.source_analyzer.detect_code_type(code)
        
        if code_type == "python":
            return self._generate_python_tests_from_code(code, file_path)
        elif code_type == "api":
            return self._generate_api_tests_from_code(code, file_path)
        else:
            return []
    
    def _generate_python_tests(self, file_path: str) -> List[str]:
        """Generate Python tests."""
        module_info = self.code_analyzer.analyze_file(file_path)
        test_files = self.test_builder.build_tests_for_module(module_info)
        
        # Write test files
        written_files = []
        for test_file in test_files:
            output_path = os.path.join(self.config.output_dir, test_file.file_path)
            with open(output_path, 'w') as f:
                f.write(test_file.content)
            written_files.append(output_path)
        
        return written_files
    
    def _generate_api_tests(self, file_path: str) -> List[str]:
        """Generate API tests."""
        api_info = self.api_analyzer.analyze_file(file_path)
        test_files = self.test_builder.build_tests_for_api(api_info)
        
        # Write test files
        written_files = []
        for test_file in test_files:
            output_path = os.path.join(self.config.output_dir, test_file.file_path)
            with open(output_path, 'w') as f:
                f.write(test_file.content)
            written_files.append(output_path)
        
        return written_files
    
    def _generate_python_tests_from_code(self, code: str, file_path: str) -> List[str]:
        """Generate Python tests from code string."""
        module_info = self.code_analyzer.analyze_code(code, file_path)
        test_files = self.test_builder.build_tests_for_module(module_info)
        
        # Write test files
        written_files = []
        for test_file in test_files:
            output_path = os.path.join(self.config.output_dir, test_file.file_path)
            with open(output_path, 'w') as f:
                f.write(test_file.content)
            written_files.append(output_path)
        
        return written_files
    
    def _generate_api_tests_from_code(self, code: str, file_path: str) -> List[str]:
        """Generate API tests from code string."""
        api_info = self.api_analyzer.analyze_code(code, file_path)
        test_files = self.test_builder.build_tests_for_api(api_info)
        
        # Write test files
        written_files = []
        for test_file in test_files:
            output_path = os.path.join(self.config.output_dir, test_file.file_path)
            with open(output_path, 'w') as f:
                f.write(test_file.content)
            written_files.append(output_path)
        
        return written_files
