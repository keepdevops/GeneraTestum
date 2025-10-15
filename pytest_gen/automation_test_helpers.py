"""
Helper functions for test automation commands.
"""

import click
import os
from typing import Dict, Any
from .auto_test_runner import AutoTestRunner
from .auto_coverage_analyzer import AutoCoverageAnalyzer
from .auto_refactoring import AutoRefactoringAnalyzer
from .auto_performance_testing import AutoPerformanceTesting
from .integration_helper_fix import analyze_integration_requirements
from .auto_security_testing import AutoSecurityTesting
from .auto_documentation_generator import AutoDocumentationGenerator
from .auto_cicd_generator import AutoCICDGenerator
from .auto_test_optimizer import AutoTestOptimizer


def run_automated_tests(test_path: str, with_coverage: bool, timeout: int, output: str):
    """Run tests automatically with intelligent analysis."""
    runner = AutoTestRunner({'timeout': timeout})
    
    click.echo(f"🧪 Running automated test execution...")
    click.echo(f"Test path: {test_path}")
    click.echo(f"Coverage analysis: {'Enabled' if with_coverage else 'Disabled'}")
    click.echo(f"Timeout: {timeout}s")
    click.echo("")
    
    # Run tests
    suite_result = runner.run_tests(test_path, with_coverage=with_coverage, timeout=timeout)
    
    # Generate and display report
    report = runner.generate_report(suite_result)
    click.echo(report)
    
    # Generate fix suggestions
    suggestions = runner.auto_fix_suggestions(suite_result)
    if suggestions:
        click.echo("\n🔧 AUTO-FIX SUGGESTIONS:")
        for i, suggestion in enumerate(suggestions, 1):
            click.echo(f"  {i}. {suggestion}")
    
    # Save detailed report if requested
    if output:
        with open(output, 'w') as f:
            f.write(report)
        click.echo(f"\n📄 Detailed report saved to: {output}")


def analyze_coverage_gaps(source_path: str, test_path: str, min_coverage: int, output: str):
    """Analyze code coverage and identify gaps."""
    analyzer = AutoCoverageAnalyzer({'min_coverage': min_coverage})
    
    click.echo(f"📊 Running automated coverage analysis...")
    click.echo(f"Source path: {source_path}")
    click.echo(f"Test path: {test_path or 'Auto-detect'}")
    click.echo(f"Min coverage: {min_coverage}%")
    click.echo("")
    
    # Run coverage analysis
    coverage_report = analyzer.analyze_coverage(source_path, test_path)
    
    # Generate and display report
    report = analyzer.generate_coverage_report(coverage_report)
    click.echo(report)
    
    # Save detailed report if requested
    if output:
        with open(output, 'w') as f:
            f.write(report)
        click.echo(f"\n📄 Coverage report saved to: {output}")


def run_complete_analysis(source_path: str, test_path: str, min_coverage: int, 
                          auto_fix: bool, output_dir: str):
    """Run complete automated analysis with all features."""
    click.echo(f"🚀 Running complete automated analysis...")
    click.echo(f"Source path: {source_path}")
    click.echo(f"Test path: {test_path or 'Auto-detect'}")
    click.echo(f"Min coverage: {min_coverage}%")
    click.echo(f"Auto-fix: {'Enabled' if auto_fix else 'Disabled'}")
    click.echo(f"Output directory: {output_dir}")
    click.echo("")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run test execution
    test_output = os.path.join(output_dir, 'test_execution_report.txt')
    run_automated_tests(test_path, with_coverage=True, timeout=300, output=test_output)
    
    # Run coverage analysis
    coverage_output = os.path.join(output_dir, 'coverage_analysis_report.txt')
    analyze_coverage_gaps(source_path, test_path, min_coverage, coverage_output)
    
    # Run refactoring analysis if auto-fix is enabled
    if auto_fix:
        refactor_output = os.path.join(output_dir, 'refactoring_suggestions.txt')
        analyze_refactoring_suggestions(test_path, refactor_output)
        
        # Generate additional tests for coverage gaps
        coverage_report = analyzer.analyze_coverage(source_path, test_path)
        test_suggestions = analyzer.auto_generate_missing_tests(coverage_report.gaps)
        
        if test_suggestions:
            test_output_file = os.path.join(output_dir, 'suggested_tests.py')
            with open(test_output_file, 'w') as f:
                f.write("# Auto-generated test suggestions\n\n")
                for suggestion in test_suggestions:
                    f.write(suggestion)
                    f.write("\n\n")
            click.echo(f"📄 Suggested tests saved to: {test_output_file}")
    
    # Summary
    click.echo(f"\n✅ Complete analysis finished!")
    click.echo(f"📁 Reports saved to: {output_dir}")
    click.echo(f"  • Test execution: test_execution_report.txt")
    click.echo(f"  • Coverage analysis: coverage_analysis_report.txt")
    if auto_fix:
        click.echo(f"  • Refactoring suggestions: refactoring_suggestions.txt")
        click.echo(f"  • Suggested tests: suggested_tests.py")


def analyze_refactoring_suggestions(test_path: str, output: str):
    """Analyze test failures and suggest code refactoring improvements."""
    runner = AutoTestRunner()
    analyzer = AutoRefactoringAnalyzer()
    
    click.echo(f"🔧 Running automated refactoring analysis...")
    click.echo(f"Test path: {test_path}")
    click.echo("")
    
    # Run tests to get failure information
    suite_result = runner.run_tests(test_path)
    
    # Analyze failures for refactoring suggestions
    suggestions = analyzer.analyze_failures(suite_result)
    
    # Generate refactoring report
    report = analyzer.generate_refactoring_report(suggestions)
    click.echo(report)
    
    # Save detailed report if requested
    if output:
        with open(output, 'w') as f:
            f.write(report)
        click.echo(f"\n📄 Refactoring report saved to: {output}")
    
    # Return suggestions for further processing
    return suggestions


def analyze_performance_requirements(source_file: str, output: str):
    """Analyze source file and generate performance tests."""
    analyzer = AutoPerformanceTesting()
    
    click.echo(f"⚡ Running automatic performance test analysis...")
    click.echo(f"Source file: {source_file}")
    click.echo("")
    
    # Analyze and generate performance tests
    tests = analyzer.analyze_and_generate_tests(source_file)
    
    # Generate report
    report = analyzer.generate_performance_report(tests)
    click.echo(report)
    
    # Save detailed report if requested
    if output:
        with open(output, 'w') as f:
            f.write(report)
            if tests:
                f.write("\n\n" + "=" * 60 + "\n")
                f.write("GENERATED PERFORMANCE TESTS\n")
                f.write("=" * 60 + "\n")
                for test in tests:
                    f.write(f"\n# Performance tests for {test.function_name}\n")
                    f.write(test.test_code)
        click.echo(f"\n📄 Performance analysis saved to: {output}")
    
    return tests


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


def analyze_test_optimization(test_directory: str, output: str):
    """Analyze test suite and generate optimization suggestions."""
    optimizer = AutoTestOptimizer()
    
    click.echo(f"⚡ Running automatic test suite optimization analysis...")
    click.echo(f"Test directory: {test_directory}")
    click.echo("")
    
    # Analyze test suite
    report = optimizer.analyze_test_suite(test_directory)
    
    # Generate optimization report
    optimization_report = optimizer.generate_optimization_report(report)
    click.echo(optimization_report)
    
    # Generate optimized configuration
    config = optimizer.generate_optimized_test_config(report)
    
    # Save detailed report if requested
    if output:
        with open(output, 'w') as f:
            f.write(optimization_report)
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("OPTIMIZED TEST CONFIGURATION\n")
            f.write("=" * 60 + "\n")
            f.write(config)
        click.echo(f"\n📄 Optimization analysis saved to: {output}")
    
    return report
