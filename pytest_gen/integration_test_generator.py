"""
Integration test generator.
"""

from typing import Dict, List, Any
from .integration_test_models import IntegrationTest, IntegrationTestSuite, APIRelationship, WorkflowStep


class IntegrationTestGenerator:
    """Generates integration tests based on API relationships."""

    def __init__(self):
        self.test_templates = {
            'workflow': self._generate_workflow_test,
            'data_flow': self._generate_data_flow_test,
            'dependency': self._generate_dependency_test
        }

    def generate_integration_tests(self, relationships: List[APIRelationship], 
                                 workflows: List[List[WorkflowStep]]) -> IntegrationTestSuite:
        """Generate integration tests from relationships and workflows."""
        tests = []
        
        # Generate tests for workflows
        for i, workflow in enumerate(workflows):
            test = self._generate_workflow_test(workflow, i)
            if test:
                tests.append(test)
        
        # Generate tests for relationships
        for relationship in relationships:
            test = self._generate_relationship_test(relationship)
            if test:
                tests.append(test)
        
        # Generate test file content
        test_file_content = self._generate_test_file_content(tests)
        
        # Calculate coverage
        endpoints_covered = self._calculate_endpoint_coverage(tests)
        coverage_percentage = len(endpoints_covered) / len(set().union(*[t.endpoints for t in tests])) * 100 if tests else 0
        
        return IntegrationTestSuite(
            tests=tests,
            total_tests=len(tests),
            endpoints_covered=endpoints_covered,
            test_file_content=test_file_content,
            coverage_percentage=coverage_percentage
        )

    def _generate_workflow_test(self, workflow: List[WorkflowStep], index: int) -> IntegrationTest:
        """Generate a workflow integration test."""
        if not workflow:
            return None
        
        test_name = f"test_integration_workflow_{index + 1}"
        endpoints = [f"{step.endpoint.method} {step.endpoint.path}" for step in workflow]
        
        test_code = f'''def {test_name}():
    \"\"\"Integration test for workflow: {' -> '.join(endpoints)}\"\"\"
    import pytest
    import requests
    
    base_url = "http://localhost:8000"
    session_data = {{}}
    
    # Step 1: {workflow[0].endpoint.method} {workflow[0].endpoint.path}'''
        
        # Generate steps
        for i, step in enumerate(workflow):
            if i == 0:
                # First step - create initial data
                test_code += f'''
    
    # Create initial data
    response1 = requests.{step.endpoint.method.lower()}(
        f"{{base_url}}{step.endpoint.path}",
        json={{test_data}}
    )
    assert response1.status_code == {step.expected_status}
    
    # Extract data for next step'''
                
                # Add data extraction
                if step.data_extraction:
                    for source_field, target_field in step.data_extraction.items():
                        test_code += f'''
    session_data["{target_field}"] = response1.json().get("{source_field}")'''
            else:
                # Subsequent steps
                test_code += f'''
    
    # Step {i + 1}: {step.endpoint.method} {step.endpoint.path}
    response{i + 1} = requests.{step.endpoint.method.lower()}(
        f"{{base_url}}{step.endpoint.path}",
        json={{session_data}}
    )
    assert response{i + 1}.status_code == {step.expected_status}'''
        
        # Add final assertions
        test_code += f'''
    
    # Verify workflow completion
    assert all([response1.status_code == 200, response{len(workflow)}.status_code == 200])
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=f"Integration test for workflow: {' -> '.join(endpoints)}",
            test_code=test_code,
            endpoints=endpoints,
            test_type='workflow'
        )

    def _generate_data_flow_test(self, relationship: APIRelationship) -> IntegrationTest:
        """Generate a data flow integration test."""
        test_name = f"test_data_flow_{relationship.source_endpoint.replace(' ', '_').replace('/', '_')}_to_{relationship.target_endpoint.replace(' ', '_').replace('/', '_')}"
        
        test_code = f'''def {test_name}():
    \"\"\"Test data flow from {relationship.source_endpoint} to {relationship.target_endpoint}.\"\"\"
    import pytest
    import requests
    
    base_url = "http://localhost:8000"
    
    # Step 1: Call source endpoint
    source_response = requests.{relationship.source_endpoint.split()[0].lower()}(
        f"{{base_url}}{relationship.source_endpoint.split()[1] if len(relationship.source_endpoint.split()) > 1 else '/'}",
        json={{test_data}}
    )
    assert source_response.status_code == 200
    
    # Extract data from source response'''
        
        # Add data extraction
        if relationship.data_flow:
            for source_field, target_field in relationship.data_flow.items():
                test_code += f'''
    {target_field} = source_response.json().get("{source_field}")'''
        
        test_code += f'''
    
    # Step 2: Call target endpoint with extracted data
    target_data = {{}}'''
        
        # Add data mapping
        if relationship.data_flow:
            for source_field, target_field in relationship.data_flow.items():
                test_code += f'''
    target_data["{target_field}"] = {target_field}'''
        
        test_code += f'''
    
    target_response = requests.{relationship.target_endpoint.split()[0].lower()}(
        f"{{base_url}}{relationship.target_endpoint.split()[1] if len(relationship.target_endpoint.split()) > 1 else '/'}",
        json=target_data
    )
    assert target_response.status_code == 200
    
    # Verify data flow
    assert target_response.json() is not None
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=f"Data flow test: {relationship.source_endpoint} -> {relationship.target_endpoint}",
            test_code=test_code,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            test_type='data_flow'
        )

    def _generate_dependency_test(self, relationship: APIRelationship) -> IntegrationTest:
        """Generate a dependency integration test."""
        test_name = f"test_dependency_{relationship.source_endpoint.replace(' ', '_').replace('/', '_')}_depends_on_{relationship.target_endpoint.replace(' ', '_').replace('/', '_')}"
        
        test_code = f'''def {test_name}():
    \"\"\"Test dependency: {relationship.source_endpoint} depends on {relationship.target_endpoint}.\"\"\"
    import pytest
    import requests
    
    base_url = "http://localhost:8000"
    
    # Test that source endpoint fails without dependency
    try:
        source_response = requests.{relationship.source_endpoint.split()[0].lower()}(
            f"{{base_url}}{relationship.source_endpoint.split()[1] if len(relationship.source_endpoint.split()) > 1 else '/'}",
            json={{test_data}}
        )
        # If it succeeds without dependency, that's unexpected
        assert source_response.status_code in [400, 404, 422]
    except requests.exceptions.RequestException:
        # Expected to fail without dependency
        pass
    
    # Step 1: Setup dependency
    dependency_response = requests.{relationship.target_endpoint.split()[0].lower()}(
        f"{{base_url}}{relationship.target_endpoint.split()[1] if len(relationship.target_endpoint.split()) > 1 else '/'}",
        json={{dependency_data}}
    )
    assert dependency_response.status_code in [200, 201]
    
    # Extract dependency data'''
        
        # Add dependency data extraction
        if relationship.data_flow:
            for source_field, target_field in relationship.data_flow.items():
                test_code += f'''
    {target_field} = dependency_response.json().get("{source_field}")'''
        
        test_code += f'''
    
    # Step 2: Test source endpoint with dependency
    source_data = {{}}'''
        
        # Add dependency data mapping
        if relationship.data_flow:
            for source_field, target_field in relationship.data_flow.items():
                test_code += f'''
    source_data["{target_field}"] = {target_field}'''
        
        test_code += f'''
    
    source_response = requests.{relationship.source_endpoint.split()[0].lower()}(
        f"{{base_url}}{relationship.source_endpoint.split()[1] if len(relationship.source_endpoint.split()) > 1 else '/'}",
        json=source_data
    )
    assert source_response.status_code == 200
    
    # Verify dependency is satisfied
    assert source_response.json() is not None
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=f"Dependency test: {relationship.source_endpoint} depends on {relationship.target_endpoint}",
            test_code=test_code,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            test_type='dependency'
        )

    def _generate_relationship_test(self, relationship: APIRelationship) -> IntegrationTest:
        """Generate a test for a specific relationship."""
        if relationship.relationship_type == 'data_flow':
            return self._generate_data_flow_test(relationship)
        elif relationship.relationship_type == 'dependency':
            return self._generate_dependency_test(relationship)
        else:
            # Default to workflow test
            return self._generate_workflow_test_from_relationship(relationship)

    def _generate_workflow_test_from_relationship(self, relationship: APIRelationship) -> IntegrationTest:
        """Generate a workflow test from a relationship."""
        test_name = f"test_workflow_{relationship.source_endpoint.replace(' ', '_').replace('/', '_')}_to_{relationship.target_endpoint.replace(' ', '_').replace('/', '_')}"
        
        test_code = f'''def {test_name}():
    \"\"\"Test workflow: {relationship.source_endpoint} -> {relationship.target_endpoint}.\"\"\"
    import pytest
    import requests
    
    base_url = "http://localhost:8000"
    
    # Step 1: Execute source endpoint
    source_response = requests.{relationship.source_endpoint.split()[0].lower()}(
        f"{{base_url}}{relationship.source_endpoint.split()[1] if len(relationship.source_endpoint.split()) > 1 else '/'}",
        json={{test_data}}
    )
    assert source_response.status_code == 200
    
    # Step 2: Execute target endpoint
    target_response = requests.{relationship.target_endpoint.split()[0].lower()}(
        f"{{base_url}}{relationship.target_endpoint.split()[1] if len(relationship.target_endpoint.split()) > 1 else '/'}",
        json={{test_data}}
    )
    assert target_response.status_code == 200
    
    # Verify workflow completion
    assert source_response.json() is not None
    assert target_response.json() is not None
'''
        
        return IntegrationTest(
            test_name=test_name,
            test_description=f"Workflow test: {relationship.source_endpoint} -> {relationship.target_endpoint}",
            test_code=test_code,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            test_type='workflow'
        )

    def _generate_test_file_content(self, tests: List[IntegrationTest]) -> str:
        """Generate complete test file content."""
        content = "# Integration tests for API endpoints\n\n"
        content += "import pytest\nimport requests\n\n"
        
        # Add test data fixtures
        content += '''@pytest.fixture
def test_data():
    """Test data for integration tests."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30
    }

@pytest.fixture
def dependency_data():
    """Dependency data for integration tests."""
    return {
        "id": 1,
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z"
    }

'''
        
        # Add tests
        for test in tests:
            content += test.test_code + "\n\n"
        
        return content

    def _calculate_endpoint_coverage(self, tests: List[IntegrationTest]) -> List[str]:
        """Calculate endpoint coverage from tests."""
        covered_endpoints = set()
        
        for test in tests:
            covered_endpoints.update(test.endpoints)
        
        return list(covered_endpoints)
