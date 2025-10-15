"""
Security analysis and project automation helpers.
"""

import click
from .auto_security_testing import AutoSecurityTesting
from .auto_documentation_generator import AutoDocumentationGenerator
from .auto_cicd_generator import AutoCICDGenerator


class SecurityAnalysisHelpers:
    """Helper functions for security analysis."""
    
    @staticmethod
    def analyze_security_requirements(source_file: str, output: str):
        """Analyze source file and generate security tests."""
        analyzer = AutoSecurityTesting()
        
        click.echo(f"🔒 Running automatic security test analysis...")
        click.echo(f"Source file: {source_file}")
        click.echo("")
        
        # Analyze file for vulnerabilities
        analysis_result = analyzer.analyze_file(source_file)
        
        # Generate security tests
        tests = analyzer.generate_security_tests(analysis_result.vulnerabilities)
        
        # Get vulnerabilities for reporting
        vulnerabilities = analysis_result.vulnerabilities
        
        # Generate report
        report = analyzer.generate_security_report([analysis_result])
        click.echo(report)
        
        # Save detailed report if requested
        if output:
            with open(output, 'w') as f:
                f.write(report)
                if tests:
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("GENERATED SECURITY TESTS\n")
                    f.write("=" * 60 + "\n")
                    for test in tests:
                        f.write(f"\n# Security tests for {test.vulnerability_type}\n")
                        f.write(test.test_code)
            click.echo(f"\n📄 Security analysis saved to: {output}")
        
        return tests


class ProjectAutomationHelpers:
    """Helper functions for project automation."""
    
    @staticmethod
    def generate_project_documentation(project_path: str, output_dir: str):
        """Generate comprehensive project documentation."""
        generator = AutoDocumentationGenerator()
        
        click.echo(f"📚 Running automatic documentation generation...")
        click.echo(f"Project path: {project_path}")
        click.echo(f"Output directory: {output_dir}")
        click.echo("")
        
        # Generate documentation
        docs = generator.generate_documentation(project_path, output_dir)
        
        # Generate report
        report = generator.generate_documentation_report(docs)
        click.echo(report)
        
        return docs
    
    @staticmethod
    def generate_cicd_pipelines(project_path: str, output_dir: str):
        """Generate comprehensive CI/CD pipeline configurations."""
        generator = AutoCICDGenerator()
        
        click.echo(f"🔧 Running automatic CI/CD pipeline generation...")
        click.echo(f"Project path: {project_path}")
        click.echo(f"Output directory: {output_dir}")
        click.echo("")
        
        # Generate CI/CD configurations
        configs = generator.generate_cicd_configs(project_path, output_dir)
        
        # Generate report
        report = generator.generate_cicd_report(configs)
        click.echo(report)
        
        return configs
