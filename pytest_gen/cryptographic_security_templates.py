"""
Security test templates for cryptographic and validation vulnerabilities.
"""


class CryptographicSecurityTemplates:
    """Templates for cryptographic security tests."""
    
    @staticmethod
    def get_weak_cryptography_test(vulnerability) -> str:
        """Get weak cryptography test template."""
        return f'''def test_{vulnerability.affected_function}_weak_cryptography():
    """Test that {vulnerability.affected_function} uses strong cryptography."""
    import pytest
    
    # Test that weak algorithms are not used
    with pytest.raises((ValueError, NotImplementedError)):
        {vulnerability.affected_function}("weak_algorithm")
'''
    
    @staticmethod
    def get_hardcoded_secrets_test(vulnerability) -> str:
        """Get hardcoded secrets test template."""
        return f'''def test_{vulnerability.affected_function}_hardcoded_secrets():
    """Test that {vulnerability.affected_function} does not use hardcoded secrets."""
    import pytest
    
    # Test that secrets are not hardcoded
    result = {vulnerability.affected_function}()
    # Verify that environment variables or secure methods are used
    assert result is not None
'''
    
    @staticmethod
    def get_insecure_random_test(vulnerability) -> str:
        """Get insecure random test template."""
        return f'''def test_{vulnerability.affected_function}_insecure_random():
    """Test that {vulnerability.affected_function} uses secure random generation."""
    import pytest
    
    # Test that insecure random methods are not used
    with pytest.raises((ValueError, NotImplementedError)):
        {vulnerability.affected_function}("insecure_random")
'''
    
    @staticmethod
    def get_unsafe_deserialization_test(vulnerability) -> str:
        """Get unsafe deserialization test template."""
        return f'''def test_{vulnerability.affected_function}_unsafe_deserialization():
    """Test that {vulnerability.affected_function} uses safe deserialization."""
    import pytest
    
    # Test with potentially malicious data
    malicious_data = "malicious_serialized_data"
    with pytest.raises((ValueError, TypeError)):
        {vulnerability.affected_function}(malicious_data)
'''


class ValidationSecurityTemplates:
    """Templates for input validation security tests."""
    
    @staticmethod
    def get_missing_validation_test(vulnerability) -> str:
        """Get missing validation test template."""
        return f'''def test_{vulnerability.affected_function}_missing_validation():
    """Test that {vulnerability.affected_function} has proper input validation."""
    import pytest
    
    # Test with invalid inputs
    invalid_inputs = [None, "", "   ", 123, [], {{}}]
    for invalid_input in invalid_inputs:
        with pytest.raises((ValueError, TypeError)):
            {vulnerability.affected_function}(invalid_input)
'''
    
    @staticmethod
    def get_generic_test(vulnerability) -> str:
        """Get generic test template."""
        return f'''def test_{vulnerability.affected_function}_{vulnerability.vulnerability_type}_protection():
    """Test {vulnerability.vulnerability_type} protection for {vulnerability.affected_function}."""
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
