"""
Core event handlers for GUI interactions.
"""

import os
from typing import Dict, Any, List
from .generator_core import GeneratorCore


class GUIEventHandlers:
    """Core event handlers for GUI interactions."""
    
    def __init__(self, generator: GeneratorCore, preview_widget, file_grid, config_widgets):
        self.generator = generator
        self.preview_widget = preview_widget
        self.file_grid = file_grid
        self.config_widgets = config_widgets
    
    def handle_generate_tests(self, event):
        """Handle test generation."""
        try:
            # Get selected files
            selected_files = self.file_grid.get_selected_files()
            
            if not selected_files:
                self.preview_widget.show_error("No files selected. Please select files from the File Browser tab.")
                return
            
            # Get configuration
            config = self.config_widgets.get_config_from_widgets()
            
            # Update generator config
            self.generator.config = config
            
            # Show progress
            self.preview_widget.update_progress(0.1, "Starting test generation...")
            
            # Generate tests for each file
            all_generated_files = []
            total_files = len(selected_files)
            
            for i, file_path in enumerate(selected_files):
                try:
                    progress = (i + 1) / total_files
                    self.preview_widget.update_progress(progress, f"Processing {os.path.basename(file_path)}...")
                    
                    # Generate tests
                    generated_files = self.generator.generate_tests(file_path)
                    all_generated_files.extend(generated_files)
                    
                except Exception as e:
                    self.preview_widget.show_error(f"Error processing {file_path}: {str(e)}")
                    continue
            
            # Show results
            if all_generated_files:
                results_html = self._generate_results_html(all_generated_files)
                self.preview_widget.show_results(results_html)
                self.preview_widget.update_progress(1.0, f"Generated {len(all_generated_files)} test files successfully!")
            else:
                self.preview_widget.show_error("No test files were generated. Please check your selection and configuration.")
            
        except Exception as e:
            self.preview_widget.show_error(f"Test generation failed: {str(e)}")
    
    def handle_preview_tests(self, event):
        """Handle test preview."""
        try:
            # Get selected files
            selected_files = self.file_grid.get_selected_files()
            
            if not selected_files:
                self.preview_widget.show_error("No files selected. Please select files from the File Browser tab.")
                return
            
            # Get configuration
            config = self.config_widgets.get_config_from_widgets()
            
            # Analyze first selected file
            file_path = selected_files[0]
            analysis = self.generator.analyze_source(file_path)
            
            # Generate preview content
            preview_content = self._generate_preview_content(file_path, analysis, config)
            
            # Show preview
            self.preview_widget.show_preview(preview_content)
            
        except Exception as e:
            self.preview_widget.show_error(f"Preview generation failed: {str(e)}")
    
    def handle_clear_selection(self, event):
        """Handle clear selection."""
        self.file_grid.clear_selection()
        self.preview_widget.clear_content()
    
    def handle_refresh_tree(self, event):
        """Handle refresh file tree."""
        self.file_grid._load_files()
        self.preview_widget.show_info("File tree refreshed.")
    
    def _generate_results_html(self, generated_files: List[str]) -> str:
        """Generate HTML results display."""
        html = "<div style='font-family: Arial, sans-serif;'>"
        html += "<h2>🎉 Test Generation Complete!</h2>"
        html += f"<p><strong>Generated {len(generated_files)} test files:</strong></p>"
        html += "<ul>"
        
        for file_path in generated_files:
            filename = os.path.basename(file_path)
            html += f"<li><code>{filename}</code></li>"
        
        html += "</ul>"
        html += "<p><em>You can now run these tests with <code>pytest</code>!</em></p>"
        html += "</div>"
        
        return html
