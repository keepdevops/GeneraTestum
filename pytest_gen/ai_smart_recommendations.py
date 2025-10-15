"""
Smart test recommendations engine.
"""

from typing import Dict, List, Any, Optional
from .ai_nlp_models import QueryAnalysis, CodePattern, TestRecommendation, QueryType


class SmartRecommendationsEngine:
    """Generates intelligent test recommendations based on analysis."""
    
    def __init__(self):
        self.recommendation_templates = {
            "coverage_gap": "Consider adding tests for: {missing_coverage}",
            "performance": "Optimize test performance by: {optimizations}",
            "maintainability": "Improve test maintainability with: {improvements}",
            "edge_cases": "Add edge case tests for: {edge_cases}",
            "integration": "Consider integration tests for: {integrations}",
            "security": "Add security tests for: {security_areas}",
            "error_handling": "Test error scenarios: {error_scenarios}"
        }
        
        self.priority_weights = {
            QueryType.DEBUGGING: 0.9,
            QueryType.OPTIMIZATION: 0.8,
            QueryType.MOCKING_HELP: 0.7,
            QueryType.TEST_STRATEGY: 0.6,
            QueryType.PATTERN_RECOGNITION: 0.5,
            QueryType.EXPLANATION: 0.4,
            QueryType.BEST_PRACTICES: 0.3,
            QueryType.GENERAL: 0.2
        }
    
    def generate_recommendations(self, 
                               query_analysis: QueryAnalysis,
                               code_patterns: List[CodePattern],
                               context: Optional[Dict[str, Any]] = None) -> List[TestRecommendation]:
        """Generate smart test recommendations."""
        recommendations = []
        
        # Based on query type
        query_recommendations = self._generate_query_recommendations(query_analysis, code_patterns)
        recommendations.extend(query_recommendations)
        
        # Based on detected patterns
        pattern_recommendations = self._generate_pattern_recommendations(code_patterns)
        recommendations.extend(pattern_recommendations)
        
        # Based on context
        if context:
            context_recommendations = self._generate_context_recommendations(context, query_analysis)
            recommendations.extend(context_recommendations)
        
        # Sort by priority and remove duplicates
        recommendations = self._deduplicate_and_prioritize(recommendations, query_analysis)
        
        return recommendations
    
    def _generate_query_recommendations(self, 
                                      query_analysis: QueryAnalysis, 
                                      patterns: List[CodePattern]) -> List[TestRecommendation]:
        """Generate recommendations based on query type."""
        recommendations = []
        
        if query_analysis.query_type == QueryType.MOCKING_HELP:
            recommendations.extend(self._generate_mocking_recommendations(patterns))
        
        if query_analysis.query_type == QueryType.OPTIMIZATION:
            recommendations.extend(self._generate_optimization_recommendations())
        
        if query_analysis.query_type == QueryType.DEBUGGING:
            recommendations.extend(self._generate_debugging_recommendations())
        
        if query_analysis.query_type == QueryType.TEST_STRATEGY:
            recommendations.extend(self._generate_strategy_recommendations(patterns))
        
        return recommendations
    
    def _generate_mocking_recommendations(self, patterns: List[CodePattern]) -> List[TestRecommendation]:
        """Generate mocking-specific recommendations."""
        recommendations = []
        
        for pattern in patterns:
            for strategy in pattern.mock_strategies:
                recommendations.append(TestRecommendation(
                    title=f"Mocking Strategy for {pattern.pattern_type}",
                    description=strategy,
                    priority="high",
                    category="mocking",
                    examples=[],
                    confidence=pattern.confidence
                ))
        
        # General mocking advice
        recommendations.append(TestRecommendation(
            title="General Mocking Best Practices",
            description="Mock external dependencies to isolate unit tests",
            priority="medium",
            category="mocking",
            examples=["Use dependency injection", "Consider factory patterns"],
            confidence=0.8
        ))
        
        return recommendations
    
    def _generate_optimization_recommendations(self) -> List[TestRecommendation]:
        """Generate performance optimization recommendations."""
        return [
            TestRecommendation(
                title="Parallel Test Execution",
                description="Use pytest-xdist for parallel test execution",
                priority="high",
                category="performance",
                examples=["pytest -n auto", "pytest -n 4"],
                confidence=0.9
            ),
            TestRecommendation(
                title="Fixture Optimization",
                description="Optimize fixtures to reduce setup/teardown time",
                priority="medium",
                category="performance",
                examples=["Use scope='session'", "Cache expensive operations"],
                confidence=0.7
            )
        ]
    
    def _generate_debugging_recommendations(self) -> List[TestRecommendation]:
        """Generate debugging recommendations."""
        return [
            TestRecommendation(
                title="Enhanced Error Reporting",
                description="Add detailed error messages and logging",
                priority="high",
                category="debugging",
                examples=["Use pytest --tb=long", "Add custom error messages"],
                confidence=0.8
            ),
            TestRecommendation(
                title="Test Isolation",
                description="Ensure tests don't interfere with each other",
                priority="high",
                category="debugging",
                examples=["Use fresh fixtures", "Clean up after tests"],
                confidence=0.7
            )
        ]
    
    def _generate_strategy_recommendations(self, patterns: List[CodePattern]) -> List[TestRecommendation]:
        """Generate testing strategy recommendations."""
        recommendations = []
        
        if any(p.pattern_type == "async_function" for p in patterns):
            recommendations.append(TestRecommendation(
                title="Async Testing Strategy",
                description="Implement comprehensive async testing",
                priority="high",
                category="strategy",
                examples=["pytest-asyncio", "async fixtures"],
                confidence=0.9
            ))
        
        if any(p.pattern_type == "database_operations" for p in patterns):
            recommendations.append(TestRecommendation(
                title="Database Testing Strategy",
                description="Plan for database testing and data management",
                priority="high",
                category="strategy",
                examples=["Test database", "Transaction testing"],
                confidence=0.8
            ))
        
        return recommendations
    
    def _generate_pattern_recommendations(self, patterns: List[CodePattern]) -> List[TestRecommendation]:
        """Generate recommendations based on detected patterns."""
        recommendations = []
        
        for pattern in patterns:
            for rec in pattern.test_recommendations:
                recommendations.append(TestRecommendation(
                    title=f"Pattern: {pattern.pattern_type}",
                    description=rec,
                    priority="medium",
                    category="pattern",
                    examples=[],
                    confidence=pattern.confidence
                ))
        
        return recommendations
    
    def _generate_context_recommendations(self, 
                                        context: Dict[str, Any], 
                                        query_analysis: QueryAnalysis) -> List[TestRecommendation]:
        """Generate recommendations based on context."""
        recommendations = []
        
        if "existing_tests" in context:
            recommendations.append(TestRecommendation(
                title="Coverage Analysis",
                description="Review existing tests for coverage gaps",
                priority="medium",
                category="coverage",
                examples=["pytest-cov", "Coverage analysis"],
                confidence=0.6
            ))
        
        if "performance_issues" in context:
            recommendations.append(TestRecommendation(
                title="Performance Profiling",
                description="Profile slow tests and optimize bottlenecks",
                priority="high",
                category="performance",
                examples=["pytest-benchmark", "cProfile"],
                confidence=0.8
            ))
        
        return recommendations
    
    def _deduplicate_and_prioritize(self, 
                                   recommendations: List[TestRecommendation],
                                   query_analysis: QueryAnalysis) -> List[TestRecommendation]:
        """Remove duplicates and prioritize recommendations."""
        # Remove duplicates based on description
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec.description not in seen:
                seen.add(rec.description)
                unique_recommendations.append(rec)
        
        # Sort by priority and query type relevance
        def sort_key(rec):
            priority_score = {"high": 3, "medium": 2, "low": 1}.get(rec.priority, 1)
            query_relevance = self.priority_weights.get(query_analysis.query_type, 0.2)
            return (priority_score * query_relevance, rec.confidence)
        
        return sorted(unique_recommendations, key=sort_key, reverse=True)
