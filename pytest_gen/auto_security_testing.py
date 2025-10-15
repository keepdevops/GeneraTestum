"""
Main automatic security testing generator.
"""

import os
from typing import Dict, List, Any
from .security_models import SecurityVulnerability, SecurityTest, SecurityTestSuite, SecurityAnalysisResult
from .security_analyzer import SecurityAnalyzer
from .security_test_generator import SecurityTestGenerator


class AutoSecurityTesting:
    """Main class for automatic security testing generation."""

    def __init__(self):
        self.analyzer = SecurityAnalyzer()
        self.test_generator = SecurityTestGenerator()

    def analyze_file(self, file_path: str) -> SecurityAnalysisResult:
        """Analyze a single file for security vulnerabilities."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            return SecurityAnalysisResult(
                vulnerabilities=[],
                total_vulnerabilities=0,
                critical_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                analysis_summary=f"Error reading file: {e}"
            )
        
        return self.analyzer.analyze_code(source_code, file_path)

    def analyze_project(self, project_path: str) -> List[SecurityAnalysisResult]:
        """Analyze entire project for security vulnerabilities."""
        results = []
        
        for root, dirs, files in os.walk(project_path):
            # Skip common directories that shouldn't be analyzed
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv', 'venv']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.php')):
                    file_path = os.path.join(root, file)
                    result = self.analyze_file(file_path)
                    if result.total_vulnerabilities > 0:
                        results.append(result)
        
        return results

    def generate_security_tests(self, vulnerabilities: List[SecurityVulnerability]) -> SecurityTestSuite:
        """Generate security tests for vulnerabilities."""
        return self.test_generator.generate_security_tests(vulnerabilities)

    def save_security_tests(self, test_suite: SecurityTestSuite, output_file: str = "test_security.py"):
        """Save security tests to file."""
        with open(output_file, 'w') as f:
            f.write(test_suite.test_file_content)
        print(f"Generated security tests: {output_file}")

    def generate_security_report(self, analysis_results: List[SecurityAnalysisResult]) -> str:
        """Generate comprehensive security analysis report."""
        total_vulnerabilities = sum(result.total_vulnerabilities for result in analysis_results)
        total_critical = sum(result.critical_count for result in analysis_results)
        total_high = sum(result.high_count for result in analysis_results)
        total_medium = sum(result.medium_count for result in analysis_results)
        total_low = sum(result.low_count for result in analysis_results)
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔒 AUTOMATIC SECURITY TEST GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n🚨 VULNERABILITIES FOUND: {total_vulnerabilities}")
        
        if total_critical > 0:
            report_lines.append(f"\n🚨 CRITICAL VULNERABILITIES ({total_critical}):")
            for result in analysis_results:
                if result.critical_count > 0:
                    for vuln in result.vulnerabilities:
                        if vuln.severity == 'critical':
                            report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.description}")
        
        if total_high > 0:
            report_lines.append(f"\n⚠️ HIGH VULNERABILITIES ({total_high}):")
            for result in analysis_results:
                if result.high_count > 0:
                    for vuln in result.vulnerabilities:
                        if vuln.severity == 'high':
                            report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.description}")
        
        if total_medium > 0:
            report_lines.append(f"\n⚠️ MEDIUM VULNERABILITIES ({total_medium}):")
            for result in analysis_results:
                if result.medium_count > 0:
                    for vuln in result.vulnerabilities:
                        if vuln.severity == 'medium':
                            report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.description}")
        
        if total_low > 0:
            report_lines.append(f"\nℹ️ LOW VULNERABILITIES ({total_low}):")
            for result in analysis_results:
                if result.low_count > 0:
                    for vuln in result.vulnerabilities:
                        if vuln.severity == 'low':
                            report_lines.append(f"  • {vuln.vulnerability_type}: {vuln.description}")
        
        report_lines.append(f"\n🧪 SECURITY TESTS GENERATED: {total_vulnerabilities}")
        
        # Group tests by vulnerability type
        vuln_types = {}
        for result in analysis_results:
            for vuln in result.vulnerabilities:
                vuln_type = vuln.vulnerability_type
                vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1
        
        for vuln_type, count in vuln_types.items():
            report_lines.append(f"\n🔒 {vuln_type.upper()} TESTS ({count}):")
            for result in analysis_results:
                for vuln in result.vulnerabilities:
                    if vuln.vulnerability_type == vuln_type:
                        report_lines.append(f"  • test_{vuln.affected_function}_{vuln_type}_protection")
                        report_lines.append(f"    Severity: {vuln.severity}")
        
        report_lines.append(f"\n💡 SECURITY RECOMMENDATIONS:")
        report_lines.append(f"  • Run security tests regularly in CI/CD pipeline")
        report_lines.append(f"  • Implement input validation and sanitization")
        report_lines.append(f"  • Use parameterized queries for database operations")
        report_lines.append(f"  • Escape output to prevent XSS attacks")
        report_lines.append(f"  • Use environment variables for secrets")
        report_lines.append(f"  • Implement proper authentication and authorization")
        report_lines.append(f"  • Keep dependencies updated and scan for vulnerabilities")
        
        return "\n".join(report_lines)

    def run_security_analysis(self, project_path: str, output_file: str = "test_security.py") -> str:
        """Run complete security analysis and generate tests."""
        # Analyze project
        analysis_results = self.analyze_project(project_path)
        
        if not analysis_results:
            return "No security vulnerabilities found in the project."
        
        # Collect all vulnerabilities
        all_vulnerabilities = []
        for result in analysis_results:
            all_vulnerabilities.extend(result.vulnerabilities)
        
        # Generate security tests
        test_suite = self.generate_security_tests(all_vulnerabilities)
        
        # Save tests
        self.save_security_tests(test_suite, output_file)
        
        # Generate report
        report = self.generate_security_report(analysis_results)
        
        return report