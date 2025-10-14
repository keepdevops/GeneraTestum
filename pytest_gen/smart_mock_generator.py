"""
Smart mock generator with intelligent dependency analysis and realistic data generation.
"""

from typing import Dict, List, Any
from .mock_models import DependencyInfo, MockConfig
from .dependency_analyzer import DependencyAnalyzer
from .mock_generators import APIMockGenerator, DatabaseMockGenerator, FileMockGenerator


class SmartMockGenerator:
    """Intelligent mock generator with dependency analysis."""

    def __init__(self):
        self.dependency_cache = {}
        self.common_patterns = {
            'user': {'id': 'int', 'name': 'str', 'email': 'str'},
            'post': {'id': 'int', 'title': 'str', 'content': 'str', 'user_id': 'int'},
            'product': {'id': 'int', 'name': 'str', 'price': 'float', 'category': 'str'},
            'order': {'id': 'int', 'user_id': 'int', 'total': 'float', 'status': 'str'}
        }
        
        # Initialize generators
        self.analyzer = DependencyAnalyzer()
        self.api_generator = APIMockGenerator()
        self.db_generator = DatabaseMockGenerator()
        self.file_generator = FileMockGenerator()

    def analyze_dependencies(self, code: str, file_path: str = None) -> List[DependencyInfo]:
        """Analyze code to identify external dependencies."""
        return self.analyzer.analyze_dependencies(code, file_path)

    def generate_smart_mocks(self, dependencies: List[DependencyInfo], config: MockConfig) -> Dict[str, str]:
        """Generate intelligent mocks for dependencies."""
        mocks = {}
        
        for dep in dependencies:
            if dep.type == 'api':
                mocks[dep.name] = self.api_generator.generate_mock(dep, config)
            elif dep.type == 'database':
                mocks[dep.name] = self.db_generator.generate_mock(dep, config)
            elif dep.type == 'file':
                mocks[dep.name] = self.file_generator.generate_mock(dep, config)
            elif dep.type == 'service':
                mocks[dep.name] = self._generate_service_mock(dep, config)
            else:
                mocks[dep.name] = self._generate_generic_mock(dep, config)
        
        return mocks

    def _generate_service_mock(self, dep: DependencyInfo, config: MockConfig) -> str:
        """Generate mock for service dependencies."""
        mock_code = []
        
        mock_code.append("from unittest.mock import Mock, MagicMock")
        mock_code.append("")
        
        mock_code.append(f"class {dep.name.title()}Mock:")
        mock_code.append(f'    """Mock for {dep.name} service."""')
        mock_code.append("")
        
        mock_code.extend([
            "    def __init__(self):",
            "        self.client = MagicMock()",
            "        self._setup_mock_responses()",
            "",
            "    def _setup_mock_responses(self):",
            "        # Setup common service responses",
            "        self.client.request.return_value = {",
            "            'status_code': 200,",
            "            'json': lambda: {'success': True, 'data': 'mock_data'}",
            "        }",
            "",
            "    def call_service(self, method, *args, **kwargs):",
            "        # Mock service call",
            "        return self.client.request(method, *args, **kwargs)",
            ""
        ])
        
        return "\n".join(mock_code)

    def _generate_generic_mock(self, dep: DependencyInfo, config: MockConfig) -> str:
        """Generate generic mock for unknown dependencies."""
        mock_code = []
        
        mock_code.append("from unittest.mock import Mock, MagicMock")
        mock_code.append("")
        
        mock_code.append(f"class {dep.name.title()}Mock:")
        mock_code.append(f'    """Generic mock for {dep.name}."""')
        mock_code.append("")
        
        mock_code.extend([
            "    def __init__(self):",
            "        self.mock = MagicMock()",
            "        self._setup_default_responses()",
            "",
            "    def _setup_default_responses(self):",
            "        # Setup default mock responses",
            "        self.mock.return_value = 'mock_response'",
            "",
            "    def __getattr__(self, name):",
            "        # Delegate all attribute access to mock",
            "        return getattr(self.mock, name)",
            ""
        ])
        
        return "\n".join(mock_code)
