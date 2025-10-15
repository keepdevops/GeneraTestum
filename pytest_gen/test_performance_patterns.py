"""
Performance analysis patterns and detection rules.
"""

from typing import Dict, List


class TestPerformancePatterns:
    """Patterns and rules for test performance analysis."""
    
    def __init__(self):
        self.complexity_keywords = {
            'loops': ['for', 'while', 'for_each', 'iterate'],
            'conditionals': ['if', 'elif', 'else', 'switch', 'case'],
            'exceptions': ['try', 'except', 'catch', 'finally', 'raise'],
            'async': ['async', 'await', 'asyncio'],
            'nested': ['def ', 'class ', 'lambda'],
            'complex_assertions': ['assert_that', 'expect', 'should', 'must']
        }
        
        self.performance_patterns = {
            'slow_operations': [
                r'sleep\s*\(',
                r'time\.sleep\s*\(',
                r'requests\.get\s*\(',
                r'requests\.post\s*\(',
                r'database\.query\s*\(',
                r'db\.execute\s*\(',
                r'file\.read\s*\(',
                r'open\s*\(',
                r'subprocess\.call\s*\(',
                r'os\.system\s*\('
            ],
            'memory_intensive': [
                r'\.copy\s*\(',
                r'\.clone\s*\(',
                r'deepcopy\s*\(',
                r'pickle\.loads\s*\(',
                r'json\.loads\s*\(',
                r'pandas\.read_csv\s*\(',
                r'numpy\.array\s*\(',
                r'list\s*\(',
                r'dict\s*\(',
                r'set\s*\('
            ],
            'io_operations': [
                r'open\s*\(',
                r'file\s*\(',
                r'\.read\s*\(',
                r'\.write\s*\(',
                r'\.save\s*\(',
                r'\.load\s*\(',
                r'requests\.',
                r'urllib\.',
                r'socket\.',
                r'ftp\.'
            ]
        }
        
        self.mock_patterns = [
            r'@mock\.',
            r'@patch\s*\(',
            r'MagicMock\s*\(',
            r'Mock\s*\(',
            r'\.mock_',
            r'patch\s*\(',
            r'unittest\.mock\.',
            r'mockito\.',
            r'sinon\.'
        ]
        
        self.data_structure_patterns = [
            r'list\s*\(',
            r'dict\s*\(',
            r'set\s*\(',
            r'tuple\s*\(',
            r'array\s*\(',
            r'matrix\s*\('
        ]
        
        self.assertion_patterns = [
            'assert', 'expect', 'should', 'must'
        ]
    
    def get_complexity_keywords(self) -> Dict[str, List[str]]:
        """Get complexity detection keywords."""
        return self.complexity_keywords
    
    def get_performance_patterns(self) -> Dict[str, List[str]]:
        """Get performance pattern regexes."""
        return self.performance_patterns
    
    def get_mock_patterns(self) -> List[str]:
        """Get mock detection patterns."""
        return self.mock_patterns
    
    def get_data_structure_patterns(self) -> List[str]:
        """Get data structure patterns."""
        return self.data_structure_patterns
    
    def get_assertion_patterns(self) -> List[str]:
        """Get assertion patterns."""
        return self.assertion_patterns
