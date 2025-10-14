"""
Pytest fixture generation for test setup and teardown.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ClassInfo, ModuleInfo
from .fixture_factory import FixtureFactory
from .fixture_models import FixtureInfo
from .fixture_helpers import FixtureHelpers


class FixtureGenerator:
    """Generates pytest fixtures for test setup."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.helpers = FixtureHelpers(config)
        self.factory = FixtureFactory(config)
        self._common_fixtures = {
            'database': self._generate_database_fixture,
            'client': self._generate_client_fixture,
            'session': self._generate_session_fixture,
            'temp_file': self._generate_temp_file_fixture,
            'mock_data': self._generate_mock_data_fixture,
        }
    
    def generate_fixtures_for_function(self, func_info: FunctionInfo) -> List[FixtureInfo]:
        """Generate fixtures needed for a specific function."""
        if not self.config.generate_fixtures:
            return []
        
        fixtures = []
        
        # Generate fixtures based on function dependencies
        for dep in func_info.dependencies:
            fixture_type = self.helpers.identify_fixture_type(dep)
            if fixture_type and fixture_type in self._common_fixtures:
                fixture = self._common_fixtures[fixture_type](func_info)
                if fixture:
                    fixtures.append(fixture)
        
        # Generate fixtures for complex parameters
        fixtures.extend(self.helpers.generate_parameter_fixtures(func_info))
        
        return self.helpers.deduplicate_fixtures(fixtures)
    
    def generate_fixtures_for_module(self, module_info: ModuleInfo) -> List[FixtureInfo]:
        """Generate fixtures for an entire module."""
        if not self.config.generate_fixtures:
            return []
        
        fixtures = []
        
        # Generate module-level fixtures using helpers
        fixtures.extend(self.helpers.generate_module_fixtures(module_info))
        
        return self.helpers.deduplicate_fixtures(fixtures)
    
    def generate_fixtures_for_class(self, class_info: ClassInfo) -> List[FixtureInfo]:
        """Generate fixtures needed for a specific class."""
        if not self.config.generate_fixtures:
            return []
        
        fixtures = []
        
        # Generate fixtures based on class dependencies
        for dep in class_info.dependencies:
            fixture_type = self.helpers.identify_fixture_type(dep)
            if fixture_type and fixture_type in self._common_fixtures:
                fixture = self._common_fixtures[fixture_type](class_info)
                if fixture:
                    fixtures.append(fixture)
        
        # Generate fixtures for class methods
        for method in class_info.methods:
            fixtures.extend(self.generate_fixtures_for_function(method))
        
        return self.helpers.deduplicate_fixtures(fixtures)
    
    def _generate_database_fixture(self, context: Any) -> FixtureInfo:
        """Generate a database fixture."""
        return FixtureInfo(
            name='database',
            scope='function',
            content='    # Setup test database\n    from unittest.mock import MagicMock\n    db = MagicMock()\n    return db',
            dependencies={'unittest.mock'},
            parameters=[],
            docstring='Fixture providing test database connection'
        )
    
    def _generate_client_fixture(self, context: Any) -> FixtureInfo:
        """Generate an HTTP client fixture."""
        return FixtureInfo(
            name='client',
            scope='function',
            content='    # Setup test client\n    from unittest.mock import MagicMock\n    client = MagicMock()\n    return client',
            dependencies={'unittest.mock'},
            parameters=[],
            docstring='Fixture providing test HTTP client'
        )
    
    def _generate_session_fixture(self, context: Any) -> FixtureInfo:
        """Generate a session fixture."""
        return FixtureInfo(
            name='session',
            scope='function',
            content='    # Setup test session\n    from unittest.mock import MagicMock\n    session = MagicMock()\n    return session',
            dependencies={'unittest.mock'},
            parameters=[],
            docstring='Fixture providing test session'
        )
    
    def _generate_temp_file_fixture(self, context: Any) -> FixtureInfo:
        """Generate a temporary file fixture."""
        return FixtureInfo(
            name='temp_file',
            scope='function',
            content='    # Setup temporary file\n    import tempfile\n    import os\n    with tempfile.NamedTemporaryFile(delete=False) as f:\n        temp_path = f.name\n    yield temp_path\n    os.unlink(temp_path)',
            dependencies={'tempfile', 'os'},
            parameters=[],
            docstring='Fixture providing temporary file path'
        )
    
    def _generate_mock_data_fixture(self, context: Any) -> FixtureInfo:
        """Generate a mock data fixture."""
        return FixtureInfo(
            name='mock_data',
            scope='function',
            content='    # Setup mock data\n    return {\n        "id": 1,\n        "name": "test",\n        "value": 42\n    }',
            dependencies=set(),
            parameters=[],
            docstring='Fixture providing mock test data'
        )