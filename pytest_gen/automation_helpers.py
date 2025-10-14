"""
Helper functions for automation commands.
"""

from .automation_test_helpers import run_automated_tests, analyze_coverage_gaps, run_complete_analysis
from .automation_mock_helpers import generate_smart_mocks

# Re-export all functions for backward compatibility
__all__ = ['run_automated_tests', 'analyze_coverage_gaps', 'generate_smart_mocks', 'run_complete_analysis']
