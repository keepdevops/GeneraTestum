"""
Core AI assistant for test generation guidance.
"""

from typing import Dict, List, Any, Optional
from .ai_config import AIConfigManager
from .ai_assistant_core import AIAssistantCore


class AIAssistant:
    """Core AI assistant for test generation guidance."""
    
    def __init__(self, config_manager: Optional[AIConfigManager] = None):
        self.core = AIAssistantCore(config_manager)
    
    def initialize(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Initialize the AI assistant."""
        return self.core.initialize_provider(api_key)
    
    def ask(self, question: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ask a question to the AI assistant."""
        return self.core.generate_response(question, context_data)
    
    def analyze_code(self, source_path: str, code: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code and provide testing recommendations."""
        return self.core.analyze_source_code(source_path, code)
    
    def suggest_tests(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest specific tests based on analysis."""
        return self.core.get_test_suggestions(analysis_result)
    
    def explain_generation(self, test_files: List[str]) -> Dict[str, Any]:
        """Explain what tests will be generated."""
        return self.core.explain_test_generation(test_files)
    
    def get_best_practices(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Get best practices for a testing topic."""
        return self.core.get_best_practices_info(topic, context)
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return self.core.count_tokens(text)
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of current context."""
        return self.core.get_context_summary()
    
    def clear_context(self) -> None:
        """Clear all context."""
        self.core.clear_context()
    
    def save_context(self, file_path: str) -> None:
        """Save context to file."""
        self.core.save_context(file_path)
    
    def load_context(self, file_path: str) -> None:
        """Load context from file."""
        self.core.load_context(file_path)