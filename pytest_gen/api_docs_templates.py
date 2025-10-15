"""
API documentation templates.
"""

class APIDocsTemplates:
    """API documentation templates."""
    
    @staticmethod
    def get_base_template() -> str:
        return """# API Documentation

## 📋 Overview

{description}

## 🔗 Base URL

```
{base_url}
```

## 🔐 Authentication

{auth_section}

## 📊 Rate Limiting

{rate_limiting_section}

## 📚 Endpoints

{endpoints_section}

## ❌ Error Codes

{error_codes_section}

## 🧪 Testing Examples

{testing_examples_section}

## 🔧 Test Configuration

### Environment Setup

```bash
# Install dependencies
pip install requests pytest pytest-cov

# Set environment variables
export API_BASE_URL={base_url}
export API_KEY=your_api_key_here
```

### Test Configuration

```python
import os
import requests
import pytest

BASE_URL = os.getenv('API_BASE_URL', '{base_url}')
API_KEY = os.getenv('API_KEY')

@pytest.fixture
def api_client():
    return requests.Session()

@pytest.fixture
def headers():
    return {{
        'Authorization': f'Bearer {{API_KEY}}',
        'Content-Type': 'application/json'
    }}
```
"""

    @staticmethod
    def get_authentication_template() -> str:
        return """### {auth_type}

{auth_description}

#### Example Usage

```python
import requests

# Set up authentication
headers = {{
    'Authorization': '{auth_header}',
    'Content-Type': 'application/json'
}}

# Make authenticated request
response = requests.get('{base_url}/endpoint', headers=headers)
```

#### Test Example

```python
def test_authenticated_request():
    headers = {{
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    }}
    
    response = requests.get(f'{{BASE_URL}}/protected', headers=headers)
    assert response.status_code == 200
```"""

    @staticmethod
    def get_rate_limiting_template() -> str:
        return """### Limits

- **Requests per minute**: {requests_per_minute}
- **Requests per hour**: {requests_per_hour}
- **Requests per day**: {requests_per_day}

### Headers

When rate limits are exceeded, the API returns:

```
HTTP 429 Too Many Requests
Retry-After: {retry_after_seconds}
X-RateLimit-Limit: {limit}
X-RateLimit-Remaining: {remaining}
X-RateLimit-Reset: {reset_timestamp}
```

### Test Example

```python
def test_rate_limiting():
    # Make multiple requests quickly
    for i in range(10):
        response = requests.get(f'{{BASE_URL}}/test')
        
    # Should eventually hit rate limit
    assert response.status_code == 429
    assert 'Retry-After' in response.headers
```"""

    @staticmethod
    def get_endpoint_template() -> str:
        return """### {method} {path}

{description}

#### Parameters

{parameters_section}

#### Response

```json
{response_example}
```

#### Test Example

```python
def test_{endpoint_name}():
    response = requests.{method.lower()}(
        f'{{BASE_URL}}{path}',
        {request_params}
    )
    
    assert response.status_code == {expected_status}
    assert response.json() is not None
    {assertions}
```"""

    @staticmethod
    def get_error_codes_template() -> str:
        return """| Code | Description | Resolution |
|------|-------------|------------|
{error_rows}

### Error Response Format

```json
{{
    "error": {{
        "code": 400,
        "message": "Bad Request",
        "details": "Invalid parameter value"
    }}
}}
```

### Test Example

```python
def test_error_handling():
    response = requests.get(f'{{BASE_URL}}/invalid')
    
    assert response.status_code == 404
    error_data = response.json()
    assert 'error' in error_data
    assert error_data['error']['code'] == 404
```"""
