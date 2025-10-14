"""
Core context management for AI conversations and code analysis.
"""

from typing import Dict, List, Any, Optional
from .ai_context_models import Message, CodeContext


class AIContextManager:
    """Core context management for AI conversations and code analysis."""
    
    def __init__(self, max_conversation_memory: int = 10):
        self.max_conversation_memory = max_conversation_memory
        self.conversation_history: List[Message] = []
        self.code_contexts: Dict[str, CodeContext] = {}
        self.current_context: Optional[str] = None
        self.user_preferences: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a message to the conversation history."""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.conversation_history.append(message)
        
        # Trim history if it exceeds max memory
        if len(self.conversation_history) > self.max_conversation_memory:
            self.conversation_history = self.conversation_history[-self.max_conversation_memory:]
    
    def add_code_context(self, file_path: str, content: str, 
                        analysis_result: Optional[Dict[str, Any]] = None,
                        dependencies: Optional[List[str]] = None,
                        framework: Optional[str] = None,
                        code_type: Optional[str] = None) -> None:
        """Add code context for analysis."""
        context = CodeContext(
            file_path=file_path,
            content=content,
            analysis_result=analysis_result,
            dependencies=dependencies or [],
            framework=framework,
            code_type=code_type
        )
        self.code_contexts[file_path] = context
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Message]:
        """Get conversation history with optional limit."""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history.copy()
    
    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get context relevant to the query."""
        context = {
            'conversation_history': self._format_conversation_history(),
            'current_code_context': None,
            'related_code_contexts': []
        }
        
        # Add current context if available
        if self.current_context and self.current_context in self.code_contexts:
            current = self.code_contexts[self.current_context]
            context['current_code_context'] = {
                'file_path': current.file_path,
                'content': current.content[:1000],  # Limit content length
                'framework': current.framework,
                'code_type': current.code_type
            }
        
        # Add related contexts based on query keywords
        query_lower = query.lower()
        for file_path, code_ctx in self.code_contexts.items():
            if (code_ctx.framework and code_ctx.framework.lower() in query_lower) or \
               (code_ctx.code_type and code_ctx.code_type.lower() in query_lower):
                context['related_code_contexts'].append({
                    'file_path': file_path,
                    'framework': code_ctx.framework,
                    'code_type': code_ctx.code_type
                })
        
        return context
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for context."""
        if not self.conversation_history:
            return "No previous conversation."
        
        formatted = []
        for msg in self.conversation_history[-5:]:  # Last 5 messages
            formatted.append(f"{msg.role}: {msg.content}")
        
        return "\n".join(formatted)
    
    def clear_conversation(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
    
    def clear_code_contexts(self) -> None:
        """Clear all code contexts."""
        self.code_contexts.clear()
    
    def clear_all_context(self) -> None:
        """Clear all context."""
        self.clear_conversation()
        self.clear_code_contexts()
        self.current_context = None
    
    def set_current_context(self, file_path: str) -> None:
        """Set the current context file."""
        self.current_context = file_path
    
    def get_current_context(self) -> Optional[CodeContext]:
        """Get the current context."""
        if self.current_context:
            return self.code_contexts.get(self.current_context)
        return None
    
    def update_user_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences."""
        self.user_preferences.update(preferences)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return self.user_preferences.copy()
