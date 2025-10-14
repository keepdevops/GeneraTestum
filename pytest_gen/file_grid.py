"""
Interactive file browser with Panel Tabulator for file selection.
"""

import os
import pandas as pd
from typing import List, Dict, Any, Optional
import panel as pn
from pathlib import Path
from .file_grid_widgets import FileGridWidgets
from .file_grid_operations import FileGridOperations


class FileGrid:
    """Interactive file grid with Tabulator for file selection."""
    
    def __init__(self):
        self.current_path = Path.cwd()
        self.selected_files = []
        self.file_data = pd.DataFrame()
        
        # Initialize components
        self.widgets = FileGridWidgets(self)
        self.operations = FileGridOperations(self)
        
        # Load initial files
        self._load_files()
    
    def _load_files(self):
        """Load files from current directory."""
        self.operations.load_files()
    
    def _apply_filter(self):
        """Apply file type filter."""
        self.operations.apply_filter()
    
    def get_selected_files(self) -> List[str]:
        """Get list of selected file paths."""
        return self.operations.get_selected_files()
    
    def get_selected_file_info(self) -> List[Dict[str, Any]]:
        """Get detailed information about selected files."""
        return self.operations.get_selected_file_info()
    
    def navigate_to_parent(self):
        """Navigate to parent directory."""
        self.operations.navigate_to_parent()
    
    def navigate_to_subdirectory(self, directory_name: str):
        """Navigate to subdirectory."""
        self.operations.navigate_to_subdirectory(directory_name)
    
    def get_layout(self):
        """Get the complete file grid layout."""
        return self.widgets.get_layout()
    
    def update_path(self, new_path: str):
        """Update current path."""
        self.operations.update_path(new_path)
    
    def clear_selection(self):
        """Clear file selection."""
        self.operations.clear_selection()
    
    def select_files_by_pattern(self, pattern: str):
        """Select files matching pattern."""
        self.operations.select_files_by_pattern(pattern)