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

    def run_complete_integration_analysis(self, api_directory: str, output_file: str = "test_integration.py") -> Dict[str, Any]:
        """Run complete integration testing analysis."""
        # Analyze API files
        analysis_results = self.analyze_api_files(api_directory)
        
        if not analysis_results:
            return {
                'success': False,
                'message': 'No API files found for analysis',
                'test_suite': None,
                'summary': {}
            }
        
        # Generate integration tests
        test_suite = self.generate_integration_tests(analysis_results)
        
        # Save tests
        self.save_integration_tests(test_suite, output_file)
        
        # Generate summary
        summary = self._generate_summary(analysis_results, test_suite)
        
        return {
            'success': True,
            'message': 'Integration tests generated successfully',
            'test_suite': test_suite,
            'summary': summary
        }

    def _generate_summary(self, analysis_results: List[APIAnalysisResult], 
                         test_suite: IntegrationTestSuite) -> Dict[str, Any]:
        """Generate analysis summary."""
        total_endpoints = sum(len(result.endpoints) for result in analysis_results)
        total_relationships = sum(len(result.relationships) for result in analysis_results)
        total_workflows = sum(len(result.workflows) for result in analysis_results)
        
        # Analyze endpoint coverage
        covered_endpoints = test_suite.endpoints_covered
        coverage_percentage = test_suite.coverage_percentage
        
        # Analyze test types
        test_types = {}
        for test in test_suite.tests:
            test_types[test.test_type] = test_types.get(test.test_type, 0) + 1
        
        # Identify critical workflows
        critical_workflows = []
        for result in analysis_results:
            for workflow in result.workflows:
                if len(workflow) > 3:  # Workflows with more than 3 steps
                    critical_workflows.append([f"{step.endpoint.method} {step.endpoint.path}" for step in workflow])
        
        return {
            'total_endpoints': total_endpoints,
            'total_relationships': total_relationships,
            'total_workflows': total_workflows,
            'generated_tests': test_suite.total_tests,
            'endpoint_coverage': len(covered_endpoints),
            'coverage_percentage': coverage_percentage,
            'test_types': test_types,
            'critical_workflows': critical_workflows,
            'covered_endpoints': covered_endpoints
        }

    def generate_integration_report(self, summary: Dict[str, Any]) -> str:
        """Generate integration testing report."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔗 AUTOMATIC INTEGRATION TEST GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n📊 API ANALYSIS:")
        report_lines.append(f"  • Total Endpoints: {summary['total_endpoints']}")
        report_lines.append(f"  • Total Relationships: {summary['total_relationships']}")
        report_lines.append(f"  • Total Workflows: {summary['total_workflows']}")
        
        report_lines.append(f"\n🧪 GENERATED TESTS:")
        report_lines.append(f"  • Total Tests: {summary['generated_tests']}")
        report_lines.append(f"  • Endpoint Coverage: {summary['endpoint_coverage']}/{summary['total_endpoints']}")
        report_lines.append(f"  • Coverage Percentage: {summary['coverage_percentage']:.1f}%")
        
        report_lines.append(f"\n📋 TEST TYPES:")
        for test_type, count in summary['test_types'].items():
            report_lines.append(f"  • {test_type}: {count} tests")
        
        if summary['critical_workflows']:
            report_lines.append(f"\n🚨 CRITICAL WORKFLOWS ({len(summary['critical_workflows'])}):")
            for i, workflow in enumerate(summary['critical_workflows'][:5], 1):
                workflow_str = " -> ".join(workflow)
                report_lines.append(f"  {i}. {workflow_str}")
        
        report_lines.append(f"\n🎯 COVERED ENDPOINTS:")
        for endpoint in summary['covered_endpoints'][:10]:  # Show first 10
            report_lines.append(f"  • {endpoint}")
        
        if len(summary['covered_endpoints']) > 10:
            report_lines.append(f"  • ... and {len(summary['covered_endpoints']) - 10} more")
        
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        report_lines.append(f"  • Run integration tests in CI/CD pipeline")
        report_lines.append(f"  • Set up test data management strategy")
        report_lines.append(f"  • Implement API versioning tests")
        report_lines.append(f"  • Add performance testing for critical workflows")
        report_lines.append(f"  • Monitor test execution times")
        
        return "\n".join(report_lines)