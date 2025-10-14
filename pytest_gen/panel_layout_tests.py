"""
Layout-specific test generation for Panel applications.
"""

from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .panel_models import PanelWidget, PanelCallback, PanelLayout, PanelApp
from .test_models import GeneratedTest
from .mock_generator import MockInfo
from .fixture_models import FixtureInfo
from .panel_test_templates import PanelTestTemplates


class PanelLayoutTests:
    """Layout-specific test generation for Panel applications."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.templates = PanelTestTemplates()
    
    def generate_layout_tests(self, layout: PanelLayout, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate tests for a Panel layout."""
        tests = []
        
        # Layout initialization test
        init_test = self._generate_layout_init_test(layout)
        tests.append(init_test)
        
        # Layout children tests
        children_tests = self._generate_layout_children_tests(layout, widgets)
        tests.extend(children_tests)
        
        # Layout parameter tests
        param_tests = self._generate_layout_parameter_tests(layout)
        tests.extend(param_tests)
        
        return tests
    
    def _generate_layout_init_test(self, layout: PanelLayout) -> GeneratedTest:
        """Generate layout initialization test."""
        content = f"""def test_{layout.name}_initialization():
    \"\"\"Test {layout.name} layout initialization.\"\"\"
    # Arrange
    layout = {layout.layout_type}()
    
    # Assert
    assert layout is not None
    assert isinstance(layout, {layout.layout_type})
"""
        
        return GeneratedTest(
            name=f"test_{layout.name}_initialization",
            content=content,
            imports={"import panel as pn"},
            fixtures=[],
            mocks=[],
            parametrize=None
        )
    
    def _generate_layout_children_tests(self, layout: PanelLayout, widgets: List[PanelWidget]) -> List[GeneratedTest]:
        """Generate layout children tests."""
        tests = []
        
        if layout.children:
            test_content = f"""def test_{layout.name}_children():
    \"\"\"Test {layout.name} layout children.\"\"\"
    # Arrange
    children = [
        {', '.join([f'{w.widget_type}()' for w in widgets[:3]])}
    ]
    
    # Act
    layout = {layout.layout_type}(*children)
    
    # Assert
    assert len(layout) == len(children)
    for child in children:
        assert child in layout
"""
            
            test = GeneratedTest(
                name=f"test_{layout.name}_children",
                content=test_content,
                imports={"import panel as pn"},
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(test)
        
        return tests
    
    def _generate_layout_parameter_tests(self, layout: PanelLayout) -> List[GeneratedTest]:
        """Generate layout parameter tests."""
        tests = []
        
        for param_name, param_value in layout.parameters.items():
            test_content = f"""def test_{layout.name}_{param_name}_parameter():
    \"\"\"Test {layout.name} {param_name} parameter.\"\"\"
    # Arrange
    layout = {layout.layout_type}({param_name}={param_value})
    
    # Assert
    assert hasattr(layout, '{param_name}')
"""
            
            test = GeneratedTest(
                name=f"test_{layout.name}_{param_name}_parameter",
                content=test_content,
                imports={"import panel as pn"},
                fixtures=[],
                mocks=[],
                parametrize=None
            )
            tests.append(test)
        
        return tests
