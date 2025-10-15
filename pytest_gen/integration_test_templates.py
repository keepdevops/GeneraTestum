"""
Integration test templates and generators.
"""

from typing import Dict, List, Any, Optional
from .integration_test_models import IntegrationTest, APIRelationship, WorkflowStep


class IntegrationTestTemplates:
    """Templates for integration test generation."""
    
    def __init__(self):
        self.workflow_template = '''def test_workflow_{workflow_id}():
    """Test complete workflow: {workflow_name}"""
    # Setup
    {setup_code}
    
    # Execute workflow steps
    {workflow_steps}
    
    # Verify final state
    {verification_code}'''

        self.data_flow_template = '''def test_data_flow_{flow_id}():
    """Test data flow between {source} and {target}"""
    # Setup initial data
    {setup_code}
    
    # Execute data flow
    {flow_execution}
    
    # Verify data transformation
    {verification_code}'''

        self.dependency_template = '''def test_dependency_{dep_id}():
    """Test dependency relationship: {dependency_name}"""
    # Mock dependencies
    {mock_setup}
    
    # Execute main operation
    {main_execution}
    
    # Verify dependency calls
    {dependency_verification}'''

    def generate_workflow_test(self, workflow: List[WorkflowStep], workflow_id: int) -> Optional[IntegrationTest]:
        """Generate test for a complete workflow."""
        if not workflow:
            return None
        
        # Extract workflow information
        workflow_name = f"workflow_{workflow_id}"
        endpoints = [step.endpoint for step in workflow]
        
        # Generate setup code
        setup_code = self._generate_workflow_setup(workflow)
        
        # Generate workflow steps
        workflow_steps = self._generate_workflow_steps(workflow)
        
        # Generate verification
        verification_code = self._generate_workflow_verification(workflow)
        
        # Create test content
        test_content = self.workflow_template.format(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            setup_code=setup_code,
            workflow_steps=workflow_steps,
            verification_code=verification_code
        )
        
        return IntegrationTest(
            test_name=f"test_workflow_{workflow_id}",
            test_type="workflow",
            description=f"Test complete workflow: {workflow_name}",
            test_content=test_content,
            endpoints=endpoints,
            dependencies=self._extract_dependencies(workflow)
        )

    def generate_data_flow_test(self, relationship: APIRelationship) -> Optional[IntegrationTest]:
        """Generate test for data flow between endpoints."""
        if relationship.relationship_type != "data_flow":
            return None
        
        source_endpoint = relationship.source_endpoint
        target_endpoint = relationship.target_endpoint
        
        # Generate test content
        setup_code = f"# Setup data for {source_endpoint.name}\n    initial_data = {{'key': 'value'}}"
        
        flow_execution = f"""# Call source endpoint
    response1 = {source_endpoint.name}()
    
    # Transform data
    transformed_data = transform_data(response1.data)
    
    # Call target endpoint
    response2 = {target_endpoint.name}(transformed_data)"""
        
        verification_code = f"""# Verify data flow
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response2.data['source'] == response1.data['id']"""
        
        test_content = self.data_flow_template.format(
            flow_id=f"{source_endpoint.name}_{target_endpoint.name}",
            source=source_endpoint.name,
            target=target_endpoint.name,
            setup_code=setup_code,
            flow_execution=flow_execution,
            verification_code=verification_code
        )
        
        return IntegrationTest(
            test_name=f"test_data_flow_{source_endpoint.name}_{target_endpoint.name}",
            test_type="data_flow",
            description=f"Test data flow between {source_endpoint.name} and {target_endpoint.name}",
            test_content=test_content,
            endpoints=[source_endpoint, target_endpoint],
            dependencies=relationship.dependencies
        )

    def generate_dependency_test(self, relationship: APIRelationship) -> Optional[IntegrationTest]:
        """Generate test for dependency relationships."""
        if relationship.relationship_type != "dependency":
            return None
        
        main_endpoint = relationship.source_endpoint
        dependency_endpoint = relationship.target_endpoint
        
        # Generate test content
        mock_setup = f"""# Mock {dependency_endpoint.name}
    with patch('module.{dependency_endpoint.name}') as mock_dep:
        mock_dep.return_value = {{'status': 'success'}}"""
        
        main_execution = f"""# Call main endpoint
    response = {main_endpoint.name}()"""
        
        dependency_verification = f"""# Verify dependency was called
    mock_dep.assert_called_once()
    assert response.status_code == 200"""
        
        test_content = self.dependency_template.format(
            dep_id=f"{main_endpoint.name}_{dependency_endpoint.name}",
            dependency_name=f"{main_endpoint.name} -> {dependency_endpoint.name}",
            mock_setup=mock_setup,
            main_execution=main_execution,
            dependency_verification=dependency_verification
        )
        
        return IntegrationTest(
            test_name=f"test_dependency_{main_endpoint.name}_{dependency_endpoint.name}",
            test_type="dependency",
            description=f"Test dependency relationship: {main_endpoint.name} -> {dependency_endpoint.name}",
            test_content=test_content,
            endpoints=[main_endpoint, dependency_endpoint],
            dependencies=relationship.dependencies
        )

    def _generate_workflow_setup(self, workflow: List[WorkflowStep]) -> str:
        """Generate setup code for workflow."""
        return """# Initialize test data
    test_data = {'id': 'test_123', 'status': 'pending'}"""

    def _generate_workflow_steps(self, workflow: List[WorkflowStep]) -> str:
        """Generate workflow execution steps."""
        steps = []
        for i, step in enumerate(workflow):
            steps.append(f"    # Step {i+1}: {step.description}")
            steps.append(f"    response_{i} = {step.endpoint.name}()")
        
        return "\n".join(steps)

    def _generate_workflow_verification(self, workflow: List[WorkflowStep]) -> str:
        """Generate verification code for workflow."""
        return """# Verify workflow completion
    assert all_step_responses_successful
    assert final_state == 'completed'"""

    def _extract_dependencies(self, workflow: List[WorkflowStep]) -> List[str]:
        """Extract dependencies from workflow."""
        dependencies = set()
        for step in workflow:
            dependencies.update(step.dependencies)
        return list(dependencies)
