"""
Plugin manager for discovering and loading language analyzers.
"""

import os
import importlib
from typing import Dict, List, Set, Optional, Any, Type
from .config import GeneratorConfig
from .language_plugin import LanguagePlugin, PluginRegistry
from .builtin_plugins import PythonLanguagePlugin, JavaLanguagePlugin, PanelLanguagePlugin


class PluginManager:
    """Manages plugin discovery, loading, and routing."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.registry = PluginRegistry()
        self._register_builtin_plugins()
        self._discover_external_plugins()
    
    def _register_builtin_plugins(self):
        """Register built-in language plugins."""
        # Python plugin
        python_plugin = PythonLanguagePlugin(self.config)
        self.registry.register_plugin(python_plugin)
        
        # Java plugin
        if self._check_java_dependencies():
            java_plugin = JavaLanguagePlugin(self.config)
            self.registry.register_plugin(java_plugin)
        
        # Panel plugin
        if self._check_panel_dependencies():
            panel_plugin = PanelLanguagePlugin(self.config)
            self.registry.register_plugin(panel_plugin)
    
    def _discover_external_plugins(self):
        """Discover and load external plugins."""
        plugin_dirs = [
            os.path.join(os.getcwd(), 'pytest_plugins'),
            os.path.expanduser('~/.pytest_gen/plugins'),
            '/usr/local/lib/pytest_gen/plugins'
        ]
        
        for plugin_dir in plugin_dirs:
            if os.path.exists(plugin_dir):
                self._load_plugins_from_directory(plugin_dir)
    
    def _load_plugins_from_directory(self, plugin_dir: str):
        """Load plugins from a directory."""
        try:
            for filename in os.listdir(plugin_dir):
                if filename.endswith('.py') and not filename.startswith('_'):
                    module_name = filename[:-3]
                    module_path = os.path.join(plugin_dir, filename)
                    self._load_plugin_module(module_path, module_name)
        except Exception:
            pass  # Ignore errors in external plugin loading
    
    def _load_plugin_module(self, module_path: str, module_name: str):
        """Load a single plugin module."""
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for plugin classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, LanguagePlugin) and 
                        attr != LanguagePlugin):
                        plugin_instance = attr(self.config)
                        self.registry.register_plugin(plugin_instance)
        except Exception:
            pass  # Ignore errors in individual plugin loading
    
    def _check_java_dependencies(self) -> bool:
        """Check if Java dependencies are available."""
        try:
            import javalang
            return True
        except ImportError:
            return False
    
    def _check_panel_dependencies(self) -> bool:
        """Check if Panel dependencies are available."""
        try:
            import panel
            return True
        except ImportError:
            return False
    
    def analyze_file(self, file_path: str) -> Optional[Any]:
        """Analyze a file using the appropriate plugin."""
        plugin = self.registry.get_plugin_for_file(file_path)
        if plugin:
            return plugin.analyze_file(file_path)
        return None
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[Any]:
        """Analyze code using the appropriate plugin."""
        plugin = self.registry.get_plugin_for_file(file_path)
        if plugin:
            return plugin.analyze_code(code, file_path)
        return None
    
    def generate_tests(self, analysis_result: Any, file_path: str) -> List[Any]:
        """Generate tests using the appropriate plugin."""
        plugin = self.registry.get_plugin_for_file(file_path)
        if plugin:
            return plugin.generate_tests(analysis_result)
        return []
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return self.registry.get_supported_languages()
    
    def get_plugin_for_file(self, file_path: str) -> Optional[LanguagePlugin]:
        """Get the appropriate plugin for a file."""
        return self.registry.get_plugin_for_file(file_path)
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        return self.registry.get_supported_extensions()
