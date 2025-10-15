"""
API endpoint extraction from different frameworks.
"""

import ast
import re
from typing import Dict, List, Tuple, Optional
from .integration_test_models import APIEndpoint
from .api_pattern_detector import APIPatternDetector


class EndpointExtractor:
    """Extracts API endpoints from different web frameworks."""

    def __init__(self):
        self.pattern_detector = APIPatternDetector()

    def extract_endpoints(self, source_code: str, framework: str, file_path: str) -> List[APIEndpoint]:
        """Extract API endpoints from source code based on framework."""
        if framework == 'flask':
            return self._extract_flask_endpoints(source_code, file_path)
        elif framework == 'fastapi':
            return self._extract_fastapi_endpoints(source_code, file_path)
        elif framework == 'django':
            return self._extract_django_endpoints(source_code, file_path)
        else:
            return []

    def _extract_flask_endpoints(self, source_code: str, file_path: str) -> List[APIEndpoint]:
        """Extract Flask endpoints."""
        endpoints = []
        
        # Find route decorators
        route_pattern = r'@app\.route\s*\(\s*["\']([^"\']+)["\']'
        methods_pattern = r'methods\s*=\s*\[([^\]]+)\]'
        
        lines = source_code.split('\n')
        for i, line in enumerate(lines):
            route_match = re.search(route_pattern, line)
            if route_match:
                path = route_match.group(1)
                
                # Extract HTTP methods
                methods = ['GET']  # Default method
                methods_match = re.search(methods_pattern, line)
                if methods_match:
                    methods_str = methods_match.group(1)
                    methods = [m.strip().strip('"\'') for m in methods_str.split(',')]
                
                # Extract function name (next function definition)
                func_name = self._extract_function_name(lines, i)
                
                # Extract parameters and response fields
                parameters, response_fields = self._extract_function_details(lines, i, func_name)
                
                endpoint = APIEndpoint(
                    method=methods[0].upper(),
                    path=path,
                    parameters=parameters,
                    response_fields=response_fields,
                    dependencies=[]
                )
                endpoints.append(endpoint)
        
        return endpoints

    def _extract_fastapi_endpoints(self, source_code: str, file_path: str) -> List[APIEndpoint]:
        """Extract FastAPI endpoints."""
        endpoints = []
        
        # Find route decorators
        route_pattern = r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
        
        lines = source_code.split('\n')
        for i, line in enumerate(lines):
            route_match = re.search(route_pattern, line)
            if route_match:
                method = route_match.group(1).upper()
                path = route_match.group(2)
                
                # Extract function name
                func_name = self._extract_function_name(lines, i)
                
                # Extract parameters and response fields
                parameters, response_fields = self._extract_function_details(lines, i, func_name)
                
                endpoint = APIEndpoint(
                    method=method,
                    path=path,
                    parameters=parameters,
                    response_fields=response_fields,
                    dependencies=[]
                )
                endpoints.append(endpoint)
        
        return endpoints

    def _extract_django_endpoints(self, source_code: str, file_path: str) -> List[APIEndpoint]:
        """Extract Django endpoints."""
        endpoints = []
        
        # Find URL patterns
        url_pattern = r'path\s*\(\s*["\']([^"\']+)["\']'
        
        lines = source_code.split('\n')
        for i, line in enumerate(lines):
            url_match = re.search(url_pattern, line)
            if url_match:
                path = url_match.group(1)
                
                # Extract view function
                view_pattern = r'(\w+View|\w+\.as_view)'
                view_match = re.search(view_pattern, line)
                if view_match:
                    view_name = view_match.group(1)
                    
                    # Extract HTTP methods from view class
                    methods = self._extract_django_methods(lines, view_name)
                    
                    endpoint = APIEndpoint(
                        method=methods[0] if methods else 'GET',
                        path=path,
                        parameters=[],
                        response_fields=[],
                        dependencies=[]
                    )
                    endpoints.append(endpoint)
        
        return endpoints

    def _extract_function_name(self, lines: List[str], start_line: int) -> str:
        """Extract function name from lines starting at start_line."""
        for i in range(start_line + 1, min(start_line + 10, len(lines))):
            line = lines[i].strip()
            if line.startswith('def '):
                func_match = re.match(r'def\s+(\w+)', line)
                if func_match:
                    return func_match.group(1)
        return 'unknown_function'

    def _extract_function_details(self, lines: List[str], start_line: int, func_name: str) -> Tuple[List[str], List[str]]:
        """Extract function parameters and response fields."""
        parameters = []
        response_fields = []
        
        # Find function definition
        func_start = -1
        for i in range(start_line, min(start_line + 10, len(lines))):
            if f'def {func_name}' in lines[i]:
                func_start = i
                break
        
        if func_start == -1:
            return parameters, response_fields
        
        # Extract parameters from function signature
        func_line = lines[func_start]
        param_match = re.search(r'def\s+\w+\s*\(([^)]*)\)', func_line)
        if param_match:
            params_str = param_match.group(1)
            parameters = [p.strip() for p in params_str.split(',') if p.strip() and p.strip() != 'self']
        
        # Extract response fields from function body
        for i in range(func_start, min(func_start + 20, len(lines))):
            line = lines[i]
            # Look for return statements with dictionaries or JSON
            if 'return' in line and ('{' in line or 'jsonify' in line):
                # Extract field names from return statement
                field_matches = re.findall(r'["\'](\w+)["\']\s*:', line)
                response_fields.extend(field_matches)
        
        return parameters, response_fields

    def _extract_django_methods(self, lines: List[str], view_name: str) -> List[str]:
        """Extract HTTP methods from Django view class."""
        methods = []
        
        # Look for view class definition
        for i, line in enumerate(lines):
            if f'class {view_name}' in line:
                # Look for method definitions in the class
                for j in range(i, min(i + 20, len(lines))):
                    method_line = lines[j].strip()
                    if method_line.startswith('def '):
                        method_name = method_line.split('(')[0].replace('def ', '')
                        if method_name in ['get', 'post', 'put', 'delete', 'patch']:
                            methods.append(method_name.upper())
                break
        
        return methods
