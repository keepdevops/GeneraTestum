"""
Main test builder that coordinates test generation.
"""

import os
from typing import List
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ModuleInfo
from .api_models import APIModuleInfo
from .test_models import TestFile
from .test_file_manager import TestFileManager
from .template_manager import TemplateManager


class TestBuilder:
    """Main test builder that coordinates test generation."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.template_manager = TemplateManager(config)
        self.file_manager = TestFileManager(config, self.template_manager)
    
    def build_tests_for_module(self, module_info: ModuleInfo) -> List[TestFile]:
        """Build complete test files for a module."""
        test_files = []
        
        # Get test candidates
        test_candidates = self._get_test_candidates(module_info)
        
        if not test_candidates:
            return test_files
        
        # Split into files if needed
        if self.config.split_large_tests:
            test_files = self.file_manager.split_tests_into_files(test_candidates, module_info)
        else:
            test_file = self.file_manager.build_single_test_file(test_candidates, module_info)
            test_files = [test_file]
        
        return test_files
    
    def build_tests_for_api(self, api_info: APIModuleInfo) -> List[TestFile]:
        """Build test files for API endpoints."""
        test_files = []
        
        if not api_info.endpoints:
            return test_files
        
        # Split endpoints into files if needed
        if self.config.split_large_tests:
            endpoint_batches = self._split_endpoints_into_batches(api_info.endpoints)
        else:
            endpoint_batches = [api_info.endpoints]
        
        for batch in endpoint_batches:
            test_file = self.file_manager.build_api_test_file(batch, api_info)
            test_files.append(test_file)
        
        return test_files
    
    def _get_test_candidates(self, module_info: ModuleInfo) -> List[FunctionInfo]:
        """Get functions that need tests."""
        candidates = []
        
        # Add standalone functions
        for func in module_info.functions:
            if self._should_generate_test(func):
                candidates.append(func)
        
        # Add class methods
        for cls in module_info.classes:
            for method in cls.methods:
                if self._should_generate_test(method):
                    candidates.append(method)
        
        return candidates
    
    def _should_generate_test(self, func_info: FunctionInfo) -> bool:
        """Determine if a function should have tests generated."""
        if not self.config.include_private_methods and func_info.name.startswith('_'):
            return False
        
        # Skip test functions
        if func_info.name.startswith('test_'):
            return False
        
        # Skip magic methods except __init__
        if func_info.name.startswith('__') and func_info.name != '__init__':
            return False
        
        return True
    
    def _split_endpoints_into_batches(self, endpoints) -> List[List]:
        """Split endpoints into batches for multiple files."""
        batches = []
        current_batch = []
        current_lines = 0
        
        for endpoint in endpoints:
            # Estimate lines for this endpoint test
            estimated_lines = 20  # Rough estimate for API tests
            
            if current_lines + estimated_lines > self.config.max_lines_per_file and current_batch:
                batches.append(current_batch)
                current_batch = []
                current_lines = 0
            
            current_batch.append(endpoint)
            current_lines += estimated_lines
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def save_test_files(self, test_files: List[TestFile]) -> List[str]:
        """Save test files to disk."""
        saved_files = []
        
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        for test_file in test_files:
            try:
                with open(test_file.file_path, 'w', encoding='utf-8') as f:
                    f.write(test_file.content)
                saved_files.append(test_file.file_path)
            except Exception as e:
                print(f"Error saving test file {test_file.file_path}: {e}")
        
        return saved_files