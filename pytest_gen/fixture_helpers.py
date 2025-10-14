"""
Helper functions for fixture generation.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ClassInfo, ModuleInfo
from .fixture_models import FixtureInfo


class FixtureHelpers:
    """Helper functions for fixture generation."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
    
    def identify_fixture_type(self, dependency: str) -> Optional[str]:
        """Identify what type of fixture is needed for a dependency."""
        dependency_lower = dependency.lower()
        
        # Database fixtures
        if any(db in dependency_lower for db in ['database', 'db', 'sql', 'orm']):
            return 'database'
        
        # HTTP client fixtures
        if any(client in dependency_lower for client in ['client', 'requests', 'http', 'api']):
            return 'client'
        
        # Session fixtures
        if any(session in dependency_lower for session in ['session', 'auth', 'login']):
            return 'session'
        
        # File fixtures
        if any(file in dependency_lower for file in ['file', 'path', 'io', 'temp']):
            return 'temp_file'
        
        # Mock data fixtures
        if any(data in dependency_lower for data in ['data', 'mock', 'test_data', 'sample']):
            return 'mock_data'
        
        return None
    
    def generate_parameter_fixtures(self, func_info: FunctionInfo) -> List[FixtureInfo]:
        """Generate fixtures for complex function parameters."""
        fixtures = []
        
        for param_name, param_type in func_info.parameters:
            if self._is_complex_type(param_type):
                fixture = self._create_parameter_fixture(param_name, param_type)
                if fixture:
                    fixtures.append(fixture)
        
        return fixtures
    
    def deduplicate_fixtures(self, fixtures: List[FixtureInfo]) -> List[FixtureInfo]:
        """Remove duplicate fixtures based on name."""
        seen = set()
        unique_fixtures = []
        
        for fixture in fixtures:
            if fixture.name not in seen:
                seen.add(fixture.name)
                unique_fixtures.append(fixture)
        
        return unique_fixtures
    
    def _is_complex_type(self, param_type: str) -> bool:
        """Check if parameter type requires a fixture."""
        if not param_type:
            return False
        
        complex_types = [
            'dict', 'list', 'tuple', 'set',
            'DataFrame', 'Series', 'ndarray',
            'Database', 'Connection', 'Session',
            'Client', 'Request', 'Response'
        ]
        
        return any(complex_type in param_type for complex_type in complex_types)
    
    def _create_parameter_fixture(self, param_name: str, param_type: str) -> Optional[FixtureInfo]:
        """Create a fixture for a complex parameter."""
        fixture_name = f"{param_name}_data"
        
        if 'dict' in param_type:
            return FixtureInfo(
                name=fixture_name,
                scope='function',
                content=f'    return {{"key": "value", "id": 1}}',
                dependencies=set(),
                parameters=[],
                docstring=f'Fixture providing test data for {param_name}'
            )
        
        elif 'list' in param_type:
            return FixtureInfo(
                name=fixture_name,
                scope='function',
                content=f'    return ["item1", "item2", "item3"]',
                dependencies=set(),
                parameters=[],
                docstring=f'Fixture providing test data for {param_name}'
            )
        
        elif 'DataFrame' in param_type:
            return FixtureInfo(
                name=fixture_name,
                scope='function',
                content='    import pandas as pd\n    return pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})',
                dependencies={'pandas'},
                parameters=[],
                docstring=f'Fixture providing test data for {param_name}'
            )
        
        return None
    
    def generate_module_fixtures(self, module_info: ModuleInfo) -> List[FixtureInfo]:
        """Generate common fixtures for a module."""
        fixtures = []
        
        # Module-level fixtures
        if any('database' in dep.lower() for dep in module_info.dependencies):
            fixtures.append(self._create_database_fixture())
        
        if any('client' in dep.lower() for dep in module_info.dependencies):
            fixtures.append(self._create_client_fixture())
        
        if any('session' in dep.lower() for dep in module_info.dependencies):
            fixtures.append(self._create_session_fixture())
        
        return fixtures
    
    def _create_database_fixture(self) -> FixtureInfo:
        """Create a database fixture."""
        return FixtureInfo(
            name='database',
            scope='function',
            content='    # Setup test database\n    from unittest.mock import MagicMock\n    db = MagicMock()\n    return db',
            dependencies={'unittest.mock'},
            parameters=[],
            docstring='Fixture providing test database connection'
        )
    
    def _create_client_fixture(self) -> FixtureInfo:
        """Create a client fixture."""
        return FixtureInfo(
            name='client',
            scope='function',
            content='    # Setup test client\n    from unittest.mock import MagicMock\n    client = MagicMock()\n    return client',
            dependencies={'unittest.mock'},
            parameters=[],
            docstring='Fixture providing test HTTP client'
        )
    
    def _create_session_fixture(self) -> FixtureInfo:
        """Create a session fixture."""
        return FixtureInfo(
            name='session',
            scope='function',
            content='    # Setup test session\n    from unittest.mock import MagicMock\n    session = MagicMock()\n    return session',
            dependencies={'unittest.mock'},
            parameters=[],
            docstring='Fixture providing test session'
        )
