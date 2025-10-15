"""
API pattern detection and framework identification.
"""

import re
from typing import Dict, List, Optional


class APIPatternDetector:
    """Detects API frameworks and patterns in source code."""

    def __init__(self):
        self.framework_patterns = {
            'flask': [
                'from flask import',
                'import flask',
                '@app.route'
            ],
            'fastapi': [
                'from fastapi import',
                'import fastapi',
                '@app.get',
                '@app.post'
            ],
            'django': [
                'from django import',
                'import django',
                'path(',
                'url('
            ],
            'tornado': [
                'from tornado import',
                'import tornado',
                'class.*Handler'
            ],
            'bottle': [
                'from bottle import',
                'import bottle',
                '@route'
            ]
        }
        
        self.endpoint_patterns = {
            'flask': [
                r'@app\.route\s*\(\s*["\']([^"\']+)["\']',
                r'@.*\.route\s*\(\s*["\']([^"\']+)["\']'
            ],
            'fastapi': [
                r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                r'@.*\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
            ],
            'django': [
                r'path\s*\(\s*["\']([^"\']+)["\']',
                r'url\s*\(\s*["\']([^"\']+)["\']'
            ]
        }

    def detect_framework(self, source_code: str) -> Optional[str]:
        """Detect the web framework used in the source code."""
        for framework, indicators in self.framework_patterns.items():
            if any(indicator in source_code for indicator in indicators):
                return framework
        return None

    def get_endpoint_patterns(self, framework: str) -> List[str]:
        """Get endpoint extraction patterns for a framework."""
        return self.endpoint_patterns.get(framework, [])

    def extract_route_patterns(self, source_code: str, framework: str) -> List[tuple]:
        """Extract route patterns from source code."""
        patterns = self.get_endpoint_patterns(framework)
        matches = []
        
        for pattern in patterns:
            found_matches = re.findall(pattern, source_code)
            matches.extend(found_matches)
        
        return matches

    def get_relationship_patterns(self) -> Dict[str, List[tuple]]:
        """Get relationship patterns between HTTP methods."""
        return {
            'create_then_get': [
                ('POST', 'GET'),
                ('PUT', 'GET'),
                ('PATCH', 'GET')
            ],
            'create_then_update': [
                ('POST', 'PUT'),
                ('POST', 'PATCH'),
                ('PUT', 'PATCH')
            ],
            'create_then_delete': [
                ('POST', 'DELETE'),
                ('PUT', 'DELETE'),
                ('PATCH', 'DELETE')
            ],
            'dependency_chain': [
                ('GET', 'POST'),
                ('POST', 'PUT'),
                ('PUT', 'DELETE')
            ]
        }

    def analyze_method_relationships(self, source_method: str, target_method: str) -> Optional[str]:
        """Analyze relationship between two HTTP methods."""
        patterns = self.get_relationship_patterns()
        
        for relationship_type, method_pairs in patterns.items():
            if (source_method, target_method) in method_pairs:
                return relationship_type
        
        return None
