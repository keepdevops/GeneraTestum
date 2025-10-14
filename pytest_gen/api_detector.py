"""
Framework detection for API analyzers.
"""

from typing import Optional


class APIFrameworkDetector:
    """Detects which API framework is being used in code."""
    
    def __init__(self):
        self.framework_indicators = {
            'flask': ['from flask import', 'import flask', '@app.route'],
            'fastapi': ['from fastapi import', 'import fastapi', '@app.get', '@app.post'],
            'django': ['from django', 'import django', 'class.*View'],
            'tornado': ['from tornado', 'import tornado', 'class.*Handler'],
            'panel': ['import panel', 'import panel as pn', 'pn.widgets', 'pn.Row', 'pn.Column', '@pn.depends']
        }
    
    def detect_framework(self, content: str) -> Optional[str]:
        """Detect which framework is being used."""
        content_lower = content.lower()
        
        for framework, indicators in self.framework_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                return framework
        
        return None
    
    def has_api_indicators(self, content: str) -> bool:
        """Check if content has any API framework indicators."""
        return self.detect_framework(content) is not None
