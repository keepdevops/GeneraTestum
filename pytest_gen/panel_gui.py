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
from .ai_chat_widget import AIChatWidget
from .ai_assistant import AIAssistant

# Configure Panel to avoid realtime plugin issues
pn.config.console_output = 'disable'
pn.config.realtime = False


class TestGeneratorGUI:
    """Main Panel GUI application for test generation."""
    
    def __init__(self):
        self.generator = GeneratorCore()
        self.file_grid = FileGrid()
        self.config_widgets = ConfigWidgets()
        self.action_widgets = ActionWidgets()
        self.preview_widget = PreviewWidget()
        self.file_tree = FileTreeWidget()
        
        # Initialize AI assistant
        self.ai_assistant = None
        self.ai_chat_widget = None
        self._initialize_ai_assistant()
        
        # Create layouts and handlers
        self.layouts = GUILayouts(
            self.file_grid, self.config_widgets, self.action_widgets,
            self.preview_widget, self.file_tree, self.ai_chat_widget
        )
        
        self.handlers = GUIHandlers(
            self.generator, self.preview_widget, self.file_grid, self.config_widgets
        )
        
        self._setup_callbacks()
        self._create_layout()
    
    def _initialize_ai_assistant(self):
        """Initialize AI assistant and chat widget."""
        try:
            self.ai_assistant = AIAssistant()
            init_result = self.ai_assistant.initialize()
            
            if init_result["success"]:
                self.ai_chat_widget = AIChatWidget(self.ai_assistant)
                # Add context callback to provide file information
                self.ai_chat_widget.add_context_callback(self._get_ai_context)
            else:
                print(f"AI Assistant initialization failed: {init_result.get('errors', [])}")
                
        except Exception as e:
            print(f"Failed to initialize AI Assistant: {e}")
    
    def _get_ai_context(self) -> dict:
        """Provide context for AI assistant based on current selection."""
        context = {}
        
        # Get selected files from file grid
        selected_files = self.file_grid.get_selected_files()
        if selected_files:
            context["selected_files"] = selected_files
            
            # Add content of first selected file
            try:
                with open(selected_files[0], 'r') as f:
                    content = f.read()
                    context["current_file_content"] = content
                    context["current_file_path"] = selected_files[0]
            except Exception:
                pass
        
        # Add current configuration
        config = self.generator.get_config()
        context["configuration"] = {
            "mock_level": str(config.mock_level),
            "coverage_type": str(config.coverage_type),
            "include_private_methods": config.include_private_methods,
            "generate_fixtures": config.generate_fixtures
        }
        
        return context
    
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
        # Remove show from kwargs to avoid duplicate parameter
        kwargs.pop('show', None)
        
        # Use a simplified approach to avoid Panel library issues
        try:
            # Try the standard approach first
            return self.layout.show(port=port, show=show, **kwargs)
        except TypeError as e:
            if "multiple values for keyword argument 'show'" in str(e):
                # Fallback: use server.serve without show parameter
                import panel.io.server as server
                return server.serve(
                    panels=self.layout,
                    port=port,
                    **kwargs
                )
            else:
                raise
    
    def get_layout(self):
        """Get the complete layout."""
        return self.layout


def launch_gui(port: int = 5007, show: bool = True, **kwargs):
    """Launch the test generator GUI."""
    # Disable realtime extensions to avoid plugin errors
    kwargs.setdefault('allow_websocket_origin', ['*'])
    kwargs.setdefault('reuse_sessions', False)
    
    # Remove show from kwargs to avoid duplicate parameter
    kwargs.pop('show', None)
    
    app = TestGeneratorGUI()
    return app.serve(port=port, show=show, **kwargs)
