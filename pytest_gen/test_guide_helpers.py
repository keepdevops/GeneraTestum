"""
Test guide helper functions.
"""


class TestGuideHelpers:
    """Helper functions for test guide generation."""

    @staticmethod
    def get_basic_test_examples() -> str:
        """Get basic test examples from templates."""
        from .test_guide_templates import get_basic_test_examples
        return get_basic_test_examples()

    @staticmethod
    def get_integration_test_examples() -> str:
        """Get integration test examples from templates."""
        from .test_guide_templates import get_integration_test_examples
        return get_integration_test_examples()

    @staticmethod
    def get_e2e_test_examples() -> str:
        """Get end-to-end test examples from templates."""
        from .test_guide_templates import get_e2e_test_examples
        return get_e2e_test_examples()

    @staticmethod
    def get_pytest_config() -> str:
        """Get pytest configuration from templates."""
        from .test_guide_templates import get_pytest_config
        return get_pytest_config()

    @staticmethod
    def get_conftest_example() -> str:
        """Get conftest.py example from templates."""
        from .test_guide_templates import get_conftest_example
        return get_conftest_example()

    @staticmethod
    def get_fixture_examples() -> str:
        """Get fixture examples from templates."""
        from .test_guide_templates import get_fixture_examples
        return get_fixture_examples()

    @staticmethod
    def get_mock_examples() -> str:
        """Get mock examples from templates."""
        from .test_guide_templates import get_mock_examples
        return get_mock_examples()

    @staticmethod
    def get_security_test_examples() -> str:
        """Get security test examples from templates."""
        from .test_guide_templates import get_security_test_examples
        return get_security_test_examples()

    @staticmethod
    def get_performance_test_examples() -> str:
        """Get performance test examples from templates."""
        from .test_guide_templates import get_performance_test_examples
        return get_performance_test_examples()
