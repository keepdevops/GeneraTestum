"""
Automation test helpers - refactored for 200LOC limit.
"""

import click
import os
from typing import Dict, Any
from .integration_helper_fix import analyze_integration_requirements
from .test_execution_helpers import TestExecutionHelpers
from .test_refactoring_helpers import TestRefactoringHelpers
from .project_automation_helpers import SecurityAnalysisHelpers, ProjectAutomationHelpers


def run_automated_tests(test_path: str, with_coverage: bool, timeout: int, output: str):
    """Run tests automatically with intelligent analysis."""
    TestExecutionHelpers.run_automated_tests(test_path, with_coverage, timeout, output)


def analyze_coverage_gaps(source_path: str, test_path: str, min_coverage: int, output: str):
    """Analyze code coverage and identify gaps."""
    TestExecutionHelpers.analyze_coverage_gaps(source_path, test_path, min_coverage, output)


def run_complete_analysis(source_path: str, test_path: str, min_coverage: int, 
                          auto_fix: bool, output_dir: str):
    """Run complete automated analysis with all features."""
    TestExecutionHelpers.run_complete_analysis(source_path, test_path, min_coverage, auto_fix, output_dir)


def analyze_refactoring_suggestions(test_path: str, output: str):
    """Analyze test failures and suggest code refactoring improvements."""
    return TestRefactoringHelpers.analyze_refactoring_suggestions(test_path, output)


def analyze_performance_requirements(source_file: str, output: str):
    """Analyze source file and generate performance tests."""
    return TestRefactoringHelpers.analyze_performance_requirements(source_file, output)


def analyze_security_requirements(source_file: str, output: str):
    """Analyze source file and generate security tests."""
    return SecurityAnalysisHelpers.analyze_security_requirements(source_file, output)


def generate_project_documentation(project_path: str, output_dir: str):
    """Generate comprehensive project documentation."""
    return ProjectAutomationHelpers.generate_project_documentation(project_path, output_dir)


def generate_cicd_pipelines(project_path: str, output_dir: str):
    """Generate comprehensive CI/CD pipeline configurations."""
    return ProjectAutomationHelpers.generate_cicd_pipelines(project_path, output_dir)


def analyze_test_optimization(test_directory: str, output: str):
    """Analyze test suite and generate optimization suggestions."""
    return TestRefactoringHelpers.analyze_test_optimization(test_directory, output)


def analyze_integration_requirements(source_file: str, output: str):
    """Analyze source file and generate integration tests."""
    click.echo(f"🔗 Running automatic integration test analysis...")
    click.echo(f"Source file: {source_file}")
    click.echo("")
    
    # Use the existing integration helper
    result = analyze_integration_requirements(source_file)
    
    # Generate report
    report = f"""
=== INTEGRATION TEST ANALYSIS REPORT ===

Source File: {source_file}
Analysis Date: {click.get_current_context().meta.get('timestamp', 'Unknown')}

INTEGRATION REQUIREMENTS FOUND:
{result.get('requirements', 'No integration requirements found')}

SUGGESTED INTEGRATION TESTS:
{result.get('suggestions', 'No integration test suggestions')}

RECOMMENDATIONS:
{result.get('recommendations', 'No specific recommendations')}
"""
    
    click.echo(report)
    
    # Save detailed report if requested
    if output:
        with open(output, 'w') as f:
            f.write(report)
        click.echo(f"\n📄 Integration analysis saved to: {output}")
    
    return result


def run_all_automation_analyses(source_path: str, test_path: str, output_dir: str):
    """Run all available automation analyses."""
    click.echo(f"🚀 Running comprehensive automation analysis suite...")
    click.echo(f"Source path: {source_path}")
    click.echo(f"Test path: {test_path}")
    click.echo(f"Output directory: {output_dir}")
    click.echo("")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run all analyses
    analyses = [
        ("Test Execution", lambda: run_automated_tests(test_path, True, 300, os.path.join(output_dir, 'test_execution.txt'))),
        ("Coverage Analysis", lambda: analyze_coverage_gaps(source_path, test_path, 80, os.path.join(output_dir, 'coverage.txt'))),
        ("Refactoring Analysis", lambda: analyze_refactoring_suggestions(test_path, os.path.join(output_dir, 'refactoring.txt'))),
        ("Performance Analysis", lambda: analyze_performance_requirements(source_path, os.path.join(output_dir, 'performance.txt'))),
        ("Security Analysis", lambda: analyze_security_requirements(source_path, os.path.join(output_dir, 'security.txt'))),
        ("Test Optimization", lambda: analyze_test_optimization(test_path, os.path.join(output_dir, 'optimization.txt'))),
        ("Integration Analysis", lambda: analyze_integration_requirements(source_path, os.path.join(output_dir, 'integration.txt'))),
        ("Documentation Generation", lambda: generate_project_documentation(source_path, os.path.join(output_dir, 'docs'))),
        ("CI/CD Generation", lambda: generate_cicd_pipelines(source_path, os.path.join(output_dir, 'cicd')))
    ]
    
    results = {}
    for analysis_name, analysis_func in analyses:
        try:
            click.echo(f"Running {analysis_name}...")
            result = analysis_func()
            results[analysis_name] = result
            click.echo(f"✅ {analysis_name} completed successfully")
        except Exception as e:
            click.echo(f"❌ {analysis_name} failed: {str(e)}")
            results[analysis_name] = None
    
    # Summary
    click.echo(f"\n🎉 Comprehensive analysis completed!")
    click.echo(f"📁 All reports saved to: {output_dir}")
    click.echo(f"📊 Analyses completed: {sum(1 for r in results.values() if r is not None)}/{len(analyses)}")
    
    return results