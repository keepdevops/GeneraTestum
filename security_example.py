"""
Example file with potential security vulnerabilities for testing.
"""

import os
import subprocess
import pickle
import hashlib
import json
from flask import Flask, request, render_template_string

app = Flask(__name__)

def vulnerable_sql_query(user_id):
    """Vulnerable function with potential SQL injection."""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # This is vulnerable to SQL injection
    return query

def vulnerable_file_access(filename):
    """Vulnerable function with potential path traversal."""
    file_path = f"/uploads/{filename}"
    with open(file_path, 'r') as f:
        return f.read()

def vulnerable_command_execution(command):
    """Vulnerable function with potential command injection."""
    result = os.system(command)
    return result

def vulnerable_deserialization(data):
    """Vulnerable function with unsafe deserialization."""
    return pickle.loads(data)

def weak_password_hash(password):
    """Function using weak cryptographic algorithm."""
    return hashlib.md5(password.encode()).hexdigest()

def hardcoded_secrets():
    """Function with hardcoded secrets."""
    api_key = "sk-1234567890abcdef"
    password = "admin123"
    return api_key, password

def missing_input_validation(user_input):
    """Function missing proper input validation."""
    # No validation of user input
    processed = user_input.upper()
    return processed

def safe_eval(expression):
    """Safely evaluate mathematical expressions using AST parsing."""
    import ast
    import operator
    
    # Define allowed operations for safe evaluation
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    def _eval_node(node):
        """Safely evaluate AST nodes."""
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.Str):  # Python < 3.8
            return node.s
        elif isinstance(node, ast.BinOp):
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            op = ALLOWED_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval_node(node.operand)
            op = ALLOWED_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operation: {type(node.op).__name__}")
            return op(operand)
        elif isinstance(node, ast.List):
            return [_eval_node(item) for item in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(_eval_node(item) for item in node.elts)
        elif isinstance(node, ast.Dict):
            keys = [_eval_node(key) for key in node.keys]
            values = [_eval_node(value) for value in node.values]
            return dict(zip(keys, values))
        else:
            raise ValueError(f"Unsupported AST node type: {type(node).__name__}")
    
    # Validate input
    if not expression or not isinstance(expression, str):
        raise ValueError("Expression must be a non-empty string")
    
    # Remove whitespace and limit length
    expression = expression.strip()
    if len(expression) > 1000:
        raise ValueError("Expression too long")
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')
        
        # Check for dangerous operations
        for node in ast.walk(tree):
            if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom)):
                raise ValueError("Function calls and imports are not allowed")
            if isinstance(node, ast.Name):
                # Only allow built-in constants
                if node.id not in ('True', 'False', 'None'):
                    raise ValueError(f"Variable '{node.id}' is not allowed")
            if isinstance(node, ast.Attribute):
                raise ValueError("Attribute access is not allowed")
            if isinstance(node, ast.Subscript):
                raise ValueError("Subscripting is not allowed")
            if isinstance(node, ast.Compare):
                raise ValueError("Comparison operations are not allowed")
            if isinstance(node, ast.BoolOp):
                raise ValueError("Boolean operations are not allowed")
        
        # Evaluate the safe expression
        return _eval_node(tree)
        
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")
    except Exception as e:
        raise ValueError(f"Expression evaluation failed: {e}")


def dangerous_eval(expression):
    """DEPRECATED: Use safe_eval instead. This function is kept for testing purposes only."""
    raise ValueError("dangerous_eval is deprecated and unsafe. Use safe_eval instead.")

@app.route('/search')
def search_users():
    """Vulnerable Flask route with SQL injection."""
    user_id = request.args.get('id')
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return f"Query: {query}"

@app.route('/file')
def get_file():
    """Vulnerable Flask route with path traversal."""
    filename = request.args.get('file')
    file_path = f"/uploads/{filename}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception:
        return "File not found"

@app.route('/execute')
def execute_command():
    """Vulnerable Flask route with command injection."""
    cmd = request.args.get('cmd')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

@app.route('/render')
def render_template():
    """Vulnerable Flask route with XSS."""
    template = request.args.get('template', 'Hello {{ name }}')
    name = request.args.get('name', 'World')
    return render_template_string(template, name=name)

def safe_function(input_data):
    """Example of a secure function."""
    if not input_data or not isinstance(input_data, str):
        raise ValueError("Invalid input")
    
    # Sanitize input
    sanitized = input_data.strip()
    if len(sanitized) > 100:
        raise ValueError("Input too long")
    
    # Use parameterized query (example)
    # query = "SELECT * FROM users WHERE id = %s"
    # cursor.execute(query, (sanitized,))
    
    return f"Processed: {sanitized}"
