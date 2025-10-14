"""
Helper functions for AI configuration management.
"""

import os
from typing import Dict, Any
from .ai_types import AIProvider


class AIConfigHelpers:
    """Helper functions for AI configuration."""
    
    @staticmethod
    def get_default_model(provider: AIProvider) -> str:
        """Get default model for provider."""
        defaults = {
            AIProvider.OPENAI: "gpt-4",
            AIProvider.ANTHROPIC: "claude-3-sonnet-20240229",
            AIProvider.OLLAMA: "llama2"
        }
        return defaults.get(provider, "gpt-4")
    
    @staticmethod
    def get_api_key_env_var(provider: AIProvider) -> str:
        """Get API key environment variable for provider."""
        env_vars = {
            AIProvider.OPENAI: "OPENAI_API_KEY",
            AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            AIProvider.OLLAMA: "OLLAMA_API_KEY"  # Usually not needed for local
        }
        return env_vars.get(provider, "OPENAI_API_KEY")
    
    @staticmethod
    def check_provider_availability(provider: AIProvider) -> bool:
        """Check if the configured provider is available."""
        if provider == AIProvider.OPENAI:
            try:
                import openai
                return True
            except ImportError:
                raise Exception("OpenAI library not installed")
        
        elif provider == AIProvider.ANTHROPIC:
            try:
                import anthropic
                return True
            except ImportError:
                raise Exception("Anthropic library not installed")
        
        elif provider == AIProvider.OLLAMA:
            # For Ollama, we assume it's running locally
            return True
        
        else:
            raise Exception(f"Unknown provider: {provider}")
    
    @staticmethod
    def validate_config_parameters(config) -> Dict[str, Any]:
        """Validate configuration parameters."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate parameters
        if config.max_tokens <= 0:
            validation_result["valid"] = False
            validation_result["errors"].append("max_tokens must be positive")
        
        if not 0.0 <= config.temperature <= 2.0:
            validation_result["valid"] = False
            validation_result["errors"].append("temperature must be between 0.0 and 2.0")
        
        if config.context_window <= 0:
            validation_result["valid"] = False
            validation_result["errors"].append("context_window must be positive")
        
        return validation_result
    
    @staticmethod
    def load_config_from_environment():
        """Load AI configuration from environment variables."""
        enabled = os.getenv('PYTEST_GEN_AI_ENABLED', 'true').lower() == 'true'
        
        provider_str = os.getenv('PYTEST_GEN_AI_PROVIDER', 'openai').lower()
        try:
            provider = AIProvider(provider_str)
        except ValueError:
            provider = AIProvider.OPENAI
        
        model = os.getenv('PYTEST_GEN_AI_MODEL', AIConfigHelpers.get_default_model(provider))
        api_key = os.getenv(AIConfigHelpers.get_api_key_env_var(provider))
        
        max_tokens = int(os.getenv('PYTEST_GEN_AI_MAX_TOKENS', '2000'))
        temperature = float(os.getenv('PYTEST_GEN_AI_TEMPERATURE', '0.7'))
        context_window = int(os.getenv('PYTEST_GEN_AI_CONTEXT_WINDOW', '8000'))
        conversation_memory = int(os.getenv('PYTEST_GEN_AI_CONVERSATION_MEMORY', '10'))
        timeout = int(os.getenv('PYTEST_GEN_AI_TIMEOUT', '30'))
        retry_attempts = int(os.getenv('PYTEST_GEN_AI_RETRY_ATTEMPTS', '3'))
        base_url = os.getenv('PYTEST_GEN_AI_BASE_URL')
        
        return {
            'enabled': enabled,
            'provider': provider,
            'model': model,
            'api_key': api_key,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'context_window': context_window,
            'conversation_memory': conversation_memory,
            'timeout': timeout,
            'retry_attempts': retry_attempts,
            'base_url': base_url
        }
    
    @staticmethod
    def save_config_to_file(config, file_path: str) -> None:
        """Save configuration to JSON file."""
        import json
        
        config_dict = {
            "ai_assistant": {
                "enabled": config.enabled,
                "provider": config.provider.value,
                "model": config.model,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "context_window": config.context_window,
                "conversation_memory": config.conversation_memory,
                "timeout": config.timeout,
                "retry_attempts": config.retry_attempts
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    @staticmethod
    def load_config_from_file(config, file_path: str) -> None:
        """Load configuration from JSON file."""
        import json
        
        if not os.path.exists(file_path):
            return
        
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
        
        ai_config = config_dict.get("ai_assistant", {})
        
        if ai_config:
            config.enabled = ai_config.get("enabled", config.enabled)
            
            provider_str = ai_config.get("provider")
            if provider_str:
                try:
                    config.provider = AIProvider(provider_str)
                except ValueError:
                    pass
            
            config.model = ai_config.get("model", config.model)
            config.max_tokens = ai_config.get("max_tokens", config.max_tokens)
            config.temperature = ai_config.get("temperature", config.temperature)
            config.context_window = ai_config.get("context_window", config.context_window)
            config.conversation_memory = ai_config.get("conversation_memory", config.conversation_memory)
            config.timeout = ai_config.get("timeout", config.timeout)
            config.retry_attempts = ai_config.get("retry_attempts", config.retry_attempts)
