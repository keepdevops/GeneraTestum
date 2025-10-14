"""
Automatic code refactoring suggestions based on test failures.
"""

import re
from typing import Dict, List, Any, Optional
from .test_runner_models import TestSuiteResult, TestResult


class AutoRefactoringAnalyzer:
    """Analyzes test failures and suggests code refactoring improvements."""

    def __init__(self):
        self.common_patterns = {
            'import_error': r"ImportError: (.*)",
            'attribute_error': r"AttributeError: (.*)",
            'type_error': r"TypeError: (.*)",
            'value_error': r"ValueError: (.*)",
            'assertion_error': r"AssertionError: (.*)",
            'name_error': r"NameError: (.*)",
            'module_not_found': r"ModuleNotFoundError: (.*)"
        }

    def analyze_failures(self, suite_result: TestSuiteResult) -> List[Dict[str, Any]]:
        """Analyze test failures and generate refactoring suggestions."""
        suggestions = []
        
        for test_result in suite_result.test_results:
            if test_result.status in ['failed', 'error'] and test_result.error_message:
                suggestion = self._analyze_single_failure(test_result)
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions

    def _analyze_single_failure(self, test_result: TestResult) -> Optional[Dict[str, Any]]:
        """Analyze a single test failure and suggest fixes."""
        error_message = test_result.error_message or ""
        
        # Check for import errors
        if self._is_import_error(error_message):
            return self._suggest_import_fix(test_result, error_message)
        
        # Check for attribute errors
        if self._is_attribute_error(error_message):
            return self._suggest_attribute_fix(test_result, error_message)
        
        # Check for type errors
        if self._is_type_error(error_message):
            return self._suggest_type_fix(test_result, error_message)
        
        # Check for assertion errors
        if self._is_assertion_error(error_message):
            return self._suggest_assertion_fix(test_result, error_message)
        
        return None

    def _is_import_error(self, error_message: str) -> bool:
        """Check if error is an import-related error."""
        return any(pattern in error_message for pattern in ['ImportError', 'ModuleNotFoundError'])

    def _is_attribute_error(self, error_message: str) -> bool:
        """Check if error is an attribute-related error."""
        return 'AttributeError' in error_message

    def _is_type_error(self, error_message: str) -> bool:
        """Check if error is a type-related error."""
        return 'TypeError' in error_message

    def _is_assertion_error(self, error_message: str) -> bool:
        """Check if error is an assertion-related error."""
        return 'AssertionError' in error_message

    def _suggest_import_fix(self, test_result: TestResult, error_message: str) -> Dict[str, Any]:
        """Suggest fixes for import errors."""
        # Extract module name from error
        module_match = re.search(r"'(.*?)'", error_message)
        module_name = module_match.group(1) if module_match else "unknown"
        
        return {
            'type': 'import_error',
            'test_name': test_result.test_name,
            'error_message': error_message,
            'suggestions': [
                f"Add import statement: `import {module_name}`",
                f"Check if {module_name} is installed: `pip install {module_name}`",
                f"Verify import path and module structure",
                f"Consider using relative imports if appropriate"
            ],
            'priority': 'high',
            'auto_fixable': True
        }

    def _suggest_attribute_fix(self, test_result: TestResult, error_message: str) -> Dict[str, Any]:
        """Suggest fixes for attribute errors."""
        # Extract attribute name from error
        attr_match = re.search(r"'(.*?)' object has no attribute '(.*?)'", error_message)
        if attr_match:
            object_name = attr_match.group(1)
            attribute_name = attr_match.group(2)
            
            return {
                'type': 'attribute_error',
                'test_name': test_result.test_name,
                'error_message': error_message,
                'suggestions': [
                    f"Add missing attribute '{attribute_name}' to {object_name} class",
                    f"Check if attribute name is correct: '{attribute_name}'",
                    f"Verify object initialization and method calls",
                    f"Consider adding property or method to {object_name}"
                ],
                'priority': 'high',
                'auto_fixable': False
            }
        
        return None

    def _suggest_type_fix(self, test_result: TestResult, error_message: str) -> Dict[str, Any]:
        """Suggest fixes for type errors."""
        return {
            'type': 'type_error',
            'test_name': test_result.test_name,
            'error_message': error_message,
            'suggestions': [
                "Check parameter types and expected return types",
                "Add type hints to function signatures",
                "Verify argument types in function calls",
                "Consider type conversion if appropriate"
            ],
            'priority': 'medium',
            'auto_fixable': False
        }

    def _suggest_assertion_fix(self, test_result: TestResult, error_message: str) -> Dict[str, Any]:
        """Suggest fixes for assertion errors."""
        return {
            'type': 'assertion_error',
            'test_name': test_result.test_name,
            'error_message': error_message,
            'suggestions': [
                "Review test expectations and actual values",
                "Check test data setup and mock configurations",
                "Verify assertion logic and conditions",
                "Consider adding more descriptive assertions"
            ],
            'priority': 'medium',
            'auto_fixable': False
        }

    def generate_refactoring_report(self, suggestions: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive refactoring report."""
        if not suggestions:
            return "✅ No refactoring suggestions found - all tests are passing!"
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔧 AUTOMATIC REFACTORING SUGGESTIONS")
        report_lines.append("=" * 60)
        
        # Group by priority
        high_priority = [s for s in suggestions if s.get('priority') == 'high']
        medium_priority = [s for s in suggestions if s.get('priority') == 'medium']
        low_priority = [s for s in suggestions if s.get('priority') == 'low']
        
        # High priority issues
        if high_priority:
            report_lines.append(f"\n🚨 HIGH PRIORITY ({len(high_priority)} issues):")
            for suggestion in high_priority:
                report_lines.append(f"\n  ❌ {suggestion['test_name']}")
                report_lines.append(f"     Type: {suggestion['type']}")
                report_lines.append(f"     Error: {suggestion['error_message'][:80]}...")
                report_lines.append("     Suggestions:")
                for sug in suggestion['suggestions']:
                    report_lines.append(f"       • {sug}")
        
        # Medium priority issues
        if medium_priority:
            report_lines.append(f"\n⚠️  MEDIUM PRIORITY ({len(medium_priority)} issues):")
            for suggestion in medium_priority:
                report_lines.append(f"\n  ⚠️  {suggestion['test_name']}")
                report_lines.append(f"     Type: {suggestion['type']}")
                report_lines.append("     Suggestions:")
                for sug in suggestion['suggestions']:
                    report_lines.append(f"       • {sug}")
        
        # Summary
        report_lines.append(f"\n📊 SUMMARY:")
        report_lines.append(f"  Total Issues: {len(suggestions)}")
        report_lines.append(f"  High Priority: {len(high_priority)}")
        report_lines.append(f"  Medium Priority: {len(medium_priority)}")
        report_lines.append(f"  Low Priority: {len(low_priority)}")
        
        auto_fixable = [s for s in suggestions if s.get('auto_fixable', False)]
        if auto_fixable:
            report_lines.append(f"  Auto-fixable: {len(auto_fixable)}")
        
        return "\n".join(report_lines)
