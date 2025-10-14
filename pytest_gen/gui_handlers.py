"""
Event handlers and business logic for the Panel GUI.
"""

import os
from typing import Dict, Any, List
from .generator_core import GeneratorCore
from .config import GeneratorConfig
from .gui_event_handlers import GUIEventHandlers
from .gui_config_handlers import GUIConfigHandlers
from .gui_preview_handlers import GUIPreviewHandlers


class GUIHandlers:
    """Event handlers for GUI interactions."""
    
    def __init__(self, generator: GeneratorCore, preview_widget, file_grid, config_widgets):
        self.generator = generator
        self.preview_widget = preview_widget
        self.file_grid = file_grid
        self.config_widgets = config_widgets
        
        # Initialize component handlers
        self.event_handlers = GUIEventHandlers(generator, preview_widget, file_grid, config_widgets)
        self.config_handlers = GUIConfigHandlers(generator, preview_widget, config_widgets)
        self.preview_handlers = GUIPreviewHandlers(preview_widget)
    
    def handle_generate_tests(self, event):
        """Handle test generation."""
        self.event_handlers.handle_generate_tests(event)
    
    def handle_preview_tests(self, event):
        """Handle test preview."""
        self.event_handlers.handle_preview_tests(event)
    
    def handle_clear_selection(self, event):
        """Handle clear selection."""
        self.event_handlers.handle_clear_selection(event)
    
    def handle_save_config(self, event):
        """Handle save configuration."""
        self.config_handlers.handle_save_config(event)
    
    def handle_load_config(self, event):
        """Handle load configuration."""
        self.config_handlers.handle_load_config(event)
    
    def handle_refresh_tree(self, event):
        """Handle refresh file tree."""
        self.event_handlers.handle_refresh_tree(event)