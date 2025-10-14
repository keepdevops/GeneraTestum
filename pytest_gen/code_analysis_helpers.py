"""
Helper methods for code analysis.
"""

from typing import List, Set
from .code_models import FunctionInfo, ModuleInfo


class CodeAnalysisHelpers:
    """Helper methods for code analysis."""
    
    def __init__(self, config):
        self.config = config
    
    def should_test_function(self, func: FunctionInfo) -> bool:
        """Determine if a function should have tests generated."""
        # Skip private functions unless configured to include them
        if func.name.startswith('_') and not self.config.include_private_methods:
            return False
        
        # Skip magic methods
        if func.name.startswith('__') and func.name.endswith('__'):
            return False
        
        # Skip test functions
        if func.name.startswith('test_'):
            return False
        
        return True
    
    def should_test_method(self, method: FunctionInfo) -> bool:
        """Determine if a method should have tests generated."""
        # Skip private methods unless configured to include them
        if method.name.startswith('_') and not self.config.include_private_methods:
            return False
        
        # Skip magic methods
        if method.name.startswith('__') and method.name.endswith('__'):
            return False
        
        # Skip test methods
        if method.name.startswith('test_'):
            return False
        
        return True
    
    def get_test_candidates(self, module_info: ModuleInfo) -> List[FunctionInfo]:
        """Get functions that should have tests generated."""
        candidates = []
        
        # Add standalone functions
        for func in module_info.functions:
            if self.should_test_function(func):
                candidates.append(func)
        
        # Add class methods
        for class_info in module_info.classes:
            for method in class_info.methods:
                if self.should_test_method(method):
                    candidates.append(method)
        
        return candidates
