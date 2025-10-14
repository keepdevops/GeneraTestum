"""
AI chat widget component creation and management.
"""

import panel as pn
from typing import Dict


class AIWidgetComponents:
    """Component creation for AI chat widget."""
    
    @staticmethod
    def create_chat_display():
        """Create chat display widget."""
        from .ai_chat_widget import AIChatWidget
        empty_chat = AIChatWidget._format_empty_chat_static()
        return pn.pane.HTML(
            empty_chat,
            sizing_mode='stretch_both'
        )
    
    @staticmethod
    def create_input_widgets() -> Dict[str, pn.widgets.Widget]:
        """Create input-related widgets."""
        widgets = {}
        
        widgets['message_input'] = pn.widgets.TextAreaInput(
            placeholder="Ask me about testing, mocking, or test generation...",
            height=100,
            max_height=200,
            sizing_mode='stretch_width'
        )
        
        widgets['send_button'] = pn.widgets.Button(
            name="Send",
            button_type="primary",
            width=100
        )
        
        widgets['clear_button'] = pn.widgets.Button(
            name="Clear",
            button_type="light",
            width=100
        )
        
        return widgets
    
    @staticmethod
    def create_status_widget():
        """Create status indicator widget."""
        return pn.pane.HTML(
            "<div style='color: #28a745;'>✓ AI Assistant Ready</div>",
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_action_buttons() -> Dict[str, pn.widgets.Widget]:
        """Create quick action buttons."""
        widgets = {}
        
        button_configs = [
            ("analyze_btn", "Analyze Selected Files"),
            ("suggest_btn", "Suggest Tests"),
            ("explain_btn", "Explain Configuration"),
            ("practices_btn", "Best Practices")
        ]
        
        for key, name in button_configs:
            widgets[key] = pn.widgets.Button(
                name=name,
                button_type="light",
                width=150
            )
        
        return widgets
    
    @staticmethod
    def format_empty_chat() -> str:
        """Format empty chat state."""
        return """
        <div style='text-align: center; color: #6c757d; padding: 40px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;'>
            <h3>🤖 AI Testing Assistant</h3>
            <p>Ask me anything about testing, mocking, or test generation!</p>
            <div style='margin-top: 20px;'>
                <div style='background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; text-align: left;'>
                    <strong>Try asking:</strong><br>
                    • "How do I test async functions?"<br>
                    • "What should I mock in this code?"<br>
                    • "Explain the test generator configuration"<br>
                    • "What are pytest best practices?"
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def format_user_message(content: str, timestamp: str) -> str:
        """Format user message as HTML."""
        return f"""
        <div style='margin: 10px 0; text-align: right;'>
            <div style='display: inline-block; background: #007bff; color: white; padding: 10px 15px; border-radius: 18px; max-width: 70%; word-wrap: break-word;'>
                {AIWidgetComponents._escape_html(content)}
            </div>
            <div style='font-size: 0.8em; color: #6c757d; margin-top: 5px;'>{timestamp}</div>
        </div>
        """
    
    @staticmethod
    def format_assistant_message(content: str, timestamp: str, is_error: bool, tokens_used: int) -> str:
        """Format assistant message as HTML."""
        bg_color = "#dc3545" if is_error else "#28a745"
        
        return f"""
        <div style='margin: 10px 0; text-align: left;'>
            <div style='display: inline-block; background: {bg_color}; color: white; padding: 10px 15px; border-radius: 18px; max-width: 70%; word-wrap: break-word;'>
                {AIWidgetComponents._escape_html(content)}
            </div>
            <div style='font-size: 0.8em; color: #6c757d; margin-top: 5px;'>
                {timestamp}
                {f' • {tokens_used} tokens' if tokens_used > 0 else ''}
            </div>
        </div>
        """
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML characters in text."""
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&#39;",
            ">": "&gt;",
            "<": "&lt;",
        }
        return "".join(html_escape_table.get(c, c) for c in text)
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
