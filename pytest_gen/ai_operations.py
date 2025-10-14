"""
AI assistant operations and utilities.
"""

import os
from typing import Dict, List, Any, Optional
from .ai_prompts import PromptTemplates, PromptType

# Optional imports for AI functionality
try:
    import tiktoken
except ImportError:
    tiktoken = None


class AIOperations:
    """AI assistant operations and utilities."""
    
    def __init__(self, prompts: PromptTemplates, provider, token_encoder):
        self.prompts = prompts
        self.provider = provider
        self.token_encoder = token_encoder
    
    def generate_response_with_context(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
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
        
        return self.provider.call_api(full_prompt)
    
    def analyze_code_with_prompt(self, code: str, file_path: str) -> Dict[str, Any]:
        """Analyze code using test strategy prompt."""
        # Generate analysis prompt
        prompt = self.prompts.get_prompt(
            PromptType.TEST_STRATEGY,
            code=code,
            code_type="Python",  # TODO: Detect from code
            framework="Unknown"   # TODO: Detect from code
        )
        
        response = self.provider.call_api(prompt)
        
        return {
            "success": True,
            "analysis": response["content"],
            "file_path": file_path,
            "tokens_used": response.get("tokens_used", 0)
        }
    
    def suggest_tests_with_prompt(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest tests using coverage analysis prompt."""
        prompt = self.prompts.get_prompt(
            PromptType.COVERAGE_ANALYSIS,
            source_code=analysis_result.get("code", ""),
            existing_tests=analysis_result.get("existing_tests", "")
        )
        
        response = self.provider.call_api(prompt)
        
        return {
            "success": True,
            "suggestions": response["content"],
            "tokens_used": response.get("tokens_used", 0)
        }
    
    def explain_generation_with_prompt(self, test_files: List[str]) -> Dict[str, Any]:
        """Explain test generation using code explanation prompt."""
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
        
        response = self.provider.call_api(prompt)
        
        return {
            "success": True,
            "explanation": response["content"],
            "test_files": test_files,
            "tokens_used": response.get("tokens_used", 0)
        }
    
    def get_best_practices_with_prompt(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Get best practices using best practices prompt."""
        prompt = self.prompts.get_prompt(
            PromptType.BEST_PRACTICES,
            topic=topic,
            context=context
        )
        
        response = self.provider.call_api(prompt)
        
        return {
            "success": True,
            "best_practices": response["content"],
            "topic": topic,
            "tokens_used": response.get("tokens_used", 0)
        }
    
    def read_file_safely(self, file_path: str) -> str:
        """Read file content safely."""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Failed to read file: {str(e)}")
    
    def count_tokens_in_text(self, text: str) -> int:
        """Count tokens in text."""
        if self.token_encoder:
            return len(self.token_encoder.encode(text))
        else:
            # Rough estimation: 1 token ≈ 4 characters
            return len(text) // 4
    
    def initialize_token_encoder(self):
        """Initialize token encoder for counting tokens."""
        try:
            if tiktoken:
                return tiktoken.get_encoding("cl100k_base")
            else:
                return None
        except Exception:
            return None
