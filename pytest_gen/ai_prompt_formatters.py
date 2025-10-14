"""
Prompt formatting utilities for AI assistant.
"""

from typing import Dict, Any
from .ai_prompt_templates import PromptTemplates


class PromptFormatters:
    """Utility class for formatting AI prompts."""
    
    @staticmethod
    def format_test_strategy_prompt(template: str, **kwargs) -> str:
        """Format test strategy prompt."""
        return template.format(
            code_type=kwargs.get('code_type', 'Python'),
            framework=kwargs.get('framework', 'Unknown'),
            code=kwargs.get('code', '')
        )
    
    @staticmethod
    def format_coverage_analysis_prompt(template: str, **kwargs) -> str:
        """Format coverage analysis prompt."""
        return template.format(
            source_code=kwargs.get('source_code', ''),
            existing_tests=kwargs.get('existing_tests', '')
        )
    
    @staticmethod
    def format_mock_recommendation_prompt(template: str, **kwargs) -> str:
        """Format mock recommendation prompt."""
        return template.format(
            code=kwargs.get('code', ''),
            dependencies=kwargs.get('dependencies', [])
        )
    
    @staticmethod
    def format_configuration_help_prompt(template: str, **kwargs) -> str:
        """Format configuration help prompt."""
        return template.format(
            requirements=kwargs.get('requirements', ''),
            code_type=kwargs.get('code_type', 'Python'),
            framework=kwargs.get('framework', 'Unknown')
        )
    
    @staticmethod
    def format_error_resolution_prompt(template: str, **kwargs) -> str:
        """Format error resolution prompt."""
        return template.format(
            error_message=kwargs.get('error_message', ''),
            code=kwargs.get('code', ''),
            config=kwargs.get('config', '')
        )
    
    @staticmethod
    def format_code_explanation_prompt(template: str, **kwargs) -> str:
        """Format code explanation prompt."""
        return template.format(
            code=kwargs.get('code', ''),
            config=kwargs.get('config', '')
        )
    
    @staticmethod
    def format_best_practices_prompt(template: str, **kwargs) -> str:
        """Format best practices prompt."""
        return template.format(
            topic=kwargs.get('topic', 'general testing'),
            context=kwargs.get('context', '')
        )
    
    @staticmethod
    def format_conversation_prompt(template: str, **kwargs) -> str:
        """Format conversation prompt."""
        return template.format(
            context=kwargs.get('context', ''),
            conversation_history=kwargs.get('conversation_history', ''),
            question=kwargs.get('question', '')
        )


class PromptManager:
    """Manager for AI prompt templates."""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.formatters = PromptFormatters()
    
    def _load_templates(self) -> dict:
        """Load all prompt templates."""
        return {
            "system": PromptTemplates.system_prompt(),
            "test_strategy": PromptTemplates.test_strategy_prompt(),
            "coverage_analysis": PromptTemplates.coverage_analysis_prompt(),
            "mock_recommendation": PromptTemplates.mock_recommendation_prompt(),
            "configuration_help": PromptTemplates.configuration_help_prompt(),
            "error_resolution": PromptTemplates.error_resolution_prompt(),
            "code_explanation": PromptTemplates.code_explanation_prompt(),
            "best_practices": PromptTemplates.best_practices_prompt(),
            "conversation": PromptTemplates.conversation_prompt()
        }
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        """Get a formatted prompt template."""
        template = self.templates.get(prompt_type, "")
        
        if prompt_type == "test_strategy":
            return self.formatters.format_test_strategy_prompt(template, **kwargs)
        elif prompt_type == "coverage_analysis":
            return self.formatters.format_coverage_analysis_prompt(template, **kwargs)
        elif prompt_type == "mock_recommendation":
            return self.formatters.format_mock_recommendation_prompt(template, **kwargs)
        elif prompt_type == "configuration_help":
            return self.formatters.format_configuration_help_prompt(template, **kwargs)
        elif prompt_type == "error_resolution":
            return self.formatters.format_error_resolution_prompt(template, **kwargs)
        elif prompt_type == "code_explanation":
            return self.formatters.format_code_explanation_prompt(template, **kwargs)
        elif prompt_type == "best_practices":
            return self.formatters.format_best_practices_prompt(template, **kwargs)
        elif prompt_type == "conversation":
            return self.formatters.format_conversation_prompt(template, **kwargs)
        
        return template