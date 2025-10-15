"""
Integration test generator - refactored for 200LOC limit.
"""

from typing import Dict, List, Any
from .integration_test_models import IntegrationTest, IntegrationTestSuite, APIRelationship, WorkflowStep
from .integration_test_templates import IntegrationTestTemplates


class IntegrationTestGenerator:
    """Generates integration tests based on API relationships."""

    def __init__(self):
        self.templates = IntegrationTestTemplates()

    def generate_integration_tests(self, relationships: List[APIRelationship], 
                                 workflows: List[List[WorkflowStep]]) -> IntegrationTestSuite:
        """Generate integration tests from relationships and workflows."""
        tests = []
        
        # Generate tests for workflows
        for i, workflow in enumerate(workflows):
            test = self.templates.generate_workflow_test(workflow, i)
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
        coverage_percentage = self._calculate_coverage_percentage(tests, endpoints_covered)
        
        return IntegrationTestSuite(
            tests=tests,
            total_tests=len(tests),
            endpoints_covered=endpoints_covered,
            test_file_content=test_file_content,
            coverage_percentage=coverage_percentage
        )

    def _generate_relationship_test(self, relationship: APIRelationship) -> IntegrationTest:
        """Generate test for a specific relationship."""
        if relationship.relationship_type == "data_flow":
            return self.templates.generate_data_flow_test(relationship)
        elif relationship.relationship_type == "dependency":
            return self.templates.generate_dependency_test(relationship)
        else:
            return self._generate_generic_relationship_test(relationship)

    def _generate_generic_relationship_test(self, relationship: APIRelationship) -> IntegrationTest:
        """Generate generic relationship test."""
        test_name = f"test_relationship_{relationship.source_endpoint.name}_{relationship.target_endpoint.name}"
        
        test_content = f'''def {test_name}():
    """Test relationship: {relationship.relationship_type}"""
    # Setup
    source_data = {{'id': 'test_123'}}
    
    # Execute source endpoint
    source_response = {relationship.source_endpoint.name}(source_data)
    assert source_response.status_code == 200
    
    # Execute target endpoint
    target_response = {relationship.target_endpoint.name}(source_response.data)
    assert target_response.status_code == 200
    
    # Verify relationship
    assert target_response.data['source_id'] == source_response.data['id']'''
        
        return IntegrationTest(
            test_name=test_name,
            test_type=relationship.relationship_type,
            description=f"Test relationship: {relationship.relationship_type}",
            test_content=test_content,
            endpoints=[relationship.source_endpoint, relationship.target_endpoint],
            dependencies=relationship.dependencies
        )

    def _generate_test_file_content(self, tests: List[IntegrationTest]) -> str:
        """Generate complete test file content."""
        if not tests:
            return "# No integration tests generated"
        
        # File header
        content = '''"""Integration tests for API relationships."""
import pytest
from unittest.mock import patch, MagicMock

'''
        
        # Add imports for all endpoints
        endpoints = set()
        for test in tests:
            endpoints.update([ep.name for ep in test.endpoints])
        
        if endpoints:
            content += f"# Import endpoints\n"
            for endpoint in sorted(endpoints):
                content += f"from api.{endpoint} import {endpoint}\n"
            content += "\n"
        
        # Add test functions
        for test in tests:
            content += test.test_content + "\n\n"
        
        return content

    def _calculate_endpoint_coverage(self, tests: List[IntegrationTest]) -> List[str]:
        """Calculate which endpoints are covered by tests."""
        covered = set()
        for test in tests:
            covered.update([ep.name for ep in test.endpoints])
        return list(covered)

    def _calculate_coverage_percentage(self, tests: List[IntegrationTest], endpoints_covered: List[str]) -> float:
        """Calculate coverage percentage."""
        if not tests:
            return 0.0
        
        all_endpoints = set()
        for test in tests:
            all_endpoints.update([ep.name for ep in test.endpoints])
        
        if not all_endpoints:
            return 0.0
        
        return len(endpoints_covered) / len(all_endpoints) * 100

    def generate_test_summary(self, test_suite: IntegrationTestSuite) -> Dict[str, Any]:
        """Generate summary of integration tests."""
        return {
            "total_tests": test_suite.total_tests,
            "coverage_percentage": test_suite.coverage_percentage,
            "endpoints_covered": len(test_suite.endpoints_covered),
            "test_types": {
                "workflow": len([t for t in test_suite.tests if t.test_type == "workflow"]),
                "data_flow": len([t for t in test_suite.tests if t.test_type == "data_flow"]),
                "dependency": len([t for t in test_suite.tests if t.test_type == "dependency"])
            }
        }

    def validate_test_suite(self, test_suite: IntegrationTestSuite) -> Dict[str, Any]:
        """Validate generated test suite."""
        issues = []
        
        if test_suite.total_tests == 0:
            issues.append("No tests generated")
        
        if test_suite.coverage_percentage < 50:
            issues.append(f"Low coverage: {test_suite.coverage_percentage:.1f}%")
        
        # Check for duplicate test names
        test_names = [test.test_name for test in test_suite.tests]
        duplicates = set([name for name in test_names if test_names.count(name) > 1])
        if duplicates:
            issues.append(f"Duplicate test names: {', '.join(duplicates)}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": []
        }