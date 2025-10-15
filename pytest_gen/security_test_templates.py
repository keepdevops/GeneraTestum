"""
Security test templates - refactored for 200LOC limit.
"""

from .injection_security_templates import InjectionSecurityTemplates
from .web_security_templates import WebSecurityTemplates
from .cryptographic_security_templates import CryptographicSecurityTemplates, ValidationSecurityTemplates


class SecurityTestTemplates:
    """Templates for generating security tests."""
    
    def __init__(self):
        self.injection_templates = InjectionSecurityTemplates()
        self.web_templates = WebSecurityTemplates()
        self.crypto_templates = CryptographicSecurityTemplates()
        self.validation_templates = ValidationSecurityTemplates()
    
    def get_sql_injection_test(self, vulnerability) -> str:
        """Get SQL injection test template."""
        return self.injection_templates.get_sql_injection_test(vulnerability)
    
    def get_xss_test(self, vulnerability) -> str:
        """Get XSS test template."""
        return self.web_templates.get_xss_test(vulnerability)
    
    def get_path_traversal_test(self, vulnerability) -> str:
        """Get path traversal test template."""
        return self.web_templates.get_path_traversal_test(vulnerability)
    
    def get_command_injection_test(self, vulnerability) -> str:
        """Get command injection test template."""
        return self.injection_templates.get_command_injection_test(vulnerability)
    
    def get_code_injection_test(self, vulnerability) -> str:
        """Get code injection test template."""
        return self.injection_templates.get_code_injection_test(vulnerability)
    
    def get_generic_test(self, vulnerability) -> str:
        """Get generic test template."""
        return self.validation_templates.get_generic_test(vulnerability)
    
    def get_weak_cryptography_test(self, vulnerability) -> str:
        """Get weak cryptography test template."""
        return self.crypto_templates.get_weak_cryptography_test(vulnerability)
    
    def get_hardcoded_secrets_test(self, vulnerability) -> str:
        """Get hardcoded secrets test template."""
        return self.crypto_templates.get_hardcoded_secrets_test(vulnerability)
    
    def get_unsafe_deserialization_test(self, vulnerability) -> str:
        """Get unsafe deserialization test template."""
        return self.crypto_templates.get_unsafe_deserialization_test(vulnerability)
    
    def get_missing_validation_test(self, vulnerability) -> str:
        """Get missing validation test template."""
        return self.validation_templates.get_missing_validation_test(vulnerability)
    
    def get_insecure_random_test(self, vulnerability) -> str:
        """Get insecure random test template."""
        return self.crypto_templates.get_insecure_random_test(vulnerability)
    
    def get_test_by_vulnerability_type(self, vulnerability) -> str:
        """Get appropriate test template based on vulnerability type."""
        vulnerability_type = vulnerability.vulnerability_type.lower()
        
        template_mapping = {
            'sql_injection': self.get_sql_injection_test,
            'xss': self.get_xss_test,
            'path_traversal': self.get_path_traversal_test,
            'command_injection': self.get_command_injection_test,
            'code_injection': self.get_code_injection_test,
            'weak_cryptography': self.get_weak_cryptography_test,
            'hardcoded_secrets': self.get_hardcoded_secrets_test,
            'unsafe_deserialization': self.get_unsafe_deserialization_test,
            'missing_validation': self.get_missing_validation_test,
            'insecure_random': self.get_insecure_random_test
        }
        
        template_func = template_mapping.get(vulnerability_type, self.get_generic_test)
        return template_func(vulnerability)
    
    def get_all_vulnerability_tests(self, vulnerability) -> str:
        """Get comprehensive test suite for a vulnerability."""
        tests = []
        
        # Get the specific test for the vulnerability type
        specific_test = self.get_test_by_vulnerability_type(vulnerability)
        tests.append(specific_test)
        
        # Add generic validation test
        generic_test = self.get_generic_test(vulnerability)
        tests.append(generic_test)
        
        # Add missing validation test if not already included
        if vulnerability.vulnerability_type.lower() != 'missing_validation':
            validation_test = self.get_missing_validation_test(vulnerability)
            tests.append(validation_test)
        
        return "\n\n".join(tests)
    
    def get_security_test_header(self) -> str:
        """Get common header for security test files."""
        return '''"""Security tests for vulnerability protection."""
import pytest
import os
import sys
from unittest.mock import patch, Mock

# Add any necessary imports for security testing
try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

try:
    import secrets
except ImportError:
    secrets = None

def setup_security_test_environment():
    """Setup environment for security testing."""
    # Disable dangerous functions for testing
    os.environ['SECURITY_TEST_MODE'] = 'true'
    
    # Mock dangerous modules if needed
    with patch.dict('sys.modules', {'os': Mock()}):
        pass

'''