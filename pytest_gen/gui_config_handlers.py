"""
Configuration management handlers for GUI.
"""

import json
from typing import Dict, Any
from .config import GeneratorConfig


class GUIConfigHandlers:
    """Configuration management handlers for GUI."""
    
    def __init__(self, generator, preview_widget, config_widgets):
        self.generator = generator
        self.preview_widget = preview_widget
        self.config_widgets = config_widgets
    
    def handle_save_config(self, event):
        """Handle save configuration."""
        try:
            # Get current configuration
            config = self.config_widgets.get_config_from_widgets()
            
            # Save to default location
            config_file = "pytest_gen_config.json"
            with open(config_file, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
            
            self.preview_widget.show_info(f"Configuration saved to {config_file}")
            
        except Exception as e:
            self.preview_widget.show_error(f"Failed to save configuration: {str(e)}")
    
    def handle_load_config(self, event):
        """Handle load configuration."""
        try:
            # Load from default location
            config_file = "pytest_gen_config.json"
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Update generator config
            config = GeneratorConfig.from_dict(config_data)
            self.generator.config = config
            
            # Update widgets
            self.config_widgets.update_widgets_from_config(config)
            
            self.preview_widget.show_info(f"Configuration loaded from {config_file}")
            
        except Exception as e:
            self.preview_widget.show_error(f"Failed to load configuration: {str(e)}")
