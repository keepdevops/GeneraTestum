"""
API documentation formatters.
"""

from typing import Dict, Any, List


class APIDocsFormatters:
    """API documentation formatters."""
    
    @staticmethod
    def format_authentication(auth_info: Dict[str, Any]) -> str:
        auth_type = auth_info.get('type', 'Bearer Token')
        auth_description = auth_info.get('description', 'API key authentication required')
        auth_header = auth_info.get('header', 'Authorization: Bearer <token>')
        base_url = auth_info.get('base_url', 'https://api.example.com/v1')
        
        return f"""### {auth_type}

{auth_description}

#### Example Usage

```python
import requests

headers = {{
    'Authorization': '{auth_header}',
    'Content-Type': 'application/json'
}}

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
    def format_rate_limiting(rate_info: Dict[str, Any]) -> str:
        requests_per_minute = rate_info.get('requests_per_minute', 60)
        requests_per_hour = rate_info.get('requests_per_hour', 1000)
        requests_per_day = rate_info.get('requests_per_day', 10000)
        retry_after_seconds = rate_info.get('retry_after_seconds', 60)
        
        return f"""### Limits

- **Requests per minute**: {requests_per_minute}
- **Requests per hour**: {requests_per_hour}
- **Requests per day**: {requests_per_day}

### Headers

When rate limits are exceeded, the API returns:

```
HTTP 429 Too Many Requests
Retry-After: {retry_after_seconds}
X-RateLimit-Limit: {requests_per_minute}
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200
```

### Test Example

```python
def test_rate_limiting():
    for i in range(10):
        response = requests.get(f'{{BASE_URL}}/test')
        
    assert response.status_code == 429
    assert 'Retry-After' in response.headers
```"""

    @staticmethod
    def format_endpoints(endpoints: List[Dict[str, Any]]) -> str:
        if not endpoints:
            return "No endpoints documented."
        
        endpoint_docs = []
        for endpoint in endpoints:
            method = endpoint.get('method', 'GET')
            path = endpoint.get('path', '/')
            description = endpoint.get('description', 'No description available')
            parameters = endpoint.get('parameters', [])
            response_example = endpoint.get('response_example', '{}')
            
            endpoint_name = path.replace('/', '_').replace('{', '').replace('}', '').strip('_')
            
            parameters_section = APIDocsFormatters.format_parameters(parameters)
            
            endpoint_doc = f"""### {method} {path}

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
        f'{{BASE_URL}}{path}'
    )
    
    assert response.status_code == 200
    assert response.json() is not None
```"""
            endpoint_docs.append(endpoint_doc)
        
        return '\n\n'.join(endpoint_docs)

    @staticmethod
    def format_parameters(parameters: List[Dict[str, Any]]) -> str:
        if not parameters:
            return "No parameters required."
        
        param_rows = []
        for param in parameters:
            name = param.get('name', '')
            param_type = param.get('type', 'string')
            required = param.get('required', False)
            description = param.get('description', 'No description')
            
            required_text = "Required" if required else "Optional"
            param_rows.append(f"- **{name}** ({param_type}, {required_text}): {description}")
        
        return '\n'.join(param_rows)

    @staticmethod
    def format_error_codes(error_codes: Dict[int, str]) -> str:
        if not error_codes:
            return "Standard HTTP status codes are used."
        
        error_rows = []
        for code, description in error_codes.items():
            error_rows.append(f"| {code} | {description} | Check request parameters |")
        
        error_table = '\n'.join(error_rows)
        
        return f"""| Code | Description | Resolution |
|------|-------------|------------|
{error_table}

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

    @staticmethod
    def format_testing_examples(examples: List[Dict[str, Any]]) -> str:
        if not examples:
            return "No testing examples provided."
        
        example_docs = []
        for example in examples:
            name = example.get('name', 'Example')
            description = example.get('description', 'Test example')
            code = example.get('code', '# Example code here')
            
            example_doc = f"""### {name}

{description}

```python
{code}
```"""
            example_docs.append(example_doc)
        
        return '\n\n'.join(example_docs)
