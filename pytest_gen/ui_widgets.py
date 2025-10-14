"""
UI widgets and components for the Panel GUI.
"""

import panel as pn
from panel.widgets import Button, TextAreaInput
from typing import List


class ActionWidgets:
    """Action buttons and controls for test generation."""
    
    def __init__(self):
        self.widgets = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """Create action widgets."""
        self.widgets['generate_btn'] = Button(
            name="🎯 Generate Tests",
            button_type="primary",
            width=150,
            height=40
        )
        
        self.widgets['preview_btn'] = Button(
            name="🔍 Preview",
            button_type="default",
            width=100,
            height=40
        )
        
        self.widgets['clear_btn'] = Button(
            name="🗑️ Clear",
            button_type="light",
            width=100,
            height=40
        )
        
        self.widgets['save_config_btn'] = Button(
            name="💾 Save Config",
            button_type="light",
            width=120,
            height=40
        )
        
        self.widgets['load_config_btn'] = Button(
            name="📁 Load Config",
            button_type="light",
            width=120,
            height=40
        )
    
    def get_layout(self):
        """Get action buttons layout."""
        return pn.Row(
            self.widgets['generate_btn'],
            self.widgets['preview_btn'],
            self.widgets['clear_btn'],
            pn.Spacer(),
            self.widgets['save_config_btn'],
            self.widgets['load_config_btn']
        )


class PreviewWidget:
    """Preview widget for generated test code."""
    
    def __init__(self):
        self.widgets = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """Create preview widgets."""
        self.widgets['preview_text'] = TextAreaInput(
            name="Generated Test Preview",
            value="# Select files and click 'Preview' to see generated tests...",
            height=400,
            width=800,
            readonly=True
        )
        
        self.widgets['progress'] = pn.indicators.Progress(
            name="Generation Progress",
            value=0,
            bar_color="primary",
            width=800
        )
        
        self.widgets['status'] = pn.pane.HTML(
            "<div style='padding: 10px; background: #f0f0f0;'>Ready</div>",
            width=800
        )
    
    def update_preview(self, content: str):
        """Update the preview content."""
        self.widgets['preview_text'].value = content
    
    def update_progress(self, value: float, message: str = ""):
        """Update progress indicator."""
        self.widgets['progress'].value = value
        if message:
            self.widgets['status'].object = f"<div style='padding: 10px; background: #f0f0f0;'>{message}</div>"
    
    def show_error(self, error_message: str):
        """Show error message."""
        self.widgets['preview_text'].value = f"# Error\n{error_message}"
        self.widgets['status'].object = f"<div style='padding: 10px; background: #ffebee; color: #c62828;'>{error_message}</div>"
    
    def show_success(self, message: str):
        """Show success message."""
        self.widgets['status'].object = f"<div style='padding: 10px; background: #e8f5e8; color: #2e7d32;'>{message}</div>"
    
    def get_layout(self):
        """Get preview layout."""
        return pn.Column(
            self.widgets['progress'],
            self.widgets['status'],
            self.widgets['preview_text']
        )


class FileTreeWidget:
    """Simple file tree widget for directory navigation."""
    
    def __init__(self, root_path: str = None):
        self.root_path = root_path or "."
        self.widgets = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """Create file tree widgets."""
        self.widgets['tree'] = pn.pane.HTML(
            self._generate_tree_html(),
            width=300,
            height=400
        )
        
        self.widgets['refresh_btn'] = Button(
            name="🔄",
            button_type="light",
            width=40
        )
    
    def _generate_tree_html(self) -> str:
        """Generate HTML for file tree."""
        import os
        from pathlib import Path
        
        def tree_html(path: Path, level: int = 0) -> str:
            html = ""
            indent = "  " * level
            
            try:
                items = sorted(path.iterdir())
                for item in items:
                    if item.is_dir():
                        html += f"{indent}<div>📁 {item.name}</div>\n"
                        html += tree_html(item, level + 1)
                    else:
                        html += f"{indent}<div>📄 {item.name}</div>\n"
            except PermissionError:
                html += f"{indent}<div>❌ Permission denied</div>\n"
            
            return html
        
        root = Path(self.root_path)
        html = f"<div style='font-family: monospace; font-size: 12px;'>{tree_html(root)}</div>"
        return html
    
    def get_layout(self):
        """Get file tree layout."""
        return pn.Column(
            pn.Row(
                pn.pane.HTML("<b>File Tree</b>"),
                self.widgets['refresh_btn'],
                pn.Spacer()
            ),
            self.widgets['tree']
        )
