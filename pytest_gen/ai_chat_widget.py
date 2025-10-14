"""
Panel chat widget for AI assistant interface.
"""

import panel as pn
from typing import Dict, List, Any, Optional, Callable
from .ai_assistant import AIAssistant
from .ai_config import AIConfigManager
from .ai_widget_components import AIWidgetComponents
from .ai_chat_handlers import AIChatHandlers


class AIChatWidget:
    """Panel widget for AI assistant chat interface."""
    
    def __init__(self, assistant: Optional[AIAssistant] = None):
        self.assistant = assistant or AIAssistant()
        self.widgets = self._create_widgets()
        self.handlers = AIChatHandlers(self.assistant, self.widgets)
        self._setup_callbacks()
    
    def _create_widgets(self) -> Dict[str, pn.widgets.Widget]:
        """Create all chat widgets."""
        widgets = {}
        
        # Chat display area
        widgets['chat_display'] = AIWidgetComponents.create_chat_display()
        
        # Input widgets
        input_widgets = AIWidgetComponents.create_input_widgets()
        widgets.update(input_widgets)
        
        # Status indicator
        widgets['status'] = AIWidgetComponents.create_status_widget()
        
        # Quick action buttons
        action_widgets = AIWidgetComponents.create_action_buttons()
        widgets.update(action_widgets)
        
        return widgets
    
    def _setup_callbacks(self):
        """Setup widget callbacks."""
        self.handlers.setup_callbacks()
    
    def create_layout(self) -> pn.layout.Panel:
        """Create the complete chat layout."""
        # Input row
        input_row = pn.Row(
            self.widgets['message_input'],
            pn.Column(
                self.widgets['send_button'],
                self.widgets['clear_button']
            ),
            sizing_mode='stretch_width'
        )
        
        # Quick actions row
        quick_actions = pn.Row(
            self.widgets['analyze_btn'],
            self.widgets['suggest_btn'],
            self.widgets['explain_btn'],
            self.widgets['practices_btn'],
            sizing_mode='stretch_width'
        )
        
        # Complete layout
        layout = pn.Column(
            pn.pane.HTML("<h2>💬 AI Testing Assistant</h2>", sizing_mode='stretch_width'),
            self.widgets['status'],
            self.widgets['chat_display'],
            quick_actions,
            input_row,
            sizing_mode='stretch_both'
        )
        
        return layout
    
    def add_context_callback(self, callback: Callable[[], Dict[str, Any]]):
        """Add callback to provide context for AI responses."""
        self.handlers.add_context_callback(callback)
    
    def set_selected_files(self, file_paths: List[str]):
        """Set currently selected files for context."""
        self.handlers.set_selected_files(file_paths)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get current conversation history."""
        return self.handlers.get_conversation_history()