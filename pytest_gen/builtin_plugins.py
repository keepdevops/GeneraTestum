"""
Built-in language plugins for the test generator.
"""

from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .language_plugin import LanguagePlugin
from .code_analyzer import CodeAnalyzer
from .java_analyzer import JavaAnalyzer
from .panel_analyzer import PanelAnalyzer


class PythonLanguagePlugin(LanguagePlugin):
    """Plugin for Python language analysis."""
    
    def get_language_name(self) -> str:
        return "Python"
    
    def get_supported_extensions(self) -> List[str]:
        return ['.py']
    
    def get_framework_indicators(self) -> Dict[str, List[str]]:
        return {
            'flask': ['from flask import', 'import flask', '@app.route'],
            'fastapi': ['from fastapi import', 'import fastapi', '@app.get', '@app.post'],
            'django': ['from django', 'import django', 'class.*View'],
            'tornado': ['from tornado', 'import tornado', 'class.*Handler']
        }
    
    def can_analyze_file(self, file_path: str) -> bool:
        return file_path.endswith('.py')
    
    def analyze_file(self, file_path: str) -> Optional[Any]:
        analyzer = CodeAnalyzer(self.config)
        return analyzer.analyze_file(file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[Any]:
        analyzer = CodeAnalyzer(self.config)
        return analyzer.analyze_code(code, file_path)
    
    def generate_tests(self, analysis_result: Any) -> List[Any]:
        from .test_builder import TestBuilder
        test_builder = TestBuilder(self.config)
        return test_builder.generate_tests_for_module(analysis_result)
    
    def detect_framework(self, analysis_result: Any) -> Optional[str]:
        return None  # Python framework detection handled by API analyzer


class JavaLanguagePlugin(LanguagePlugin):
    """Plugin for Java language analysis."""
    
    def get_language_name(self) -> str:
        return "Java"
    
    def get_supported_extensions(self) -> List[str]:
        return ['.java']
    
    def get_framework_indicators(self) -> Dict[str, List[str]]:
        return {
            'spring': ['@Controller', '@Service', '@Repository', '@Component', '@Autowired'],
            'junit': ['@Test', '@BeforeEach', '@AfterEach', '@BeforeAll', '@AfterAll'],
            'mockito': ['@Mock', '@InjectMocks', '@Spy', '@Captor']
        }
    
    def get_test_framework_name(self) -> str:
        return "JUnit 5"
    
    def get_mock_framework_name(self) -> str:
        return "Mockito"
    
    def can_analyze_file(self, file_path: str) -> bool:
        return file_path.endswith('.java')
    
    def analyze_file(self, file_path: str) -> Optional[Any]:
        analyzer = JavaAnalyzer(self.config)
        return analyzer.analyze_file(file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[Any]:
        analyzer = JavaAnalyzer(self.config)
        return analyzer.analyze_code(code, file_path)
    
    def generate_tests(self, analysis_result: Any) -> List[Any]:
        from .java_test_builder import JavaTestBuilder
        test_builder = JavaTestBuilder(self.config)
        return test_builder.generate_tests_for_file(analysis_result)
    
    def detect_framework(self, analysis_result: Any) -> Optional[str]:
        analyzer = JavaAnalyzer(self.config)
        return analyzer.detect_framework(analysis_result)
    
    def get_required_dependencies(self) -> List[str]:
        return ['javalang']


class PanelLanguagePlugin(LanguagePlugin):
    """Plugin for Panel application analysis."""
    
    def get_language_name(self) -> str:
        return "Panel"
    
    def get_supported_extensions(self) -> List[str]:
        return ['.py']  # Panel apps are Python files
    
    def get_framework_indicators(self) -> Dict[str, List[str]]:
        return {
            'panel': ['import panel', 'import panel as pn', 'pn.widgets', 'pn.Row', 'pn.Column']
        }
    
    def can_analyze_file(self, file_path: str) -> bool:
        if not file_path.endswith('.py'):
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return any(indicator in content for indicator in self.get_framework_indicators()['panel'])
        except Exception:
            return False
    
    def analyze_file(self, file_path: str) -> Optional[Any]:
        analyzer = PanelAnalyzer(self.config)
        return analyzer.analyze_file(file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[Any]:
        analyzer = PanelAnalyzer(self.config)
        return analyzer.analyze_code(code, file_path)
    
    def generate_tests(self, analysis_result: Any) -> List[Any]:
        from .panel_test_generator import PanelTestGenerator
        test_generator = PanelTestGenerator(self.config)
        return test_generator.generate_tests_for_panel_app(analysis_result)
    
    def detect_framework(self, analysis_result: Any) -> Optional[str]:
        return "panel"
    
    def get_required_dependencies(self) -> List[str]:
        return ['panel']
