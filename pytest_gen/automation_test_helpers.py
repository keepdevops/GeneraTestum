"""
Helper functions for test automation commands.
"""

import click
import os
from typing import Dict, Any
from .auto_test_runner import AutoTestRunner
from .auto_coverage_analyzer import AutoCoverageAnalyzer


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
    
    # Analyze coverage
    report = analyzer.analyze_coverage(source_path, test_path)
    
    # Generate and display report
    coverage_report = analyzer.generate_coverage_report(report)
    click.echo(coverage_report)
    
    # Generate missing test suggestions
    if report.gaps:
        click.echo("\n🔧 AUTO-GENERATE MISSING TESTS:")
        test_suggestions = analyzer.auto_generate_missing_tests(report.gaps)
        for suggestion in test_suggestions[:5]:  # Show first 5
            click.echo(suggestion)
    
    # Save report if requested
    if output:
        with open(output, 'w') as f:
            f.write(coverage_report)
        click.echo(f"\n📄 Coverage report saved to: {output}")


def run_complete_analysis(source_path: str, test_path: str, min_coverage: int, 
                          auto_fix: bool, output_dir: str):
    """Run complete automated analysis with all features."""
    click.echo("🚀 Running complete automated analysis...")
    click.echo("=" * 60)
    
    # 1. Run tests
    click.echo("\n1️⃣  Running automated test execution...")
    runner = AutoTestRunner({'timeout': 300})
    suite_result = runner.run_tests(test_path, with_coverage=True)
    
    test_report = runner.generate_report(suite_result)
    click.echo(test_report)
    
    # 2. Analyze coverage
    click.echo("\n2️⃣  Analyzing coverage gaps...")
    analyzer = AutoCoverageAnalyzer({'min_coverage': min_coverage})
    coverage_report = analyzer.analyze_coverage(source_path, test_path)
    
    coverage_report_text = analyzer.generate_coverage_report(coverage_report)
    click.echo(coverage_report_text)
    
    # 3. Generate missing tests if requested
    if auto_fix and coverage_report.gaps:
        click.echo("\n3️⃣  Auto-generating missing tests...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        test_suggestions = analyzer.auto_generate_missing_tests(coverage_report.gaps)
        
        for i, suggestion in enumerate(test_suggestions[:10]):  # Limit to 10
            filename = f"auto_generated_test_{i+1}.py"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(suggestion)
            
            click.echo(f"  ✅ Generated: {filepath}")
    
    # 4. Generate smart mocks
    click.echo("\n4️⃣  Generating smart mocks...")
    from .smart_mock_generator import SmartMockGenerator
    from .mock_models import MockConfig
    
    generator = SmartMockGenerator()
    
    # Analyze main source file
    if os.path.isfile(source_path):
        with open(source_path, 'r') as f:
            code = f.read()
        
        dependencies = generator.analyze_dependencies(code, source_path)
        
        if dependencies:
            mock_config = MockConfig(mock_type='intelligent')
            mocks = generator.generate_smart_mocks(dependencies, mock_config)
            
            mock_file = os.path.join(output_dir, 'generated_mocks.py')
            with open(mock_file, 'w') as f:
                f.write("# Auto-generated Smart Mocks\n\n")
                for dep_name, mock_code in mocks.items():
                    f.write(f"# Mock for {dep_name}\n")
                    f.write(mock_code)
                    f.write("\n\n" + "="*50 + "\n\n")
            
            click.echo(f"  ✅ Generated mocks: {mock_file}")
    
    # Summary
    click.echo("\n🎉 COMPLETE ANALYSIS SUMMARY:")
    click.echo(f"  • Tests executed: {suite_result.total_tests}")
    click.echo(f"  • Coverage: {coverage_report.total_coverage:.1f}%")
    click.echo(f"  • Coverage gaps: {len(coverage_report.gaps)}")
    if auto_fix:
        click.echo(f"  • Auto-generated tests: {len(test_suggestions) if 'test_suggestions' in locals() else 0}")
    click.echo(f"  • Output directory: {output_dir}")
