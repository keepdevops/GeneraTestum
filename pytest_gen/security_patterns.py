"""
Security vulnerability patterns and detection rules.
"""

from typing import Dict, List
from .security_models import SecurityPattern


class SecurityPatterns:
    """Collection of security vulnerability patterns."""
    
    @staticmethod
    def get_vulnerability_patterns() -> Dict[str, SecurityPattern]:
        """Get all vulnerability patterns."""
        return {
            'sql_injection': SecurityPattern(
                patterns=[
                    r'execute\s*\(\s*["\'].*%s.*["\']',
                    r'cursor\.execute\s*\(.*%s',
                    r'query\s*\(\s*["\'].*\+.*["\']',
                    r'SELECT.*\+.*FROM',
                    r'INSERT.*\+.*INTO',
                    r'UPDATE.*\+.*SET',
                    r'DELETE.*\+.*FROM'
                ],
                severity='high',
                description='SQL injection vulnerability detected',
                mitigation='Use parameterized queries or prepared statements',
                test_template='sql_injection_test'
            ),
            
            'xss': SecurityPattern(
                patterns=[
                    r'response\.write\s*\(.*request\.',
                    r'print\s*\(.*request\.',
                    r'innerHTML\s*=.*request\.',
                    r'document\.write\s*\(.*request\.',
                    r'eval\s*\(.*request\.'
                ],
                severity='medium',
                description='Cross-site scripting vulnerability detected',
                mitigation='Escape output and validate input',
                test_template='xss_test'
            ),
            
            'path_traversal': SecurityPattern(
                patterns=[
                    r'open\s*\(.*request\.',
                    r'file\s*\(.*request\.',
                    r'\.\.\/.*request\.',
                    r'\.\.\\\.*request\.',
                    r'os\.path\.join\s*\(.*request\.'
                ],
                severity='high',
                description='Path traversal vulnerability detected',
                mitigation='Validate and sanitize file paths',
                test_template='path_traversal_test'
            ),
            
            'command_injection': SecurityPattern(
                patterns=[
                    r'os\.system\s*\(.*request\.',
                    r'subprocess\.call\s*\(.*request\.',
                    r'subprocess\.run\s*\(.*request\.',
                    r'os\.popen\s*\(.*request\.',
                    r'exec\s*\(.*request\.',
                    r'eval\s*\(.*request\.'
                ],
                severity='critical',
                description='Command injection vulnerability detected',
                mitigation='Use safe subprocess methods and validate input',
                test_template='command_injection_test'
            ),
            
            'unsafe_deserialization': SecurityPattern(
                patterns=[
                    r'pickle\.loads\s*\(.*request\.',
                    r'yaml\.load\s*\(.*request\.',
                    r'marshal\.loads\s*\(.*request\.',
                    r'json\.loads\s*\(.*request\.',
                    r'ast\.literal_eval\s*\(.*request\.'
                ],
                severity='high',
                description='Unsafe deserialization vulnerability detected',
                mitigation='Use safe deserialization methods',
                test_template='unsafe_deserialization_test'
            ),
            
            'weak_cryptography': SecurityPattern(
                patterns=[
                    r'hashlib\.md5\s*\(',
                    r'hashlib\.sha1\s*\(',
                    r'DES\s*\(',
                    r'RC4\s*\(',
                    r'random\.random\s*\(',
                    r'random\.randint\s*\('
                ],
                severity='medium',
                description='Weak cryptography detected',
                mitigation='Use strong cryptographic algorithms',
                test_template='weak_cryptography_test'
            ),
            
            'hardcoded_secrets': SecurityPattern(
                patterns=[
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    r'api_key\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']',
                    r'private_key\s*=\s*["\'][^"\']+["\']'
                ],
                severity='high',
                description='Hardcoded secrets detected',
                mitigation='Use environment variables or secure key management',
                test_template='hardcoded_secrets_test'
            ),
            
            'code_injection': SecurityPattern(
                patterns=[
                    r'eval\s*\(',
                    r'exec\s*\(',
                    r'compile\s*\(',
                    r'__import__\s*\(',
                    r'getattr\s*\(.*request\.',
                    r'setattr\s*\(.*request\.'
                ],
                severity='critical',
                description='Code injection vulnerability detected',
                mitigation='Avoid dynamic code execution with user input',
                test_template='code_injection_test'
            ),
            
            'missing_input_validation': SecurityPattern(
                patterns=[
                    r'def\s+\w+.*request\.',
                    r'def\s+\w+.*args',
                    r'def\s+\w+.*kwargs',
                    r'input\s*\(',
                    r'raw_input\s*\('
                ],
                severity='medium',
                description='Missing input validation detected',
                mitigation='Add proper input validation and sanitization',
                test_template='missing_validation_test'
            ),
            
            'insecure_random': SecurityPattern(
                patterns=[
                    r'random\.choice\s*\(',
                    r'random\.sample\s*\(',
                    r'random\.shuffle\s*\(',
                    r'random\.uniform\s*\(',
                    r'random\.gauss\s*\('
                ],
                severity='low',
                description='Insecure random number generation detected',
                mitigation='Use cryptographically secure random functions',
                test_template='insecure_random_test'
            )
        }
    
    @staticmethod
    def get_severity_levels() -> Dict[str, int]:
        """Get severity level mappings."""
        return {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1
        }
    
    @staticmethod
    def get_test_payloads() -> Dict[str, List[str]]:
        """Get test payloads for different vulnerability types."""
        return {
            'sql_injection': [
                "'; DROP TABLE users; --",
                "' OR '1'='1",
                "' UNION SELECT * FROM users --",
                "'; INSERT INTO users VALUES ('hacker', 'password'); --"
            ],
            'xss': [
                "<script>alert('xss')</script>",
                "<img src=x onerror=alert('xss')>",
                "javascript:alert('xss')",
                "<svg onload=alert('xss')>"
            ],
            'path_traversal': [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "/etc/passwd",
                "C:\\Windows\\System32\\drivers\\etc\\hosts"
            ],
            'command_injection': [
                "; ls -la",
                "| cat /etc/passwd",
                "& whoami",
                "`id`",
                "$(whoami)"
            ],
            'code_injection': [
                "__import__('os').system('id')",
                "exec('import os; os.system(\\'id\\')')",
                "eval('__import__(\\'os\\').system(\\'id\\')')",
                "compile('import os; os.system(\\'id\\')', '<string>', 'exec')"
            ]
        }
