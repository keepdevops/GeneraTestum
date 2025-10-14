"""
API mock generation functionality.
"""

import requests
from typing import Dict, List, Any
from .mock_models import DependencyInfo, MockConfig


class APIMockGenerator:
    """Generates mocks for API dependencies."""

    def __init__(self):
        self.api_schemas = {}

    def generate_mock(self, dep: DependencyInfo, config: MockConfig) -> str:
        """Generate mock for API dependencies."""
        mock_code = []
        
        # Import statements
        mock_code.append("import json")
        mock_code.append("from unittest.mock import Mock, patch")
        mock_code.append("import requests")
        mock_code.append("")
        
        # Mock class definition
        mock_code.append(f"class {dep.name.title()}Mock:")
        mock_code.append(f'    """Mock for {dep.name} API."""')
        mock_code.append("")
        
        # Initialize with realistic data
        mock_code.append("    def __init__(self):")
        mock_code.append("        self.responses = {")
        
        if dep.url:
            # Try to fetch actual API schema
            schema = self._fetch_api_schema(dep.url)
            if schema:
                self.api_schemas[dep.name] = schema
                mock_code.append("            'get': self._generate_get_response(),")
                mock_code.append("            'post': self._generate_post_response(),")
                mock_code.append("            'put': self._generate_put_response(),")
                mock_code.append("            'delete': self._generate_delete_response(),")
            else:
                # Fallback to generic responses
                mock_code.extend(self._generate_generic_api_responses())
        else:
            mock_code.extend(self._generate_generic_api_responses())
        
        mock_code.append("        }")
        mock_code.append("")
        
        # HTTP method implementations
        for method in ['get', 'post', 'put', 'delete']:
            mock_code.extend(self._generate_http_method(dep.name, method, config))
        
        # Response generators
        if config.include_responses:
            mock_code.extend(self._generate_response_generators(dep, config))
        
        return "\n".join(mock_code)

    def _fetch_api_schema(self, url: str) -> Dict[str, Any]:
        """Fetch API schema from URL (OpenAPI/Swagger)."""
        try:
            # Try common schema endpoints
            schema_urls = [
                f"{url}/openapi.json",
                f"{url}/swagger.json",
                f"{url}/api/schema",
                f"{url}/docs/swagger.json"
            ]
            
            for schema_url in schema_urls:
                try:
                    response = requests.get(schema_url, timeout=5)
                    if response.status_code == 200:
                        return response.json()
                except:
                    continue
                    
        except Exception:
            pass
        
        return None

    def _generate_generic_api_responses(self) -> List[str]:
        """Generate generic API responses."""
        return [
            "            'get': {'status_code': 200, 'json': {'data': 'mock_data'}},",
            "            'post': {'status_code': 201, 'json': {'id': 1, 'status': 'created'}},",
            "            'put': {'status_code': 200, 'json': {'id': 1, 'status': 'updated'}},",
            "            'delete': {'status_code': 204, 'json': {'status': 'deleted'}},"
        ]

    def _generate_http_method(self, dep_name: str, method: str, config: MockConfig) -> List[str]:
        """Generate HTTP method implementation."""
        lines = []
        
        lines.append(f"    def {method}(self, url, *args, **kwargs):")
        lines.append(f'        """Mock {method.upper()} request."""')
        lines.append(f"        response = self.responses.get('{method}', {{'status_code': 200}})")
        
        if config.include_error_cases:
            lines.append("        # Simulate error cases occasionally")
            lines.append("        if kwargs.get('simulate_error'):")
            lines.append("            response = {'status_code': 500, 'json': {'error': 'Internal server error'}}")
        
        lines.append("        return Mock(**response)")
        lines.append("")
        
        return lines

    def _generate_response_generators(self, dep: DependencyInfo, config: MockConfig) -> List[str]:
        """Generate response data generators."""
        lines = []
        
        for method in ['get', 'post', 'put', 'delete']:
            lines.extend([
                f"    def _generate_{method}_response(self):",
                f'        """Generate mock {method.upper()} response."""',
                "        return {",
                f"            'status_code': {200 if method == 'get' else 201 if method == 'post' else 200},",
                "            'json': lambda: self._generate_sample_data()",
                "        }",
                ""
            ])
        
        lines.extend([
            "    def _generate_sample_data(self):",
            "        # Generate realistic sample data",
            "        return {",
            "            'id': 1,",
            "            'name': 'Sample Item',",
            "            'created_at': '2024-01-01T00:00:00Z'",
            "        }",
            ""
        ])
        
        return lines
