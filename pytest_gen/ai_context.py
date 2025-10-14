"""
AI context management for conversation history and code context.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Message:
    """Represents a message in the conversation."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeContext:
    """Represents code context for analysis."""
    file_path: str
    content: str
    analysis_result: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    framework: Optional[str] = None
    code_type: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class AIContext:
    """Manages context for AI conversations and code analysis."""
    
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
        
        # Trim conversation history if it exceeds max memory
        if len(self.conversation_history) > self.max_conversation_memory:
            self.conversation_history = self.conversation_history[-self.max_conversation_memory:]
    
    def add_code_context(self, file_path: str, content: str, 
                        analysis_result: Optional[Dict[str, Any]] = None,
                        dependencies: Optional[List[str]] = None,
                        framework: Optional[str] = None,
                        code_type: Optional[str] = None) -> None:
        """Add code context for analysis."""
        code_context = CodeContext(
            file_path=file_path,
            content=content,
            analysis_result=analysis_result,
            dependencies=dependencies or [],
            framework=framework,
            code_type=code_type
        )
        self.code_contexts[file_path] = code_context
        self.current_context = file_path
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Message]:
        """Get conversation history, optionally limited."""
        if limit is None:
            return self.conversation_history
        return self.conversation_history[-limit:]
    
    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get relevant context for a query."""
        relevant_context = {
            "conversation_history": self._format_conversation_history(),
            "current_code": None,
            "available_files": list(self.code_contexts.keys()),
            "user_preferences": self.user_preferences
        }
        
        # If we have a current context, include it
        if self.current_context and self.current_context in self.code_contexts:
            code_context = self.code_contexts[self.current_context]
            relevant_context["current_code"] = {
                "file_path": code_context.file_path,
                "content": code_context.content[:1000],  # Limit content length
                "framework": code_context.framework,
                "code_type": code_context.code_type,
                "dependencies": code_context.dependencies
            }
        
        # Try to find relevant code based on query keywords
        query_lower = query.lower()
        for file_path, code_context in self.code_contexts.items():
            if any(keyword in code_context.content.lower() for keyword in 
                   ['test', 'mock', 'fixture', 'parametrize'] if keyword in query_lower):
                relevant_context["relevant_code"] = {
                    "file_path": file_path,
                    "content": code_context.content[:500],
                    "framework": code_context.framework
                }
                break
        
        return relevant_context
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for AI consumption."""
        if not self.conversation_history:
            return ""
        
        formatted_history = []
        for message in self.conversation_history[-5:]:  # Last 5 messages
            formatted_history.append(f"{message.role}: {message.content}")
        
        return "\n".join(formatted_history)
    
    def clear_conversation(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
    
    def clear_code_contexts(self) -> None:
        """Clear all code contexts."""
        self.code_contexts.clear()
        self.current_context = None
    
    def clear_all_context(self) -> None:
        """Clear all context."""
        self.clear_conversation()
        self.clear_code_contexts()
        self.user_preferences.clear()
    
    def set_current_context(self, file_path: str) -> None:
        """Set the current active context file."""
        if file_path in self.code_contexts:
            self.current_context = file_path
    
    def get_current_context(self) -> Optional[CodeContext]:
        """Get the current active code context."""
        if self.current_context and self.current_context in self.code_contexts:
            return self.code_contexts[self.current_context]
        return None
    
    def update_user_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences."""
        self.user_preferences.update(preferences)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return self.user_preferences.copy()
    
    def save_context(self, file_path: str) -> None:
        """Save context to file."""
        context_data = {
            "conversation_history": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in self.conversation_history
            ],
            "code_contexts": {
                path: {
                    "file_path": ctx.file_path,
                    "content": ctx.content,
                    "analysis_result": ctx.analysis_result,
                    "dependencies": ctx.dependencies,
                    "framework": ctx.framework,
                    "code_type": ctx.code_type,
                    "timestamp": ctx.timestamp.isoformat()
                }
                for path, ctx in self.code_contexts.items()
            },
            "current_context": self.current_context,
            "user_preferences": self.user_preferences
        }
        
        with open(file_path, 'w') as f:
            json.dump(context_data, f, indent=2)
    
    def load_context(self, file_path: str) -> None:
        """Load context from file."""
        try:
            with open(file_path, 'r') as f:
                context_data = json.load(f)
            
            # Load conversation history
            self.conversation_history = []
            for msg_data in context_data.get("conversation_history", []):
                message = Message(
                    role=msg_data["role"],
                    content=msg_data["content"],
                    timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                    metadata=msg_data.get("metadata", {})
                )
                self.conversation_history.append(message)
            
            # Load code contexts
            self.code_contexts = {}
            for path, ctx_data in context_data.get("code_contexts", {}).items():
                code_context = CodeContext(
                    file_path=ctx_data["file_path"],
                    content=ctx_data["content"],
                    analysis_result=ctx_data.get("analysis_result"),
                    dependencies=ctx_data.get("dependencies", []),
                    framework=ctx_data.get("framework"),
                    code_type=ctx_data.get("code_type"),
                    timestamp=datetime.fromisoformat(ctx_data["timestamp"])
                )
                self.code_contexts[path] = code_context
            
            self.current_context = context_data.get("current_context")
            self.user_preferences = context_data.get("user_preferences", {})
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # If loading fails, start with empty context
            self.clear_all_context()
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of current context."""
        return {
            "conversation_length": len(self.conversation_history),
            "code_files": len(self.code_contexts),
            "current_context": self.current_context,
            "available_files": list(self.code_contexts.keys()),
            "preferences_count": len(self.user_preferences)
        }
    
    def search_conversation(self, query: str) -> List[Message]:
        """Search conversation history for messages containing query."""
        query_lower = query.lower()
        matching_messages = []
        
        for message in self.conversation_history:
            if query_lower in message.content.lower():
                matching_messages.append(message)
        
        return matching_messages
    
    def get_code_by_framework(self, framework: str) -> List[CodeContext]:
        """Get all code contexts for a specific framework."""
        return [
            ctx for ctx in self.code_contexts.values()
            if ctx.framework == framework
        ]
    
    def get_code_by_type(self, code_type: str) -> List[CodeContext]:
        """Get all code contexts for a specific code type."""
        return [
            ctx for ctx in self.code_contexts.values()
            if ctx.code_type == code_type
        ]
