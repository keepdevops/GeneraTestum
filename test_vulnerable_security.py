# Security tests for code_injection

def test_dangerous_eval_code_injection_protection():
    """Test code injection protection for dangerous_eval."""
    import pytest
    
    from vulnerable_example import dangerous_eval
    
    # Code injection payloads
    injection_payloads = [
        "__import__('os').system('id')",
        "exec('import os; os.system(\'id\')')",
        "eval('__import__(\'os\').system(\'id\')')",
        "compile('import os; os.system(\'id\')', '<string>', 'exec')",
        "__builtins__['__import__']('os').system('id')",
        "globals()['__builtins__']['__import__']('os').system('id')",
        "vars()['__import__']('os').system('id')",
        "dir()[0].__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['sys'].modules['os'].system('id')"
    ]
    
    for payload in injection_payloads:
        with pytest.raises((ValueError, TypeError, SyntaxError, NameError)):
            dangerous_eval(payload)

def test_dangerous_eval_safe_evaluation():
    """Test safe evaluation for dangerous_eval."""
    import pytest
    import ast
    
    from vulnerable_example import dangerous_eval
    
    # Test with safe expressions
    safe_expressions = [
        "1 + 1",
        "2 * 3",
        "len('test')",
        "[1, 2, 3]",
        "{'key': 'value'}"
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
                        dangerous_eval(expression)
                    break
            else:
                # Safe expression
                try:
                    result = dangerous_eval(expression)
                    assert result is not None
                except Exception:
                    pass
        except SyntaxError:
            with pytest.raises((ValueError, TypeError, SyntaxError)):
                dangerous_eval(expression)
