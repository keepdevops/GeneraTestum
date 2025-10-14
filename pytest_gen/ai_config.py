"""
AI Assistant configuration and settings.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .ai_types import AIProvider
from .ai_config_helpers import AIConfigHelpers


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
        env_config = AIConfigHelpers.load_config_from_environment()
        
        return AIConfig(
            enabled=env_config['enabled'],
            provider=env_config['provider'],
            model=env_config['model'],
            api_key=env_config['api_key'],
            max_tokens=env_config['max_tokens'],
            temperature=env_config['temperature'],
            context_window=env_config['context_window'],
            conversation_memory=env_config['conversation_memory'],
            timeout=env_config['timeout'],
            retry_attempts=env_config['retry_attempts'],
            base_url=env_config['base_url']
        )
    
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
            env_var = AIConfigHelpers.get_api_key_env_var(self.config.provider)
            validation_result["errors"].append(f"API key not found. Set {env_var} environment variable")
        
        # Check provider availability
        try:
            AIConfigHelpers.check_provider_availability(self.config.provider)
            validation_result["provider_available"] = True
        except Exception as e:
            validation_result["warnings"].append(f"Provider check failed: {str(e)}")
        
        # Validate parameters
        param_validation = AIConfigHelpers.validate_config_parameters(self.config)
        validation_result["valid"] = validation_result["valid"] and param_validation["valid"]
        validation_result["errors"].extend(param_validation["errors"])
        
        return validation_result
    
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
        AIConfigHelpers.save_config_to_file(self.config, file_path)
    
    def load_from_file(self, file_path: str) -> None:
        """Load configuration from JSON file."""
        AIConfigHelpers.load_config_from_file(self.config, file_path)


# Global configuration instance
ai_config_manager = AIConfigManager()