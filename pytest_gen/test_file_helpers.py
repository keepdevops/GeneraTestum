"""
Helper methods for test file operations.
"""

import os
from typing import List, Set
from .code_analyzer import FunctionInfo, ModuleInfo
from .test_models import TestFile, GeneratedTest, FixtureInfo


class TestFileHelpers:
    """Helper methods for test file operations."""
    
    @staticmethod
    def generate_test_file_name(module_info: ModuleInfo, test_candidates: List[FunctionInfo]) -> str:
        """Generate test file name."""
        module_name = os.path.splitext(os.path.basename(module_info.file_path))[0]
        return f"test_{module_name}.py"
    
    @staticmethod
    def deduplicate_fixtures(fixtures: List[FixtureInfo]) -> List[FixtureInfo]:
        """Remove duplicate fixtures."""
        seen = set()
        unique_fixtures = []
        
        for fixture in fixtures:
            if fixture.name not in seen:
                seen.add(fixture.name)
                unique_fixtures.append(fixture)
        
        return unique_fixtures
    
    @staticmethod
    def generate_file_content(tests: List[GeneratedTest], fixtures: List[FixtureInfo], imports: Set[str]) -> str:
        """Generate complete test file content."""
        lines = []
        
        # Add imports
        sorted_imports = sorted(imports)
        for imp in sorted_imports:
            lines.append(imp)
        
        if lines and sorted_imports:
            lines.append("")  # Empty line after imports
        
        # Add fixtures
        if fixtures:
            for fixture in fixtures:
                lines.append(f"@pytest.fixture(scope='{fixture.scope}')")
                lines.append(f"def {fixture.name}():")
                lines.append(f'    """{fixture.docstring or "Fixture"}"""')
                
                # Add fixture content with proper indentation
                if fixture.content:
                    for content_line in fixture.content.split('\n'):
                        lines.append(f"    {content_line}")
                
                lines.append("")  # Empty line after fixture
        
        # Add tests
        for test in tests:
            lines.append(test.content)
            lines.append("")  # Empty line after test
        
        return "\n".join(lines)
