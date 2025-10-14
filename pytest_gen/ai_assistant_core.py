"""
Core functionality for AI assistant operations.
"""

import os
from typing import Dict, List, Any, Optional
from .ai_config import AIConfigManager, AIProvider
from .ai_context import AIContext
from .ai_prompts import PromptTemplates, PromptType
from .ai_providers import AIProviderFactory

# Optional imports for AI functionality
try:
    import tiktoken
except ImportError:
    tiktoken = None


class AIAssistantCore:
    """Core functionality for AI assistant."""
    
    def __init__(self, config_manager: Optional[AIConfigManager] = None):
        self.config_manager = config_manager or AIConfigManager()
        self.config = self.config_manager.get_config()
        self.context = AIContext(max_conversation_memory=self.config.conversation_memory)
        self.prompts = PromptTemplates()
        self._token_encoder = None
        self._provider = None
        self._initialize_token_encoder()
    
    def _initialize_token_encoder(self):
        """Initialize token encoder for counting tokens."""
        try:
            if tiktoken:
                self._token_encoder = tiktoken.get_encoding("cl100k_base")
            else:
                self._token_encoder = None
        except Exception:
            self._token_encoder = None
    
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
        
        if not self._provider:
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
            response = self._generate_response(question, relevant_context)
            
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
                with open(source_path, 'r') as f:
                    code = f.read()
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to read file: {str(e)}"
                }
        
        # Add code to context
        self.context.add_code_context(source_path, code)
        
        # Generate analysis prompt
        prompt = self.prompts.get_prompt(
            PromptType.TEST_STRATEGY,
            code=code,
            code_type="Python",  # TODO: Detect from code
            framework="Unknown"   # TODO: Detect from code
        )
        
        try:
            response = self._call_ai_api(prompt)
            
            return {
                "success": True,
                "analysis": response["content"],
                "file_path": source_path,
                "tokens_used": response.get("tokens_used", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to analyze code: {str(e)}"
            }
    
    def get_test_suggestions(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest specific tests based on analysis."""
        try:
            prompt = self.prompts.get_prompt(
                PromptType.COVERAGE_ANALYSIS,
                source_code=analysis_result.get("code", ""),
                existing_tests=analysis_result.get("existing_tests", "")
            )
            
            response = self._call_ai_api(prompt)
            
            return {
                "success": True,
                "suggestions": response["content"],
                "tokens_used": response.get("tokens_used", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to suggest tests: {str(e)}"
            }
    
    def explain_test_generation(self, test_files: List[str]) -> Dict[str, Any]:
        """Explain what tests will be generated."""
        try:
            # Read test file contents
            test_contents = []
            for file_path in test_files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        test_contents.append(f"File: {file_path}\n{content}")
                except Exception:
                    continue
            
            combined_tests = "\n\n".join(test_contents)
            
            prompt = self.prompts.get_prompt(
                PromptType.CODE_EXPLANATION,
                code=combined_tests,
                config="Default configuration"
            )
            
            response = self._call_ai_api(prompt)
            
            return {
                "success": True,
                "explanation": response["content"],
                "test_files": test_files,
                "tokens_used": response.get("tokens_used", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to explain generation: {str(e)}"
            }
    
    def get_best_practices_info(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Get best practices for a testing topic."""
        try:
            prompt = self.prompts.get_prompt(
                PromptType.BEST_PRACTICES,
                topic=topic,
                context=context
            )
            
            response = self._call_ai_api(prompt)
            
            return {
                "success": True,
                "best_practices": response["content"],
                "topic": topic,
                "tokens_used": response.get("tokens_used", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get best practices: {str(e)}"
            }
    
    def _generate_response(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI response with context."""
        # Build conversation prompt
        conversation_prompt = self.prompts.get_prompt(
            PromptType.CONVERSATION,
            question=question,
            context=str(context.get("current_code", "")),
            conversation_history=context.get("conversation_history", "")
        )
        
        # Add system prompt
        system_prompt = self.prompts.get_prompt(PromptType.SYSTEM)
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\n{conversation_prompt}"
        
        return self._call_ai_api(full_prompt)
    
    def _call_ai_api(self, prompt: str) -> Dict[str, Any]:
        """Call the appropriate AI API based on configuration."""
        if not self._provider:
            raise Exception("AI provider not initialized")
        
        return self._provider.call_api(prompt)
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self._token_encoder:
            return len(self._token_encoder.encode(text))
        else:
            # Rough estimation: 1 token ≈ 4 characters
            return len(text) // 4
    
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
