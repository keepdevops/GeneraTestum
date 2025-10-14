"""
API test template.
Use this template for testing REST API endpoints.
"""

import pytest
import json
from {module_name} import app

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    """Provide authentication headers."""
    return {'Authorization': 'Bearer test-token'}

@pytest.fixture
def sample_data():
    """Provide sample data for API tests."""
    return {sample_data}

class Test{EndpointName}API:
    """Test cases for {endpoint_name} API endpoints."""

    def test_get_{endpoint_name}(self, client):
        """Test GET {endpoint_path} endpoint."""
        response = client.get('{endpoint_path}')
        assert response.status_code == {expected_status}
        assert '{expected_field}' in response.json()

    def test_get_{endpoint_name}_with_params(self, client):
        """Test GET {endpoint_path} with query parameters."""
        params = {query_params}
        response = client.get('{endpoint_path}', query_string=params)
        assert response.status_code == {expected_status}
        {response_assertions}

    def test_post_{endpoint_name}(self, client, sample_data):
        """Test POST {endpoint_path} endpoint."""
        response = client.post('{endpoint_path}', 
                             json=sample_data,
                             content_type='application/json')
        assert response.status_code == {expected_status}
        assert response.json()['{expected_field}'] == {expected_value}

    def test_post_{endpoint_name}_invalid_data(self, client):
        """Test POST {endpoint_path} with invalid data."""
        invalid_data = {invalid_data}
        response = client.post('{endpoint_path}', 
                             json=invalid_data,
                             content_type='application/json')
        assert response.status_code == 400
        assert 'error' in response.json()

    def test_put_{endpoint_name}(self, client, sample_data):
        """Test PUT {endpoint_path} endpoint."""
        response = client.put('{endpoint_path}', 
                            json=sample_data,
                            content_type='application/json')
        assert response.status_code == {expected_status}
        {response_assertions}

    def test_delete_{endpoint_name}(self, client):
        """Test DELETE {endpoint_path} endpoint."""
        response = client.delete('{endpoint_path}')
        assert response.status_code == {expected_status}

    def test_{endpoint_name}_authentication_required(self, client):
        """Test {endpoint_name} requires authentication."""
        response = client.get('{endpoint_path}')
        assert response.status_code == 401

    def test_{endpoint_name}_authenticated(self, client, auth_headers):
        """Test {endpoint_name} with authentication."""
        response = client.get('{endpoint_path}', headers=auth_headers)
        assert response.status_code == 200

    def test_{endpoint_name}_not_found(self, client):
        """Test {endpoint_name} returns 404 for non-existent resource."""
        response = client.get('{endpoint_path}')
        assert response.status_code == 404
        assert 'error' in response.json()

    def test_{endpoint_name}_method_not_allowed(self, client):
        """Test {endpoint_name} returns 405 for unsupported method."""
        response = client.patch('{endpoint_path}')
        assert response.status_code == 405

    # Performance tests
    def test_{endpoint_name}_performance(self, client):
        """Test {endpoint_name} performance."""
        import time
        start_time = time.time()
        response = client.get('{endpoint_path}')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < {max_response_time}  # seconds

    # Load testing
    @pytest.mark.parametrize("request_count", [1, 10, 100])
    def test_{endpoint_name}_load(self, client, request_count):
        """Test {endpoint_name} under load."""
        responses = []
        for _ in range(request_count):
            response = client.get('{endpoint_path}')
            responses.append(response)
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in responses)
