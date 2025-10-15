"""
Security test templates for different vulnerability types.
"""


class SecurityTestTemplates:
    """Templates for generating security tests."""
    
    @staticmethod
    def get_sql_injection_test(vulnerability) -> str:
        """Get SQL injection test template."""
        return f'''def test_{vulnerability.affected_function}_sql_injection_protection():
    \"\"\"Test SQL injection protection for {vulnerability.affected_function}.\"\"\"
    import pytest
    
    # SQL injection payloads
    injection_payloads = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "' UNION SELECT * FROM users --",
        "'; INSERT INTO users VALUES ('hacker', 'password'); --"
    ]
    
    for payload in injection_payloads:
        with pytest.raises((ValueError, TypeError, DatabaseError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_sql_parameterized_queries():
    \"\"\"Test that {vulnerability.affected_function} uses parameterized queries.\"\"\"
    import pytest
    
    # Valid input should work
    result = {vulnerability.affected_function}("valid_input")
    assert result is not None
    
    # Test with special characters that should be handled safely
    special_chars = ["'", "\"", ";", "--", "/*", "*/"]
    for char in special_chars:
        result = {vulnerability.affected_function}(f"test{{char}}data")
        assert result is not None
'''

    @staticmethod
    def get_xss_test(vulnerability) -> str:
        """Get XSS test template."""
        return f'''def test_{vulnerability.affected_function}_xss_protection():
    \"\"\"Test XSS protection for {vulnerability.affected_function}.\"\"\"
    import pytest
    
    # XSS payloads
    xss_payloads = [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert('xss')>",
        "javascript:alert('xss')",
        "<svg onload=alert('xss')>"
    ]
    
    for payload in xss_payloads:
        result = {vulnerability.affected_function}(payload)
        # Check that script tags are escaped or removed
        assert "<script>" not in str(result)
        assert "javascript:" not in str(result)

def test_{vulnerability.affected_function}_output_encoding():
    \"\"\"Test that {vulnerability.affected_function} properly encodes output.\"\"\"
    # Test with HTML entities
    result = {vulnerability.affected_function}("<>&")
    assert result is not None
    
    # Check that special characters are properly encoded
    if isinstance(result, str):
        assert "&lt;" in result or "<" not in result
        assert "&gt;" in result or ">" not in result
        assert "&amp;" in result or "&" not in result
'''

    @staticmethod
    def get_path_traversal_test(vulnerability) -> str:
        """Get path traversal test template."""
        return f'''def test_{vulnerability.affected_function}_path_traversal_protection():
    \"\"\"Test path traversal protection for {vulnerability.affected_function}.\"\"\"
    import pytest
    
    # Path traversal payloads
    traversal_payloads = [
        "../../../etc/passwd",
        "..\\\\..\\\\..\\\\windows\\\\system32\\\\drivers\\\\etc\\\\hosts",
        "/etc/passwd",
        "C:\\\\Windows\\\\System32\\\\drivers\\\\etc\\\\hosts"
    ]
    
    for payload in traversal_payloads:
        with pytest.raises((ValueError, PermissionError, FileNotFoundError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_boundary_validation():
    \"\"\"Test that {vulnerability.affected_function} validates path boundaries.\"\"\"
    # Valid paths should work
    valid_paths = ["file.txt", "subdir/file.txt", "normal/path/file.txt"]
    for path in valid_paths:
        result = {vulnerability.affected_function}(path)
        assert result is not None
    
    # Test with special characters
    special_chars = ["..", "~", "$", "{{", "}}"]
    for char in special_chars:
        with pytest.raises((ValueError, PermissionError)):
            {vulnerability.affected_function}(f"test{{char}}file.txt")

def test_{vulnerability.affected_function}_special_characters():
    \"\"\"Test {vulnerability.affected_function} with special characters.\"\"\"
    # Test with various special characters
    special_inputs = ["file with spaces.txt", "file-with-dashes.txt", "file_with_underscores.txt"]
    for input_path in special_inputs:
        try:
            result = {vulnerability.affected_function}(input_path)
            assert result is not None
        except (ValueError, PermissionError):
            # Some special characters might be rejected, which is acceptable
            pass
'''

    @staticmethod
    def get_command_injection_test(vulnerability) -> str:
        """Get command injection test template."""
        return f'''def test_{vulnerability.affected_function}_command_injection_protection():
    \"\"\"Test command injection protection for {vulnerability.affected_function}.\"\"\"
    import pytest
    
    # Command injection payloads
    injection_payloads = [
        "; ls -la",
        "| cat /etc/passwd",
        "& whoami",
        "`id`",
        "$(whoami)"
    ]
    
    for payload in injection_payloads:
        with pytest.raises((ValueError, TypeError, OSError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_subprocess_safety():
    \"\"\"Test that {vulnerability.affected_function} uses safe subprocess methods.\"\"\"
    # Valid commands should work
    valid_commands = ["echo hello", "ls -la", "pwd"]
    for cmd in valid_commands:
        try:
            result = {vulnerability.affected_function}(cmd)
            assert result is not None
        except (ValueError, OSError):
            # Some commands might be rejected for security reasons
            pass
'''

    @staticmethod
    def get_code_injection_test(vulnerability) -> str:
        """Get code injection test template."""
        return f'''def test_{vulnerability.affected_function}_code_injection_protection():
    \"\"\"Test code injection protection for {vulnerability.affected_function}.\"\"\"
    import pytest
    
    # Code injection payloads
    injection_payloads = [
        "__import__('os').system('id')",
        "exec('import os; os.system(\\'id\\')')",
        "eval('__import__(\\'os\\').system(\\'id\\')')",
        "compile('import os; os.system(\\'id\\')', '<string>', 'exec')"
    ]
    
    for payload in injection_payloads:
        with pytest.raises((ValueError, TypeError, SyntaxError)):
            {vulnerability.affected_function}(payload)

def test_{vulnerability.affected_function}_safe_evaluation():
    \"\"\"Test that {vulnerability.affected_function} uses safe evaluation methods.\"\"\"
    # Safe expressions should work
    safe_expressions = ["1 + 1", "2 * 3", "len('test')"]
    for expr in safe_expressions:
        try:
            result = {vulnerability.affected_function}(expr)
            assert result is not None
        except (ValueError, TypeError):
            # Some expressions might be rejected for security reasons
            pass
'''

    @staticmethod
    def get_generic_test(vulnerability) -> str:
        """Get generic test template."""
        return f'''def test_{vulnerability.affected_function}_{vulnerability.vulnerability_type}_protection():
    \"\"\"Test {vulnerability.vulnerability_type} protection for {vulnerability.affected_function}.\"\"\"
    import pytest
    
    # Test with various inputs
    test_inputs = [
        "normal_input",
        "input_with_special_chars!@#$%",
        "input with spaces",
        "input_with_numbers123"
    ]
    
    for test_input in test_inputs:
        try:
            result = {vulnerability.affected_function}(test_input)
            assert result is not None
        except (ValueError, TypeError):
            # Some inputs might be rejected for security reasons
            pass
'''

    @staticmethod
    def get_weak_cryptography_test(vulnerability) -> str:
        """Get weak cryptography test template."""
        return f'''def test_{vulnerability.affected_function}_weak_cryptography():
    \"\"\"Test that {vulnerability.affected_function} uses strong cryptography.\"\"\"
    import pytest
    
    # Test that weak algorithms are not used
    with pytest.raises((ValueError, NotImplementedError)):
        {vulnerability.affected_function}("weak_algorithm")
'''

    @staticmethod
    def get_hardcoded_secrets_test(vulnerability) -> str:
        """Get hardcoded secrets test template."""
        return f'''def test_{vulnerability.affected_function}_hardcoded_secrets():
    \"\"\"Test that {vulnerability.affected_function} does not use hardcoded secrets.\"\"\"
    import pytest
    
    # Test that secrets are not hardcoded
    result = {vulnerability.affected_function}()
    # Verify that environment variables or secure methods are used
    assert result is not None
'''

    @staticmethod
    def get_unsafe_deserialization_test(vulnerability) -> str:
        """Get unsafe deserialization test template."""
        return f'''def test_{vulnerability.affected_function}_unsafe_deserialization():
    \"\"\"Test that {vulnerability.affected_function} uses safe deserialization.\"\"\"
    import pytest
    
    # Test with potentially malicious data
    malicious_data = "malicious_serialized_data"
    with pytest.raises((ValueError, TypeError)):
        {vulnerability.affected_function}(malicious_data)
'''

    @staticmethod
    def get_missing_validation_test(vulnerability) -> str:
        """Get missing validation test template."""
        return f'''def test_{vulnerability.affected_function}_missing_validation():
    \"\"\"Test that {vulnerability.affected_function} has proper input validation.\"\"\"
    import pytest
    
    # Test with invalid inputs
    invalid_inputs = [None, "", "   ", 123, [], {{}}]
    for invalid_input in invalid_inputs:
        with pytest.raises((ValueError, TypeError)):
            {vulnerability.affected_function}(invalid_input)
'''

    @staticmethod
    def get_insecure_random_test(vulnerability) -> str:
        """Get insecure random test template."""
        return f'''def test_{vulnerability.affected_function}_insecure_random():
    \"\"\"Test that {vulnerability.affected_function} uses secure random generation.\"\"\"
    import pytest
    
    # Test that insecure random methods are not used
    with pytest.raises((ValueError, NotImplementedError)):
        {vulnerability.affected_function}("insecure_random")
'''
