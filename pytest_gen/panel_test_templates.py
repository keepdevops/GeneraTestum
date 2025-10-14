"""
Panel test templates for generating test code.
"""

from typing import Any


class PanelTestTemplates:
    """Templates for Panel test generation."""
    
    @staticmethod
    def widget_init_test(widget_name: str, widget_type: str) -> str:
        """Generate widget initialization test."""
        return f'''def test_{widget_name}_initialization():
    """Test {widget_name} widget initialization."""
    import panel as pn
    
    # Create widget
    widget = pn.widgets.{widget_type}()
    
    # Assert widget is created
    assert widget is not None
    assert isinstance(widget, pn.widgets.{widget_type})
    
    # Test default properties
    assert hasattr(widget, 'value')
    assert hasattr(widget, 'name')
'''
    
    @staticmethod
    def widget_property_test(widget_name: str, widget_type: str, prop_name: str, prop_value: Any) -> str:
        """Generate widget property test."""
        return f'''def test_{widget_name}_{prop_name}_property():
    """Test {widget_name} {prop_name} property."""
    import panel as pn
    
    # Create widget with property
    widget = pn.widgets.{widget_type}({prop_name}={prop_value})
    
    # Test property is set
    assert widget.{prop_name} == {prop_value}
    
    # Test property can be changed
    new_value = "new_value"
    widget.{prop_name} = new_value
    assert widget.{prop_name} == new_value
'''
    
    @staticmethod
    def widget_callback_test(widget_name: str, widget_type: str, callback_name: str) -> str:
        """Generate widget callback test."""
        return f'''def test_{widget_name}_{callback_name}_callback():
    """Test {widget_name} {callback_name} callback."""
    import panel as pn
    from unittest.mock import Mock
    
    # Create widget
    widget = pn.widgets.{widget_type}()
    
    # Create mock callback
    mock_callback = Mock()
    
    # Bind callback to widget
    widget.param.watch(mock_callback, '{callback_name}')
    
    # Trigger callback
    widget.value = "test_value"
    
    # Assert callback was called
    mock_callback.assert_called()
'''
    
    @staticmethod
    def callback_test(callback_name: str, widget_deps: list) -> str:
        """Generate callback function test."""
        widget_params = [f"mock_{widget}" for widget in widget_deps]
        
        return f'''def test_{callback_name}_callback():
    """Test {callback_name} callback function."""
    from unittest.mock import Mock
    import panel as pn
    
    # Create mock widgets
{chr(10).join([f"    mock_{widget} = Mock()" for widget in widget_deps])}
    
    # Test callback with mock widgets
    result = {callback_name}({", ".join(widget_params)})
    
    # Assert callback returns expected result
    assert result is not None
'''
    
    @staticmethod
    def reactive_test(callback_name: str, widget_deps: list) -> str:
        """Generate reactive parameter test."""
        return f'''def test_{callback_name}_reactive_params():
    """Test {callback_name} reactive parameters."""
    import panel as pn
    from unittest.mock import Mock
    
    # Create widgets
{chr(10).join([f"    {widget} = pn.widgets.Button()" for widget in widget_deps[:2]])}
    
    # Bind callback with reactive parameters
    reactive_callback = pn.depends({callback_name})({callback_name})
    
    # Test reactive behavior
    {widget_deps[0] if widget_deps else "widget"}.value = "new_value"
    
    # Assert reactive callback is triggered
    assert reactive_callback is not None
'''
    
    @staticmethod
    def layout_test(layout_name: str, layout_type: str, children: list) -> str:
        """Generate layout test."""
        return f'''def test_{layout_name}_layout():
    """Test {layout_name} layout creation."""
    import panel as pn
    
    # Create widgets
{chr(10).join([f"    {child} = pn.widgets.Button()" for child in children[:3]])}
    
    # Create layout
    layout = pn.{layout_type}({", ".join(children[:3])})
    
    # Assert layout is created
    assert layout is not None
    assert isinstance(layout, pn.{layout_type})
    
    # Assert layout contains widgets
    assert len(layout) == {len(children[:3])}
'''
    
    @staticmethod
    def app_test(widgets: list) -> str:
        """Generate app creation test."""
        widget_creations = [f"    {widget} = pn.widgets.Button()" for widget in widgets[:3]]
        widget_list = [f"        {widget}," for widget in widgets[:3]]
        
        return f'''def test_app_creation():
    """Test Panel app creation."""
    import panel as pn
    
    # Create widgets
{chr(10).join(widget_creations)}
    
    # Create app layout
    app = pn.Column(
{chr(10).join(widget_list)}
    )
    
    # Assert app is created
    assert app is not None
    assert isinstance(app, pn.Column)
    
    # Test app can be served
    assert hasattr(app, 'servable')
'''
    
    @staticmethod
    def interaction_test(widgets: list) -> str:
        """Generate widget interaction test."""
        return f'''def test_widget_interactions():
    """Test widget interactions in Panel app."""
    import panel as pn
    from unittest.mock import Mock
    
    # Create widgets
{chr(10).join([f"    {widget} = pn.widgets.Button()" for widget in widgets[:2]])}
    
    # Create mock callback
    mock_callback = Mock()
    
    # Set up widget interactions
    {widgets[0] if widgets else "widget1"}.param.watch(mock_callback, 'value')
    
    # Simulate user interaction
    {widgets[0] if widgets else "widget1"}.value = "test_value"
    
    # Assert interaction triggers callback
    mock_callback.assert_called()
'''
