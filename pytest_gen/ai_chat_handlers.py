"""
AI chat widget event handlers and message processing.
"""

import panel as pn
from typing import Dict, List, Any, Optional, Callable
from .ai_assistant import AIAssistant
from .ai_widget_components import AIWidgetComponents


class AIChatHandlers:
    """Event handlers for AI chat widget."""
    
    def __init__(self, assistant: AIAssistant, widgets: Dict[str, pn.widgets.Widget]):
        self.assistant = assistant
        self.widgets = widgets
        self.conversation_history = []
    
    def setup_callbacks(self):
        """Setup widget callbacks."""
        # Send message callback
        self.widgets['send_button'].param.watch(
            self._on_send_message, 'clicks'
        )
        
        # Enter key in input field
        self.widgets['message_input'].param.watch(
            self._on_enter_key, 'value'
        )
        
        # Clear conversation callback
        self.widgets['clear_button'].param.watch(
            self._on_clear_conversation, 'clicks'
        )
        
        # Quick action callbacks
        action_buttons = ['analyze_btn', 'suggest_btn', 'explain_btn', 'practices_btn']
        for btn_key in action_buttons:
            if btn_key in self.widgets:
                self.widgets[btn_key].param.watch(
                    lambda event, key=btn_key: self._on_quick_action(key), 'clicks'
                )
    
    def _on_send_message(self, event):
        """Handle send message button click."""
        message = self.widgets['message_input'].value.strip()
        if message:
            self._send_message(message)
            self.widgets['message_input'].value = ""
    
    def _on_enter_key(self, event):
        """Handle enter key in input field."""
        if event.new and not event.old:  # New message entered
            message = event.new.strip()
            if message:
                self._send_message(message)
                self.widgets['message_input'].value = ""
    
    def _on_clear_conversation(self, event):
        """Handle clear conversation button click."""
        self.conversation_history = []
        self.assistant.clear_context()
        self._update_chat_display()
        self._update_status("Conversation cleared", "info")
    
    def _on_quick_action(self, action_key: str):
        """Handle quick action button clicks."""
        action_messages = {
            'analyze_btn': "Please analyze the selected files and suggest test strategies.",
            'suggest_btn': "What tests should I write for better coverage?",
            'explain_btn': "Help me understand the test generator configuration options.",
            'practices_btn': "What are the best practices for writing pytest tests?"
        }
        
        message = action_messages.get(action_key, "How can I help you?")
        self._send_message(message)
    
    def _send_message(self, message: str):
        """Send a message to the AI assistant."""
        # Add user message to conversation
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": AIWidgetComponents.get_timestamp()
        })
        
        # Update chat display
        self._update_chat_display()
        
        # Update status
        self._update_status("AI is thinking...", "warning")
        
        # Disable send button
        self.widgets['send_button'].disabled = True
        
        try:
            # Get AI response
            response = self.assistant.ask(message)
            
            if response["success"]:
                ai_message = {
                    "role": "assistant",
                    "content": response["response"],
                    "timestamp": AIWidgetComponents.get_timestamp(),
                    "tokens_used": response.get("tokens_used", 0)
                }
                self.conversation_history.append(ai_message)
                
                self._update_status(
                    f"Response received ({ai_message['tokens_used']} tokens)",
                    "success"
                )
            else:
                error_message = {
                    "role": "assistant",
                    "content": f"Error: {response['error']}",
                    "timestamp": AIWidgetComponents.get_timestamp(),
                    "is_error": True
                }
                self.conversation_history.append(error_message)
                
                self._update_status(f"Error: {response['error']}", "danger")
        
        except Exception as e:
            error_message = {
                "role": "assistant",
                "content": f"Unexpected error: {str(e)}",
                "timestamp": AIWidgetComponents.get_timestamp(),
                "is_error": True
            }
            self.conversation_history.append(error_message)
            self._update_status(f"Error: {str(e)}", "danger")
        
        finally:
            # Re-enable send button
            self.widgets['send_button'].disabled = False
            self._update_chat_display()
    
    def _update_chat_display(self):
        """Update the chat display with current conversation."""
        chat_html = self._format_conversation_html()
        self.widgets['chat_display'].value = chat_html
        
        # Scroll to bottom
        try:
            self.widgets['chat_display'].scroll_to_bottom()
        except AttributeError:
            pass  # Some Panel versions don't have this method
    
    def _format_conversation_html(self) -> str:
        """Format conversation as HTML."""
        if not self.conversation_history:
            return AIWidgetComponents.format_empty_chat()
        
        html_parts = [
            "<div style='font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif;'>"
        ]
        
        for message in self.conversation_history:
            role = message["role"]
            content = message["content"]
            timestamp = message["timestamp"]
            
            if role == "user":
                html_parts.append(AIWidgetComponents.format_user_message(content, timestamp))
            else:
                is_error = message.get("is_error", False)
                tokens_used = message.get("tokens_used", 0)
                html_parts.append(
                    AIWidgetComponents.format_assistant_message(content, timestamp, is_error, tokens_used)
                )
        
        html_parts.append("</div>")
        return "".join(html_parts)
    
    def _update_status(self, message: str, status_type: str):
        """Update status indicator."""
        colors = {
            "success": "#28a745",
            "warning": "#ffc107",
            "danger": "#dc3545",
            "info": "#17a2b8"
        }
        
        color = colors.get(status_type, "#6c757d")
        self.widgets['status'].value = f"<div style='color: {color};'>{message}</div>"
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get current conversation history."""
        return self.conversation_history.copy()
    
    def add_context_callback(self, callback: Callable[[], Dict[str, Any]]):
        """Add callback to provide context for AI responses."""
        self._context_callback = callback
    
    def set_selected_files(self, file_paths: List[str]):
        """Set currently selected files for context."""
        self.selected_files = file_paths
