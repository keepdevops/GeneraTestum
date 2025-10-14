"""
Persistence and search methods for AI context.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from .ai_context_models import Message, CodeContext


class AIContextPersistence:
    """Persistence and search methods for AI context."""
    
    def __init__(self, context_manager):
        self.context_manager = context_manager
    
    def save_context(self, file_path: str) -> None:
        """Save context to file."""
        context_data = {
            'conversation_history': [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'metadata': msg.metadata
                }
                for msg in self.context_manager.conversation_history
            ],
            'code_contexts': {
                path: {
                    'file_path': ctx.file_path,
                    'content': ctx.content,
                    'analysis_result': ctx.analysis_result,
                    'dependencies': ctx.dependencies,
                    'framework': ctx.framework,
                    'code_type': ctx.code_type,
                    'timestamp': ctx.timestamp.isoformat()
                }
                for path, ctx in self.context_manager.code_contexts.items()
            },
            'current_context': self.context_manager.current_context,
            'user_preferences': self.context_manager.user_preferences,
            'saved_at': datetime.now().isoformat()
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(context_data, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to save context: {e}")
    
    def load_context(self, file_path: str) -> None:
        """Load context from file."""
        if not os.path.exists(file_path):
            return
        
        try:
            with open(file_path, 'r') as f:
                context_data = json.load(f)
            
            # Load conversation history
            self.context_manager.conversation_history = [
                Message(
                    role=msg['role'],
                    content=msg['content'],
                    timestamp=datetime.fromisoformat(msg['timestamp']),
                    metadata=msg.get('metadata', {})
                )
                for msg in context_data.get('conversation_history', [])
            ]
            
            # Load code contexts
            self.context_manager.code_contexts = {
                path: CodeContext(
                    file_path=ctx['file_path'],
                    content=ctx['content'],
                    analysis_result=ctx.get('analysis_result'),
                    dependencies=ctx.get('dependencies', []),
                    framework=ctx.get('framework'),
                    code_type=ctx.get('code_type'),
                    timestamp=datetime.fromisoformat(ctx['timestamp'])
                )
                for path, ctx in context_data.get('code_contexts', {}).items()
            }
            
            # Load other data
            self.context_manager.current_context = context_data.get('current_context')
            self.context_manager.user_preferences = context_data.get('user_preferences', {})
            
        except Exception as e:
            raise RuntimeError(f"Failed to load context: {e}")
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of current context."""
        return {
            'conversation_messages': len(self.context_manager.conversation_history),
            'code_contexts': len(self.context_manager.code_contexts),
            'current_context': self.context_manager.current_context,
            'user_preferences': len(self.context_manager.user_preferences)
        }
    
    def search_conversation(self, query: str) -> List[Message]:
        """Search conversation history for messages containing query."""
        query_lower = query.lower()
        results = []
        
        for msg in self.context_manager.conversation_history:
            if query_lower in msg.content.lower():
                results.append(msg)
        
        return results
    
    def get_code_by_framework(self, framework: str) -> List[CodeContext]:
        """Get code contexts by framework."""
        return [
            ctx for ctx in self.context_manager.code_contexts.values()
            if ctx.framework and ctx.framework.lower() == framework.lower()
        ]
    
    def get_code_by_type(self, code_type: str) -> List[CodeContext]:
        """Get code contexts by type."""
        return [
            ctx for ctx in self.context_manager.code_contexts.values()
            if ctx.code_type and ctx.code_type.lower() == code_type.lower()
        ]
