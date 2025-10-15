"""
Security tests for the fixed security_example.py file.
Tests both the deprecated dangerous_eval and the new safe_eval functions.
"""

import pytest
from security_example import dangerous_eval, safe_eval


class TestDangerousEvalDeprecated:
    """Test that dangerous_eval is properly deprecated and raises errors."""
    
    def test_dangerous_eval_deprecated_raises_error(self):
        """Test that dangerous_eval raises ValueError for all inputs."""
        with pytest.raises(ValueError, match="dangerous_eval is deprecated"):
            dangerous_eval("1 + 1")
    
    def test_dangerous_eval_malicious_input_raises_error(self):
        """Test that dangerous_eval blocks malicious input."""
        malicious_inputs = [
            "__import__('os').system('id')",
            "exec('import os; os.system(\'id\')')",
            "eval('__import__(\'os\').system(\'id\')')",
            "compile('import os; os.system(\'id\')', '<string>', 'exec')",
            "__builtins__['__import__']('os').system('id')",
            "globals()['__builtins__']['__import__']('os').system('id')",
            "vars()['__import__']('os').system('id')",
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="dangerous_eval is deprecated"):
                dangerous_eval(malicious_input)


class TestSafeEval:
    """Test the new safe_eval function."""
    
    def test_safe_eval_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        test_cases = [
            ("1 + 1", 2),
            ("5 - 3", 2),
            ("2 * 3", 6),
            ("8 / 2", 4.0),
            ("7 // 2", 3),
            ("7 % 3", 1),
            ("2 ** 3", 8),
        ]
        
        for expression, expected in test_cases:
            result = safe_eval(expression)
            assert result == expected, f"Expression '{expression}' should equal {expected}, got {result}"
    
    def test_safe_eval_unary_operations(self):
        """Test unary operations."""
        test_cases = [
            ("-5", -5),
            ("+10", 10),
            ("--3", 3),
            ("+-4", -4),
        ]
        
        for expression, expected in test_cases:
            result = safe_eval(expression)
            assert result == expected, f"Expression '{expression}' should equal {expected}, got {result}"
    
    def test_safe_eval_constants(self):
        """Test built-in constants."""
        test_cases = [
            ("True", True),
            ("False", False),
            ("None", None),
        ]
        
        for expression, expected in test_cases:
            result = safe_eval(expression)
            assert result == expected, f"Expression '{expression}' should equal {expected}, got {result}"
    
    def test_safe_eval_literals(self):
        """Test literal values."""
        test_cases = [
            ("42", 42),
            ("3.14", 3.14),
            ("'hello'", "hello"),
            ("\"world\"", "world"),
            ("[1, 2, 3]", [1, 2, 3]),
            ("(1, 2, 3)", (1, 2, 3)),
            ("{'a': 1, 'b': 2}", {'a': 1, 'b': 2}),
        ]
        
        for expression, expected in test_cases:
            result = safe_eval(expression)
            assert result == expected, f"Expression '{expression}' should equal {expected}, got {result}"
    
    def test_safe_eval_complex_expressions(self):
        """Test complex but safe expressions."""
        test_cases = [
            ("(1 + 2) * 3", 9),
            ("2 ** (3 + 1)", 16),
            ("(10 - 2) / (2 + 2)", 2.0),
            ("-[1, 2, 3][0]", -1),  # This should fail due to subscripting
        ]
        
        for expression, expected in test_cases:
            if "[" in expression:  # Contains subscripting
                with pytest.raises(ValueError, match="Subscripting is not allowed"):
                    safe_eval(expression)
            else:
                result = safe_eval(expression)
                assert result == expected, f"Expression '{expression}' should equal {expected}, got {result}"
    
    def test_safe_eval_input_validation(self):
        """Test input validation."""
        invalid_inputs = [
            None,
            "",
            "   ",
            "x" * 1001,  # Too long
            123,  # Not a string
            [],
            {},
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                safe_eval(invalid_input)
    
    def test_safe_eval_blocks_function_calls(self):
        """Test that function calls are blocked."""
        malicious_inputs = [
            "__import__('os').system('id')",
            "exec('import os; os.system(\'id\')')",
            "eval('1 + 1')",
            "compile('1 + 1', '<string>', 'eval')",
            "len('test')",
            "print('hello')",
            "open('file.txt')",
            "input()",
        ]
        
        for malicious_input in malicious_inputs:
            # Some expressions may have syntax errors or be blocked at different stages
            with pytest.raises(ValueError, match="(Function calls and imports are not allowed|Invalid expression syntax|Expression evaluation failed)"):
                safe_eval(malicious_input)
    
    def test_safe_eval_blocks_variables(self):
        """Test that variable access is blocked."""
        malicious_inputs = [
            "x + 1",
            "my_var",
            "builtin_function",
            "__name__",
            "__file__",
            "sys.path",
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="is not allowed"):
                safe_eval(malicious_input)
    
    def test_safe_eval_blocks_attribute_access(self):
        """Test that attribute access is blocked."""
        malicious_inputs = [
            "obj.method",
            "module.function",
            "dict.keys",
            "list.append",
            "__builtins__.__import__",
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Attribute access is not allowed"):
                safe_eval(malicious_input)
    
    def test_safe_eval_blocks_subscripting(self):
        """Test that subscripting is blocked."""
        malicious_inputs = [
            "obj[0]",
            "dict['key']",
            "list[1:3]",
            "str[0]",
            "tuple[0]",
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Subscripting is not allowed"):
                safe_eval(malicious_input)
    
    def test_safe_eval_blocks_comparisons(self):
        """Test that comparison operations are blocked."""
        malicious_inputs = [
            "1 == 1",
            "2 > 1",
            "3 < 5",
            "1 != 2",
            "1 <= 2",
            "2 >= 1",
            "1 in [1, 2, 3]",
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Comparison operations are not allowed"):
                safe_eval(malicious_input)
    
    def test_safe_eval_blocks_boolean_operations(self):
        """Test that boolean operations are blocked."""
        malicious_inputs = [
            "True and False",
            "True or False",
            "not True",
            "1 and 2",
            "1 or 2",
        ]
        
        for malicious_input in malicious_inputs:
            # Boolean operations may be blocked at different stages (AST walk or evaluation)
            with pytest.raises(ValueError, match="(Boolean operations are not allowed|Expression evaluation failed)"):
                safe_eval(malicious_input)
    
    def test_safe_eval_syntax_errors(self):
        """Test that syntax errors are handled properly."""
        invalid_syntax = [
            "1 +",
            "2 *",
            "(",
            ")",
            "1 1",
            "def",
            "class",
            "import",
        ]
        
        for invalid_expression in invalid_syntax:
            with pytest.raises(ValueError, match="Invalid expression syntax"):
                safe_eval(invalid_expression)
    
    def test_safe_eval_edge_cases(self):
        """Test edge cases."""
        # Test empty lists and dicts
        assert safe_eval("[]") == []
        assert safe_eval("()") == ()
        assert safe_eval("{}") == {}
        
        # Test nested structures
        assert safe_eval("[1, [2, 3], 4]") == [1, [2, 3], 4]
        assert safe_eval("{'a': [1, 2], 'b': 3}") == {'a': [1, 2], 'b': 3}
        
        # Test complex arithmetic
        assert safe_eval("2 ** 3 ** 2") == 512  # Right-associative
        assert safe_eval("(2 ** 3) ** 2") == 64


if __name__ == "__main__":
    pytest.main([__file__])
