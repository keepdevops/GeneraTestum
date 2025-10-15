"""
Security test templates for web and file vulnerabilities.
"""


class WebSecurityTemplates:
    """Templates for web-based security tests."""
    
    @staticmethod
    def get_xss_test(vulnerability) -> str:
        """Get XSS test template."""
        return f'''def test_{vulnerability.affected_function}_xss_protection():
    """Test XSS protection for {vulnerability.affected_function}."""
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
    """Test that {vulnerability.affected_function} properly encodes output."""
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
    """Test path traversal protection for {vulnerability.affected_function}."""
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
    """Test that {vulnerability.affected_function} validates path boundaries."""
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
    """Test {vulnerability.affected_function} with special characters."""
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
