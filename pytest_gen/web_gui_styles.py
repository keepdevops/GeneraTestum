"""
Web GUI styles orchestrator.
"""

from .web_gui_css import WebGUICSS
from .web_gui_javascript import WebGUIJavaScript


class WebGUIStyles:
    """Web GUI styles orchestrator."""
    
    def __init__(self):
        self.css = WebGUICSS()
        self.js = WebGUIJavaScript()
    
    def get_css_styles(self) -> str:
        return self.css.get_base_styles()
    
    def get_javascript(self) -> str:
        return self.js.get_core_functions()
    
    def get_error_styles(self) -> str:
        return self.css.get_error_styles()
    
    def get_component_styles(self) -> str:
        return self.css.get_component_styles()
    
    def get_test_functions(self) -> str:
        return self.js.get_test_functions()
    
    def get_settings_functions(self) -> str:
        return self.js.get_settings_functions()
    
    def get_all_javascript(self) -> str:
        return f"""
        {self.js.get_core_functions()}
        {self.js.get_test_functions()}
        {self.js.get_settings_functions()}
        """