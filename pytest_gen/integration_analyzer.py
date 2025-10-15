"""
Integration test analyzer for API relationships.
"""

from typing import Dict, List, Any, Optional
from .integration_test_models import APIRelationship, APIEndpoint, APIAnalysisResult
from .api_pattern_detector import APIPatternDetector
from .endpoint_extractor import EndpointExtractor
from .relationship_analyzer import RelationshipAnalyzer
from .workflow_generator import WorkflowGenerator


class APIRelationshipAnalyzer:
    """Analyzes API code to identify endpoint relationships."""

    def __init__(self):
        self.pattern_detector = APIPatternDetector()
        self.endpoint_extractor = EndpointExtractor()
        self.relationship_analyzer = RelationshipAnalyzer()
        self.workflow_generator = WorkflowGenerator()

    def analyze_api_file(self, file_path: str) -> List[APIEndpoint]:
        """Analyze a single API file and extract endpoints."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Detect framework
            framework = self.pattern_detector.detect_framework(source_code)
            if not framework:
                return []
            
            # Extract endpoints
            endpoints = self.endpoint_extractor.extract_endpoints(
                source_code, framework, file_path
            )
            
            return endpoints
            
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
            return []

    def analyze_relationships(self, endpoints: List[APIEndpoint]) -> List[APIRelationship]:
        """Analyze relationships between endpoints."""
        return self.relationship_analyzer.analyze_relationships(endpoints)

    def generate_workflows(self, endpoints: List[APIEndpoint], 
                          relationships: List[APIRelationship]) -> List[Dict[str, any]]:
        """Generate workflows from endpoints and relationships."""
        return self.workflow_generator.generate_workflows(endpoints, relationships)

    def create_analysis_result(self, endpoints: List[APIEndpoint], 
                              relationships: List[APIRelationship],
                              workflows: List[Dict[str, any]]) -> APIAnalysisResult:
        """Create comprehensive analysis result."""
        return self.workflow_generator.create_analysis_result(
            endpoints, relationships, workflows
        )

    def analyze_multiple_files(self, file_paths: List[str]) -> APIAnalysisResult:
        """Analyze multiple API files and create comprehensive result."""
        all_endpoints = []
        
        # Analyze each file
        for file_path in file_paths:
            endpoints = self.analyze_api_file(file_path)
            all_endpoints.extend(endpoints)
        
        # Analyze relationships
        relationships = self.analyze_relationships(all_endpoints)
        
        # Generate workflows
        workflows = self.generate_workflows(all_endpoints, relationships)
        
        # Create analysis result
        return self.create_analysis_result(all_endpoints, relationships, workflows)

    def get_framework_support(self) -> List[str]:
        """Get list of supported frameworks."""
        return list(self.pattern_detector.framework_patterns.keys())

    def get_relationship_types(self) -> List[str]:
        """Get list of supported relationship types."""
        patterns = self.pattern_detector.get_relationship_patterns()
        return list(patterns.keys())

    def validate_endpoint(self, endpoint: APIEndpoint) -> Dict[str, Any]:
        """Validate an API endpoint."""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        if not endpoint.method:
            validation_result['errors'].append('Method is required')
            validation_result['valid'] = False
        
        if not endpoint.path:
            validation_result['errors'].append('Path is required')
            validation_result['valid'] = False
        
        # Validate HTTP method
        valid_methods = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}
        if endpoint.method and endpoint.method.upper() not in valid_methods:
            validation_result['errors'].append(f'Invalid HTTP method: {endpoint.method}')
            validation_result['valid'] = False
        
        # Check path format
        if endpoint.path and not endpoint.path.startswith('/'):
            validation_result['warnings'].append('Path should start with /')
        
        return validation_result