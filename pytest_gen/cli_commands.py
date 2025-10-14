"""
CLI command implementations for pytest code generator.
"""

import click
import sys
from typing import Optional
from .generator_core import GeneratorCore
from .config import GeneratorConfig, MockLevel, TestCoverage, load_config_from_file


def generate_command(source: str, output: str, config: Optional[str], mock_level: str, 
                    coverage: str, include_private: bool, no_fixtures: bool, no_parametrize: bool,
                    max_lines: int, split_files: bool, dry_run: bool, verbose: bool):
    """Generate test files for Python code or API endpoints."""
    
    try:
        # Load configuration
        if config:
            generator_config = load_config_from_file(config)
        else:
            generator_config = GeneratorConfig()
        
        # Override config with CLI options
        generator_config.output_dir = output
        generator_config.mock_level = MockLevel(mock_level)
        generator_config.coverage_type = TestCoverage(coverage)
        generator_config.include_private_methods = include_private
        generator_config.generate_fixtures = not no_fixtures
        generator_config.generate_parametrize = not no_parametrize
        generator_config.max_lines_per_file = max_lines
        generator_config.split_large_tests = split_files
        
        if verbose:
            click.echo(f"Configuration:")
            click.echo(f"  Source: {source}")
            click.echo(f"  Output: {output}")
            click.echo(f"  Mock Level: {mock_level}")
            click.echo(f"  Coverage: {coverage}")
            click.echo(f"  Max Lines: {max_lines}")
            click.echo("")
        
        # Create generator
        generator = GeneratorCore(generator_config)
        
        if dry_run:
            # Analyze source without generating files
            analysis = generator.analyze_source(source)
            _display_analysis(analysis, verbose)
        else:
            # Generate tests
            click.echo(f"Generating tests for: {source}")
            test_files = generator.generate_tests(source)
            
            if test_files:
                click.echo(f"Generated {len(test_files)} test file(s):")
                for file_path in test_files:
                    click.echo(f"  {file_path}")
            else:
                click.echo("No tests generated.")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def analyze_command(source: str, verbose: bool):
    """Analyze source code and show what tests would be generated."""
    
    try:
        generator = GeneratorCore()
        analysis = generator.analyze_source(source)
        _display_analysis(analysis, verbose)
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def init_config_command(output: str, fmt: str):
    """Create a default configuration file."""
    
    try:
        config = GeneratorConfig()
        
        # Set file extension based on format
        if fmt == 'yaml' and not output.endswith(('.yaml', '.yml')):
            output += '.yaml'
        elif fmt == 'json' and not output.endswith('.json'):
            output += '.json'
        
        from .config import save_config_to_file
        save_config_to_file(config, output)
        
        click.echo(f"Created configuration file: {output}")
        click.echo("Edit this file to customize test generation settings.")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def info_command():
    """Show information about the pytest code generator."""
    click.echo("Pytest Code Generator v1.0.0")
    click.echo("")
    click.echo("Features:")
    click.echo("  • AST-based Python code analysis")
    click.echo("  • API endpoint detection (Flask, FastAPI, Django, Tornado)")
    click.echo("  • Automatic mock generation for external dependencies")
    click.echo("  • Pytest fixture generation")
    click.echo("  • Parametrized test cases")
    click.echo("  • Comprehensive test coverage (happy path, edge cases, error handling)")
    click.echo("  • CLI and library interfaces")
    click.echo("  • Configurable test generation")
    click.echo("")
    click.echo("Usage Examples:")
    click.echo("  pytest-gen generate my_module.py")
    click.echo("  pytest-gen generate src/ --output tests/")
    click.echo("  pytest-gen analyze my_api.py")
    click.echo("  pytest-gen init-config")


def _display_analysis(analysis: dict, verbose: bool):
    """Display analysis results."""
    if 'directory_path' in analysis:
        # Directory analysis
        click.echo(f"Directory: {analysis['directory_path']}")
        click.echo(f"Files found: {len(analysis['files'])}")
        click.echo(f"Total estimated tests: {analysis['total_estimated_tests']}")
        
        if verbose:
            for file_info in analysis['files']:
                click.echo(f"\n  {file_info['file_path']}:")
                click.echo(f"    Type: {file_info['file_type']}")
                click.echo(f"    Functions: {len(file_info['functions'])}")
                click.echo(f"    Classes: {len(file_info['classes'])}")
                click.echo(f"    Endpoints: {len(file_info['endpoints'])}")
                click.echo(f"    Estimated tests: {file_info['estimated_tests']}")
    
    else:
        # File analysis
        click.echo(f"File: {analysis['file_path']}")
        click.echo(f"Type: {analysis['file_type']}")
        click.echo(f"Functions: {len(analysis['functions'])}")
        click.echo(f"Classes: {len(analysis['classes'])}")
        click.echo(f"Endpoints: {len(analysis['endpoints'])}")
        click.echo(f"Estimated tests: {analysis['estimated_tests']}")
        
        if verbose:
            if analysis['functions']:
                click.echo("\nFunctions:")
                for func in analysis['functions']:
                    click.echo(f"  • {func['name']} ({func['parameters']} parameters)")
            
            if analysis['classes']:
                click.echo("\nClasses:")
                for cls in analysis['classes']:
                    click.echo(f"  • {cls['name']} ({cls['methods']} methods)")
            
            if analysis['endpoints']:
                click.echo("\nEndpoints:")
                for endpoint in analysis['endpoints']:
                    click.echo(f"  • {endpoint['name']} ({endpoint['method']} {endpoint['path']})")
            
            if analysis['dependencies']:
                click.echo(f"\nDependencies: {', '.join(analysis['dependencies'])}")
