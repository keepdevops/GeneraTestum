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


class EnhancedTestBuilder(TestBuilder):
    """Enhanced test builder that uses test library patterns and templates."""

    def __init__(self, config: GeneratorConfig, template_manager: TemplateManager):
        super().__init__(config, template_manager)
        self.library_manager = TestLibraryManager()
        self.pattern_cache = {}

    def build_tests_for_module(self, module_info: ModuleInfo) -> List[TestFile]:
        """Build tests for a module using enhanced patterns."""
        test_files = []
        
        # Group functions and classes by type
        functions = module_info.functions
        classes = module_info.classes
        
        # Build tests for standalone functions
        if functions:
            function_tests = self._build_function_tests(functions, module_info)
            test_files.extend(function_tests)
        
        # Build tests for classes
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
            # Get patterns for this function type
            function_type = self._determine_function_type(func_info)
            patterns = self.library_manager.get_patterns_for_function(func_info.name, function_type)
            
            # Generate enhanced test content
            test_content = self._generate_enhanced_function_test(func_info, patterns, module_info)
            
            # Estimate lines
            estimated_lines = len(test_content.split('\n'))
            
            # If adding this test would exceed limit, create a new file
            if current_lines + estimated_lines > self.config.max_lines_per_file and current_batch:
                test_file = self._build_test_file_from_batch(current_batch, module_info)
                test_files.append(test_file)
                current_batch = []
                current_lines = 0

            current_batch.append((func_info, test_content))
            current_lines += estimated_lines

        # Add remaining tests
        if current_batch:
            test_file = self._build_enhanced_test_file_from_batch(current_batch, module_info)
            test_files.append(test_file)

        return test_files

    def _build_class_tests(self, classes: List[ClassInfo], module_info: ModuleInfo) -> List[TestFile]:
        """Build tests for classes using library patterns."""
        test_files = []
        
        for class_info in classes:
            # Get patterns for classes
            patterns = self.library_manager.get_patterns_for_class(class_info.name)
            
            # Generate enhanced test content
            test_content = self._generate_enhanced_class_test(class_info, patterns, module_info)
            
            # Create test file for this class
            test_file = self._create_enhanced_test_file(class_info, test_content, module_info)
            test_files.append(test_file)
        
        return test_files

    def _determine_function_type(self, func_info: FunctionInfo) -> str:
        """Determine the type of function for pattern matching."""
        # Simple heuristics to determine function type
        if any(keyword in func_info.name.lower() for keyword in ['validate', 'check', 'is_', 'has_']):
            return "validation"
        elif any(keyword in func_info.name.lower() for keyword in ['api', 'endpoint', 'route']):
            return "api"
        elif any(keyword in func_info.name.lower() for keyword in ['calculate', 'compute', 'add', 'multiply']):
            return "arithmetic"
        else:
            return "basic"

    def _generate_enhanced_function_test(self, func_info: FunctionInfo, patterns: List[Dict], module_info: ModuleInfo) -> str:
        """Generate enhanced test content for a function using patterns."""
        test_lines = []
        
        # Add imports
        test_lines.append(f"from {module_info.module_name} import {func_info.name}")
        test_lines.append("import pytest")
        test_lines.append("")
        
        # Add class definition
        class_name = f"Test{func_info.name.title()}"
        test_lines.append(f"class {class_name}:")
        test_lines.append(f'    """Test cases for {func_info.name} function."""')
        test_lines.append("")
        
        # Generate test methods based on patterns
        for pattern in patterns:
            test_method = self._generate_test_method_from_pattern(func_info, pattern)
            if test_method:
                test_lines.extend(test_method)
                test_lines.append("")
        
        # Add parametrized tests if applicable
        if len(func_info.parameters) > 0:
            parametrized_test = self._generate_parametrized_test(func_info)
            if parametrized_test:
                test_lines.extend(parametrized_test)
                test_lines.append("")
        
        return "\n".join(test_lines)

    def _generate_test_method_from_pattern(self, func_info: FunctionInfo, pattern: Dict) -> List[str]:
        """Generate a test method from a pattern."""
        pattern_name = pattern.get("name", "")
        pattern_desc = pattern.get("description", "")
        template = pattern.get("template", "")
        
        if not template:
            return []
        
        method_lines = []
        method_name = f"test_{func_info.name}_{pattern_name}"
        
        method_lines.append(f"    def {method_name}(self):")
        method_lines.append(f'        """Test {func_info.name} {pattern_desc}."""')
        
        # Generate test content based on pattern type
        if pattern_name == "happy_path":
            method_lines.extend(self._generate_happy_path_test(func_info, template))
        elif pattern_name == "edge_cases":
            method_lines.extend(self._generate_edge_case_test(func_info, template))
        elif pattern_name == "error_cases":
            method_lines.extend(self._generate_error_case_test(func_info, template))
        else:
            # Generic pattern implementation
            method_lines.append(f"        # {template}")
            method_lines.append("        assert True  # TODO: Implement test")
        
        return method_lines

    def _generate_happy_path_test(self, func_info: FunctionInfo, template: str) -> List[str]:
        """Generate happy path test cases."""
        lines = []
        
        # Generate basic test cases based on function parameters
        if len(func_info.parameters) == 2:
            # Binary function
            lines.append(f"        result = {func_info.name}(2, 3)")
            lines.append("        assert result == 5  # TODO: Adjust expected result")
        elif len(func_info.parameters) == 1:
            # Unary function
            lines.append(f"        result = {func_info.name}(10)")
            lines.append("        assert result is not None  # TODO: Adjust expected result")
        else:
            # Generic implementation
            lines.append(f"        result = {func_info.name}()")
            lines.append("        assert result is not None  # TODO: Adjust expected result")
        
        return lines

    def _generate_edge_case_test(self, func_info: FunctionInfo, template: str) -> List[str]:
        """Generate edge case test cases."""
        lines = []
        
        # Add common edge cases
        if len(func_info.parameters) == 2:
            lines.append(f"        # Test with zero")
            lines.append(f"        result = {func_info.name}(0, 5)")
            lines.append("        assert result is not None  # TODO: Adjust expected result")
            lines.append("")
            lines.append(f"        # Test with negative numbers")
            lines.append(f"        result = {func_info.name}(-1, 1)")
            lines.append("        assert result is not None  # TODO: Adjust expected result")
        elif len(func_info.parameters) == 1:
            lines.append(f"        # Test with zero")
            lines.append(f"        result = {func_info.name}(0)")
            lines.append("        assert result is not None  # TODO: Adjust expected result")
            lines.append("")
            lines.append(f"        # Test with negative number")
            lines.append(f"        result = {func_info.name}(-1)")
            lines.append("        assert result is not None  # TODO: Adjust expected result")
        
        return lines

    def _generate_error_case_test(self, func_info: FunctionInfo, template: str) -> List[str]:
        """Generate error case test cases."""
        lines = []
        
        # Add common error cases
        lines.append(f"        # Test error conditions")
        lines.append(f"        # with pytest.raises(ValueError):")
        lines.append(f"        #     {func_info.name}(invalid_args)")
        lines.append("        assert True  # TODO: Implement error tests")
        
        return lines

    def _generate_parametrized_test(self, func_info: FunctionInfo) -> List[str]:
        """Generate parametrized test cases."""
        if len(func_info.parameters) == 0:
            return []
        
        lines = []
        lines.append(f"    @pytest.mark.parametrize(\"input_val,expected\", [")
        lines.append("        (1, 2),  # TODO: Add test cases")
        lines.append("        (3, 4),  # TODO: Add test cases")
        lines.append("    ])")
        lines.append(f"    def test_{func_info.name}_parametrized(self, input_val, expected):")
        lines.append(f'        """Test {func_info.name} with multiple inputs."""')
        lines.append(f"        result = {func_info.name}(input_val)")
        lines.append("        assert result == expected  # TODO: Adjust assertion")
        
        return lines

    def _generate_enhanced_class_test(self, class_info: ClassInfo, patterns: List[Dict], module_info: ModuleInfo) -> str:
        """Generate enhanced test content for a class using patterns."""
        test_lines = []
        
        # Add imports
        test_lines.append(f"from {module_info.module_name} import {class_info.name}")
        test_lines.append("import pytest")
        test_lines.append("")
        
        # Add class definition
        test_lines.append(f"class Test{class_info.name}:")
        test_lines.append(f'    """Test cases for {class_info.name} class."""')
        test_lines.append("")
        
        # Add setup method
        test_lines.append("    def setup_method(self):")
        test_lines.append(f'        """Set up test fixtures before each test method."""')
        test_lines.append(f"        self.instance = {class_info.name}()")
        test_lines.append("")
        
        # Add initialization test
        test_lines.append(f"    def test_{class_info.name.lower()}_initialization(self):")
        test_lines.append(f'        """Test {class_info.name} initialization."""')
        test_lines.append("        instance = self.instance")
        test_lines.append("        assert instance is not None")
        test_lines.append("")
        
        # Add method tests
        for method in class_info.methods:
            if not method.name.startswith('_'):  # Skip private methods
                test_lines.extend(self._generate_method_test(method, class_info.name))
                test_lines.append("")
        
        return "\n".join(test_lines)

    def _generate_method_test(self, method_info: FunctionInfo, class_name: str) -> List[str]:
        """Generate test for a class method."""
        lines = []
        
        lines.append(f"    def test_{method_info.name}(self):")
        lines.append(f'        """Test {class_name}.{method_info.name} method."""')
        
        # Generate basic test
        if len(method_info.parameters) == 0:
            lines.append(f"        result = self.instance.{method_info.name}()")
            lines.append("        assert result is not None  # TODO: Adjust assertion")
        elif len(method_info.parameters) == 1:
            lines.append(f"        result = self.instance.{method_info.name}(10)")
            lines.append("        assert result is not None  # TODO: Adjust assertion")
        else:
            lines.append(f"        result = self.instance.{method_info.name}(2, 3)")
            lines.append("        assert result is not None  # TODO: Adjust assertion")
        
        return lines

    def _build_enhanced_test_file_from_batch(self, batch: List, module_info: ModuleInfo) -> TestFile:
        """Build a test file from a batch of enhanced tests."""
        content_lines = []
        all_imports = set()
        
        # Add imports
        all_imports.add("import pytest")
        content_lines.extend(sorted(all_imports))
        content_lines.append("")
        
        # Add test content
        for func_info, test_content in batch:
            content_lines.append(test_content)
            content_lines.append("")
        
        content = "\n".join(content_lines)
        file_name = f"test_{module_info.module_name}.py"
        
        return TestFile(
            file_path=file_name,
            tests=[],  # TODO: Convert content to GeneratedTest objects
            imports=all_imports,
            fixtures=[],
            content=content,
            line_count=len(content.split('\n'))
        )

    def _create_enhanced_test_file(self, class_info: ClassInfo, content: str, module_info: ModuleInfo) -> TestFile:
        """Create a test file for a class."""
        imports = {"import pytest"}
        file_name = f"test_{class_info.name.lower()}.py"
        
        return TestFile(
            file_path=file_name,
            tests=[],
            imports=imports,
            fixtures=[],
            content=content,
            line_count=len(content.split('\n'))
        )
