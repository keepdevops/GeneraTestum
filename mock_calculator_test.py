# Generated Smart Mocks

# Mock for math
from unittest.mock import Mock, MagicMock

class MathMock:
    """Generic mock for math."""

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

