"""
Layout components for the Panel GUI.
"""

import panel as pn
from typing import Any
from .file_grid import FileGrid
from .config_widgets import ConfigWidgets
from .ui_widgets import ActionWidgets, PreviewWidget, FileTreeWidget


class GUILayouts:
    """Layout components for the Panel GUI."""
    
    def __init__(self, file_grid: FileGrid, config_widgets: ConfigWidgets, 
                 action_widgets: ActionWidgets, preview_widget: PreviewWidget, 
                 file_tree: FileTreeWidget):
        self.file_grid = file_grid
        self.config_widgets = config_widgets
        self.action_widgets = action_widgets
        self.preview_widget = preview_widget
        self.file_tree = file_tree
    
    def create_header(self) -> pn.Row:
        """Create the application header."""
        return pn.Row(
            pn.pane.HTML(
                "<h1>🎯 Pytest Code Generator</h1>",
                margin=(10, 0, 20, 0)
            ),
            pn.Spacer(),
            pn.pane.HTML(
                "<p style='text-align: right; color: #666;'>v1.0.0</p>",
                margin=(10, 0, 0, 0)
            )
        )
    
    def create_file_browser_tab(self) -> pn.Row:
        """Create the file browser tab."""
        return pn.Row(
            # File grid (left side)
            pn.Column(
                pn.pane.HTML("<h3>📁 File Selection</h3>"),
                self.file_grid.get_layout(),
                width=800
            ),
            pn.Spacer(width=20),
            # File tree (right side)
            pn.Column(
                self.file_tree.get_layout(),
                width=300
            )
        )
    
    def create_config_tab(self) -> pn.Column:
        """Create the configuration tab."""
        return pn.Column(
            pn.pane.HTML("<h3>⚙️ Test Generation Configuration</h3>"),
            self.config_widgets.get_layout(),
            pn.Divider(),
            self.action_widgets.get_layout()
        )
    
    def create_preview_tab(self) -> pn.Column:
        """Create the preview tab."""
        return pn.Column(
            pn.pane.HTML("<h3>🔍 Generated Test Preview</h3>"),
            self.preview_widget.get_layout()
        )
    
    def create_results_tab(self) -> pn.Column:
        """Create the results tab."""
        results_text = pn.pane.HTML(
            "<div style='padding: 20px; text-align: center; color: #666;'>"
            "Generated test files will appear here after running the generator."
            "</div>",
            height=400
        )
        
        return pn.Column(
            pn.pane.HTML("<h3>📊 Generation Results</h3>"),
            results_text
        )
    
    def create_main_layout(self) -> pn.Column:
        """Create the complete main layout."""
        # Header
        header = self.create_header()
        
        # Main content area
        main_content = pn.Tabs(
            ("📁 File Browser", self.create_file_browser_tab()),
            ("⚙️ Configuration", self.create_config_tab()),
            ("🔍 Preview", self.create_preview_tab()),
            ("📊 Results", self.create_results_tab())
        )
        
        # Assemble complete layout
        return pn.Column(
            header,
            pn.Divider(),
            main_content,
            sizing_mode='stretch_width'
        )
