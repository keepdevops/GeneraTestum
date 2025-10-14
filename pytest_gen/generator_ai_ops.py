"""
AI assistant integration for generator operations.
"""

from typing import List, Dict, Any, Optional
from .ai_assistant import AIAssistant


class GeneratorAIOperations:
    """AI assistant integration for generator operations."""
    
    def __init__(self, config):
        self.config = config
        self.ai_assistant = None
        self._initialize_ai_assistant()
    
    def _initialize_ai_assistant(self):
        """Initialize AI assistant for recommendations."""
        try:
            self.ai_assistant = AIAssistant()
            init_result = self.ai_assistant.initialize()
            if not init_result["success"]:
                # AI assistant not available, continue without it
                self.ai_assistant = None
        except Exception:
            # AI assistant not available, continue without it
            self.ai_assistant = None
    
    def get_ai_recommendations(self, source_path: str) -> Dict[str, Any]:
        """Get AI recommendations for test generation."""
        if not self.ai_assistant:
            return {"success": False, "error": "AI Assistant not available"}
        
        try:
            # Analyze the source code
            analysis_result = self.ai_assistant.analyze_code(source_path)
            
            if not analysis_result["success"]:
                return analysis_result
            
            # Get recommendations based on analysis
            recommendations = {
                "success": True,
                "source_path": source_path,
                "analysis": analysis_result.get("analysis", {}),
                "recommendations": [],
                "suggested_tests": [],
                "mocking_strategy": {},
                "coverage_gaps": []
            }
            
            # Add specific recommendations based on code analysis
            analysis = analysis_result.get("analysis", {})
            if "functions" in analysis:
                recommendations["suggested_tests"].extend([
                    f"Test {func['name']} with various input scenarios"
                    for func in analysis["functions"]
                ])
            
            if "classes" in analysis:
                recommendations["suggested_tests"].extend([
                    f"Test {cls['name']} methods and interactions"
                    for cls in analysis["classes"]
                ])
            
            return recommendations
            
        except Exception as e:
            return {"success": False, "error": f"Failed to get recommendations: {e}"}
    
    def get_ai_test_suggestions(self, test_files: List[str]) -> Dict[str, Any]:
        """Get AI suggestions for improving existing tests."""
        if not self.ai_assistant:
            return {"success": False, "error": "AI Assistant not available"}
        
        try:
            # Read test files content
            test_content = {}
            for test_file in test_files:
                try:
                    with open(test_file, 'r') as f:
                        test_content[test_file] = f.read()
                except Exception:
                    test_content[test_file] = ""
            
            # Get AI review
            review_result = self.ai_assistant.review_tests(test_content)
            
            if not review_result["success"]:
                return review_result
            
            # Format suggestions
            suggestions = {
                "success": True,
                "test_files": test_files,
                "overall_score": review_result.get("overall_score", 0),
                "suggestions": review_result.get("suggestions", []),
                "improvements": review_result.get("improvements", []),
                "best_practices": review_result.get("best_practices", [])
            }
            
            return suggestions
            
        except Exception as e:
            return {"success": False, "error": f"Failed to get test suggestions: {e}"}
    
    def ask_ai_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ask the AI assistant a question with optional context."""
        if not self.ai_assistant:
            return {"success": False, "error": "AI Assistant not available"}
        
        try:
            response = self.ai_assistant.ask(question, context)
            return response
        except Exception as e:
            return {"success": False, "error": f"Failed to ask AI question: {e}"}
