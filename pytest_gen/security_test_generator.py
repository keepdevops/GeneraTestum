"""
Security test generator.
"""

from typing import Dict, List, Any
from .security_models import SecurityTest, SecurityTestSuite, SecurityVulnerability
from .security_patterns import SecurityPatterns


class SecurityTestGenerator:
    """Generates security tests for identified vulnerabilities."""

    def __init__(self):
        self.patterns = SecurityPatterns.get_vulnerability_patterns()
        self.payloads = SecurityPatterns.get_test_payloads()

    def generate_security_tests(self, vulnerabilities: List[SecurityVulnerability]) -> SecurityTestSuite:
        """Generate security tests for vulnerabilities."""
        tests = []
        coverage = {}
        
        for vulnerability in vulnerabilities:
            test = self._generate_test_for_vulnerability(vulnerability)
            if test:
                tests.append(test)
                
                # Update coverage
                vuln_type = vulnerability.vulnerability_type
                coverage[vuln_type] = coverage.get(vuln_type, 0) + 1
        
        # Generate test file content
        test_file_content = self._generate_test_file_content(tests)
        
        return SecurityTestSuite(
            tests=tests,
            total_tests=len(tests),
            coverage=coverage,
            test_file_content=test_file_content
        )

    def _generate_test_for_vulnerability(self, vulnerability: SecurityVulnerability) -> SecurityTest:
        """Generate a test for a specific vulnerability."""
        from .security_test_templates import SecurityTestTemplates
        
        template_map = {
            'sql_injection': SecurityTestTemplates.get_sql_injection_test,
            'xss': SecurityTestTemplates.get_xss_test,
            'path_traversal': SecurityTestTemplates.get_path_traversal_test,
            'command_injection': SecurityTestTemplates.get_command_injection_test,
            'unsafe_deserialization': SecurityTestTemplates.get_unsafe_deserialization_test,
            'weak_cryptography': SecurityTestTemplates.get_weak_cryptography_test,
            'hardcoded_secrets': SecurityTestTemplates.get_hardcoded_secrets_test,
            'code_injection': SecurityTestTemplates.get_code_injection_test,
            'missing_input_validation': SecurityTestTemplates.get_missing_validation_test,
            'insecure_random': SecurityTestTemplates.get_insecure_random_test
        }
        
        template_func = template_map.get(vulnerability.vulnerability_type)
        if template_func:
            test_code = template_func(vulnerability)
            test_name = f"test_{vulnerability.affected_function}_{vulnerability.vulnerability_type}_protection"
        else:
            # Generic test for unknown vulnerability types
            test_code = SecurityTestTemplates.get_generic_test(vulnerability)
            test_name = f"test_{vulnerability.affected_function}_{vulnerability.vulnerability_type}_protection"
        
        return SecurityTest(
            test_name=test_name,
            test_description=f"{vulnerability.vulnerability_type} protection for {vulnerability.affected_function}",
            test_code=test_code,
            vulnerability_type=vulnerability.vulnerability_type,
            severity=vulnerability.severity
        )

    def _generate_test_file_content(self, tests: List[SecurityTest]) -> str:
        """Generate complete test file content."""
        content = "# Security tests for identified vulnerabilities\n\n"
        
        for test in tests:
            content += test.test_code + "\n\n"
        
        return content