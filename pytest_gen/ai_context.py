"""
AI context management for conversation history and code context.
"""

from typing import Dict, List, Any, Optional
from .ai_context_models import Message, CodeContext
from .ai_context_manager import AIContextManager
from .ai_context_persistence import AIContextPersistence


class AIContext(AIContextManager):
    """Manages context for AI conversations and code analysis."""
    
    def __init__(self, max_conversation_memory: int = 10):
        super().__init__(max_conversation_memory)
        self.persistence = AIContextPersistence(self)
    
    def save_context(self, file_path: str) -> None:
        """Save context to file."""
        return self.persistence.save_context(file_path)
    
    def load_context(self, file_path: str) -> None:
        """Load context from file."""
        return self.persistence.load_context(file_path)
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of current context."""
        return self.persistence.get_context_summary()
    
    def search_conversation(self, query: str) -> List[Message]:
        """Search conversation history for messages containing query."""
        return self.persistence.search_conversation(query)
    
    def get_code_by_framework(self, framework: str) -> List[CodeContext]:
        """Get code contexts by framework."""
        return self.persistence.get_code_by_framework(framework)
    
    def get_code_by_type(self, code_type: str) -> List[CodeContext]:
        """Get code contexts by type."""
        return self.persistence.get_code_by_type(code_type)