"""
Query analysis and intent detection for AI assistant.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from .ai_nlp_models import QueryType, QueryAnalysis


class QueryAnalyzer:
    """Analyzes user queries for intent and context."""
    
    def __init__(self):
        self.query_patterns = {
            QueryType.TEST_STRATEGY: [
                r"how.*test", r"test.*strategy", r"what.*test", 
                r"testing.*approach", r"test.*coverage"
            ],
            QueryType.MOCKING_HELP: [
                r"mock", r"stub", r"fake", r"spy", r"patch",
                r"dependency", r"external", r"api.*call"
            ],
            QueryType.PATTERN_RECOGNITION: [
                r"pattern", r"design.*pattern", r"common.*approach",
                r"best.*practice", r"typical.*way"
            ],
            QueryType.OPTIMIZATION: [
                r"optimize", r"improve", r"performance", r"speed",
                r"faster", r"efficient", r"slow.*test"
            ],
            QueryType.DEBUGGING: [
                r"debug", r"fix", r"error", r"problem", r"issue",
                r"not.*working", r"fail", r"exception"
            ],
            QueryType.EXPLANATION: [
                r"explain", r"what.*does", r"how.*work", r"why",
                r"meaning", r"purpose"
            ]
        }
        
        self.code_keywords = {
            "async": ["async", "await", "coroutine", "asyncio"],
            "database": ["db", "database", "sql", "query", "orm", "model"],
            "api": ["api", "endpoint", "route", "request", "response", "http"],
            "file": ["file", "read", "write", "path", "directory"],
            "network": ["socket", "connection", "http", "tcp", "udp"],
            "cache": ["cache", "redis", "memcache", "ttl"],
            "auth": ["auth", "login", "password", "token", "session"],
            "validation": ["validate", "schema", "input", "format"]
        }
    
    def analyze_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> QueryAnalysis:
        """Analyze user query for intent and context."""
        query_lower = query.lower()
        
        # Determine query type
        query_type, confidence = self._classify_query(query_lower)
        
        # Extract keywords and entities
        keywords = self._extract_keywords(query_lower)
        entities = self._extract_entities(query_lower)
        
        # Determine intent
        intent = self._determine_intent(query_type, keywords, entities)
        
        # Identify context needed
        context_needed = self._identify_context_needed(query_type, keywords)
        
        # Suggest actions
        suggested_actions = self._suggest_actions(query_type, keywords, context)
        
        return QueryAnalysis(
            query_type=query_type,
            confidence=confidence,
            keywords=keywords,
            entities=entities,
            intent=intent,
            context_needed=context_needed,
            suggested_actions=suggested_actions
        )
    
    def _classify_query(self, query: str) -> Tuple[QueryType, float]:
        """Classify the type of query."""
        scores = {}
        
        for query_type, patterns in self.query_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query):
                    score += 1
            
            if score > 0:
                scores[query_type] = score / len(patterns)
        
        if not scores:
            return QueryType.GENERAL, 0.5
        
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]
        
        return best_type, confidence
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from query."""
        keywords = []
        
        # Technical keywords
        for category, words in self.code_keywords.items():
            for word in words:
                if word in query:
                    keywords.append(word)
        
        # Testing keywords
        testing_words = ["test", "assert", "mock", "fixture", "parametrize", "coverage"]
        for word in testing_words:
            if word in query:
                keywords.append(word)
        
        return list(set(keywords))
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract entities (filenames, function names, etc.)."""
        entities = []
        
        # File extensions
        file_patterns = [r'\w+\.py', r'\w+\.java', r'\w+\.js', r'\w+\.ts']
        for pattern in file_patterns:
            entities.extend(re.findall(pattern, query))
        
        # Function/class names (simple heuristic)
        name_patterns = [r'[A-Z][a-zA-Z0-9_]*', r'[a-z][a-zA-Z0-9_]*\(']
        for pattern in name_patterns:
            entities.extend(re.findall(pattern, query))
        
        return list(set(entities))
    
    def _determine_intent(self, query_type: QueryType, keywords: List[str], entities: List[str]) -> str:
        """Determine the user's intent."""
        intents = {
            QueryType.TEST_STRATEGY: "User wants guidance on testing approach",
            QueryType.MOCKING_HELP: "User needs help with mocking dependencies",
            QueryType.PATTERN_RECOGNITION: "User wants to understand testing patterns",
            QueryType.OPTIMIZATION: "User wants to improve test performance",
            QueryType.DEBUGGING: "User has testing issues to resolve",
            QueryType.EXPLANATION: "User wants explanation of test concepts",
            QueryType.BEST_PRACTICES: "User wants testing best practices",
            QueryType.GENERAL: "User has general testing questions"
        }
        
        base_intent = intents.get(query_type, "General inquiry")
        
        if entities:
            base_intent += f" related to {', '.join(entities[:3])}"
        
        return base_intent
    
    def _identify_context_needed(self, query_type: QueryType, keywords: List[str]) -> List[str]:
        """Identify what context is needed for the query."""
        context_map = {
            QueryType.TEST_STRATEGY: ["source_code", "existing_tests"],
            QueryType.MOCKING_HELP: ["source_code", "dependencies"],
            QueryType.PATTERN_RECOGNITION: ["source_code", "test_patterns"],
            QueryType.OPTIMIZATION: ["test_performance", "existing_tests"],
            QueryType.DEBUGGING: ["error_logs", "failing_tests"],
            QueryType.EXPLANATION: ["source_code"],
            QueryType.BEST_PRACTICES: ["project_context"],
            QueryType.GENERAL: []
        }
        
        return context_map.get(query_type, [])
    
    def _suggest_actions(self, query_type: QueryType, keywords: List[str], context: Optional[Dict[str, Any]]) -> List[str]:
        """Suggest actions based on query analysis."""
        actions = {
            QueryType.TEST_STRATEGY: ["analyze_code", "suggest_tests", "show_patterns"],
            QueryType.MOCKING_HELP: ["analyze_dependencies", "suggest_mocks", "show_examples"],
            QueryType.OPTIMIZATION: ["analyze_performance", "suggest_optimizations"],
            QueryType.DEBUGGING: ["analyze_errors", "suggest_fixes"],
            QueryType.EXPLANATION: ["explain_concepts", "show_examples"],
            QueryType.GENERAL: ["provide_general_help"]
        }
        
        return actions.get(query_type, ["provide_help"])
