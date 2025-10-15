"""
Test execution and coverage analysis automation helpers.
"""

import click
import os
from typing import Dict, Any
from .auto_test_runner import AutoTestRunner
from .auto_coverage_analyzer import AutoCoverageAnalyzer


class TestExecutionHelpers:
    """Helper functions for test execution and coverage analysis."""
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
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
        TestExecutionHelpers.run_automated_tests(test_path, with_coverage=True, timeout=300, output=test_output)
        
        # Run coverage analysis
        coverage_output = os.path.join(output_dir, 'coverage_analysis_report.txt')
        TestExecutionHelpers.analyze_coverage_gaps(source_path, test_path, min_coverage, coverage_output)
        
        # Run refactoring analysis if auto-fix is enabled
        if auto_fix:
            refactor_output = os.path.join(output_dir, 'refactoring_suggestions.txt')
            TestRefactoringHelpers.analyze_refactoring_suggestions(test_path, refactor_output)
            
            # Generate additional tests for coverage gaps
            analyzer = AutoCoverageAnalyzer({'min_coverage': min_coverage})
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
