"""
File operations and navigation for file grid.
"""

import os
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path


class FileGridOperations:
    """File operations and navigation for file grid."""
    
    def __init__(self, file_grid):
        self.file_grid = file_grid
    
    def load_files(self):
        """Load files from current directory."""
        files = []
        
        try:
            for item in self.file_grid.current_path.iterdir():
                if item.is_file():
                    stat = item.stat()
                    file_info = {
                        'name': item.name,
                        'path': str(item),
                        'size': stat.st_size,
                        'modified': pd.Timestamp.fromtimestamp(stat.st_mtime),
                        'type': item.suffix.lower(),
                        'size_formatted': self._format_size(stat.st_size)
                    }
                    files.append(file_info)
                elif item.is_dir():
                    dir_info = {
                        'name': f"📁 {item.name}",
                        'path': str(item),
                        'size': 0,
                        'modified': pd.Timestamp.now(),
                        'type': 'directory',
                        'size_formatted': ''
                    }
                    files.append(dir_info)
            
            self.file_grid.file_data = pd.DataFrame(files)
            self.file_grid._apply_filter()
            
        except Exception as e:
            print(f"Error loading files: {e}")
            self.file_grid.file_data = pd.DataFrame()
    
    def apply_filter(self):
        """Apply file type filter."""
        if self.file_grid.file_data.empty:
            self.file_grid.widgets.grid.value = pd.DataFrame()
            return
        
        filter_type = self.file_grid.widgets.file_filter.value
        
        if filter_type == "All":
            filtered_data = self.file_grid.file_data
        elif filter_type == "Python (.py)":
            filtered_data = self.file_grid.file_data[self.file_grid.file_data['type'] == '.py']
        elif filter_type == "Java (.java)":
            filtered_data = self.file_grid.file_data[self.file_grid.file_data['type'] == '.java']
        elif filter_type == "JavaScript (.js)":
            filtered_data = self.file_grid.file_data[self.file_grid.file_data['type'] == '.js']
        elif filter_type == "TypeScript (.ts)":
            filtered_data = self.file_grid.file_data[self.file_grid.file_data['type'] == '.ts']
        else:
            filtered_data = self.file_grid.file_data
        
        # Sort by name
        filtered_data = filtered_data.sort_values('name')
        self.file_grid.widgets.grid.value = filtered_data
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_selected_files(self) -> List[str]:
        """Get list of selected file paths."""
        return self.file_grid.selected_files.copy()
    
    def get_selected_file_info(self) -> List[Dict[str, Any]]:
        """Get detailed information about selected files."""
        selected_info = []
        for file_path in self.file_grid.selected_files:
            file_info = self.file_grid.file_data[self.file_grid.file_data['path'] == file_path]
            if not file_info.empty:
                selected_info.append(file_info.iloc[0].to_dict())
        return selected_info
    
    def navigate_to_parent(self):
        """Navigate to parent directory."""
        if self.file_grid.current_path.parent != self.file_grid.current_path:
            self.file_grid.current_path = self.file_grid.current_path.parent
            self.file_grid.widgets.path_input.value = str(self.file_grid.current_path)
            self.file_grid._load_files()
    
    def navigate_to_subdirectory(self, directory_name: str):
        """Navigate to subdirectory."""
        new_path = self.file_grid.current_path / directory_name
        if new_path.exists() and new_path.is_dir():
            self.file_grid.current_path = new_path
            self.file_grid.widgets.path_input.value = str(self.file_grid.current_path)
            self.file_grid._load_files()
    
    def update_path(self, new_path: str):
        """Update current path."""
        try:
            path = Path(new_path)
            if path.exists() and path.is_dir():
                self.file_grid.current_path = path
                self.file_grid.widgets.path_input.value = str(path)
                self.file_grid._load_files()
        except Exception as e:
            print(f"Invalid path: {e}")
    
    def clear_selection(self):
        """Clear file selection."""
        self.file_grid.selected_files = []
        self.file_grid.widgets.grid.selection = []
    
    def select_files_by_pattern(self, pattern: str):
        """Select files matching pattern."""
        if self.file_grid.file_data.empty:
            return
        
        matching_files = self.file_grid.file_data[
            self.file_grid.file_data['name'].str.contains(pattern, case=False, na=False)
        ]
        
        selected_paths = matching_files['path'].tolist()
        self.file_grid.selected_files = selected_paths
        self.file_grid.widgets.grid.selection = matching_files.to_dict('records')
