"""
Manages test file creation and organization.
"""

import os
from typing import List, Set
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ModuleInfo
from .api_models import APIEndpoint, APIModuleInfo
from .test_models import TestFile, GeneratedTest
from .template_manager import TemplateManager


class TestFileManager:
    """Manages test file creation and organization."""
    
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
    
    def build_api_test_file(self, endpoints: List[APIEndpoint], api_info: APIModuleInfo) -> TestFile:
        """Build a test file for API endpoints."""
        file_name = f"test_{api_info.framework}_api.py"
        file_path = os.path.join(self.config.output_dir, file_name)
        
        # Generate tests for each endpoint
        generated_tests = []
        all_imports = set()
        all_fixtures = []
        
        for endpoint in endpoints:
            test = self._generate_api_test(endpoint, api_info)
            generated_tests.append(test)
            all_imports.update(test.imports)
            all_fixtures.extend(test.fixtures)
        
        # Deduplicate fixtures
        unique_fixtures = self._deduplicate_fixtures(all_fixtures)
        
        # Generate file content
        content = self._generate_file_content(generated_tests, unique_fixtures, all_imports)
        
        return TestFile(
            file_path=file_path,
            tests=generated_tests,
            imports=all_imports,
            fixtures=unique_fixtures,
            content=content,
            line_count=len(content.split('\n'))
        )
    
    def _build_test_file_from_batch(self, test_candidates: List[FunctionInfo], module_info: ModuleInfo) -> TestFile:
        """Build a test file from a batch of test candidates."""
        file_name = self._generate_test_file_name(module_info, test_candidates)
        file_path = os.path.join(self.config.output_dir, file_name)
        
        # Generate tests for each candidate
        generated_tests = []
        all_imports = set()
        all_fixtures = []
        
        for candidate in test_candidates:
            test = self._generate_single_test(candidate, module_info)
            generated_tests.append(test)
            all_imports.update(test.imports)
            all_fixtures.extend(test.fixtures)
        
        # Deduplicate fixtures
        unique_fixtures = self._deduplicate_fixtures(all_fixtures)
        
        # Generate file content
        content = self._generate_file_content(generated_tests, unique_fixtures, all_imports)
        
        return TestFile(
            file_path=file_path,
            tests=generated_tests,
            imports=all_imports,
            fixtures=unique_fixtures,
            content=content,
            line_count=len(content.split('\n'))
        )
    
    def _generate_single_test(self, func_info: FunctionInfo, module_info: ModuleInfo) -> GeneratedTest:
        """Generate a single test for a function."""
        test_name = self.template_manager.format_test_name(func_info.name)
        
        # Generate mocks, fixtures, and parametrize
        from .mock_generator import MockGenerator
        from .fixture_generator import FixtureGenerator
        from .parametrize_generator import ParametrizeGenerator
        
        mock_generator = MockGenerator(self.config)
        fixture_generator = FixtureGenerator(self.config)
        parametrize_generator = ParametrizeGenerator(self.config)
        
        mocks = mock_generator.generate_mocks_for_function(func_info)
        fixtures = fixture_generator.generate_fixtures_for_function(func_info)
        parametrize = parametrize_generator.generate_parametrize_for_function(func_info)
        
        # Generate test content
        content = self.template_manager.generate_function_test(func_info, mocks, fixtures)
        
        # Collect imports
        imports = set()
        imports.update(mock_generator.generate_mock_imports(mocks))
        imports.update(fixture_generator.get_fixture_imports(fixtures))
        imports.update(parametrize_generator.get_parametrize_imports())
        
        # Add module import
        module_name = os.path.splitext(os.path.basename(module_info.file_path))[0]
        imports.add(f"from {module_name} import {func_info.name}")
        
        return GeneratedTest(
            name=test_name,
            content=content,
            imports=imports,
            fixtures=fixtures,
            mocks=mocks,
            parametrize=parametrize,
            file_path="",  # Will be set by caller
            line_count=len(content.split('\n'))
        )
    
    def _generate_api_test(self, endpoint, api_info) -> GeneratedTest:
        """Generate a test for an API endpoint."""
        test_name = self.template_manager.format_test_name(endpoint.name)
        
        # Generate mocks and fixtures
        from .mock_generator import MockGenerator
        from .fixture_generator import FixtureGenerator
        
        mock_generator = MockGenerator(self.config)
        fixture_generator = FixtureGenerator(self.config)
        
        mocks = mock_generator.generate_mocks_for_module(api_info)
        fixtures = fixture_generator.generate_fixtures_for_module(api_info)
        
        # Generate test content
        content = self.template_manager.generate_api_test(endpoint, mocks)
        
        # Collect imports
        imports = set()
        imports.update(mock_generator.generate_mock_imports(mocks))
        imports.update(fixture_generator.get_fixture_imports(fixtures))
        imports.add("import pytest")
        imports.add("import requests")
        
        return GeneratedTest(
            name=test_name,
            content=content,
            imports=imports,
            fixtures=fixtures,
            mocks=mocks,
            parametrize=[],
            file_path="",  # Will be set by caller
            line_count=len(content.split('\n'))
        )
    
    def _estimate_test_lines(self, func_info: FunctionInfo) -> int:
        """Estimate the number of lines a test will take."""
        base_lines = 10  # Basic test structure
        param_lines = len(func_info.parameters) * 2  # Parameter setup
        mock_lines = len(func_info.dependencies) * 3  # Mock setup
        
        return base_lines + param_lines + mock_lines
    
    def _generate_test_file_name(self, module_info: ModuleInfo, test_candidates: List[FunctionInfo]) -> str:
        """Generate a test file name."""
        base_name = os.path.splitext(os.path.basename(module_info.file_path))[0]
        return f"test_{base_name}.py"
    
    def _deduplicate_fixtures(self, fixtures) -> List:
        """Remove duplicate fixtures."""
        seen = set()
        unique_fixtures = []
        
        for fixture in fixtures:
            if fixture.name not in seen:
                seen.add(fixture.name)
                unique_fixtures.append(fixture)
        
        return unique_fixtures
    
    def _generate_file_content(self, tests: List[GeneratedTest], fixtures, imports: Set[str]) -> str:
        """Generate the complete file content."""
        content_lines = []
        
        # Add imports
        if imports:
            for imp in sorted(imports):
                content_lines.append(imp)
            content_lines.append("")
        
        # Add fixtures
        if fixtures:
            content_lines.append("# Fixtures")
            for fixture in fixtures:
                fixture_content = self.template_manager.generate_fixture_code(fixture)
                content_lines.append(fixture_content)
            content_lines.append("")
        
        # Add tests
        content_lines.append("# Test Functions")
        for test in tests:
            content_lines.append(test.content)
            content_lines.append("")
        
        return "\n".join(content_lines)
