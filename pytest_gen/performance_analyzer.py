"""
Performance analyzer for identifying performance-critical functions.
"""

import ast
from typing import Dict, List, Any, Optional
from .performance_test_models import PerformanceRequirement, PerformanceAnalysis


class PerformanceAnalyzer:
    """Analyzes code to identify performance-critical functions."""

    def __init__(self):
        self.performance_indicators = {
            'loops': ['for', 'while', 'range', 'enumerate'],
            'recursion': ['def ', 'return'],
            'data_structures': ['list', 'dict', 'set', 'tuple'],
            'algorithms': ['sort', 'search', 'find', 'filter', 'map'],
            'io_operations': ['open', 'read', 'write', 'request', 'query'],
            'computation': ['math', 'calculate', 'compute', 'process']
        }

    def analyze_function_performance(self, func_ast: ast.FunctionDef) -> Optional[PerformanceRequirement]:
        """Analyze a function to determine if it needs performance testing."""
        function_name = func_ast.name
        
        # Check for performance-critical patterns
        performance_score = 0
        complexity_indicators = []
        
        # Analyze function body
        for node in ast.walk(func_ast):
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                performance_score += 2
                complexity_indicators.append("loop")
            
            elif isinstance(node, ast.ListComp) or isinstance(node, ast.DictComp):
                performance_score += 1
                complexity_indicators.append("comprehension")
            
            elif isinstance(node, ast.Call):
                if self._is_performance_critical_call(node):
                    performance_score += 1
                    complexity_indicators.append("critical_call")
        
        # Determine if function needs performance testing
        if performance_score >= 3:
            max_time = self._estimate_max_execution_time(performance_score)
            complexity = self._determine_complexity(complexity_indicators)
            
            return PerformanceRequirement(
                function_name=function_name,
                max_execution_time=max_time,
                complexity_threshold=complexity
            )
        
        return None

    def _is_performance_critical_call(self, call_node: ast.Call) -> bool:
        """Check if a function call is performance-critical."""
        if isinstance(call_node.func, ast.Name):
            func_name = call_node.func.id.lower()
            
            # Check for critical operations
            critical_patterns = [
                'sort', 'search', 'find', 'filter', 'map', 'reduce',
                'open', 'read', 'write', 'request', 'query', 'execute',
                'calculate', 'compute', 'process', 'transform'
            ]
            
            return any(pattern in func_name for pattern in critical_patterns)
        
        return False

    def _estimate_max_execution_time(self, performance_score: int) -> float:
        """Estimate maximum execution time based on performance score."""
        if performance_score <= 3:
            return 0.1  # 100ms
        elif performance_score <= 6:
            return 0.5  # 500ms
        elif performance_score <= 10:
            return 1.0  # 1 second
        else:
            return 2.0  # 2 seconds

    def _determine_complexity(self, indicators: List[str]) -> str:
        """Determine algorithmic complexity based on indicators."""
        if 'loop' in indicators and len(indicators) > 2:
            return 'O(n²)'
        elif 'loop' in indicators:
            return 'O(n)'
        elif 'comprehension' in indicators:
            return 'O(n)'
        else:
            return 'O(1)'

    def get_performance_analysis(self, func_ast: ast.FunctionDef) -> PerformanceAnalysis:
        """Get detailed performance analysis for a function."""
        function_name = func_ast.name
        performance_score = 0
        critical_operations = []
        
        # Analyze function complexity
        for node in ast.walk(func_ast):
            if isinstance(node, ast.For):
                performance_score += 2
                critical_operations.append(f"Nested loop at line {node.lineno}")
            elif isinstance(node, ast.While):
                performance_score += 2
                critical_operations.append(f"While loop at line {node.lineno}")
            elif isinstance(node, ast.ListComp):
                performance_score += 1
                critical_operations.append(f"List comprehension at line {node.lineno}")
        
        # Determine complexity level
        if performance_score >= 8:
            complexity_level = "high"
            estimated_complexity = "O(n²) or higher"
        elif performance_score >= 4:
            complexity_level = "medium"
            estimated_complexity = "O(n)"
        else:
            complexity_level = "low"
            estimated_complexity = "O(1) or O(log n)"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(performance_score, critical_operations)
        
        return PerformanceAnalysis(
            function_name=function_name,
            performance_score=performance_score,
            complexity_level=complexity_level,
            critical_operations=critical_operations,
            estimated_complexity=estimated_complexity,
            recommendations=recommendations
        )

    def _generate_recommendations(self, score: int, operations: List[str]) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        if score >= 8:
            recommendations.extend([
                "Consider algorithmic optimization",
                "Profile the function for bottlenecks",
                "Test with large datasets"
            ])
        elif score >= 4:
            recommendations.extend([
                "Monitor execution time",
                "Consider caching results",
                "Test with medium datasets"
            ])
        else:
            recommendations.append("Basic performance monitoring recommended")
        
        return recommendations
