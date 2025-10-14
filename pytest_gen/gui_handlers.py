"""
Event handlers and business logic for the Panel GUI.
"""

import os
from typing import Dict, Any, List
from .generator_core import GeneratorCore
from .config import GeneratorConfig


class GUIHandlers:
    """Event handlers for GUI interactions."""
    
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
                    error_msg = f"Error processing {file_path}: {str(e)}"
                    self.preview_widget.show_error(error_msg)
                    return
            
            # Show success
            success_msg = f"Successfully generated {len(all_generated_files)} test files!"
            self.preview_widget.show_success(success_msg)
            self.preview_widget.update_progress(1.0, "Generation complete!")
            
            # Show results summary
            results_html = self._generate_results_html(all_generated_files)
            self.preview_widget.update_preview(results_html)
            
        except Exception as e:
            self.preview_widget.show_error(f"Generation failed: {str(e)}")
    
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
            
            # Generate preview for first selected file
            first_file = selected_files[0]
            
            # Analyze the file
            analysis = self.generator.analyze_source(first_file)
            
            # Generate preview content
            preview_content = self._generate_preview_content(first_file, analysis, config)
            
            self.preview_widget.update_preview(preview_content)
            self.preview_widget.show_success(f"Preview generated for {os.path.basename(first_file)}")
            
        except Exception as e:
            self.preview_widget.show_error(f"Preview failed: {str(e)}")
    
    def handle_clear_selection(self, event):
        """Handle clear selection."""
        self.file_grid.clear_selection()
        self.preview_widget.update_preview("# Selection cleared. Select files to generate tests.")
        self.preview_widget.show_success("Selection cleared")
    
    def handle_save_config(self, event):
        """Handle save configuration."""
        try:
            config = self.config_widgets.get_config_from_widgets()
            
            # Save to default location
            config_path = "pytest_gen_config.json"
            from .config import save_config_to_file
            save_config_to_file(config, config_path)
            
            self.preview_widget.show_success(f"Configuration saved to {config_path}")
            
        except Exception as e:
            self.preview_widget.show_error(f"Failed to save configuration: {str(e)}")
    
    def handle_load_config(self, event):
        """Handle load configuration."""
        try:
            # Load from default location
            config_path = "pytest_gen_config.json"
            
            if os.path.exists(config_path):
                from .config import load_config_from_file
                config = load_config_from_file(config_path)
                self.config_widgets.update_widgets_from_config(config)
                self.preview_widget.show_success(f"Configuration loaded from {config_path}")
            else:
                self.preview_widget.show_error(f"Configuration file not found: {config_path}")
                
        except Exception as e:
            self.preview_widget.show_error(f"Failed to load configuration: {str(e)}")
    
    def handle_refresh_tree(self, event):
        """Handle file tree refresh."""
        self.file_tree.widgets['tree'].object = self.file_tree._generate_tree_html()
        self.preview_widget.show_success("File tree refreshed")
    
    def _generate_preview_content(self, file_path: str, analysis: Dict[str, Any], config: GeneratorConfig) -> str:
        """Generate preview content for selected file."""
        content = f"# Test Generation Preview\n\n"
        content += f"**File:** `{file_path}`\n\n"
        
        if 'file_type' in analysis:
            content += f"**Detected Type:** {analysis['file_type']}\n\n"
        
        if 'functions' in analysis:
            content += f"**Functions Found:** {len(analysis['functions'])}\n"
            for func in analysis['functions']:
                content += f"- `{func['name']}` ({func['parameters']} parameters)\n"
            content += "\n"
        
        if 'classes' in analysis:
            content += f"**Classes Found:** {len(analysis['classes'])}\n"
            for cls in analysis['classes']:
                content += f"- `{cls['name']}` ({cls['methods']} methods)\n"
            content += "\n"
        
        if 'endpoints' in analysis:
            content += f"**API Endpoints Found:** {len(analysis['endpoints'])}\n"
            for endpoint in analysis['endpoints']:
                content += f"- `{endpoint['name']}` ({endpoint['method']} {endpoint['path']})\n"
            content += "\n"
        
        content += f"**Estimated Tests:** {analysis.get('estimated_tests', 0)}\n\n"
        content += "## Configuration\n\n"
        content += f"- Mock Level: {config.mock_level.value}\n"
        content += f"- Coverage: {config.coverage_type.value}\n"
        content += f"- Generate Fixtures: {config.generate_fixtures}\n"
        content += f"- Generate Parametrize: {config.generate_parametrize}\n"
        content += f"- Max Lines Per File: {config.max_lines_per_file}\n\n"
        
        content += "## Sample Generated Test\n\n"
        content += "```python\n"
        content += "import pytest\n"
        content += "from unittest.mock import patch, MagicMock\n\n"
        content += "def test_sample_function():\n"
        content += '    """Test sample function."""\n'
        content += "    # Arrange\n"
        content += "    input_value = 'test'\n\n"
        content += "    # Act\n"
        content += "    result = sample_function(input_value)\n\n"
        content += "    # Assert\n"
        content += "    assert result is not None\n"
        content += "```\n"
        
        return content
    
    def _generate_results_html(self, generated_files: List[str]) -> str:
        """Generate HTML for results summary."""
        html = "# Test Generation Results\n\n"
        html += f"**Total Files Generated:** {len(generated_files)}\n\n"
        
        html += "## Generated Test Files:\n\n"
        for file_path in generated_files:
            html += f"- `{file_path}`\n"
        
        html += "\n## Next Steps:\n\n"
        html += "1. Review the generated test files\n"
        html += "2. Run the tests: `pytest tests/`\n"
        html += "3. Customize tests as needed\n"
        html += "4. Add additional test cases for edge scenarios\n"
        
        return html
