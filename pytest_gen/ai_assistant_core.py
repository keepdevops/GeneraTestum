"""
Core functionality for AI assistant operations.
"""

from typing import Dict, List, Any, Optional
from .ai_config import AIConfigManager
from .ai_types import AIProvider
from .ai_context import AIContext
from .ai_prompts import PromptTemplates, PromptType
from .ai_providers import AIProviderFactory
from .ai_operations import AIOperations


class AIAssistantCore:
    """Core functionality for AI assistant."""
    
    def __init__(self, config_manager: Optional[AIConfigManager] = None):
        self.config_manager = config_manager or AIConfigManager()
        self.config = self.config_manager.get_config()
        self.context = AIContext(max_conversation_memory=self.config.conversation_memory)
        self.prompts = PromptTemplates()
        self._token_encoder = None
        self._provider = None
        self._operations = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize token encoder and operations."""
        self._token_encoder = self._initialize_token_encoder()
        # Operations will be initialized after provider is set
    
    def _initialize_token_encoder(self):
        """Initialize token encoder for counting tokens."""
        try:
            import tiktoken
            return tiktoken.get_encoding("cl100k_base")
        except ImportError:
            return None
        except Exception:
            return None
    
    def initialize_provider(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Initialize the AI provider."""
        if api_key:
            self.config.api_key = api_key
        
        validation_result = self.config_manager.validate_config()
        
        if not validation_result["valid"]:
            return {
                "success": False,
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"]
            }
        
        # Initialize provider
        try:
            self._provider = AIProviderFactory.create_provider(
                self.config.provider.value, self.config
            )
            # Initialize operations with provider
            self._operations = AIOperations(self.prompts, self._provider, self._token_encoder)
        except Exception as e:
            return {
                "success": False,
                "errors": [f"Failed to initialize provider: {str(e)}"]
            }
        
        return {
            "success": True,
            "provider": self.config.provider.value,
            "model": self.config.model,
            "warnings": validation_result["warnings"]
        }
    
    def generate_response(self, question: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate AI response for a question."""
        if not self.config.enabled:
            return {
                "success": False,
                "error": "AI assistant is disabled"
            }
        
        if not self._provider or not self._operations:
            return {
                "success": False,
                "error": "AI provider not initialized"
            }
        
        try:
            # Get relevant context
            relevant_context = self.context.get_relevant_context(question)
            if context_data:
                relevant_context.update(context_data)
            
            # Add user message to context
            self.context.add_message("user", question)
            
            # Generate response
            response = self._operations.generate_response_with_context(question, relevant_context)
            
            # Add assistant response to context
            self.context.add_message("assistant", response["content"])
            
            return {
                "success": True,
                "response": response["content"],
                "metadata": response.get("metadata", {}),
                "tokens_used": response.get("tokens_used", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate response: {str(e)}"
            }
    
    def analyze_source_code(self, source_path: str, code: Optional[str] = None) -> Dict[str, Any]:
        """Analyze source code and provide testing recommendations."""
        if code is None:
            try:
                code = self._operations.read_file_safely(source_path)
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Add code to context
        self.context.add_code_context(source_path, code)
        
        try:
            return self._operations.analyze_code_with_prompt(code, source_path)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to analyze code: {str(e)}"
            }
    
    def get_test_suggestions(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest specific tests based on analysis."""
        try:
            return self._operations.suggest_tests_with_prompt(analysis_result)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to suggest tests: {str(e)}"
            }
    
    def explain_test_generation(self, test_files: List[str]) -> Dict[str, Any]:
        """Explain what tests will be generated."""
        try:
            return self._operations.explain_generation_with_prompt(test_files)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to explain generation: {str(e)}"
            }
    
    def get_best_practices_info(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Get best practices for a testing topic."""
        try:
            return self._operations.get_best_practices_with_prompt(topic, context)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get best practices: {str(e)}"
            }
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return self._operations.count_tokens_in_text(text)
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of current context."""
        return self.context.get_context_summary()
    
    def clear_context(self) -> None:
        """Clear all context."""
        self.context.clear_all_context()
    
    def save_context(self, file_path: str) -> None:
        """Save context to file."""
        self.context.save_context(file_path)
    
    def load_context(self, file_path: str) -> None:
        """Load context from file."""
        self.context.load_context(file_path)