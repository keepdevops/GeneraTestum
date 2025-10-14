"""
Widget setup and event handlers for file grid.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
import panel as pn
from panel.widgets import Tabulator, TextInput, Button, Select
from pathlib import Path


class FileGridWidgets:
    """Widget setup and event handlers for file grid."""
    
    def __init__(self, file_grid):
        self.file_grid = file_grid
        self.grid = None
        self.path_input = None
        self.refresh_button = None
        self.file_filter = None
        self._setup_widgets()
    
    def _setup_widgets(self):
        """Setup Panel widgets for file grid."""
        # Path input
        self.path_input = TextInput(
            name="Directory Path",
            value=str(self.file_grid.current_path),
            width=400
        )
        
        # Refresh button
        self.refresh_button = Button(
            name="🔄 Refresh",
            button_type="primary",
            width=100
        )
        
        # File type filter
        self.file_filter = Select(
            name="File Type",
            options=["All", "Python (.py)", "Java (.java)", "JavaScript (.js)", "TypeScript (.ts)"],
            value="All",
            width=150
        )
        
        # File grid
        self.grid = Tabulator(
            value=pd.DataFrame(),
            selection=[],
            show_index=False,
            height=400,
            pagination='remote',
            page_size=50,
            sizing_mode='stretch_width'
        )
        
        # Setup event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Setup event handlers for widgets."""
        self.path_input.param.watch(self._on_path_change, 'value')
        self.refresh_button.param.watch(self._on_refresh, 'clicks')
        self.file_filter.param.watch(self._on_filter_change, 'value')
        self.grid.param.watch(self._on_selection_change, 'selection')
    
    def _on_path_change(self, event):
        """Handle path input change."""
        try:
            new_path = Path(event.new)
            if new_path.exists() and new_path.is_dir():
                self.file_grid.current_path = new_path
                self.file_grid._load_files()
        except Exception as e:
            print(f"Invalid path: {e}")
    
    def _on_refresh(self, event):
        """Handle refresh button click."""
        self.file_grid._load_files()
    
    def _on_filter_change(self, event):
        """Handle file filter change."""
        self.file_grid._apply_filter()
    
    def _on_selection_change(self, event):
        """Handle file selection change."""
        if event.new:
            self.file_grid.selected_files = [row['path'] for row in event.new]
    
    def get_layout(self):
        """Get the complete widget layout."""
        return pn.Column(
            pn.Row(
                self.path_input,
                self.refresh_button,
                self.file_filter,
                sizing_mode='stretch_width'
            ),
            self.grid,
            sizing_mode='stretch_width'
        )
