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


class PanelTestGenerator:
    """Generates Panel-specific test cases."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.templates = PanelTestTemplates()
    
    def generate_tests_for_panel_app(self, panel_app: PanelApp) -> List[GeneratedTest]:
        """Generate tests for a complete Panel application."""
        tests = []
        
        # Generate widget tests
        for widget in panel_app.widgets:
            widget_tests = self._generate_widget_tests(widget)
            tests.extend(widget_tests)
        
        # Generate callback tests
        for callback in panel_app.callbacks:
            callback_tests = self._generate_callback_tests(callback, panel_app.widgets)
            tests.extend(callback_tests)
        
        # Generate layout tests
        for layout in panel_app.layouts:
            layout_tests = self._generate_layout_tests(layout, panel_app.widgets)
            tests.extend(layout_tests)
        
        # Generate integration tests
        integration_tests = self._generate_integration_tests(panel_app)
        tests.extend(integration_tests)
        
        return tests
    
    def _generate_widget_tests(self, widget: PanelWidget) -> List[GeneratedTest]:
        """Generate tests for a Panel widget."""
        tests = []
        
        # Widget initialization test
        init_test = GeneratedTest(
            name=f"test_{widget.name}_initialization",
            content=self.templates.widget_init_test(widget.name, widget.widget_type),
            imports=self._get_widget_imports(),
            fixtures=[],
            mocks=[],
            parametrize=[],
            file_path="",
            line_count=0
        )
        tests.append(init_test)
        
        # Widget property tests
        for param_name, param_value in widget.parameters:
            if param_name in ['value', 'options', 'disabled', 'visible']:
                prop_test = GeneratedTest(
                    name=f"test_{widget.name}_{param_name}_property",
                    content=self.templates.widget_property_test(widget.name, widget.widget_type, param_name, param_value),
                    imports=self._get_widget_imports(),
                    fixtures=[],
                    mocks=[],
                    parametrize=[],
                    file_path="",
                    line_count=0
                )
                tests.append(prop_test)
        
        # Widget callback tests
        for callback_name in widget.callbacks:
            callback_test = GeneratedTest(
                name=f"test_{widget.name}_{callback_name}_callback",
                content=self.templates.widget_callback_test(widget.name, widget.widget_type, callback_name),
                imports=self._get_widget_imports(),
                fixtures=[],
                mocks=[],
                parametrize=[],
                file_path="",
                line_count=0
            )
            tests.append(callback_test)
        
        return tests
    
    def _generate_callback_tests(self, callback: PanelCallback, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate tests for Panel callbacks."""
        tests = []
        
        # Basic callback test
        basic_test = GeneratedTest(
            name=f"test_{callback.name}_callback",
            content=self.templates.callback_test(callback.name, callback.widget_dependencies),
            imports=self._get_callback_imports(),
            fixtures=[],
            mocks=[],
            parametrize=[],
            file_path="",
            line_count=0
        )
        tests.append(basic_test)
        
        # Reactive parameter tests
        if callback.reactive_params:
            reactive_test = GeneratedTest(
                name=f"test_{callback.name}_reactive_params",
                content=self.templates.reactive_test(callback.name, callback.widget_dependencies),
                imports=self._get_callback_imports(),
                fixtures=[],
                mocks=[],
                parametrize=[],
                file_path="",
                line_count=0
            )
            tests.append(reactive_test)
        
        return tests
    
    def _generate_layout_tests(self, layout: PanelLayout, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate tests for Panel layouts."""
        tests = []
        
        # Layout creation test
        layout_test = GeneratedTest(
            name=f"test_{layout.name}_layout",
            content=self.templates.layout_test(layout.name, layout.layout_type, layout.children),
            imports=self._get_layout_imports(),
            fixtures=[],
            mocks=[],
            parametrize=[],
            file_path="",
            line_count=0
        )
        tests.append(layout_test)
        
        return tests
    
    def _generate_integration_tests(self, panel_app: PanelApp) -> List[GeneratedTest]:
        """Generate integration tests for the complete Panel app."""
        tests = []
        
        # App creation test
        widget_names = [widget.name for widget in panel_app.widgets]
        app_test = GeneratedTest(
            name="test_app_creation",
            content=self.templates.app_test(widget_names),
            imports=self._get_app_imports(),
            fixtures=[],
            mocks=[],
            parametrize=[],
            file_path="",
            line_count=0
        )
        tests.append(app_test)
        
        # Widget interaction test
        if panel_app.widgets and panel_app.callbacks:
            widget_names = [widget.name for widget in panel_app.widgets]
            interaction_test = GeneratedTest(
                name="test_widget_interactions",
                content=self.templates.interaction_test(widget_names),
                imports=self._get_app_imports(),
                fixtures=[],
                mocks=[],
                parametrize=[],
                file_path="",
                line_count=0
            )
            tests.append(interaction_test)
        
        return tests
    
    def _get_widget_imports(self) -> Set[str]:
        """Get imports needed for widget tests."""
        return {
            "import panel as pn",
            "from unittest.mock import Mock"
        }
    
    def _get_callback_imports(self) -> Set[str]:
        """Get imports needed for callback tests."""
        return {
            "import panel as pn",
            "from unittest.mock import Mock"
        }
    
    def _get_layout_imports(self) -> Set[str]:
        """Get imports needed for layout tests."""
        return {
            "import panel as pn"
        }
    
    def _get_app_imports(self) -> Set[str]:
        """Get imports needed for app tests."""
        return {
            "import panel as pn",
            "from unittest.mock import Mock"
        }