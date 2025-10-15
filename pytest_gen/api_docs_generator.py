"""
API documentation generator.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation
from .api_docs_templates import APIDocsTemplates
from .api_docs_formatters import APIDocsFormatters


class APIDocsGenerator:
    """Generates API documentation."""

    def __init__(self):
        self.templates = APIDocsTemplates()
        self.formatters = APIDocsFormatters()

    def generate_api_documentation(self, api_info: Dict[str, Any]) -> TestDocumentation:
        """Generate API documentation."""
        base_url = api_info.get('base_url', 'https://api.example.com/v1')
        description = api_info.get('description', 'Comprehensive API documentation with examples and testing information.')
        
        # Format sections
        auth_section = self.formatters.format_authentication(api_info.get('authentication', {}))
        rate_limiting_section = self.formatters.format_rate_limiting(api_info.get('rate_limiting', {}))
        endpoints_section = self.formatters.format_endpoints(api_info.get('endpoints', []))
        error_codes_section = self.formatters.format_error_codes(api_info.get('error_codes', {}))
        testing_examples_section = self.formatters.format_testing_examples(api_info.get('examples', []))
        
        # Generate content
        content = self.templates.get_base_template().format(
            description=description,
            base_url=base_url,
            auth_section=auth_section,
            rate_limiting_section=rate_limiting_section,
            endpoints_section=endpoints_section,
            error_codes_section=error_codes_section,
            testing_examples_section=testing_examples_section
        )
        
        return TestDocumentation(
            title="API Documentation",
            content=content,
            file_path="docs/API.md",
            doc_type="api_docs"
        )

    def generate_minimal_api_docs(self, endpoints: list, base_url: str = "https://api.example.com/v1") -> TestDocumentation:
        """Generate minimal API documentation."""
        api_info = {
            'base_url': base_url,
            'description': 'Minimal API documentation with endpoint information.',
            'endpoints': endpoints,
            'authentication': {'type': 'API Key', 'description': 'Include API key in headers'},
            'rate_limiting': {'requests_per_minute': 60},
            'error_codes': {
                400: 'Bad Request',
                401: 'Unauthorized',
                404: 'Not Found',
                500: 'Internal Server Error'
            },
            'examples': []
        }
        
        return self.generate_api_documentation(api_info)

    def generate_comprehensive_api_docs(self, api_info: Dict[str, Any]) -> TestDocumentation:
        """Generate comprehensive API documentation with all sections."""
        # Ensure all required sections are present
        default_api_info = {
            'base_url': 'https://api.example.com/v1',
            'description': 'Comprehensive API documentation with examples and testing information.',
            'authentication': {
                'type': 'Bearer Token',
                'description': 'Include Bearer token in Authorization header',
                'header': 'Authorization: Bearer <token>'
            },
            'rate_limiting': {
                'requests_per_minute': 60,
                'requests_per_hour': 1000,
                'requests_per_day': 10000,
                'retry_after_seconds': 60
            },
            'endpoints': [],
            'error_codes': {
                400: 'Bad Request - Invalid parameters',
                401: 'Unauthorized - Invalid or missing authentication',
                403: 'Forbidden - Insufficient permissions',
                404: 'Not Found - Resource does not exist',
                429: 'Too Many Requests - Rate limit exceeded',
                500: 'Internal Server Error - Server error occurred'
            },
            'examples': [
                {
                    'name': 'Basic Authentication',
                    'description': 'Example of making an authenticated request',
                    'code': 'import requests\n\nheaders = {\'Authorization\': \'Bearer your_token\'}\nresponse = requests.get(\'https://api.example.com/v1/users\', headers=headers)'
                }
            ]
        }
        
        # Merge with provided info
        merged_info = {**default_api_info, **api_info}
        
        return self.generate_api_documentation(merged_info)