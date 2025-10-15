"""
Workflow generation from API relationships.
"""

from typing import Dict, List, Optional
from .integration_test_models import APIRelationship, APIEndpoint, WorkflowStep, APIAnalysisResult


class WorkflowGenerator:
    """Generates workflows from API relationships."""

    def __init__(self):
        self.workflow_templates = {
            'create_then_get': {
                'name': 'Create and Retrieve',
                'description': 'Create a resource and then retrieve it',
                'steps': [
                    {'action': 'create', 'description': 'Create new resource'},
                    {'action': 'retrieve', 'description': 'Retrieve created resource'}
                ]
            },
            'create_then_update': {
                'name': 'Create and Update',
                'description': 'Create a resource and then update it',
                'steps': [
                    {'action': 'create', 'description': 'Create new resource'},
                    {'action': 'update', 'description': 'Update the resource'}
                ]
            },
            'create_then_delete': {
                'name': 'Create and Delete',
                'description': 'Create a resource and then delete it',
                'steps': [
                    {'action': 'create', 'description': 'Create new resource'},
                    {'action': 'delete', 'description': 'Delete the resource'}
                ]
            },
            'dependency_chain': {
                'name': 'Dependency Chain',
                'description': 'Sequential operations with dependencies',
                'steps': [
                    {'action': 'setup', 'description': 'Setup initial state'},
                    {'action': 'process', 'description': 'Process data'},
                    {'action': 'cleanup', 'description': 'Clean up resources'}
                ]
            }
        }

    def generate_workflows(self, endpoints: List[APIEndpoint], 
                          relationships: List[APIRelationship]) -> List[Dict[str, any]]:
        """Generate workflows from endpoints and relationships."""
        workflows = []
        
        # Group relationships by type
        relationship_groups = self._group_relationships_by_type(relationships)
        
        # Generate workflows for each relationship type
        for rel_type, rels in relationship_groups.items():
            for relationship in rels:
                workflow = self._create_workflow_from_relationship(relationship, rel_type)
                if workflow:
                    workflows.append(workflow)
        
        return workflows

    def _group_relationships_by_type(self, relationships: List[APIRelationship]) -> Dict[str, List[APIRelationship]]:
        """Group relationships by their type."""
        groups = {}
        for rel in relationships:
            if rel.relationship_type not in groups:
                groups[rel.relationship_type] = []
            groups[rel.relationship_type].append(rel)
        return groups

    def _create_workflow_from_relationship(self, relationship: APIRelationship,
                                         rel_type: str) -> Optional[Dict[str, any]]:
        """Create workflow from a relationship."""
        if rel_type not in self.workflow_templates:
            return None
        
        template = self.workflow_templates[rel_type]
        
        workflow = {
            'name': template['name'],
            'description': template['description'],
            'relationship_type': rel_type,
            'source_endpoint': relationship.source_endpoint,
            'target_endpoint': relationship.target_endpoint,
            'steps': [],
            'data_flow': relationship.data_flow,
            'conditions': relationship.conditions
        }
        
        # Create workflow steps
        for step_template in template['steps']:
            step = WorkflowStep(
                step_name=step_template['action'],
                endpoint=f"{relationship.source_endpoint} -> {relationship.target_endpoint}",
                expected_response="success",
                data_dependencies=list(relationship.data_flow.keys())
            )
            workflow['steps'].append(step)
        
        return workflow

    def generate_integration_test_cases(self, workflows: List[Dict[str, any]]) -> List[str]:
        """Generate integration test cases from workflows."""
        test_cases = []
        
        for workflow in workflows:
            test_case = self._generate_test_case_for_workflow(workflow)
            test_cases.append(test_case)
        
        return test_cases

    def _generate_test_case_for_workflow(self, workflow: Dict[str, any]) -> str:
        """Generate test case for a specific workflow."""
        workflow_name = workflow['name'].lower().replace(' ', '_')
        
        test_code = f"""
def test_{workflow_name}_workflow():
    \"\"\"Test {workflow['name']} workflow.\"\"\"
    
    # Test setup
    client = TestClient(app)
    
    # Workflow: {workflow['description']}
    # Source: {workflow['source_endpoint']}
    # Target: {workflow['target_endpoint']}
    
    # Step 1: Execute source endpoint
    source_response = client.{self._get_http_method(workflow['source_endpoint'])}(
        "{self._extract_path(workflow['source_endpoint'])}"
    )
    assert source_response.status_code == 200
    
    # Extract data for next step
    source_data = source_response.json()
    
    # Step 2: Execute target endpoint with data flow
    target_path = "{self._extract_path(workflow['target_endpoint'])}"
    target_response = client.{self._get_http_method(workflow['target_endpoint'])}(
        target_path,
        json=self._prepare_target_data(source_data, {workflow['data_flow']})
    )
    assert target_response.status_code == 200
    
    # Verify workflow completion
    assert target_response.json() is not None

def _prepare_target_data(source_data, data_flow):
    \"\"\"Prepare data for target endpoint based on data flow.\"\"\"
    target_data = {{}}
    for source_field, target_param in data_flow.items():
        if source_field in source_data:
            target_data[target_param] = source_data[source_field]
    return target_data
"""
        return test_code

    def _get_http_method(self, endpoint: str) -> str:
        """Extract HTTP method from endpoint string."""
        method = endpoint.split()[0].lower()
        return method

    def _extract_path(self, endpoint: str) -> str:
        """Extract path from endpoint string."""
        parts = endpoint.split()
        if len(parts) > 1:
            return parts[1]
        return '/'

    def create_analysis_result(self, endpoints: List[APIEndpoint], 
                              relationships: List[APIRelationship],
                              workflows: List[Dict[str, any]]) -> APIAnalysisResult:
        """Create comprehensive analysis result."""
        return APIAnalysisResult(
            endpoints=endpoints,
            relationships=relationships,
            workflows=workflows,
            coverage_metrics={
                'total_endpoints': len(endpoints),
                'endpoints_with_relationships': len(set(
                    rel.source_endpoint for rel in relationships
                )),
                'relationship_coverage': len(relationships) / max(len(endpoints), 1) * 100
            },
            recommendations=self._generate_recommendations(endpoints, relationships)
        )

    def _generate_recommendations(self, endpoints: List[APIEndpoint], 
                                 relationships: List[APIRelationship]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Check for isolated endpoints
        connected_endpoints = set()
        for rel in relationships:
            connected_endpoints.add(rel.source_endpoint)
            connected_endpoints.add(rel.target_endpoint)
        
        isolated_endpoints = [ep for ep in endpoints 
                             if f"{ep.method} {ep.path}" not in connected_endpoints]
        
        if isolated_endpoints:
            recommendations.append(
                f"Found {len(isolated_endpoints)} isolated endpoints that could benefit from integration tests"
            )
        
        # Check for missing CRUD operations
        crud_patterns = {'POST', 'GET', 'PUT', 'DELETE'}
        endpoint_methods = {ep.method for ep in endpoints}
        missing_methods = crud_patterns - endpoint_methods
        
        if missing_methods:
            recommendations.append(
                f"Consider adding missing HTTP methods: {', '.join(missing_methods)}"
            )
        
        return recommendations
