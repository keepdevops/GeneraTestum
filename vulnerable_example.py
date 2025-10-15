"""
Example file with security vulnerabilities for testing the auto-security system.
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

def dangerous_eval(expression):
    """Function using dangerous eval."""
    return eval(expression)

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
