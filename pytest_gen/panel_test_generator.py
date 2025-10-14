"""
Panel-specific test generation for widgets, callbacks, and layouts.
"""

from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .panel_models import PanelWidget, PanelCallback, PanelLayout, PanelApp
from .test_models import GeneratedTest
from .mock_generator import MockInfo
from .fixture_models import FixtureInfo
from .panel_test_templates import PanelTestTemplates
from .panel_widget_tests import PanelWidgetTests
from .panel_callback_tests import PanelCallbackTests
from .panel_layout_tests import PanelLayoutTests


class PanelTestGenerator:
    """Generates Panel-specific test cases."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.templates = PanelTestTemplates()
        self.widget_tests = PanelWidgetTests(config)
        self.callback_tests = PanelCallbackTests(config)
        self.layout_tests = PanelLayoutTests(config)
    
    def generate_tests_for_panel_app(self, panel_app: PanelApp) -> List[GeneratedTest]:
        """Generate tests for a complete Panel application."""
        tests = []
        
        # Generate widget tests
        for widget in panel_app.widgets:
            widget_tests = self.widget_tests.generate_widget_tests(widget)
            tests.extend(widget_tests)
        
        # Generate callback tests
        for callback in panel_app.callbacks:
            callback_tests = self.callback_tests.generate_callback_tests(callback, panel_app.widgets)
            tests.extend(callback_tests)
        
        # Generate layout tests
        for layout in panel_app.layouts:
            layout_tests = self.layout_tests.generate_layout_tests(layout, panel_app.widgets)
            tests.extend(layout_tests)
        
        # Generate integration tests
        integration_tests = self._generate_integration_tests(panel_app)
        tests.extend(integration_tests)
        
        return tests
    
    def _generate_integration_tests(self, panel_app: PanelApp) -> List[GeneratedTest]:
        """Generate integration tests for the entire Panel app."""
        tests = []
        
        # App initialization test
        init_test_content = f"""def test_panel_app_initialization():
    \"\"\"Test Panel app initialization.\"\"\"
    # Arrange
    app = create_panel_app()
    
    # Assert
    assert app is not None
    assert hasattr(app, 'widgets')
    assert hasattr(app, 'callbacks')
    assert hasattr(app, 'layouts')
"""
        
        init_test = GeneratedTest(
            name="test_panel_app_initialization",
            content=init_test_content,
            imports=self._get_app_imports(),
            fixtures=[],
            mocks=[],
            parametrize=None
        )
        tests.append(init_test)
        
        # Widget-callback integration test
        if panel_app.widgets and panel_app.callbacks:
            integration_test_content = """def test_widget_callback_integration():
    \"\"\"Test widget-callback integration.\"\"\"
    # Arrange
    widget = TextInput()
    callback = mock_callback_function
    
    # Act
    widget.param.watch(callback, 'value')
    widget.value = "test"
    
    # Assert
    assert callback.called
"""
            
            integration_test = GeneratedTest(
                name="test_widget_callback_integration",
                content=integration_test_content,
                imports=self._get_app_imports(),
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(integration_test)
        
        return tests
    
    def _get_app_imports(self) -> Set[str]:
        """Get imports needed for Panel app tests."""
        return {
            "import panel as pn",
            "from unittest.mock import Mock, patch",
            "import pytest"
        }