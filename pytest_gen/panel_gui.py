"""
Main Panel GUI application for the test generator.
"""

import panel as pn
from .file_grid import FileGrid
from .config_widgets import ConfigWidgets
from .ui_widgets import ActionWidgets, PreviewWidget, FileTreeWidget
from .gui_layouts import GUILayouts
from .gui_handlers import GUIHandlers
from .generator_core import GeneratorCore


class TestGeneratorGUI:
    """Main Panel GUI application for test generation."""
    
    def __init__(self):
        self.generator = GeneratorCore()
        self.file_grid = FileGrid()
        self.config_widgets = ConfigWidgets()
        self.action_widgets = ActionWidgets()
        self.preview_widget = PreviewWidget()
        self.file_tree = FileTreeWidget()
        
        # Create layouts and handlers
        self.layouts = GUILayouts(
            self.file_grid, self.config_widgets, self.action_widgets,
            self.preview_widget, self.file_tree
        )
        
        self.handlers = GUIHandlers(
            self.generator, self.preview_widget, self.file_grid, self.config_widgets
        )
        
        self._setup_callbacks()
        self._create_layout()
    
    def _setup_callbacks(self):
        """Setup event callbacks for widgets."""
        # Action button callbacks
        self.action_widgets.widgets['generate_btn'].param.watch(
            self.handlers.handle_generate_tests, 'clicks'
        )
        
        self.action_widgets.widgets['preview_btn'].param.watch(
            self.handlers.handle_preview_tests, 'clicks'
        )
        
        self.action_widgets.widgets['clear_btn'].param.watch(
            self.handlers.handle_clear_selection, 'clicks'
        )
        
        self.action_widgets.widgets['save_config_btn'].param.watch(
            self.handlers.handle_save_config, 'clicks'
        )
        
        self.action_widgets.widgets['load_config_btn'].param.watch(
            self.handlers.handle_load_config, 'clicks'
        )
        
        # File tree refresh
        self.file_tree.widgets['refresh_btn'].param.watch(
            self.handlers.handle_refresh_tree, 'clicks'
        )
    
    def _create_layout(self):
        """Create the main application layout."""
        self.layout = self.layouts.create_main_layout()
    
    def serve(self, port: int = 5007, show: bool = True, **kwargs):
        """Serve the Panel application."""
        return self.layout.show(port=port, show=show, **kwargs)
    
    def get_layout(self):
        """Get the complete layout."""
        return self.layout


def launch_gui(port: int = 5007, show: bool = True, **kwargs):
    """Launch the test generator GUI."""
    app = TestGeneratorGUI()
    return app.serve(port=port, show=show, **kwargs)
