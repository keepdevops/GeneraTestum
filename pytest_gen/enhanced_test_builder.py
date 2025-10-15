"""
Enhanced test builder that uses the test library for better test generation.
"""

import os
from typing import List, Dict, Any, Optional
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ClassInfo, ModuleInfo
from .test_builder import TestBuilder, TestFile
from .test_library_manager import TestLibraryManager
from .template_manager import TemplateManager
from .test_pattern_analyzer import TestPatternAnalyzer
from .test_method_generator import TestMethodGenerator


class EnhancedTestBuilder(TestBuilder):
    """Enhanced test builder that uses test library patterns and templates."""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.library_manager = TestLibraryManager()
        self.pattern_analyzer = TestPatternAnalyzer()
        self.method_generator = TestMethodGenerator()
        self.pattern_cache = {}

    def build_tests_for_module(self, module_info: ModuleInfo) -> List[TestFile]:
        """Build tests for a module using enhanced patterns."""
        test_files = []
        
        functions = module_info.functions
        classes = module_info.classes
        
        if functions:
            function_tests = self._build_function_tests(functions, module_info)
            test_files.extend(function_tests)
        
        if classes:
            class_tests = self._build_class_tests(classes, module_info)
            test_files.extend(class_tests)
        
        return test_files

    def _build_function_tests(self, functions: List[FunctionInfo], module_info: ModuleInfo) -> List[TestFile]:
        """Build tests for functions using library patterns."""
        test_files = []
        current_batch = []
        current_lines = 0

        for func_info in functions:
            function_type = self.pattern_analyzer.determine_function_type(func_info)
            patterns = self.pattern_analyzer.get_enhanced_patterns(func_info)
            
            test_content = self._generate_enhanced_function_test(func_info, patterns, module_info)
            estimated_lines = len(test_content.split('\n'))
            
            if current_lines + estimated_lines > self.config.max_lines_per_file:
                if current_batch:
                    test_file = self._build_enhanced_test_file_from_batch(current_batch, module_info)
                    test_files.append(test_file)
                    current_batch = []
                    current_lines = 0
            
            current_batch.append((func_info, test_content))
            current_lines += estimated_lines
        
        if current_batch:
            test_file = self._build_enhanced_test_file_from_batch(current_batch, module_info)
            test_files.append(test_file)
        
        return test_files

    def _build_class_tests(self, classes: List[ClassInfo], module_info: ModuleInfo) -> List[TestFile]:
        """Build tests for classes using enhanced patterns."""
        test_files = []
        
        for class_info in classes:
            class_type = self.pattern_analyzer.determine_class_type(class_info)
            patterns = self.pattern_analyzer.get_class_patterns(class_info)
            
            test_content = self._generate_enhanced_class_test(class_info, patterns, module_info)
            test_file = self._create_enhanced_test_file(class_info, test_content, module_info)
            test_files.append(test_file)
        
        return test_files

    def _generate_enhanced_function_test(self, func_info: FunctionInfo, patterns: List[Dict], module_info: ModuleInfo) -> str:
        """Generate enhanced test content for a function."""
        test_lines = []
        
        # Add imports
        test_lines.append(f"import pytest")
        test_lines.append(f"from {module_info.name} import {func_info.name}")
        test_lines.append("")
        
        # Add test class
        test_lines.append(f"class Test{func_info.name.title()}:")
        test_lines.append('    """Enhanced tests for {} function."""'.format(func_info.name))
        test_lines.append("")
        
        # Generate test methods based on patterns
        for pattern in patterns:
            pattern_type = pattern['type']
            
            if pattern_type == 'happy_path':
                method_lines = self.method_generator.generate_happy_path_test(func_info)
            elif pattern_type == 'edge_cases':
                method_lines = self.method_generator.generate_edge_case_test(func_info)
            elif pattern_type == 'error_handling':
                method_lines = self.method_generator.generate_error_case_test(func_info)
            elif pattern_type == 'parametrized':
                method_lines = self.method_generator.generate_parametrized_test(func_info)
            else:
                continue
            
            test_lines.extend(method_lines)
            test_lines.append("")
        
        return '\n'.join(test_lines)

    def _generate_enhanced_class_test(self, class_info: ClassInfo, patterns: List[str], module_info: ModuleInfo) -> str:
        """Generate enhanced test content for a class."""
        test_lines = []
        
        # Add imports
        test_lines.append("import pytest")
        test_lines.append(f"from {module_info.name} import {class_info.name}")
        test_lines.append("")
        
        # Add test class
        test_lines.append(f"class Test{class_info.name}:")
        test_lines.append(f'    """Enhanced tests for {class_info.name} class."""')
        test_lines.append("")
        
        # Add setup method
        test_lines.append("    def setup_method(self):")
        test_lines.append(f'        """Set up test fixtures."""')
        test_lines.append(f"        self.instance = {class_info.name}()")
        test_lines.append("")
        
        # Generate initialization test
        if 'initialization' in patterns:
            init_lines = self.method_generator.generate_class_initialization_test(class_info)
            test_lines.extend(init_lines)
            test_lines.append("")
        
        # Generate method tests
        if 'method_tests' in patterns and class_info.methods:
            for method in class_info.methods:
                if method.name != '__init__':
                    method_lines = self.method_generator.generate_method_test(method, class_info.name)
                    test_lines.extend(method_lines)
                    test_lines.append("")
        
        return '\n'.join(test_lines)

    def _build_enhanced_test_file_from_batch(self, batch: List, module_info: ModuleInfo) -> TestFile:
        """Build test file from a batch of functions."""
        if not batch:
            return None
        
        # Create combined content
        all_content = []
        
        for func_info, test_content in batch:
            all_content.append(test_content)
            all_content.append("")
        
        combined_content = '\n'.join(all_content)
        
        # Create test file
        test_file_name = f"test_{module_info.name}_enhanced.py"
        test_file_path = os.path.join(self.config.output_dir, test_file_name)
        
        return TestFile(
            name=test_file_name,
            path=test_file_path,
            content=combined_content,
            functions_tested=[item[0].name for item in batch],
            classes_tested=[]
        )

    def _create_enhanced_test_file(self, class_info: ClassInfo, content: str, module_info: ModuleInfo) -> TestFile:
        """Create enhanced test file for a class."""
        test_file_name = f"test_{class_info.name.lower()}_enhanced.py"
        test_file_path = os.path.join(self.config.output_dir, test_file_name)
        
        return TestFile(
            name=test_file_name,
            path=test_file_path,
            content=content,
            functions_tested=[],
            classes_tested=[class_info.name]
        )