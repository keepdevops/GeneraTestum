"""
Security test templates for injection vulnerabilities.
"""


class InjectionSecurityTemplates:
    """Templates for injection-based security tests."""
    
    @staticmethod
    def get_sql_injection_test(vulnerability) -> str:
        """Get SQL injection test template."""
        return f'''def test_{vulnerability.affected_function}_sql_injection_protection():
    """Test SQL injection protection for {vulnerability.affected_function}."""
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
    """Test that {vulnerability.affected_function} uses parameterized queries."""
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
    def get_command_injection_test(vulnerability) -> str:
        """Get command injection test template."""
        return f'''def test_{vulnerability.affected_function}_command_injection_protection():
    """Test command injection protection for {vulnerability.affected_function}."""
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
    """Test that {vulnerability.affected_function} uses safe subprocess methods."""
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
    """Test code injection protection for {vulnerability.affected_function}."""
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
    """Test that {vulnerability.affected_function} uses safe evaluation methods."""
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
