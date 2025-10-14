"""
AI Assistant configuration and settings.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AIProvider(Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


@dataclass
class AIConfig:
    """Configuration for AI assistant."""
    enabled: bool = True
    provider: AIProvider = AIProvider.OPENAI
    model: str = "gpt-4"
    api_key: Optional[str] = None
    max_tokens: int = 2000
    temperature: float = 0.7
    context_window: int = 8000
    conversation_memory: int = 10
    timeout: int = 30
    retry_attempts: int = 3
    base_url: Optional[str] = None  # For local LLMs like Ollama


class AIConfigManager:
    """Manages AI configuration loading and validation."""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> AIConfig:
        """Load AI configuration from environment and defaults."""
        # Load from environment variables
        enabled = os.getenv('PYTEST_GEN_AI_ENABLED', 'true').lower() == 'true'
        
        provider_str = os.getenv('PYTEST_GEN_AI_PROVIDER', 'openai').lower()
        try:
            provider = AIProvider(provider_str)
        except ValueError:
            provider = AIProvider.OPENAI
        
        model = os.getenv('PYTEST_GEN_AI_MODEL', self._get_default_model(provider))
        api_key = os.getenv(self._get_api_key_env_var(provider))
        
        max_tokens = int(os.getenv('PYTEST_GEN_AI_MAX_TOKENS', '2000'))
        temperature = float(os.getenv('PYTEST_GEN_AI_TEMPERATURE', '0.7'))
        context_window = int(os.getenv('PYTEST_GEN_AI_CONTEXT_WINDOW', '8000'))
        conversation_memory = int(os.getenv('PYTEST_GEN_AI_CONVERSATION_MEMORY', '10'))
        timeout = int(os.getenv('PYTEST_GEN_AI_TIMEOUT', '30'))
        retry_attempts = int(os.getenv('PYTEST_GEN_AI_RETRY_ATTEMPTS', '3'))
        base_url = os.getenv('PYTEST_GEN_AI_BASE_URL')
        
        return AIConfig(
            enabled=enabled,
            provider=provider,
            model=model,
            api_key=api_key,
            max_tokens=max_tokens,
            temperature=temperature,
            context_window=context_window,
            conversation_memory=conversation_memory,
            timeout=timeout,
            retry_attempts=retry_attempts,
            base_url=base_url
        )
    
    def _get_default_model(self, provider: AIProvider) -> str:
        """Get default model for provider."""
        defaults = {
            AIProvider.OPENAI: "gpt-4",
            AIProvider.ANTHROPIC: "claude-3-sonnet-20240229",
            AIProvider.OLLAMA: "llama2"
        }
        return defaults.get(provider, "gpt-4")
    
    def _get_api_key_env_var(self, provider: AIProvider) -> str:
        """Get API key environment variable for provider."""
        env_vars = {
            AIProvider.OPENAI: "OPENAI_API_KEY",
            AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            AIProvider.OLLAMA: "OLLAMA_API_KEY"  # Usually not needed for local
        }
        return env_vars.get(provider, "OPENAI_API_KEY")
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate AI configuration and return status."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "provider_available": False
        }
        
        if not self.config.enabled:
            validation_result["warnings"].append("AI assistant is disabled")
            return validation_result
        
        # Check API key
        if self.config.provider != AIProvider.OLLAMA and not self.config.api_key:
            validation_result["valid"] = False
            env_var = self._get_api_key_env_var(self.config.provider)
            validation_result["errors"].append(f"API key not found. Set {env_var} environment variable")
        
        # Check provider availability
        try:
            self._check_provider_availability()
            validation_result["provider_available"] = True
        except Exception as e:
            validation_result["warnings"].append(f"Provider check failed: {str(e)}")
        
        # Validate parameters
        if self.config.max_tokens <= 0:
            validation_result["valid"] = False
            validation_result["errors"].append("max_tokens must be positive")
        
        if not 0.0 <= self.config.temperature <= 2.0:
            validation_result["valid"] = False
            validation_result["errors"].append("temperature must be between 0.0 and 2.0")
        
        if self.config.context_window <= 0:
            validation_result["valid"] = False
            validation_result["errors"].append("context_window must be positive")
        
        return validation_result
    
    def _check_provider_availability(self):
        """Check if the configured provider is available."""
        if self.config.provider == AIProvider.OPENAI:
            try:
                import openai
                # Basic availability check
                return True
            except ImportError:
                raise Exception("OpenAI library not installed")
        
        elif self.config.provider == AIProvider.ANTHROPIC:
            try:
                import anthropic
                # Basic availability check
                return True
            except ImportError:
                raise Exception("Anthropic library not installed")
        
        elif self.config.provider == AIProvider.OLLAMA:
            # For Ollama, we assume it's running locally
            return True
        
        else:
            raise Exception(f"Unknown provider: {self.config.provider}")
    
    def get_config(self) -> AIConfig:
        """Get current AI configuration."""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration with new values."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def save_to_file(self, file_path: str) -> None:
        """Save configuration to JSON file."""
        import json
        
        config_dict = {
            "ai_assistant": {
                "enabled": self.config.enabled,
                "provider": self.config.provider.value,
                "model": self.config.model,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                "context_window": self.config.context_window,
                "conversation_memory": self.config.conversation_memory,
                "timeout": self.config.timeout,
                "retry_attempts": self.config.retry_attempts
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def load_from_file(self, file_path: str) -> None:
        """Load configuration from JSON file."""
        import json
        
        if not os.path.exists(file_path):
            return
        
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
        
        ai_config = config_dict.get("ai_assistant", {})
        
        if ai_config:
            self.config.enabled = ai_config.get("enabled", self.config.enabled)
            
            provider_str = ai_config.get("provider")
            if provider_str:
                try:
                    self.config.provider = AIProvider(provider_str)
                except ValueError:
                    pass
            
            self.config.model = ai_config.get("model", self.config.model)
            self.config.max_tokens = ai_config.get("max_tokens", self.config.max_tokens)
            self.config.temperature = ai_config.get("temperature", self.config.temperature)
            self.config.context_window = ai_config.get("context_window", self.config.context_window)
            self.config.conversation_memory = ai_config.get("conversation_memory", self.config.conversation_memory)
            self.config.timeout = ai_config.get("timeout", self.config.timeout)
            self.config.retry_attempts = ai_config.get("retry_attempts", self.config.retry_attempts)


# Global configuration instance
ai_config_manager = AIConfigManager()
