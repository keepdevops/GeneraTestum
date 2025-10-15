"""
CLI commands for advanced automation features.
"""

import click
from .automation_helpers import (
    run_automated_tests, analyze_coverage_gaps, generate_smart_mocks,
    run_complete_analysis, analyze_refactoring_suggestions, analyze_performance_requirements,
    analyze_integration_requirements, analyze_security_requirements, generate_project_documentation,
    generate_cicd_pipelines, analyze_test_optimization
)


@click.group()
def automation():
    """Advanced automation features for test generation and analysis."""
    pass


@automation.command()
@click.argument('test_path')
@click.option('--with-coverage', is_flag=True, help='Include coverage analysis')
@click.option('--timeout', default=300, help='Test execution timeout in seconds')
@click.option('--output', '-o', help='Output file for detailed report')
def run_tests(test_path: str, with_coverage: bool, timeout: int, output: str):
    """Run tests automatically with intelligent analysis."""
    run_automated_tests(test_path, with_coverage, timeout, output)


@automation.command()
@click.argument('source_path')
@click.option('--test-path', help='Path to existing tests for coverage analysis')
@click.option('--min-coverage', default=80, help='Minimum coverage threshold')
@click.option('--output', '-o', help='Output file for coverage report')
def analyze_coverage(source_path: str, test_path: str, min_coverage: int, output: str):
    """Analyze code coverage and identify gaps."""
    analyze_coverage_gaps(source_path, test_path, min_coverage, output)


@automation.command()
@click.argument('source_file')
@click.option('--mock-type', type=click.Choice(['simple', 'realistic', 'intelligent']), 
              default='intelligent', help='Type of mock generation')
@click.option('--include-responses', is_flag=True, default=True, help='Include mock responses')
@click.option('--include-errors', is_flag=True, default=True, help='Include error case mocks')
@click.option('--output', '-o', help='Output file for generated mocks')
def generate_mocks(source_file: str, mock_type: str, include_responses: bool, 
                   include_errors: bool, output: str):
    """Generate intelligent mocks for dependencies."""
    generate_smart_mocks(source_file, mock_type, include_responses, include_errors, output)


@automation.command()
@click.argument('source_path')
@click.argument('test_path')
@click.option('--min-coverage', default=80, help='Minimum coverage threshold')
@click.option('--auto-fix', is_flag=True, help='Automatically generate missing tests')
@click.option('--output-dir', default='auto_generated_tests', help='Output directory for generated tests')
def complete_analysis(source_path: str, test_path: str, min_coverage: int, 
                      auto_fix: bool, output_dir: str):
    """Run complete automated analysis with all features."""
    run_complete_analysis(source_path, test_path, min_coverage, auto_fix, output_dir)


@automation.command()
@click.argument('test_path')
@click.option('--output', '-o', help='Output file for refactoring report')
def refactor(test_path: str, output: str):
    """Analyze test failures and suggest code refactoring improvements."""
    analyze_refactoring_suggestions(test_path, output)


@automation.command()
@click.argument('source_file')
@click.option('--output', '-o', help='Output file for performance analysis report')
def performance(source_file: str, output: str):
    """Analyze source file and generate performance tests."""
    analyze_performance_requirements(source_file, output)


@automation.command()
@click.argument('source_file')
@click.option('--output', '-o', help='Output file for integration test analysis report')
def integration(source_file: str, output: str):
    """Analyze API file and generate integration tests."""
    analyze_integration_requirements(source_file, output)


@automation.command()
@click.argument('source_file')
@click.option('--output', '-o', help='Output file for security test analysis report')
def security(source_file: str, output: str):
    """Analyze source file and generate security tests."""
    analyze_security_requirements(source_file, output)


@automation.command()
@click.argument('project_path')
@click.option('--output-dir', '-o', default='docs', help='Output directory for documentation')
def documentation(project_path: str, output_dir: str):
    """Generate comprehensive project documentation."""
    generate_project_documentation(project_path, output_dir)


@automation.command()
@click.argument('project_path')
@click.option('--output-dir', '-o', default='.github/workflows', help='Output directory for CI/CD configurations')
def cicd(project_path: str, output_dir: str):
    """Generate CI/CD pipeline configurations."""
    generate_cicd_pipelines(project_path, output_dir)


@automation.command()
@click.argument('test_directory')
@click.option('--output', '-o', help='Output file for optimization analysis report')
def optimize(test_directory: str, output: str):
    """Analyze and optimize test suite performance."""
    analyze_test_optimization(test_directory, output)


@automation.command()
def dashboard():
    """Launch automation dashboard (future feature)."""
    click.echo("🚧 Automation Dashboard")
    click.echo("This feature is under development.")
    click.echo("Planned features:")
    click.echo("  • Real-time test execution monitoring")
    click.echo("  • Coverage trend analysis")
    click.echo("  • Performance benchmarking")
    click.echo("  • Automated test optimization")


if __name__ == '__main__':
    automation()
