"""
AI prompt templates for testing assistance.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from .ai_prompt_formatters import PromptFormatters, PromptTemplates


class PromptType(Enum):
    """Types of prompts available."""
    SYSTEM = "system"
    TEST_STRATEGY = "test_strategy"
    COVERAGE_ANALYSIS = "coverage_analysis"
    MOCK_RECOMMENDATION = "mock_recommendation"
    CONFIGURATION_HELP = "configuration_help"
    ERROR_RESOLUTION = "error_resolution"
    CODE_EXPLANATION = "code_explanation"
    BEST_PRACTICES = "best_practices"
    CONVERSATION = "conversation"


class PromptManager:
    """Manager for AI prompt templates."""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.formatters = PromptFormatters()
    
    def _load_templates(self) -> Dict[PromptType, str]:
        """Load all prompt templates."""
        return {
            PromptType.SYSTEM: PromptTemplates.system_prompt(),
            PromptType.TEST_STRATEGY: PromptTemplates.test_strategy_prompt(),
            PromptType.COVERAGE_ANALYSIS: PromptTemplates.coverage_analysis_prompt(),
            PromptType.MOCK_RECOMMENDATION: PromptTemplates.mock_recommendation_prompt(),
            PromptType.CONFIGURATION_HELP: PromptTemplates.configuration_help_prompt(),
            PromptType.ERROR_RESOLUTION: PromptTemplates.error_resolution_prompt(),
            PromptType.CODE_EXPLANATION: PromptTemplates.code_explanation_prompt(),
            PromptType.BEST_PRACTICES: PromptTemplates.best_practices_prompt(),
            PromptType.CONVERSATION: PromptTemplates.conversation_prompt()
        }
    
    def get_prompt(self, prompt_type: PromptType, **kwargs) -> str:
        """Get a formatted prompt template."""
        template = self.templates.get(prompt_type, "")
        
        if prompt_type == PromptType.TEST_STRATEGY:
            return self.formatters.format_test_strategy_prompt(template, **kwargs)
        elif prompt_type == PromptType.COVERAGE_ANALYSIS:
            return self.formatters.format_coverage_analysis_prompt(template, **kwargs)
        elif prompt_type == PromptType.MOCK_RECOMMENDATION:
            return self.formatters.format_mock_recommendation_prompt(template, **kwargs)
        elif prompt_type == PromptType.CONFIGURATION_HELP:
            return self.formatters.format_configuration_help_prompt(template, **kwargs)
        elif prompt_type == PromptType.ERROR_RESOLUTION:
            return self.formatters.format_error_resolution_prompt(template, **kwargs)
        elif prompt_type == PromptType.CODE_EXPLANATION:
            return self.formatters.format_code_explanation_prompt(template, **kwargs)
        elif prompt_type == PromptType.BEST_PRACTICES:
            return self.formatters.format_best_practices_prompt(template, **kwargs)
        elif prompt_type == PromptType.CONVERSATION:
            return self.formatters.format_conversation_prompt(template, **kwargs)
        
        return template


# Legacy compatibility - keep the old class name
class PromptTemplates(PromptManager):
    """Legacy compatibility class."""
    pass