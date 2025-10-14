"""
Generator operations and utilities.
"""

import os
from typing import List, Dict, Any, Optional
from .generator_core_ops import GeneratorCoreOperations
from .generator_ai_ops import GeneratorAIOperations


class GeneratorOperations:
    """Operations for test generation."""
    
    def __init__(self, config):
        self.config = config
        self.core_ops = GeneratorCoreOperations(config)
        self.ai_ops = GeneratorAIOperations(config)
    
    def generate_tests(self, source_path: str, output_dir: str = None) -> List[str]:
        """Generate tests for source file or directory."""
        if output_dir:
            self.config.output_dir = output_dir
        
        if os.path.isfile(source_path):
            return self.core_ops.generate_tests_for_file(source_path)
        elif os.path.isdir(source_path):
            return self.core_ops.generate_tests_for_directory(source_path)
        else:
            return []
    
    def generate_tests_from_code(self, code: str, file_path: str = "<string>", output_dir: str = None) -> List[str]:
        """Generate tests from code string."""
        if output_dir:
            self.config.output_dir = output_dir
        
        return self.core_ops.generate_tests_from_code_string(code, file_path)
    
    def analyze_source(self, source_path: str) -> dict:
        """Analyze source code and return information about what tests would be generated."""
        if os.path.isfile(source_path):
            code_type = self.core_ops.source_analyzer.detect_file_type(source_path)
            
            if code_type == "python":
                module_info = self.core_ops.code_analyzer.analyze_file(source_path)
                return {
                    'file_path': source_path,
                    'file_type': 'python',
                    'functions': [{'name': f.name, 'parameters': len(f.parameters)} for f in module_info.functions],
                    'classes': [{'name': c.name, 'methods': len(c.methods)} for c in module_info.classes],
                    'endpoints': [],
                    'dependencies': list(module_info.dependencies),
                    'estimated_tests': len(module_info.functions) + sum(len(c.methods) for c in module_info.classes)
                }
            elif code_type == "api":
                api_info = self.core_ops.api_analyzer.analyze_file(source_path)
                return {
                    'file_path': source_path,
                    'file_type': 'api',
                    'functions': [{'name': f.name, 'parameters': len(f.parameters)} for f in api_info.functions],
                    'classes': [{'name': c.name, 'methods': len(c.methods)} for c in api_info.classes],
                    'endpoints': [{'path': e.path, 'method': e.method} for e in api_info.endpoints],
                    'dependencies': list(api_info.dependencies),
                    'estimated_tests': len(api_info.endpoints)
                }
        
        return {'file_path': source_path, 'file_type': 'unknown', 'functions': [], 'classes': [], 'endpoints': [], 'dependencies': [], 'estimated_tests': 0}
    
    def update_config(self, **kwargs) -> None:
        """Update generator configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def get_ai_recommendations(self, source_path: str) -> Dict[str, Any]:
        """Get AI recommendations for test generation."""
        return self.ai_ops.get_ai_recommendations(source_path)
    
    def get_ai_test_suggestions(self, test_files: List[str]) -> Dict[str, Any]:
        """Get AI suggestions for improving existing tests."""
        return self.ai_ops.get_ai_test_suggestions(test_files)
    
    def ask_ai_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ask the AI assistant a question with optional context."""
        return self.ai_ops.ask_ai_question(question, context)