"""
Core test file building functionality.
"""

import os
from typing import List, Set
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ModuleInfo
from .test_models import TestFile, GeneratedTest
from .template_manager import TemplateManager
from .fixture_generator import FixtureInfo


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
            tests=tests,
            imports=all_imports,
            fixtures=unique_fixtures,
            content=content,
            line_count=len(content.split('\n'))
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
    
    def _generate_single_test(self, func_info: FunctionInfo, module_info: ModuleInfo) -> GeneratedTest:
        """Generate a single test for a function."""
        # Generate test name
        test_name = f"test_{func_info.name}"
        
        # Generate test content (simplified)
        test_content = f'''def {test_name}():
    """Test for {func_info.name} function."""
    # TODO: Implement test cases
    assert True
'''
        
        # Generate imports
        imports = set()
        imports.add("import pytest")
        if module_info.file_path != "<string>":
            module_name = os.path.splitext(os.path.basename(module_info.file_path))[0]
            imports.add(f"from {module_name} import {func_info.name}")
        
        return GeneratedTest(
            name=test_name,
            content=test_content,
            imports=imports,
            fixtures=[],
            mocks=[],
            parametrize=[],
            file_path=test_name + ".py",
            line_count=len(test_content.split('\n'))
        )
    
    def _deduplicate_fixtures(self, fixtures: List[FixtureInfo]) -> List[FixtureInfo]:
        """Deduplicate fixtures by name."""
        seen = set()
        unique_fixtures = []
        for fixture in fixtures:
            if fixture.name not in seen:
                seen.add(fixture.name)
                unique_fixtures.append(fixture)
        return unique_fixtures
    
    def _generate_file_content(self, tests: List[GeneratedTest], fixtures: List[FixtureInfo], imports: Set[str]) -> str:
        """Generate the complete test file content."""
        content_lines = []
        
        # Add imports
        for imp in sorted(imports):
            content_lines.append(imp)
        
        if imports:
            content_lines.append("")
        
        # Add fixtures
        for fixture in fixtures:
            content_lines.append(f"@pytest.fixture")
            content_lines.append(f"def {fixture.name}():")
            content_lines.append(fixture.content)
            content_lines.append("")
        
        # Add tests
        for test in tests:
            content_lines.append(test.content)
            content_lines.append("")
        
        return "\n".join(content_lines)
    
    def _generate_test_file_name(self, module_info: ModuleInfo, test_candidates: List[FunctionInfo]) -> str:
        """Generate a test file name based on the module."""
        if module_info.file_path == "<string>":
            return "test_generated.py"
        
        module_name = os.path.splitext(os.path.basename(module_info.file_path))[0]
        return f"test_{module_name}.py"
