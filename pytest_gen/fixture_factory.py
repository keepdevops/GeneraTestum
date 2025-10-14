"""
Factory for creating common pytest fixtures.
"""

from typing import Optional, List
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo
from .fixture_models import FixtureInfo


class FixtureFactory:
    """Factory for creating common pytest fixtures."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
    
    def create_database_fixture(self, scope: str = 'function') -> FixtureInfo:
        """Create database fixture."""
        return FixtureInfo(
            name='test_db',
            scope=scope,
            autouse=False,
            setup_code=[
                "import tempfile",
                "import sqlite3",
                "db_file = tempfile.NamedTemporaryFile(delete=False)",
                "connection = sqlite3.connect(db_file.name)",
                "yield connection"
            ],
            teardown_code=[
                "connection.close()",
                "import os",
                "os.unlink(db_file.name)"
            ],
            return_type='sqlite3.Connection'
        )
    
    def create_client_fixture(self, scope: str = 'function') -> FixtureInfo:
        """Create test client fixture."""
        return FixtureInfo(
            name='test_client',
            scope=scope,
            autouse=False,
            setup_code=[
                "from unittest.mock import MagicMock",
                "client = MagicMock()",
                "client.get.return_value.status_code = 200",
                "client.post.return_value.status_code = 201",
                "yield client"
            ],
            return_type='MagicMock'
        )
    
    def create_session_fixture(self, scope: str = 'function') -> FixtureInfo:
        """Create session fixture."""
        return FixtureInfo(
            name='test_session',
            scope=scope,
            autouse=False,
            setup_code=[
                "from unittest.mock import MagicMock",
                "session = MagicMock()",
                "yield session"
            ],
            teardown_code=[
                "session.close()"
            ],
            return_type='MagicMock'
        )
    
    def create_temp_file_fixture(self, scope: str = 'function') -> FixtureInfo:
        """Create temporary file fixture."""
        return FixtureInfo(
            name='temp_file',
            scope=scope,
            autouse=False,
            setup_code=[
                "import tempfile",
                "import os",
                "fd, path = tempfile.mkstemp()",
                "yield path"
            ],
            teardown_code=[
                "os.close(fd)",
                "os.unlink(path)"
            ],
            return_type='str'
        )
    
    def create_mock_data_fixture(self, scope: str = 'function') -> FixtureInfo:
        """Create mock data fixture."""
        return FixtureInfo(
            name='mock_data',
            scope=scope,
            autouse=False,
            setup_code=[
                "data = {",
                "    'user_id': 1,",
                "    'username': 'test_user',",
                "    'email': 'test@example.com'",
                "}",
                "yield data"
            ],
            return_type='dict'
        )
    
    def create_test_data_fixture(self, scope: str = 'function') -> FixtureInfo:
        """Create basic test data fixture."""
        return FixtureInfo(
            name='test_data',
            scope=scope,
            autouse=False,
            setup_code=[
                "data = {",
                "    'id': 1,",
                "    'name': 'test',",
                "    'value': 42",
                "}",
                "yield data"
            ],
            return_type='dict'
        )
