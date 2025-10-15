"""
AI NLP data models and enums.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any


class QueryType(Enum):
    """Types of user queries."""
    TEST_STRATEGY = "test_strategy"
    MOCKING_HELP = "mocking_help"
    PATTERN_RECOGNITION = "pattern_recognition"
    OPTIMIZATION = "optimization"
    DEBUGGING = "debugging"
    BEST_PRACTICES = "best_practices"
    EXPLANATION = "explanation"
    GENERAL = "general"


class CodeComplexity(Enum):
    """Code complexity levels."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"


@dataclass
class QueryAnalysis:
    """Analysis of user query."""
    query_type: QueryType
    confidence: float
    keywords: List[str]
    entities: List[str]
    intent: str
    context_needed: List[str]
    suggested_actions: List[str]


@dataclass
class CodePattern:
    """Detected code pattern."""
    pattern_type: str
    confidence: float
    description: str
    test_recommendations: List[str]
    mock_strategies: List[str]
    complexity: CodeComplexity


@dataclass
class TestRecommendation:
    """Test recommendation with metadata."""
    title: str
    description: str
    priority: str
    category: str
    examples: List[str]
    confidence: float
