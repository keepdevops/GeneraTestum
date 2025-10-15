"""
Integration test analyzer for API relationships.
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from .integration_test_models import APIRelationship, APIEndpoint, WorkflowStep, APIAnalysisResult


class APIRelationshipAnalyzer:
    """Analyzes API code to identify endpoint relationships."""

    def __init__(self):
        self.relationship_patterns = {
            'create_then_get': [
                ('POST', 'GET'),
                ('PUT', 'GET'),
                ('PATCH', 'GET')
            ],
            'create_then_update': [
                ('POST', 'PUT'),
                ('POST', 'PATCH'),
                ('PUT', 'PATCH')
            ],
            'create_then_delete': [
                ('POST', 'DELETE'),
                ('PUT', 'DELETE'),
                ('PATCH', 'DELETE')
            ],
            'dependency_chain': [
                ('GET', 'POST'),
                ('POST', 'PUT'),
                ('PUT', 'DELETE')
            ]
        }
        
        self.endpoint_patterns = {
            'flask': [
                r'@app\.route\s*\(\s*["\']([^"\']+)["\']',
                r'@.*\.route\s*\(\s*["\']([^"\']+)["\']'
            ],
            'fastapi': [
                r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                r'@.*\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
            ],
            'django': [
                r'path\s*\(\s*["\']([^"\']+)["\']',
                r'url\s*\(\s*["\']([^"\']+)["\']'
            ]
        }

    def analyze_api_file(self, file_path: str) -> List[APIEndpoint]:
        """Analyze an API file to extract endpoints."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception:
            return []
        
        endpoints = []
        
        # Detect framework and extract endpoints
        framework = self._detect_framework(source_code)
        if framework:
            endpoints = self._extract_endpoints(source_code, framework, file_path)
        
        return endpoints

    def _detect_framework(self, source_code: str) -> Optional[str]:
        """Detect the web framework used."""
        framework_indicators = {
            'flask': ['from flask import', 'import flask', '@app.route'],
            'fastapi': ['from fastapi import', 'import fastapi', '@app.get', '@app.post'],
            'django': ['from django import', 'import django', 'path(', 'url('],
            'tornado': ['from tornado import', 'import tornado', 'class.*Handler'],
            'bottle': ['from bottle import', 'import bottle', '@route']
        }
        
        for framework, indicators in framework_indicators.items():
            if any(indicator in source_code for indicator in indicators):
                return framework
        
        return None

    def _extract_endpoints(self, source_code: str, framework: str, file_path: str) -> List[APIEndpoint]:
        """Extract API endpoints from source code."""
        endpoints = []
        
        if framework == 'flask':
            endpoints = self._extract_flask_endpoints(source_code, file_path)
        elif framework == 'fastapi':
            endpoints = self._extract_fastapi_endpoints(source_code, file_path)
        elif framework == 'django':
            endpoints = self._extract_django_endpoints(source_code, file_path)
        
        return endpoints

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

    def analyze_relationships(self, endpoints: List[APIEndpoint]) -> List[APIRelationship]:
        """Analyze relationships between endpoints."""
        relationships = []
        
        # Group endpoints by base path
        endpoint_groups = {}
        for endpoint in endpoints:
            base_path = endpoint.path.split('/')[1] if '/' in endpoint.path else endpoint.path
            if base_path not in endpoint_groups:
                endpoint_groups[base_path] = []
            endpoint_groups[base_path].append(endpoint)
        
        # Analyze relationships within each group
        for group_endpoints in endpoint_groups.values():
            group_relationships = self._analyze_group_relationships(group_endpoints)
            relationships.extend(group_relationships)
        
        # Analyze cross-group relationships
        cross_relationships = self._analyze_cross_group_relationships(endpoint_groups)
        relationships.extend(cross_relationships)
        
        return relationships

    def _analyze_group_relationships(self, endpoints: List[APIEndpoint]) -> List[APIRelationship]:
        """Analyze relationships within a group of endpoints."""
        relationships = []
        
        for i, source in enumerate(endpoints):
            for j, target in enumerate(endpoints):
                if i != j:
                    relationship = self._determine_relationship(source, target)
                    if relationship:
                        relationships.append(relationship)
        
        return relationships

    def _determine_relationship(self, source: APIEndpoint, target: APIEndpoint) -> Optional[APIRelationship]:
        """Determine relationship between two endpoints."""
        # Check for common relationship patterns
        for pattern_name, pattern_pairs in self.relationship_patterns.items():
            if (source.method, target.method) in pattern_pairs:
                return APIRelationship(
                    source_endpoint=f"{source.method} {source.path}",
                    target_endpoint=f"{target.method} {target.path}",
                    relationship_type=pattern_name,
                    data_flow=self._extract_data_flow(source, target),
                    conditions=[]
                )
        
        return None

    def _extract_data_flow(self, source: APIEndpoint, target: APIEndpoint) -> Dict[str, str]:
        """Extract data flow between endpoints."""
        data_flow = {}
        
        # Map response fields to request parameters
        for response_field in source.response_fields:
            for param in target.parameters:
                if response_field.lower() in param.lower() or param.lower() in response_field.lower():
                    data_flow[response_field] = param
        
        return data_flow

    def _analyze_cross_group_relationships(self, endpoint_groups: Dict[str, List[APIEndpoint]]) -> List[APIRelationship]:
        """Analyze relationships between different endpoint groups."""
        relationships = []
        
        group_names = list(endpoint_groups.keys())
        for i, source_group in enumerate(group_names):
            for j, target_group in enumerate(group_names):
                if i != j:
                    source_endpoints = endpoint_groups[source_group]
                    target_endpoints = endpoint_groups[target_group]
                    
                    for source in source_endpoints:
                        for target in target_endpoints:
                            relationship = self._determine_relationship(source, target)
                            if relationship:
                                relationships.append(relationship)
        
        return relationships

    def generate_workflows(self, endpoints: List[APIEndpoint], 
                          relationships: List[APIRelationship]) -> List[List[WorkflowStep]]:
        """Generate integration workflows from endpoints and relationships."""
        workflows = []
        
        # Create workflows for each relationship
        for relationship in relationships:
            workflow = self._create_workflow_from_relationship(relationship, endpoints)
            if workflow:
                workflows.append(workflow)
        
        return workflows

    def _create_workflow_from_relationship(self, relationship: APIRelationship, 
                                         endpoints: List[APIEndpoint]) -> List[WorkflowStep]:
        """Create a workflow from a relationship."""
        workflow = []
        
        # Find source endpoint
        source_endpoint = None
        target_endpoint = None
        
        for endpoint in endpoints:
            if f"{endpoint.method} {endpoint.path}" == relationship.source_endpoint:
                source_endpoint = endpoint
            elif f"{endpoint.method} {endpoint.path}" == relationship.target_endpoint:
                target_endpoint = endpoint
        
        if source_endpoint and target_endpoint:
            # Create workflow steps
            source_step = WorkflowStep(
                step_number=1,
                endpoint=source_endpoint,
                expected_status=200,
                data_extraction=relationship.data_flow or {},
                assertions=[f"assert response.status_code == 200"]
            )
            
            target_step = WorkflowStep(
                step_number=2,
                endpoint=target_endpoint,
                expected_status=200,
                data_extraction={},
                assertions=[f"assert response.status_code == 200"]
            )
            
            workflow = [source_step, target_step]
        
        return workflow
