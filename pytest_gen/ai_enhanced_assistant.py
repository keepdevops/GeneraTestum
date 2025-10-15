"""
Enhanced AI Assistant with advanced NLP and intelligent recommendations.
"""

from typing import Dict, List, Any, Optional
from .ai_assistant import AIAssistant
from .ai_nlp_models import QueryAnalysis, CodePattern, TestRecommendation
from .ai_query_analyzer import QueryAnalyzer
from .ai_pattern_detector import CodePatternDetector
from .ai_smart_recommendations import SmartRecommendationsEngine


class EnhancedAIAssistant(AIAssistant):
    """Enhanced AI Assistant with advanced NLP capabilities."""
    
    def __init__(self, config_manager=None):
        super().__init__(config_manager)
        self.query_analyzer = QueryAnalyzer()
        self.pattern_detector = CodePatternDetector()
        self.recommendations_engine = SmartRecommendationsEngine()
    
    def enhanced_ask(self, question: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhanced question answering with NLP analysis."""
        # Analyze the query
        query_analysis = self.query_analyzer.analyze_query(question, context_data)
        
        # Get base response from parent
        base_response = self.ask(question, context_data)
        
        if not base_response.get("success", False):
            return base_response
        
        # Enhance response with analysis
        enhanced_response = {
            **base_response,
            "query_analysis": {
                "type": query_analysis.query_type.value,
                "confidence": query_analysis.confidence,
                "intent": query_analysis.intent,
                "keywords": query_analysis.keywords,
                "entities": query_analysis.entities,
                "suggested_actions": query_analysis.suggested_actions
            },
            "enhanced": True
        }
        
        return enhanced_response
    
    def intelligent_analyze_code(self, source_path: str, code: Optional[str] = None) -> Dict[str, Any]:
        """Intelligent code analysis with pattern detection."""
        # Get base analysis
        base_analysis = self.analyze_code(source_path, code)
        
        if not base_analysis.get("success", False):
            return base_analysis
        
        # Read code if not provided
        if code is None:
            try:
                with open(source_path, 'r') as f:
                    code = f.read()
            except Exception as e:
                return {"success": False, "error": f"Could not read file: {e}"}
        
        # Detect patterns
        patterns = self.pattern_detector.analyze_code(code)
        
        # Get pattern insights
        pattern_insights = self.pattern_detector.get_pattern_insights(patterns)
        
        # Enhanced analysis
        enhanced_analysis = {
            **base_analysis,
            "patterns": [
                {
                    "type": p.pattern_type,
                    "confidence": p.confidence,
                    "description": p.description,
                    "complexity": p.complexity.value,
                    "test_recommendations": p.test_recommendations,
                    "mock_strategies": p.mock_strategies
                }
                for p in patterns
            ],
            "insights": pattern_insights["insights"],
            "complexity": pattern_insights["complexity"],
            "enhanced": True
        }
        
        return enhanced_analysis
    
    def get_smart_suggestions(self, 
                            question: str,
                            source_path: Optional[str] = None,
                            context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get smart test suggestions based on query and code analysis."""
        # Analyze query
        query_analysis = self.query_analyzer.analyze_query(question, context_data)
        
        # Analyze code if provided
        patterns = []
        if source_path:
            code_analysis = self.intelligent_analyze_code(source_path)
            if code_analysis.get("success", False):
                patterns = [
                    CodePattern(
                        pattern_type=p["type"],
                        confidence=p["confidence"],
                        description=p["description"],
                        test_recommendations=p["test_recommendations"],
                        mock_strategies=p["mock_strategies"],
                        complexity=p["complexity"]
                    )
                    for p in code_analysis.get("patterns", [])
                ]
        
        # Generate smart recommendations
        recommendations = self.recommendations_engine.generate_recommendations(
            query_analysis, patterns, context_data
        )
        
        return {
            "success": True,
            "query_analysis": {
                "type": query_analysis.query_type.value,
                "confidence": query_analysis.confidence,
                "intent": query_analysis.intent
            },
            "patterns_detected": len(patterns),
            "recommendations": [
                {
                    "title": rec.title,
                    "description": rec.description,
                    "priority": rec.priority,
                    "category": rec.category,
                    "examples": rec.examples,
                    "confidence": rec.confidence
                }
                for rec in recommendations
            ],
            "total_recommendations": len(recommendations),
            "enhanced": True
        }
    
    def contextual_explain(self, 
                          test_files: List[str],
                          context_question: Optional[str] = None) -> Dict[str, Any]:
        """Provide contextual explanations with enhanced understanding."""
        # Get base explanation
        base_explanation = self.explain_generation(test_files)
        
        if not base_explanation.get("success", False):
            return base_explanation
        
        # Enhance with context analysis
        enhanced_explanation = {
            **base_explanation,
            "contextual_enhancements": {
                "files_analyzed": len(test_files),
                "has_context_question": context_question is not None
            }
        }
        
        if context_question:
            query_analysis = self.query_analyzer.analyze_query(context_question)
            enhanced_explanation["context_analysis"] = {
                "question_type": query_analysis.query_type.value,
                "intent": query_analysis.intent,
                "focus_areas": query_analysis.keywords
            }
        
        enhanced_explanation["enhanced"] = True
        
        return enhanced_explanation
    
    def get_learning_insights(self, 
                            interaction_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze interaction history for learning insights."""
        if not interaction_history:
            return {"success": True, "insights": [], "patterns": []}
        
        # Analyze query patterns
        query_types = []
        common_keywords = {}
        
        for interaction in interaction_history:
            if "query_analysis" in interaction:
                query_types.append(interaction["query_analysis"]["type"])
                for keyword in interaction["query_analysis"].get("keywords", []):
                    common_keywords[keyword] = common_keywords.get(keyword, 0) + 1
        
        # Generate insights
        insights = []
        if len(query_types) > 5:
            most_common_type = max(set(query_types), key=query_types.count)
            insights.append(f"Most common query type: {most_common_type}")
        
        if common_keywords:
            top_keywords = sorted(common_keywords.items(), key=lambda x: x[1], reverse=True)[:5]
            insights.append(f"Common topics: {', '.join([k for k, v in top_keywords])}")
        
        return {
            "success": True,
            "insights": insights,
            "interaction_count": len(interaction_history),
            "common_query_types": list(set(query_types)),
            "top_keywords": dict(sorted(common_keywords.items(), key=lambda x: x[1], reverse=True)[:10])
        }
