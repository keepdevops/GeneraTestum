"""
Automatic integration test generation based on API endpoint relationships.
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass


@dataclass
class APIRelationship:
    """Represents a relationship between API endpoints."""
    source_endpoint: str
    target_endpoint: str
    relationship_type: str  # 'dependency', 'sequence', 'data_flow'
    data_flow: Optional[Dict[str, str]] = None  # field mappings
    conditions: List[str] = None


@dataclass
class IntegrationTest:
    """Generated integration test."""
    test_name: str
    test_description: str
    test_code: str
    endpoints: List[str]
    test_type: str  # 'workflow', 'data_flow', 'dependency'


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
            'get_then_update': [
                ('GET', 'PUT'),
                ('GET', 'PATCH')
            ],
            'list_then_get': [
                ('GET', 'GET')  # list endpoint -> specific item endpoint
            ]
        }

    def analyze_api_relationships(self, api_info) -> List[APIRelationship]:
        """Analyze API endpoints to identify relationships."""
        relationships = []
        endpoints = api_info.endpoints if hasattr(api_info, 'endpoints') else []
        
        # Analyze endpoint relationships
        for i, endpoint1 in enumerate(endpoints):
            for j, endpoint2 in enumerate(endpoints[i+1:], i+1):
                relationship = self._analyze_endpoint_pair(endpoint1, endpoint2)
                if relationship:
                    relationships.append(relationship)
        
        # Analyze data flow relationships
        relationships.extend(self._analyze_data_flow_relationships(endpoints))
        
        return relationships

    def _analyze_endpoint_pair(self, endpoint1, endpoint2) -> Optional[APIRelationship]:
        """Analyze relationship between two endpoints."""
        path1 = getattr(endpoint1, 'path', '')
        path2 = getattr(endpoint2, 'path', '')
        method1 = getattr(endpoint1, 'method', '')
        method2 = getattr(endpoint2, 'method', '')
        
        # Check for common patterns
        for pattern_name, method_pairs in self.relationship_patterns.items():
            for method_pair in method_pairs:
                if (method1.upper() == method_pair[0] and 
                    method2.upper() == method_pair[1]):
                    
                    # Check if paths are related
                    if self._paths_are_related(path1, path2):
                        return APIRelationship(
                            source_endpoint=f"{method1} {path1}",
                            target_endpoint=f"{method2} {path2}",
                            relationship_type=pattern_name,
                            data_flow=self._infer_data_flow(endpoint1, endpoint2),
                            conditions=self._infer_conditions(endpoint1, endpoint2)
                        )
        
        return None

    def _paths_are_related(self, path1: str, path2: str) -> bool:
        """Check if two API paths are related."""
        # Extract resource names from paths
        path1_parts = [part.strip('/{}') for part in path1.split('/') if part]
        path2_parts = [part.strip('/{}') for part in path2.split('/') if part]
        
        # Check for common resource names
        common_resources = set(path1_parts) & set(path2_parts)
        if len(common_resources) > 0:
            return True
        
        # Check for hierarchical relationships
        if len(path1_parts) == 1 and len(path2_parts) == 2:
            if path1_parts[0] in path2_parts:
                return True
        
        # Check for ID-based relationships
        id_pattern = r'\{[^}]+\}'
        path1_ids = re.findall(id_pattern, path1)
        path2_ids = re.findall(id_pattern, path2)
        
        if path1_ids and path2_ids:
            # Check if same ID type is used
            for id1 in path1_ids:
                for id2 in path2_ids:
                    if id1 == id2:
                        return True
        
        return False

    def _infer_data_flow(self, endpoint1, endpoint2) -> Dict[str, str]:
        """Infer data flow between endpoints."""
        data_flow = {}
        
        # Extract response fields from first endpoint
        response_fields = self._extract_response_fields(endpoint1)
        
        # Extract request fields from second endpoint
        request_fields = self._extract_request_fields(endpoint2)
        
        # Map common fields
        for resp_field in response_fields:
            for req_field in request_fields:
                if self._fields_are_related(resp_field, req_field):
                    data_flow[resp_field] = req_field
        
        return data_flow

    def _extract_response_fields(self, endpoint) -> List[str]:
        """Extract potential response fields from endpoint."""
        # This is a simplified implementation
        # In a real scenario, you'd analyze the endpoint's response schema
        fields = []
        
        # Look for common response patterns
        if hasattr(endpoint, 'path'):
            path = endpoint.path.lower()
            if 'user' in path:
                fields.extend(['id', 'name', 'email'])
            elif 'post' in path:
                fields.extend(['id', 'title', 'content', 'user_id'])
            elif 'product' in path:
                fields.extend(['id', 'name', 'price', 'category'])
        
        return fields

    def _extract_request_fields(self, endpoint) -> List[str]:
        """Extract potential request fields from endpoint."""
        # This is a simplified implementation
        fields = []
        
        if hasattr(endpoint, 'path'):
            path = endpoint.path.lower()
            if 'user' in path:
                fields.extend(['name', 'email', 'password'])
            elif 'post' in path:
                fields.extend(['title', 'content', 'user_id'])
            elif 'product' in path:
                fields.extend(['name', 'price', 'category', 'description'])
        
        return fields

    def _fields_are_related(self, field1: str, field2: str) -> bool:
        """Check if two fields are related."""
        # Direct match
        if field1 == field2:
            return True
        
        # ID relationships
        if field1 == 'id' and field2.endswith('_id'):
            return True
        
        # Similar field names
        field1_clean = field1.lower().replace('_', '')
        field2_clean = field2.lower().replace('_', '')
        
        if field1_clean in field2_clean or field2_clean in field1_clean:
            return True
        
        return False

    def _infer_conditions(self, endpoint1, endpoint2) -> List[str]:
        """Infer conditions for the relationship."""
        conditions = []
        
        method1 = getattr(endpoint1, 'method', '').upper()
        method2 = getattr(endpoint2, 'method', '').upper()
        
        if method1 == 'POST' and method2 == 'GET':
            conditions.append("Creation must succeed before retrieval")
        elif method1 == 'POST' and method2 in ['PUT', 'PATCH']:
            conditions.append("Resource must exist before update")
        elif method1 == 'POST' and method2 == 'DELETE':
            conditions.append("Resource must exist before deletion")
        
        return conditions

    def _analyze_data_flow_relationships(self, endpoints) -> List[APIRelationship]:
        """Analyze data flow relationships between endpoints."""
        relationships = []
        
        # Look for endpoints that might share data
        for i, endpoint1 in enumerate(endpoints):
            for j, endpoint2 in enumerate(endpoints[i+1:], i+1):
                # Check if endpoints share common data patterns
                if self._endpoints_share_data(endpoint1, endpoint2):
                    relationship = APIRelationship(
                        source_endpoint=f"{getattr(endpoint1, 'method', '')} {getattr(endpoint1, 'path', '')}",
                        target_endpoint=f"{getattr(endpoint2, 'method', '')} {getattr(endpoint2, 'path', '')}",
                        relationship_type='data_flow',
                        data_flow=self._infer_data_flow(endpoint1, endpoint2)
                    )
                    relationships.append(relationship)
        
        return relationships

    def _endpoints_share_data(self, endpoint1, endpoint2) -> bool:
        """Check if two endpoints share data patterns."""
        path1 = getattr(endpoint1, 'path', '').lower()
        path2 = getattr(endpoint2, 'path', '').lower()
        
        # Check for common resource types
        common_resources = ['user', 'post', 'product', 'order', 'comment']
        
        for resource in common_resources:
            if resource in path1 and resource in path2:
                return True
        
        return False


class IntegrationTestGenerator:
    """Generates integration tests based on API relationships."""

    def __init__(self):
        self.test_templates = {
            'workflow': self._generate_workflow_test,
            'data_flow': self._generate_data_flow_test,
            'dependency': self._generate_dependency_test
        }

    def generate_integration_tests(self, relationships: List[APIRelationship], 
                                 api_info) -> List[IntegrationTest]:
        """Generate integration tests for API relationships."""
        tests = []
        
        # Group relationships by type
        workflow_relationships = [r for r in relationships if r.relationship_type in 
                                ['create_then_get', 'create_then_update', 'create_then_delete']]
        data_flow_relationships = [r for r in relationships if r.relationship_type == 'data_flow']
        dependency_relationships = [r for r in relationships if r.relationship_type == 'dependency']
        
        # Generate workflow tests
        for relationship in workflow_relationships:
            test = self._generate_workflow_test(relationship, api_info)
            if test:
                tests.append(test)
        
        # Generate data flow tests
        for relationship in data_flow_relationships:
            test = self._generate_data_flow_test(relationship, api_info)
            if test:
                tests.append(test)
        
        # Generate dependency tests
        for relationship in dependency_relationships:
            test = self._generate_dependency_test(relationship, api_info)
            if test:
                tests.append(test)
        
        return tests

    def _generate_workflow_test(self, relationship: APIRelationship, api_info) -> IntegrationTest:
        """Generate workflow integration test."""
        test_name = f"test_{relationship.relationship_type}_workflow"
        test_description = f"Test {relationship.relationship_type.replace('_', ' ')} workflow"
        
        # Parse endpoints
        source_method, source_path = relationship.source_endpoint.split(' ', 1)
        target_method, target_path = relationship.target_endpoint.split(' ', 1)
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import requests
    import pytest
    
    base_url = "http://localhost:5000"  # TODO: Configure base URL
    
    # Step 1: Execute source endpoint
    source_response = requests.{source_method.lower()}(
        f"{{base_url}}{source_path}",
        json={{}}  # TODO: Add appropriate request data
    )
    
    assert source_response.status_code == 200, \\
        f"Source endpoint failed: {{source_response.status_code}}"
    
    source_data = source_response.json()
    
    # Step 2: Extract data for target endpoint
    # TODO: Map source response data to target request data
    target_data = {{
        # Example mapping based on relationship:
        # "id": source_data.get("id"),
        # "name": source_data.get("name")
    }}
    
    # Step 3: Execute target endpoint
    target_response = requests.{target_method.lower()}(
        f"{{base_url}}{target_path}",
        json=target_data
    )
    
    assert target_response.status_code == 200, \\
        f"Target endpoint failed: {{target_response.status_code}}"
    
    target_result = target_response.json()
    
    # Step 4: Verify workflow completion
    assert target_result is not None, "Workflow did not complete successfully"
    
    # TODO: Add specific assertions based on expected workflow outcome
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            test_type='workflow'
        )

    def _generate_data_flow_test(self, relationship: APIRelationship, api_info) -> IntegrationTest:
        """Generate data flow integration test."""
        test_name = f"test_data_flow_{self._sanitize_endpoint_name(relationship.source_endpoint)}_to_{self._sanitize_endpoint_name(relationship.target_endpoint)}"
        test_description = f"Test data flow from {relationship.source_endpoint} to {relationship.target_endpoint}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import requests
    import pytest
    
    base_url = "http://localhost:5000"  # TODO: Configure base URL
    
    # Execute source endpoint to get data
    source_response = requests.get(f"{{base_url}}{relationship.source_endpoint.split(' ', 1)[1]}")
    assert source_response.status_code == 200
    
    source_data = source_response.json()
    
    # Verify data structure
    assert isinstance(source_data, dict), "Source data should be a dictionary"
    
    # Map data to target endpoint format
    target_data = {{}}
    {self._generate_data_mapping_code(relationship.data_flow)}
    
    # Execute target endpoint with mapped data
    target_response = requests.post(
        f"{{base_url}}{relationship.target_endpoint.split(' ', 1)[1]}",
        json=target_data
    )
    
    assert target_response.status_code in [200, 201], \\
        f"Target endpoint failed: {{target_response.status_code}}"
    
    # Verify data flow success
    target_result = target_response.json()
    assert target_result is not None
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            test_type='data_flow'
        )

    def _generate_dependency_test(self, relationship: APIRelationship, api_info) -> IntegrationTest:
        """Generate dependency integration test."""
        test_name = f"test_dependency_{self._sanitize_endpoint_name(relationship.source_endpoint)}_depends_on_{self._sanitize_endpoint_name(relationship.target_endpoint)}"
        test_description = f"Test dependency: {relationship.source_endpoint} depends on {relationship.target_endpoint}"
        
        test_code = f'''
def {test_name}():
    """{test_description}."""
    import requests
    import pytest
    
    base_url = "http://localhost:5000"  # TODO: Configure base URL
    
    # Test that source endpoint fails when dependency is not met
    source_response = requests.get(f"{{base_url}}{relationship.source_endpoint.split(' ', 1)[1]}")
    
    # Should fail if dependency is not satisfied
    assert source_response.status_code in [400, 404, 422], \\
        "Source endpoint should fail when dependency is not met"
    
    # Satisfy dependency
    dependency_response = requests.post(
        f"{{base_url}}{relationship.target_endpoint.split(' ', 1)[1]}",
        json={{}}  # TODO: Add appropriate data for dependency
    )
    
    assert dependency_response.status_code in [200, 201], \\
        f"Dependency endpoint failed: {{dependency_response.status_code}}"
    
    dependency_data = dependency_response.json()
    
    # Now source endpoint should work
    source_response = requests.get(f"{{base_url}}{relationship.source_endpoint.split(' ', 1)[1]}")
    assert source_response.status_code == 200, \\
        f"Source endpoint should work after dependency is satisfied: {{source_response.status_code}}"
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=test_description,
            test_code=test_code,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            test_type='dependency'
        )

    def _sanitize_endpoint_name(self, endpoint: str) -> str:
        """Sanitize endpoint name for use in test function names."""
        # Replace special characters with underscores
        sanitized = re.sub(r'[^\w]', '_', endpoint.lower())
        # Remove multiple underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        return sanitized.strip('_')

    def _generate_data_mapping_code(self, data_flow: Dict[str, str]) -> str:
        """Generate data mapping code."""
        if not data_flow:
            return "# TODO: Add data mapping logic"
        
        mapping_lines = []
        for source_field, target_field in data_flow.items():
            mapping_lines.append(f'    target_data["{target_field}"] = source_data.get("{source_field}")')
        
        return '\n'.join(mapping_lines)


class AutoIntegrationTesting:
    """Main class for automatic integration test generation."""

    def __init__(self):
        self.analyzer = APIRelationshipAnalyzer()
        self.generator = IntegrationTestGenerator()

    def analyze_and_generate_tests(self, api_info) -> List[IntegrationTest]:
        """Analyze API and generate integration tests."""
        # Analyze API relationships
        relationships = self.analyzer.analyze_api_relationships(api_info)
        
        if not relationships:
            return []
        
        # Generate integration tests
        tests = self.generator.generate_integration_tests(relationships, api_info)
        
        return tests

    def generate_integration_report(self, tests: List[IntegrationTest]) -> str:
        """Generate a report of integration tests."""
        if not tests:
            return "✅ No integration tests needed - no API relationships found."
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔗 AUTOMATIC INTEGRATION TEST GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n🎯 INTEGRATION TESTS GENERATED: {len(tests)}")
        
        # Group tests by type
        workflow_tests = [t for t in tests if t.test_type == 'workflow']
        data_flow_tests = [t for t in tests if t.test_type == 'data_flow']
        dependency_tests = [t for t in tests if t.test_type == 'dependency']
        
        if workflow_tests:
            report_lines.append(f"\n🔄 WORKFLOW TESTS ({len(workflow_tests)}):")
            for test in workflow_tests:
                report_lines.append(f"  • {test.test_name}")
                report_lines.append(f"    {test.test_description}")
        
        if data_flow_tests:
            report_lines.append(f"\n📊 DATA FLOW TESTS ({len(data_flow_tests)}):")
            for test in data_flow_tests:
                report_lines.append(f"  • {test.test_name}")
                report_lines.append(f"    {test.test_description}")
        
        if dependency_tests:
            report_lines.append(f"\n🔗 DEPENDENCY TESTS ({len(dependency_tests)}):")
            for test in dependency_tests:
                report_lines.append(f"  • {test.test_name}")
                report_lines.append(f"    {test.test_description}")
        
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        report_lines.append(f"  • Configure base URL and authentication for your API")
        report_lines.append(f"  • Add appropriate request data for each endpoint")
        report_lines.append(f"  • Customize assertions based on your API's behavior")
        report_lines.append(f"  • Run integration tests against a test environment")
        
        return "\n".join(report_lines)
