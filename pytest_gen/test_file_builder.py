"""
Core test file building functionality.
"""

import os
from typing import List, Set
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ModuleInfo
from .test_models import TestFile, GeneratedTest
from .template_manager import TemplateManager


class TestFileBuilder:
    """Core test file building functionality."""
    
    def __init__(self, config: GeneratorConfig, template_manager: TemplateManager):
        self.config = config
        self.template_manager = template_manager
    
    def split_tests_into_files(self, test_candidates: List[FunctionInfo], module_info: ModuleInfo) -> List[TestFile]:
        """Split tests into multiple files if they exceed line limit."""
        test_files = []
        current_batch = []
        current_lines = 0
        
        for candidate in test_candidates:
            # Estimate lines for this test
            estimated_lines = self._estimate_test_lines(candidate)
            
            # If adding this test would exceed limit, create a new file
            if current_lines + estimated_lines > self.config.max_lines_per_file and current_batch:
                test_file = self._build_test_file_from_batch(current_batch, module_info)
                test_files.append(test_file)
                current_batch = []
                current_lines = 0
            
            current_batch.append(candidate)
            current_lines += estimated_lines
        
        # Add remaining tests
        if current_batch:
            test_file = self._build_test_file_from_batch(current_batch, module_info)
            test_files.append(test_file)
        
        return test_files
    
    def build_single_test_file(self, test_candidates: List[FunctionInfo], module_info: ModuleInfo) -> TestFile:
        """Build a single test file for all candidates."""
        return self._build_test_file_from_batch(test_candidates, module_info)
    
    def _build_test_file_from_batch(self, test_candidates: List[FunctionInfo], module_info: ModuleInfo) -> TestFile:
        """Build a test file from a batch of candidates."""
        tests = []
        all_fixtures = []
        all_imports = set()
        
        for candidate in test_candidates:
            test = self._generate_single_test(candidate, module_info)
            tests.append(test)
            all_fixtures.extend(test.fixtures)
            all_imports.update(test.imports)
        
        # Deduplicate fixtures
        unique_fixtures = self._deduplicate_fixtures(all_fixtures)
        
        # Generate file content
        content = self._generate_file_content(tests, unique_fixtures, all_imports)
        
        # Generate file name
        file_name = self._generate_test_file_name(module_info, test_candidates)
        
        return TestFile(
            file_path=file_name,
            content=content,
            test_count=len(tests),
            fixtures_count=len(unique_fixtures)
        )
    
    def _estimate_test_lines(self, func_info: FunctionInfo) -> int:
        """Estimate number of lines for a test function."""
        # Base lines: function definition, docstring, arrange/act/assert
        base_lines = 10
        
        # Add lines for parameters
        param_lines = len(func_info.parameters) * 2
        
        # Add lines for complex return types
        if func_info.return_annotation and 'List' in str(func_info.return_annotation):
            param_lines += 5
        
        return base_lines + param_lines
