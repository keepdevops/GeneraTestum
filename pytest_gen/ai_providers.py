"""
AI provider implementations for different LLM services.
"""

from typing import Dict, Any, Optional


class AIProviderBase:
    """Base class for AI providers."""
    
    def __init__(self, config):
        self.config = config
    
    def call_api(self, prompt: str) -> Dict[str, Any]:
        """Call the AI API and return response."""
        raise NotImplementedError


class OpenAIProvider(AIProviderBase):
    """OpenAI API provider."""
    
    def call_api(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API."""
        try:
            import openai
        except ImportError:
            raise Exception("OpenAI library not installed. Install with: pip install openai")
        
        try:
            client = openai.OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
            
            response = client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                timeout=self.config.timeout
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            return {
                "content": content,
                "tokens_used": tokens_used,
                "metadata": {"model": self.config.model}
            }
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


class AnthropicProvider(AIProviderBase):
    """Anthropic API provider."""
    
    def call_api(self, prompt: str) -> Dict[str, Any]:
        """Call Anthropic API."""
        try:
            import anthropic
        except ImportError:
            raise Exception("Anthropic library not installed. Install with: pip install anthropic")
        
        try:
            client = anthropic.Anthropic(api_key=self.config.api_key)
            
            response = client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            return {
                "content": content,
                "tokens_used": tokens_used,
                "metadata": {"model": self.config.model}
            }
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")


class OllamaProvider(AIProviderBase):
    """Ollama API provider for local LLMs."""
    
    def call_api(self, prompt: str) -> Dict[str, Any]:
        """Call Ollama API (local LLM)."""
        try:
            import requests
        except ImportError:
            raise Exception("Requests library not installed. Install with: pip install requests")
        
        try:
            base_url = self.config.base_url or "http://localhost:11434"
            url = f"{base_url}/api/generate"
            
            data = {
                "model": self.config.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens
                }
            }
            
            response = requests.post(url, json=data, timeout=self.config.timeout)
            response.raise_for_status()
            
            result = response.json()
            content = result.get("response", "")
            
            return {
                "content": content,
                "tokens_used": 0,  # Ollama doesn't provide token counts
                "metadata": {"model": self.config.model, "provider": "ollama"}
            }
            
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")


class AIProviderFactory:
    """Factory for creating AI providers."""
    
    @staticmethod
    def create_provider(provider_type: str, config) -> AIProviderBase:
        """Create provider based on type."""
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "ollama": OllamaProvider
        }
        
        provider_class = providers.get(provider_type.lower())
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider_type}")
        
        return provider_class(config)
