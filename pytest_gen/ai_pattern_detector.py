"""
Intelligent code pattern detection for test recommendations.
"""

from typing import List, Dict, Any
from .ai_nlp_models import CodePattern, CodeComplexity


class CodePatternDetector:
    """Detects patterns in code for intelligent test recommendations."""
    
    def __init__(self):
        self.patterns = {
            "async_function": {
                "indicators": ["async def", "await"],
                "test_recommendations": [
                    "Use pytest-asyncio for async testing",
                    "Test both success and error cases",
                    "Mock async dependencies properly"
                ],
                "mock_strategies": [
                    "Use AsyncMock for async dependencies",
                    "Patch async context managers"
                ]
            },
            "database_operations": {
                "indicators": ["db.", "session.", "query(", "SQL"],
                "test_recommendations": [
                    "Use database fixtures",
                    "Test with test database",
                    "Verify transactions"
                ],
                "mock_strategies": [
                    "Mock database connections",
                    "Use in-memory database for tests"
                ]
            },
            "api_endpoint": {
                "indicators": ["@app.route", "@router", "FastAPI", "Flask"],
                "test_recommendations": [
                    "Test HTTP status codes",
                    "Test request/response formats",
                    "Test authentication"
                ],
                "mock_strategies": [
                    "Mock external API calls",
                    "Use test client"
                ]
            },
            "file_operations": {
                "indicators": ["open(", "read", "write", "Path("],
                "test_recommendations": [
                    "Test file existence",
                    "Test file permissions",
                    "Test error handling"
                ],
                "mock_strategies": [
                    "Mock file system operations",
                    "Use temporary files"
                ]
            },
            "authentication": {
                "indicators": ["login", "auth", "token", "session", "jwt"],
                "test_recommendations": [
                    "Test authentication flows",
                    "Test authorization levels",
                    "Test token validation"
                ],
                "mock_strategies": [
                    "Mock authentication services",
                    "Use test user fixtures"
                ]
            }
        }
    
    def analyze_code(self, code: str) -> List[CodePattern]:
        """Analyze code and detect patterns."""
        detected_patterns = []
        
        for pattern_name, pattern_info in self.patterns.items():
            confidence = self._calculate_pattern_confidence(code, pattern_info["indicators"])
            
            if confidence > 0.3:  # Threshold for pattern detection
                complexity = self._determine_complexity(code, pattern_name)
                
                pattern = CodePattern(
                    pattern_type=pattern_name,
                    confidence=confidence,
                    description=self._get_pattern_description(pattern_name),
                    test_recommendations=pattern_info["test_recommendations"],
                    mock_strategies=pattern_info["mock_strategies"],
                    complexity=complexity
                )
                detected_patterns.append(pattern)
        
        return detected_patterns
    
    def _calculate_pattern_confidence(self, code: str, indicators: List[str]) -> float:
        """Calculate confidence for a pattern match."""
        matches = 0
        for indicator in indicators:
            if indicator in code:
                matches += 1
        
        return matches / len(indicators) if indicators else 0
    
    def _determine_complexity(self, code: str, pattern_type: str) -> CodeComplexity:
        """Determine code complexity level."""
        lines = code.split('\n')
        line_count = len(lines)
        
        # Count complexity indicators
        complexity_indicators = 0
        for line in lines:
            if any(keyword in line for keyword in ["try:", "except:", "if ", "for ", "while "]):
                complexity_indicators += 1
        
        if line_count > 100 or complexity_indicators > 20:
            return CodeComplexity.ENTERPRISE
        elif line_count > 50 or complexity_indicators > 10:
            return CodeComplexity.COMPLEX
        elif line_count > 20 or complexity_indicators > 5:
            return CodeComplexity.MEDIUM
        else:
            return CodeComplexity.SIMPLE
    
    def _get_pattern_description(self, pattern_type: str) -> str:
        """Get human-readable description of pattern."""
        descriptions = {
            "async_function": "Asynchronous function requiring special testing",
            "database_operations": "Database interaction requiring data fixtures",
            "api_endpoint": "API endpoint requiring HTTP testing",
            "file_operations": "File system operations requiring I/O mocking",
            "authentication": "Authentication/authorization requiring security testing"
        }
        return descriptions.get(pattern_type, "Detected code pattern")
    
    def get_pattern_insights(self, patterns: List[CodePattern]) -> Dict[str, Any]:
        """Get insights from detected patterns."""
        if not patterns:
            return {"insights": [], "complexity": "simple", "recommendations": []}
        
        # Analyze complexity distribution
        complexity_counts = {}
        for pattern in patterns:
            complexity = pattern.complexity.value
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        # Determine overall complexity
        if complexity_counts.get("enterprise", 0) > 0:
            overall_complexity = "enterprise"
        elif complexity_counts.get("complex", 0) > 0:
            overall_complexity = "complex"
        elif complexity_counts.get("medium", 0) > 0:
            overall_complexity = "medium"
        else:
            overall_complexity = "simple"
        
        # Generate insights
        insights = []
        if len(patterns) > 3:
            insights.append("Multiple patterns detected - consider comprehensive test suite")
        
        if any(p.pattern_type == "async_function" for p in patterns):
            insights.append("Async code detected - ensure proper async testing setup")
        
        if any(p.pattern_type == "database_operations" for p in patterns):
            insights.append("Database operations detected - plan for data management in tests")
        
        return {
            "insights": insights,
            "complexity": overall_complexity,
            "recommendations": self._generate_pattern_recommendations(patterns)
        }
    
    def _generate_pattern_recommendations(self, patterns: List[CodePattern]) -> List[str]:
        """Generate recommendations based on patterns."""
        recommendations = []
        
        # Collect all recommendations
        for pattern in patterns:
            recommendations.extend(pattern.test_recommendations)
            recommendations.extend(pattern.mock_strategies)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations
