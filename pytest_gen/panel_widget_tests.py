"""
Widget-specific test generation for Panel applications.
"""

from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .panel_models import PanelWidget, PanelCallback, PanelLayout, PanelApp
from .test_models import GeneratedTest
from .mock_generator import MockInfo
from .fixture_models import FixtureInfo
from .panel_test_templates import PanelTestTemplates


class PanelWidgetTests:
    """Widget-specific test generation for Panel applications."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.templates = PanelTestTemplates()
    
    def generate_widget_tests(self, widget: PanelWidget) -> List[GeneratedTest]:
        """Generate tests for a Panel widget."""
        tests = []
        
        # Widget initialization test
        init_test = self._generate_widget_init_test(widget)
        tests.append(init_test)
        
        # Widget parameter tests
        param_tests = self._generate_widget_parameter_tests(widget)
        tests.extend(param_tests)
        
        # Widget interaction tests
        interaction_tests = self._generate_widget_interaction_tests(widget)
        tests.extend(interaction_tests)
        
        return tests
    
    def _generate_widget_init_test(self, widget: PanelWidget) -> GeneratedTest:
        """Generate widget initialization test."""
        content = f"""def test_{widget.name}_initialization():
    \"\"\"Test {widget.name} widget initialization.\"\"\"
    # Arrange
    widget = {widget.widget_type}()
    
    # Assert
    assert widget is not None
    assert isinstance(widget, {widget.widget_type})
"""
        
        return GeneratedTest(
            name=f"test_{widget.name}_initialization",
            content=content,
            imports={"import panel as pn"},
            fixtures=[],
            mocks=[],
            parametrize=None
        )
    
    def _generate_widget_parameter_tests(self, widget: PanelWidget) -> List[GeneratedTest]:
        """Generate widget parameter tests."""
        tests = []
        
        for param_name, param_value in widget.parameters.items():
            test_content = f"""def test_{widget.name}_{param_name}_parameter():
    \"\"\"Test {widget.name} {param_name} parameter.\"\"\"
    # Arrange
    widget = {widget.widget_type}({param_name}="{param_value}")
    
    # Assert
    assert widget.{param_name} == "{param_value}"
"""
            
            test = GeneratedTest(
                name=f"test_{widget.name}_{param_name}_parameter",
                content=test_content,
                imports={"import panel as pn"},
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(test)
        
        return tests
    
    def _generate_widget_interaction_tests(self, widget: PanelWidget) -> List[GeneratedTest]:
        """Generate widget interaction tests."""
        tests = []
        
        # Test value changes
        if 'value' in widget.parameters:
            test_content = f"""def test_{widget.name}_value_change():
    \"\"\"Test {widget.name} value change.\"\"\"
    # Arrange
    widget = {widget.widget_type}()
    original_value = widget.value
    
    # Act
    new_value = "new_value"
    widget.value = new_value
    
    # Assert
    assert widget.value == new_value
    assert widget.value != original_value
"""
            
            test = GeneratedTest(
                name=f"test_{widget.name}_value_change",
                content=test_content,
                imports={"import panel as pn"},
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(test)
        
        return tests
