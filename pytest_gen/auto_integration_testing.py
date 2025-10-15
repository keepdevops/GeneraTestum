"""
Main automatic integration testing generator.
"""

import os
from typing import Dict, List, Any
from .integration_test_models import APIRelationship, IntegrationTest, IntegrationTestSuite, APIAnalysisResult
from .integration_analyzer import APIRelationshipAnalyzer
from .integration_test_generator import IntegrationTestGenerator


class AutoIntegrationTesting:
    """Main class for automatic integration testing generation."""

    def __init__(self):
        self.analyzer = APIRelationshipAnalyzer()
        self.generator = IntegrationTestGenerator()

    def analyze_api_files(self, directory: str) -> List[APIAnalysisResult]:
        """Analyze API files in a directory."""
        results = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and any(keyword in file.lower() for keyword in ['api', 'route', 'endpoint', 'view']):
                    file_path = os.path.join(root, file)
                    endpoints = self.analyzer.analyze_api_file(file_path)
                    
                    if endpoints:
                        relationships = self.analyzer.analyze_relationships(endpoints)
                        workflows = self.analyzer.generate_workflows(endpoints, relationships)
                        
                        result = APIAnalysisResult(
                            endpoints=endpoints,
                            relationships=relationships,
                            workflows=workflows,
                            coverage_analysis={}
                        )
                        results.append(result)
        
        return results

    def generate_integration_tests(self, analysis_results: List[APIAnalysisResult]) -> IntegrationTestSuite:
        """Generate integration tests from analysis results."""
        all_relationships = []
        all_workflows = []
        
        for result in analysis_results:
            all_relationships.extend(result.relationships)
            all_workflows.extend(result.workflows)
        
        return self.generator.generate_integration_tests(all_relationships, all_workflows)

    def save_integration_tests(self, test_suite: IntegrationTestSuite, output_file: str = "test_integration.py"):
        """Save integration tests to file."""
        with open(output_file, 'w') as f:
            f.write(test_suite.test_file_content)
        print(f"Generated integration tests: {output_file}")

    def generate_integration_report(self, summary: Dict[str, Any]) -> str:
        """Generate integration testing report."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔗 AUTOMATIC INTEGRATION TEST GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n📊 API ANALYSIS:")
        report_lines.append(f"  • Total Endpoints: {summary.get('total_endpoints', 0)}")
        report_lines.append(f"  • Total Relationships: {summary.get('total_relationships', 0)}")
        report_lines.append(f"  • Total Workflows: {summary.get('total_workflows', 0)}")
        
        report_lines.append(f"\n🧪 GENERATED TESTS:")
        report_lines.append(f"  • Total Tests: {summary.get('generated_tests', 0)}")
        report_lines.append(f"  • Endpoint Coverage: {summary.get('endpoint_coverage', 0)}")
        report_lines.append(f"  • Coverage Percentage: {summary.get('coverage_percentage', 0):.1f}%")
        
        return "\n".join(report_lines)