"""
AI prompt templates for testing assistance.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from .ai_prompt_formatters import PromptManager


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


class PromptTemplates(PromptManager):
    """Manager for AI prompt templates."""
    
    def __init__(self):
        super().__init__()
    
    def get_prompt(self, prompt_type: PromptType, **kwargs) -> str:
        """Get a formatted prompt template."""
        return super().get_prompt(prompt_type.value, **kwargs)