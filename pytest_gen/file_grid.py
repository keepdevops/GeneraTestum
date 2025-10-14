"""
Interactive file browser with Panel Tabulator for file selection.
"""

import os
import pandas as pd
from typing import List, Dict, Any, Optional
import panel as pn
from panel.widgets import Tabulator, TextInput, Button, Select
from pathlib import Path


class FileGrid:
    """Interactive file grid with Tabulator for file selection."""
    
    def __init__(self):
        self.current_path = Path.cwd()
        self.selected_files = []
        self.file_data = pd.DataFrame()
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
            value=str(self.current_path),
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
            value=self.file_data,
            selectable='checkbox',
            sortable=True,
            pagination='remote',
            page_size=50,
            layout='fit_columns',
            theme='modern',
            width=800,
            height=400
        )
        
        # Wire callbacks
        self.path_input.param.watch(self._on_path_change, 'value')
        self.refresh_button.param.watch(self._on_refresh, 'clicks')
        self.file_filter.param.watch(self._on_filter_change, 'value')
        self.grid.param.watch(self._on_selection_change, 'selection')
        
        # Initial load
        self._load_files()
    
    def _load_files(self):
        """Load files from current directory."""
        try:
            files = []
            for item in self.current_path.iterdir():
                if item.is_file():
                    files.append({
                        'Name': item.name,
                        'Type': item.suffix,
                        'Size': self._format_size(item.stat().st_size),
                        'Modified': pd.to_datetime(item.stat().st_mtime, unit='s').strftime('%Y-%m-%d %H:%M'),
                        'Path': str(item),
                        'Full_Path': str(item.absolute())
                    })
            
            self.file_data = pd.DataFrame(files)
            self._apply_filter()
            
        except PermissionError:
            pn.state.notifications.error(f"Permission denied: {self.current_path}")
        except Exception as e:
            pn.state.notifications.error(f"Error loading files: {str(e)}")
    
    def _apply_filter(self):
        """Apply file type filter."""
        if self.file_filter.value == "All":
            filtered_data = self.file_data
        else:
            extension_map = {
                "Python (.py)": ".py",
                "Java (.java)": ".java",
                "JavaScript (.js)": ".js",
                "TypeScript (.ts)": ".ts"
            }
            
            extension = extension_map.get(self.file_filter.value, "")
            if extension:
                filtered_data = self.file_data[self.file_data['Type'] == extension]
            else:
                filtered_data = self.file_data
        
        self.grid.value = filtered_data
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def _on_path_change(self, event):
        """Handle path input change."""
        new_path = event.new
        try:
            self.current_path = Path(new_path)
            if self.current_path.exists() and self.current_path.is_dir():
                self._load_files()
            else:
                pn.state.notifications.warning(f"Path does not exist: {new_path}")
        except Exception as e:
            pn.state.notifications.error(f"Invalid path: {str(e)}")
    
    def _on_refresh(self, event):
        """Handle refresh button click."""
        self._load_files()
        pn.state.notifications.success("Files refreshed")
    
    def _on_filter_change(self, event):
        """Handle file filter change."""
        self._apply_filter()
    
    def _on_selection_change(self, event):
        """Handle file selection change."""
        self.selected_files = event.new if event.new else []
    
    def get_selected_files(self) -> List[str]:
        """Get list of selected file paths."""
        return [row['Full_Path'] for row in self.selected_files]
    
    def get_selected_file_info(self) -> List[Dict[str, Any]]:
        """Get detailed info about selected files."""
        return self.selected_files.copy()
    
    def navigate_to_parent(self):
        """Navigate to parent directory."""
        if self.current_path.parent != self.current_path:
            self.current_path = self.current_path.parent
            self.path_input.value = str(self.current_path)
            self._load_files()
    
    def navigate_to_subdirectory(self, directory_name: str):
        """Navigate to subdirectory."""
        new_path = self.current_path / directory_name
        if new_path.exists() and new_path.is_dir():
            self.current_path = new_path
            self.path_input.value = str(self.current_path)
            self._load_files()
    
    def get_layout(self):
        """Get the complete Panel layout for the file grid."""
        return pn.Column(
            pn.Row(
                self.path_input,
                self.refresh_button,
                self.file_filter,
                pn.Spacer(width=50)
            ),
            pn.Row(
                self.grid,
                pn.Spacer(width=50)
            ),
            pn.Row(
                pn.pane.HTML(f"<b>Selected:</b> {len(self.selected_files)} files"),
                pn.Spacer()
            )
        )
    
    def update_path(self, new_path: str):
        """Update the current path programmatically."""
        self.path_input.value = new_path
        self._on_path_change(type('Event', (), {'new': new_path})())
    
    def clear_selection(self):
        """Clear current file selection."""
        self.grid.selection = []
        self.selected_files = []
    
    def select_files_by_pattern(self, pattern: str):
        """Select files matching a pattern."""
        import fnmatch
        matching_indices = []
        
        for i, row in self.file_data.iterrows():
            if fnmatch.fnmatch(row['Name'], pattern):
                matching_indices.append(i)
        
        if matching_indices:
            self.grid.selection = [self.file_data.iloc[i].to_dict() for i in matching_indices]
            self.selected_files = self.grid.selection
