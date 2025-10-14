"""
Main test generation orchestrator that coordinates all components.
"""

import os
from typing import List
from .config import GeneratorConfig, DEFAULT_CONFIG, CodeType
from .code_analyzer import CodeAnalyzer, ModuleInfo
from .api_analyzer import APIAnalyzer
from .api_models import APIModuleInfo
from .test_builder import TestBuilder, TestFile
from .source_analyzer import SourceAnalyzer


class GeneratorCore:
    """Main orchestrator for test generation."""
    
    def __init__(self, config: GeneratorConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.code_analyzer = CodeAnalyzer(self.config)
        self.api_analyzer = APIAnalyzer(self.config)
        self.test_builder = TestBuilder(self.config)
        self.source_analyzer = SourceAnalyzer(self.config)
    
    def generate_tests(self, source_path: str, output_dir: str = None) -> List[str]:
        """Generate tests for a source file or directory."""
        if output_dir:
            self.config.output_dir = output_dir
        
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        if os.path.isfile(source_path):
            return self._generate_tests_for_file(source_path)
        elif os.path.isdir(source_path):
            return self._generate_tests_for_directory(source_path)
        else:
            raise ValueError(f"Source path '{source_path}' does not exist")
    
    def generate_tests_from_code(self, code: str, file_path: str = "<string>", output_dir: str = None) -> List[str]:
        """Generate tests from code string."""
        if output_dir:
            self.config.output_dir = output_dir
        
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Try to detect code type
        code_type = self.source_analyzer.detect_code_type(code)
        
        if code_type == CodeType.PYTHON:
            module_info = self.code_analyzer.analyze_code(code, file_path)
            test_files = self.test_builder.build_tests_for_module(module_info)
        elif code_type == CodeType.API:
            api_info = self.api_analyzer.analyze_code(code, file_path)
            if api_info:
                test_files = self.test_builder.build_tests_for_api(api_info)
            else:
                return []
        else:
            # Try both analyzers
            test_files = []
            
            # Try Python analysis
            try:
                module_info = self.code_analyzer.analyze_code(code, file_path)
                test_files.extend(self.test_builder.build_tests_for_module(module_info))
            except Exception:
                pass
            
            # Try API analysis
            try:
                api_info = self.api_analyzer.analyze_code(code, file_path)
                if api_info:
                    test_files.extend(self.test_builder.build_tests_for_api(api_info))
            except Exception:
                pass
        
        return self.test_builder.save_test_files(test_files)
    
    def _generate_tests_for_file(self, file_path: str) -> List[str]:
        """Generate tests for a single file."""
        # Detect file type
        code_type = self.source_analyzer.detect_file_type(file_path)
        
        if code_type == CodeType.PYTHON:
            return self._generate_python_tests(file_path)
        elif code_type == CodeType.API:
            return self._generate_api_tests(file_path)
        else:
            # Try both analyzers
            test_files = []
            
            # Try Python analysis
            try:
                test_files.extend(self._generate_python_tests(file_path))
            except Exception:
                pass
            
            # Try API analysis
            try:
                test_files.extend(self._generate_api_tests(file_path))
            except Exception:
                pass
            
            return test_files
    
    def _generate_tests_for_directory(self, dir_path: str) -> List[str]:
        """Generate tests for all files in a directory."""
        all_test_files = []
        
        for root, dirs, files in os.walk(dir_path):
            # Skip test directories
            if any(skip_dir in root for skip_dir in ['test', 'tests', '__pycache__']):
                continue
            
            for file in files:
                if self.source_analyzer._should_process_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        test_files = self._generate_tests_for_file(file_path)
                        all_test_files.extend(test_files)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        
        return all_test_files
    
    def _generate_python_tests(self, file_path: str) -> List[str]:
        """Generate tests for Python code."""
        module_info = self.code_analyzer.analyze_file(file_path)
        test_files = self.test_builder.build_tests_for_module(module_info)
        return self.test_builder.save_test_files(test_files)
    
    def _generate_api_tests(self, file_path: str) -> List[str]:
        """Generate tests for API code."""
        api_info = self.api_analyzer.analyze_file(file_path)
        if not api_info:
            return []
        
        test_files = self.test_builder.build_tests_for_api(api_info)
        return self.test_builder.save_test_files(test_files)
    
    def update_config(self, **kwargs) -> None:
        """Update generator configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def get_config(self) -> GeneratorConfig:
        """Get current configuration."""
        return self.config
    
    def analyze_source(self, source_path: str) -> dict:
        """Analyze source code and return information about what tests would be generated."""
        return self.source_analyzer.analyze_source(source_path)


# Convenience function for library usage
def generate_tests(source_path: str, config: GeneratorConfig = None, **kwargs) -> List[str]:
    """Generate tests for source code.
    
    Args:
        source_path: Path to source file or directory
        config: Generator configuration (optional)
        **kwargs: Additional configuration options
    
    Returns:
        List of generated test file paths
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    # Update config with kwargs
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    generator = GeneratorCore(config)
    return generator.generate_tests(source_path)