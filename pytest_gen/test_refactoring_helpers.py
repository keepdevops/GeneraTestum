"""
Test refactoring and optimization automation helpers.
"""

import click
from .auto_test_runner import AutoTestRunner
from .auto_refactoring import AutoRefactoringAnalyzer
from .auto_performance_testing import AutoPerformanceTesting
from .auto_test_optimizer import AutoTestOptimizer


class TestRefactoringHelpers:
    """Helper functions for test refactoring and optimization."""
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
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
