# Generated Smart Mocks

# Mock for flask
from unittest.mock import Mock, MagicMock

class FlaskMock:
    """Generic mock for flask."""

    def __init__(self):
        self.mock = MagicMock()
        self._setup_default_responses()

    def _setup_default_responses(self):
        # Setup default mock responses
        self.mock.return_value = 'mock_response'

    def __getattr__(self, name):
        # Delegate all attribute access to mock
        return getattr(self.mock, name)


==================================================

# Mock for typing
from unittest.mock import Mock, MagicMock

class TypingMock:
    """Generic mock for typing."""

    def __init__(self):
        self.mock = MagicMock()
        self._setup_default_responses()

    def _setup_default_responses(self):
        # Setup default mock responses
        self.mock.return_value = 'mock_response'

    def __getattr__(self, name):
        # Delegate all attribute access to mock
        return getattr(self.mock, name)


==================================================

# Mock for json
from unittest.mock import Mock, MagicMock

class JsonMock:
    """Generic mock for json."""

    def __init__(self):
        self.mock = MagicMock()
        self._setup_default_responses()

    def _setup_default_responses(self):
        # Setup default mock responses
        self.mock.return_value = 'mock_response'

    def __getattr__(self, name):
        # Delegate all attribute access to mock
        return getattr(self.mock, name)


==================================================

# Mock for uuid
from unittest.mock import Mock, MagicMock

class UuidMock:
    """Generic mock for uuid."""

    def __init__(self):
        self.mock = MagicMock()
        self._setup_default_responses()

    def _setup_default_responses(self):
        # Setup default mock responses
        self.mock.return_value = 'mock_response'

    def __getattr__(self, name):
        # Delegate all attribute access to mock
        return getattr(self.mock, name)


==================================================

# Mock for datetime
from unittest.mock import Mock, MagicMock

class DatetimeMock:
    """Generic mock for datetime."""

    def __init__(self):
        self.mock = MagicMock()
        self._setup_default_responses()

    def _setup_default_responses(self):
        # Setup default mock responses
        self.mock.return_value = 'mock_response'

    def __getattr__(self, name):
        # Delegate all attribute access to mock
        return getattr(self.mock, name)


==================================================

