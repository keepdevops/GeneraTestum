"""
Main API analyzer that coordinates framework-specific analyzers.
"""

from typing import Optional
from .config import GeneratorConfig
from .api_models import APIModuleInfo
from .api_detector import APIFrameworkDetector
from .flask_analyzer import FlaskAnalyzer
from .fastapi_analyzer import FastAPIAnalyzer
from .django_analyzer import DjangoAnalyzer
from .tornado_analyzer import TornadoAnalyzer


class APIAnalyzer:
    """Main API analyzer that coordinates framework-specific analyzers."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.detector = APIFrameworkDetector()
        self.framework_patterns = {
            'flask': self._analyze_flask,
            'fastapi': self._analyze_fastapi,
            'django': self._analyze_django,
            'tornado': self._analyze_tornado,
            'panel': self._analyze_panel
        }
    
    def analyze_file(self, file_path: str) -> Optional[APIModuleInfo]:
        """Analyze an API file and extract endpoint information."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self._detect_framework_and_analyze(content, file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[APIModuleInfo]:
        """Analyze API code string."""
        return self._detect_framework_and_analyze(code, file_path)
    
    def _detect_framework_and_analyze(self, content: str, file_path: str) -> Optional[APIModuleInfo]:
        """Detect framework and analyze accordingly."""
        detected_framework = self.detector.detect_framework(content)
        
        if not detected_framework:
            return None
        
        analyzer_func = self.framework_patterns.get(detected_framework)
        if not analyzer_func:
            return None
        
        return analyzer_func(content, file_path)
    
    def _analyze_flask(self, content: str, file_path: str) -> APIModuleInfo:
        """Analyze Flask application."""
        import ast
        tree = ast.parse(content)
        analyzer = FlaskAnalyzer()
        analyzer.visit(tree)
        
        return APIModuleInfo(
            endpoints=analyzer.endpoints,
            framework='flask',
            imports=analyzer.imports,
            dependencies=analyzer.dependencies,
            file_path=file_path
        )
    
    def _analyze_fastapi(self, content: str, file_path: str) -> APIModuleInfo:
        """Analyze FastAPI application."""
        import ast
        tree = ast.parse(content)
        analyzer = FastAPIAnalyzer()
        analyzer.visit(tree)
        
        return APIModuleInfo(
            endpoints=analyzer.endpoints,
            framework='fastapi',
            imports=analyzer.imports,
            dependencies=analyzer.dependencies,
            file_path=file_path
        )
    
    def _analyze_django(self, content: str, file_path: str) -> APIModuleInfo:
        """Analyze Django views."""
        import ast
        tree = ast.parse(content)
        analyzer = DjangoAnalyzer()
        analyzer.visit(tree)
        
        return APIModuleInfo(
            endpoints=analyzer.endpoints,
            framework='django',
            imports=analyzer.imports,
            dependencies=analyzer.dependencies,
            file_path=file_path
        )
    
    def _analyze_tornado(self, content: str, file_path: str) -> APIModuleInfo:
        """Analyze Tornado handlers."""
        import ast
        tree = ast.parse(content)
        analyzer = TornadoAnalyzer()
        analyzer.visit(tree)
        
        return APIModuleInfo(
            endpoints=analyzer.endpoints,
            framework='tornado',
            imports=analyzer.imports,
            dependencies=analyzer.dependencies,
            file_path=file_path
        )
    
    def _analyze_panel(self, content: str, file_path: str) -> APIModuleInfo:
        """Analyze Panel application."""
        from .panel_analyzer import PanelAnalyzer
        
        panel_analyzer = PanelAnalyzer(self.config)
        panel_app = panel_analyzer.analyze_code(content, file_path)
        
        if not panel_app:
            return None
        
        # Convert Panel app to APIModuleInfo format
        endpoints = []
        for widget in panel_app.widgets:
            from .api_models import APIEndpoint
            endpoint = APIEndpoint(
                name=f"{widget.name}_widget",
                path=f"/widgets/{widget.name}",
                method="GET",
                handler=widget.name,
                parameters=[(param[0], param[1]) for param in widget.parameters],
                return_type="PanelWidget",
                decorators=[],
                framework="panel",
                dependencies=widget.dependencies,
                line_number=widget.line_number,
                docstring=widget.docstring
            )
            endpoints.append(endpoint)
        
        return APIModuleInfo(
            endpoints=endpoints,
            framework='panel',
            imports=panel_app.imports,
            dependencies=panel_app.dependencies,
            file_path=file_path
        )