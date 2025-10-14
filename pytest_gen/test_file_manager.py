"""
Manages test file creation and organization.
"""

import os
from typing import List, Set
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ModuleInfo
from .api_models import APIEndpoint, APIModuleInfo
from .test_models import TestFile, GeneratedTest, FixtureInfo
from .template_manager import TemplateManager
from .test_file_builder import TestFileBuilder
from .test_file_helpers import TestFileHelpers
from .mock_generator import MockGenerator
from .fixture_generator import FixtureGenerator
from .parametrize_generator import ParametrizeGenerator


class TestFileManager:
    """Manages test file creation and organization."""
    
    def __init__(self, config: GeneratorConfig, template_manager: TemplateManager):
        self.config = config
        self.template_manager = template_manager
        self.builder = TestFileBuilder(config, template_manager)
        self.helpers = TestFileHelpers()
        self.mock_generator = MockGenerator(config)
        self.fixture_generator = FixtureGenerator(config)
        self.parametrize_generator = ParametrizeGenerator(config)
    
    def split_tests_into_files(self, test_candidates: List[FunctionInfo], module_info: ModuleInfo) -> List[TestFile]:
        """Split tests into multiple files if they exceed line limit."""
        return self.builder.split_tests_into_files(test_candidates, module_info)
    
    def build_single_test_file(self, test_candidates: List[FunctionInfo], module_info: ModuleInfo) -> TestFile:
        """Build a single test file for all candidates."""
        return self.builder.build_single_test_file(test_candidates, module_info)
    
    def build_api_test_file(self, endpoints: List[APIEndpoint], api_info: APIModuleInfo) -> TestFile:
        """Build test file for API endpoints."""
        tests = []
        all_fixtures = []
        all_imports = set()
        
        for endpoint in endpoints:
            test = self._generate_api_test(endpoint, api_info)
            tests.append(test)
            all_fixtures.extend(test.fixtures)
            all_imports.update(test.imports)
        
        # Deduplicate fixtures
        unique_fixtures = self.helpers.deduplicate_fixtures(all_fixtures)
        
        # Generate file content
        content = self.helpers.generate_file_content(tests, unique_fixtures, all_imports)
        
        # Generate file name
        # Extract module name from file path
        import os
        module_name = os.path.splitext(os.path.basename(api_info.file_path))[0]
        file_name = f"test_{module_name}_api.py"
        
        return TestFile(
            file_path=file_name,
            tests=tests,
            imports=all_imports,
            fixtures=unique_fixtures,
            content=content,
            line_count=len(content.split('\n'))
        )
    
    def _generate_single_test(self, func_info: FunctionInfo, module_info: ModuleInfo) -> GeneratedTest:
        """Generate a single test for a function."""
        # Generate mocks, fixtures, and parametrize
        mocks = self.mock_generator.generate_mocks_for_function(func_info)
        fixtures = self.fixture_generator.generate_fixtures_for_function(func_info)
        parametrize = self.parametrize_generator.generate_parametrize_for_function(func_info)
        
        # Generate test content
        content = self.template_manager.generate_function_test(func_info, mocks, fixtures)
        
        # Collect imports
        imports = set()
        imports.update(self.mock_generator.get_mock_imports(mocks))
        imports.update(self.fixture_generator.get_fixture_imports(fixtures))
        imports.update(self.parametrize_generator.get_parametrize_imports())
        
        # Add module import
        module_name = os.path.splitext(os.path.basename(module_info.file_path))[0]
        imports.add(f"from {module_name} import {func_info.name}")
        
        return GeneratedTest(
            name=f"test_{func_info.name}",
            content=content,
            imports=imports,
            fixtures=fixtures,
            mocks=mocks,
            parametrize=parametrize
        )
    
    def _generate_api_test(self, endpoint, api_info) -> GeneratedTest:
        """Generate a test for an API endpoint."""
        # Generate mocks and fixtures
        mocks = self.mock_generator.generate_mocks_for_api_endpoint(endpoint)
        fixtures = self.fixture_generator.generate_fixtures_for_module(api_info)
        
        # Generate test content
        content = self.template_manager.generate_api_test(endpoint, mocks)
        
        # Collect imports
        imports = set()
        imports.update(self.mock_generator.get_mock_imports(mocks))
        imports.update(self.fixture_generator.get_fixture_imports(fixtures))
        imports.add("import pytest")
        imports.add("import requests")
        
        return GeneratedTest(
            name=f"test_{endpoint.method.lower()}_{endpoint.path.replace('/', '_').replace('{', '').replace('}', '')}",
            content=content,
            imports=imports,
            fixtures=fixtures,
            mocks=mocks,
            parametrize=None,
            file_path=f"test_{endpoint.method.lower()}_{endpoint.path.replace('/', '_').replace('{', '').replace('}', '')}.py",
            line_count=len(content.split('\n'))
        )