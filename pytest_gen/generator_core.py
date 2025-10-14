"""
Main test generation orchestrator that coordinates all components.
"""

import os
from typing import List, Dict, Any, Optional
from .config import GeneratorConfig, DEFAULT_CONFIG, CodeType
from .generator_operations import GeneratorOperations


class GeneratorCore:
    """Main orchestrator for test generation."""
    
    def __init__(self, config: GeneratorConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.operations = GeneratorOperations(self.config)
    
    def generate_tests(self, source_path: str, output_dir: str = None) -> List[str]:
        """Generate tests for a source file or directory."""
        if output_dir:
            self.config.output_dir = output_dir
        
        return self.operations.generate_tests(source_path)
    
    def generate_tests_from_code(self, code: str, file_path: str = "<string>", output_dir: str = None) -> List[str]:
        """Generate tests from code string."""
        if output_dir:
            self.config.output_dir = output_dir
        
        return self.operations.generate_tests_from_code_string(code, file_path)
    
    def get_ai_recommendations(self, source_path: str) -> Dict[str, Any]:
        """Get AI recommendations for test generation."""
        return self.operations.get_ai_recommendations(source_path)
    
    def get_ai_test_suggestions(self, test_files: List[str]) -> Dict[str, Any]:
        """Get AI suggestions for improving existing tests."""
        return self.operations.get_ai_test_suggestions(test_files)
    
    def ask_ai_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ask the AI assistant a question with optional context."""
        return self.operations.ask_ai_question(question, context)
    
    def update_config(self, **kwargs) -> None:
        """Update generator configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def get_config(self) -> GeneratorConfig:
        """Get current configuration."""
        return self.config
    
    def analyze_source(self, source_path: str) -> dict:
        """Analyze source code and return information about what tests would be generated."""
        return self.operations.analyze_source(source_path)


# Convenience function for library usage
def generate_tests(source_path: str, config: GeneratorConfig = None, **kwargs) -> List[str]:
    """Generate tests for source code.
    
    Args:
        source_path: Path to source file or directory
        config: Generator configuration (optional)
        **kwargs: Additional configuration parameters
        
    Returns:
        List of generated test file paths
    """
    generator = GeneratorCore(config)
    
    # Update config with kwargs
    if kwargs:
        generator.update_config(**kwargs)
    
    return generator.generate_tests(source_path)