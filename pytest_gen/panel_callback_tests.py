"""
Callback-specific test generation for Panel applications.
"""

from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .panel_models import PanelWidget, PanelCallback, PanelLayout, PanelApp
from .test_models import GeneratedTest
from .mock_generator import MockInfo
from .fixture_models import FixtureInfo
from .panel_test_templates import PanelTestTemplates


class PanelCallbackTests:
    """Callback-specific test generation for Panel applications."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.templates = PanelTestTemplates()
    
    def generate_callback_tests(self, callback: PanelCallback, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate tests for a Panel callback."""
        tests = []
        
        # Callback function test
        func_test = self._generate_callback_function_test(callback)
        tests.append(func_test)
        
        # Callback dependency tests
        dep_tests = self._generate_callback_dependency_tests(callback, widgets)
        tests.extend(dep_tests)
        
        # Callback integration tests
        integration_tests = self._generate_callback_integration_tests(callback, widgets)
        tests.extend(integration_tests)
        
        return tests
    
    def _generate_callback_function_test(self, callback: PanelCallback) -> GeneratedTest:
        """Generate callback function test."""
        content = f"""def test_{callback.name}_function():
    \"\"\"Test {callback.name} callback function.\"\"\"
    # Arrange
    # Mock dependencies
    mock_widget = Mock()
    
    # Act
    result = {callback.name}(mock_widget)
    
    # Assert
    assert result is not None
"""
        
        return GeneratedTest(
            name=f"test_{callback.name}_function",
            content=content,
            imports={"import panel as pn", "from unittest.mock import Mock"},
            fixtures=[],
            mocks=[],
            parametrize=None
        )
    
    def _generate_callback_dependency_tests(self, callback: PanelCallback, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate callback dependency tests."""
        tests = []
        
        for dependency in callback.dependencies:
            test_content = f"""def test_{callback.name}_{dependency}_dependency():
    \"\"\"Test {callback.name} {dependency} dependency.\"\"\"
    # Arrange
    mock_{dependency} = Mock()
    
    # Act
    # Test callback with mocked dependency
    result = {callback.name}(mock_{dependency})
    
    # Assert
    assert mock_{dependency}.called
"""
            
            test = GeneratedTest(
                name=f"test_{callback.name}_{dependency}_dependency",
                content=test_content,
                imports={"import panel as pn", "from unittest.mock import Mock"},
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(test)
        
        return tests
    
    def _generate_callback_integration_tests(self, callback: PanelCallback, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate callback integration tests."""
        tests = []
        
        # Find widgets that might be related to this callback
        related_widgets = [w for w in widgets if w.name in callback.dependencies]
        
        if related_widgets:
            test_content = f"""def test_{callback.name}_integration():
    \"\"\"Test {callback.name} integration with widgets.\"\"\"
    # Arrange
    widgets = {{
        {', '.join([f'"{w.name}": {w.widget_type}()' for w in related_widgets[:3]])}
    }}
    
    # Act
    result = {callback.name}(**widgets)
    
    # Assert
    assert result is not None
"""
            
            test = GeneratedTest(
                name=f"test_{callback.name}_integration",
                content=test_content,
                imports={"import panel as pn"},
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(test)
        
        return tests
