"""
API documentation generator.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation


class APIDocsGenerator:
    """Generates API documentation."""

    def generate_api_documentation(self, api_info: Dict[str, Any]) -> TestDocumentation:
        """Generate API documentation."""
        content = f"""# API Documentation

## 📋 Overview

{api_info.get('description', 'Comprehensive API documentation with examples and testing information.')}

## 🔗 Base URL

```
{api_info.get('base_url', 'https://api.example.com/v1')}
```

## 🔐 Authentication

{self._format_authentication(api_info.get('authentication', {}))}

## 📊 Rate Limiting

{self._format_rate_limiting(api_info.get('rate_limiting', {}))}

## 📚 Endpoints

{self._format_endpoints(api_info.get('endpoints', []))}

## ❌ Error Codes

{self._format_error_codes(api_info.get('error_codes', {}))}

## 🧪 Testing Examples

{self._format_testing_examples(api_info.get('examples', []))}

## 🔧 Test Configuration

### Environment Setup

```bash
# Set environment variables
export API_BASE_URL="{api_info.get('base_url', 'https://api.example.com/v1')}"
export API_KEY="{api_info.get('api_key', 'your-api-key')}"
export API_SECRET="{api_info.get('api_secret', 'your-api-secret')}"
```

### Test Configuration

```python
# conftest.py
import pytest
import requests

@pytest.fixture
def api_client():
    return requests.Session()

@pytest.fixture
def api_base_url():
    return "{api_info.get('base_url', 'https://api.example.com/v1')}"

@pytest.fixture
def api_headers():
    return {{
        "Authorization": f"Bearer {{os.getenv('API_KEY')}}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }}
```

## 📈 Performance Testing

### Load Testing Example

```python
import pytest
import requests
import time

def test_api_performance():
    \"\"\"Test API response time under load.\"\"\"
    base_url = "{api_info.get('base_url', 'https://api.example.com/v1')}"
    endpoint = "/users"
    
    start_time = time.time()
    response = requests.get(f"{{base_url}}{{endpoint}}")
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response.status_code == 200
    assert response_time < 1.0  # Should respond within 1 second
```

### Concurrent Testing

```python
import asyncio
import aiohttp
import pytest

async def test_concurrent_requests():
    \"\"\"Test API under concurrent load.\"\"\"
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(10):
            task = session.get("{api_info.get('base_url', 'https://api.example.com/v1')}/users")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            assert response.status == 200
```

## 🔒 Security Testing

### Input Validation Testing

```python
def test_input_validation():
    \"\"\"Test API input validation.\"\"\"
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "<script>alert('xss')</script>",
        "../../../etc/passwd",
        "{{{{7*7}}}}"
    ]
    
    for malicious_input in malicious_inputs:
        response = requests.post(
            "{api_info.get('base_url', 'https://api.example.com/v1')}/users",
            json={{"name": malicious_input}}
        )
        assert response.status_code in [400, 422]  # Should reject malicious input
```

### Authentication Testing

```python
def test_authentication():
    \"\"\"Test API authentication.\"\"\"
    # Test without authentication
    response = requests.get("{api_info.get('base_url', 'https://api.example.com/v1')}/users")
    assert response.status_code == 401
    
    # Test with invalid token
    headers = {{"Authorization": "Bearer invalid-token"}}
    response = requests.get(
        "{api_info.get('base_url', 'https://api.example.com/v1')}/users",
        headers=headers
    )
    assert response.status_code == 401
    
    # Test with valid token
    headers = {{"Authorization": f"Bearer {{os.getenv('API_KEY')}}"}}
    response = requests.get(
        "{api_info.get('base_url', 'https://api.example.com/v1')}/users",
        headers=headers
    )
    assert response.status_code == 200
```

## 📊 Monitoring and Metrics

### Health Check

```python
def test_health_check():
    \"\"\"Test API health endpoint.\"\"\"
    response = requests.get("{api_info.get('base_url', 'https://api.example.com/v1')}/health")
    assert response.status_code == 200
    
    health_data = response.json()
    assert health_data["status"] == "healthy"
    assert "uptime" in health_data
    assert "version" in health_data
```

### Metrics Collection

```python
def test_metrics_endpoint():
    \"\"\"Test API metrics endpoint.\"\"\"
    response = requests.get("{api_info.get('base_url', 'https://api.example.com/v1')}/metrics")
    assert response.status_code == 200
    
    metrics_data = response.json()
    assert "requests_total" in metrics_data
    assert "response_time_avg" in metrics_data
    assert "error_rate" in metrics_data
```

---

**Last Updated**: {api_info.get('last_updated', '2024-01-01')}
**API Version**: {api_info.get('version', '1.0.0')}
"""

        return TestDocumentation(
            title="API Documentation",
            content=content,
            file_path="docs/API.md",
            doc_type="api_docs"
        )

    def _format_authentication(self, auth_info: Dict[str, Any]) -> str:
        """Format authentication information."""
        if not auth_info:
            return "No authentication required."
        
        auth_type = auth_info.get('type', 'Bearer Token')
        description = auth_info.get('description', '')
        
        return f"""
**Type**: {auth_type}

**Description**: {description}

**Usage**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \\
     "{auth_info.get('base_url', 'https://api.example.com/v1')}/endpoint"
```
"""

    def _format_rate_limiting(self, rate_info: Dict[str, Any]) -> str:
        """Format rate limiting information."""
        if not rate_info:
            return "No rate limiting applied."
        
        limit = rate_info.get('limit', '100')
        period = rate_info.get('period', 'hour')
        
        return f"""
**Limit**: {limit} requests per {period}

**Headers**:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

**Example**:
```
X-RateLimit-Limit: {limit}
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```
"""

    def _format_endpoints(self, endpoints: list) -> str:
        """Format endpoints documentation."""
        if not endpoints:
            return "No endpoints documented."
        
        formatted = []
        for endpoint in endpoints:
            method = endpoint.get('method', 'GET')
            path = endpoint.get('path', '/')
            description = endpoint.get('description', '')
            
            formatted.append(f"""
### {method} {path}

{description}

**Parameters**:
{self._format_parameters(endpoint.get('parameters', []))}

**Response**:
```json
{endpoint.get('response', '{}')}
```

**Example**:
```python
def test_{endpoint.get('name', 'endpoint')}():
    response = requests.{method.lower()}("{endpoint.get('base_url', 'https://api.example.com/v1')}{path}")
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
```
""")
        
        return "\n".join(formatted)

    def _format_parameters(self, parameters: list) -> str:
        """Format parameters documentation."""
        if not parameters:
            return "No parameters required."
        
        formatted = []
        for param in parameters:
            name = param.get('name', '')
            param_type = param.get('type', 'string')
            required = param.get('required', False)
            description = param.get('description', '')
            
            required_text = "Required" if required else "Optional"
            formatted.append(f"- `{name}` ({param_type}, {required_text}): {description}")
        
        return "\n".join(formatted)

    def _format_error_codes(self, error_codes: Dict[int, str]) -> str:
        """Format error codes documentation."""
        if not error_codes:
            return "No specific error codes documented."
        
        formatted = []
        for code, description in error_codes.items():
            formatted.append(f"| {code} | {description} |")
        
        return f"""
| Code | Description |
|------|-------------|
{chr(10).join(formatted)}
"""

    def _format_testing_examples(self, examples: list) -> str:
        """Format testing examples."""
        if not examples:
            return "No testing examples provided."
        
        formatted = []
        for example in examples:
            name = example.get('name', 'Example')
            description = example.get('description', '')
            code = example.get('code', '')
            
            formatted.append(f"""
### {name}

{description}

```python
{code}
```
""")
        
        return "\n".join(formatted)