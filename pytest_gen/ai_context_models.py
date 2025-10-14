"""
Data models for AI context management.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """Represents a message in the conversation."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeContext:
    """Represents code context for analysis."""
    file_path: str
    content: str
    analysis_result: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    framework: Optional[str] = None
    code_type: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
