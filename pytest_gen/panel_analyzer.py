"""
Panel application analysis for widget and callback detection.
"""

import ast
from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .panel_models import PanelWidget, PanelCallback, PanelLayout, PanelApp
from .panel_ast_analyzer import PanelASTAnalyzer


class PanelAnalyzer:
    """Analyzes Panel applications to extract widgets, callbacks, and layouts."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.widget_types = {
            'pn.widgets.Button': 'Button',
            'pn.widgets.TextInput': 'TextInput',
            'pn.widgets.IntSlider': 'IntSlider',
            'pn.widgets.FloatSlider': 'FloatSlider',
            'pn.widgets.Select': 'Select',
            'pn.widgets.MultiSelect': 'MultiSelect',
            'pn.widgets.Checkbox': 'Checkbox',
            'pn.widgets.RadioBox': 'RadioBox',
            'pn.widgets.DatePicker': 'DatePicker',
            'pn.widgets.TextAreaInput': 'TextAreaInput',
            'pn.widgets.PasswordInput': 'PasswordInput',
            'pn.widgets.FileInput': 'FileInput',
        }
        self.layout_types = {
            'pn.Row': 'Row',
            'pn.Column': 'Column',
            'pn.Tabs': 'Tabs',
            'pn.GridBox': 'GridBox',
            'pn.Spacer': 'Spacer',
        }
    
    def analyze_file(self, file_path: str) -> Optional[PanelApp]:
        """Analyze a Panel file and extract application information."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.analyze_code(content, file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[PanelApp]:
        """Analyze Panel code string."""
        if not self._has_panel_indicators(code):
            return None
        
        tree = ast.parse(code)
        analyzer = PanelASTAnalyzer(self.widget_types, self.layout_types)
        analyzer.visit(tree)
        
        return PanelApp(
            name=self._extract_app_name(file_path),
            widgets=analyzer.widgets,
            callbacks=analyzer.callbacks,
            layouts=analyzer.layouts,
            imports=analyzer.imports,
            dependencies=analyzer.dependencies,
            file_path=file_path,
            entry_point=analyzer.entry_point
        )
    
    def _has_panel_indicators(self, content: str) -> bool:
        """Check if content has Panel framework indicators."""
        panel_indicators = [
            'import panel',
            'import panel as pn',
            'from panel import',
            'pn.widgets',
            'pn.Row',
            'pn.Column',
            'pn.bind',
            'pn.depends',
            '@pn.depends'
        ]
        
        content_lower = content.lower()
        return any(indicator in content for indicator in panel_indicators)
    
    def _extract_app_name(self, file_path: str) -> str:
        """Extract application name from file path."""
        import os
        return os.path.splitext(os.path.basename(file_path))[0]
