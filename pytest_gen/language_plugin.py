"""
Base plugin interface for language analyzers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .test_models import GeneratedTest


class LanguagePlugin(ABC):
    """Base interface for language analyzer plugins."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.supported_extensions = self.get_supported_extensions()
        self.framework_indicators = self.get_framework_indicators()
    
    @abstractmethod
    def get_language_name(self) -> str:
        """Get the name of the language this plugin supports."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Get list of file extensions this plugin supports."""
        pass
    
    @abstractmethod
    def get_framework_indicators(self) -> Dict[str, List[str]]:
        """Get framework detection indicators for this language."""
        pass
    
    @abstractmethod
    def can_analyze_file(self, file_path: str) -> bool:
        """Check if this plugin can analyze the given file."""
        pass
    
    @abstractmethod
    def analyze_file(self, file_path: str) -> Optional[Any]:
        """Analyze a file and return language-specific information."""
        pass
    
    @abstractmethod
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[Any]:
        """Analyze code string and return language-specific information."""
        pass
    
    @abstractmethod
    def generate_tests(self, analysis_result: Any) -> List[str]:
        """Generate tests from analysis result and return file paths."""
        pass
    
    @abstractmethod
    def detect_framework(self, analysis_result: Any) -> Optional[str]:
        """Detect framework used in the analyzed code."""
        pass
    
    def get_test_framework_name(self) -> str:
        """Get the name of the test framework used for this language."""
        return "pytest"  # Default to pytest
    
    def get_mock_framework_name(self) -> str:
        """Get the name of the mocking framework used for this language."""
        return "unittest.mock"  # Default to unittest.mock
    
    def get_import_statements(self, test_imports: Set[str]) -> List[str]:
        """Get formatted import statements for the language."""
        imports = []
        for import_stmt in test_imports:
            if self.get_language_name().lower() == 'java':
                imports.append(f"import {import_stmt};")
            else:
                imports.append(f"import {import_stmt}")
        return imports
    
    def get_test_file_extension(self) -> str:
        """Get the file extension for test files in this language."""
        if self.get_language_name().lower() == 'java':
            return '.java'
        else:
            return '.py'
    
    def get_test_file_prefix(self) -> str:
        """Get the prefix for test files (e.g., 'test_' for Python)."""
        if self.get_language_name().lower() == 'java':
            return 'Test'  # Java convention: TestClassName.java
        else:
            return 'test_'  # Python convention: test_module.py
    
    def validate_config(self) -> bool:
        """Validate that the plugin configuration is correct."""
        return True  # Default implementation
    
    def get_required_dependencies(self) -> List[str]:
        """Get list of required dependencies for this plugin."""
        return []  # Default: no additional dependencies
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are available."""
        dependencies = self.get_required_dependencies()
        if not dependencies:
            return True
        
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                return False
        return True


class PluginRegistry:
    """Registry for managing language plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, LanguagePlugin] = {}
        self.extensions_map: Dict[str, str] = {}
    
    def register_plugin(self, plugin: LanguagePlugin):
        """Register a language plugin."""
        language_name = plugin.get_language_name().lower()
        self.plugins[language_name] = plugin
        
        # Map file extensions to language
        for ext in plugin.get_supported_extensions():
            self.extensions_map[ext.lower()] = language_name
    
    def get_plugin_for_file(self, file_path: str) -> Optional[LanguagePlugin]:
        """Get the appropriate plugin for a file."""
        import os
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        language_name = self.extensions_map.get(ext)
        if language_name:
            return self.plugins.get(language_name)
        
        return None
    
    def get_plugin_for_language(self, language_name: str) -> Optional[LanguagePlugin]:
        """Get plugin for a specific language."""
        return self.plugins.get(language_name.lower())
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self.plugins.keys())
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of all supported file extensions."""
        return list(self.extensions_map.keys())
    
    def validate_all_plugins(self) -> Dict[str, bool]:
        """Validate all registered plugins."""
        results = {}
        for language_name, plugin in self.plugins.items():
            results[language_name] = plugin.validate_config() and plugin.check_dependencies()
        return results
