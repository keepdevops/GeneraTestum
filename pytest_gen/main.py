"""
CLI interface for pytest code generator.
"""

import click
from .cli_commands import (
    generate_command, analyze_command, init_config_command, info_command
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Pytest Code Generator - Generate comprehensive test cases from Python code."""
    pass


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--output', '-o', default='tests', help='Output directory for test files')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--mock-level', type=click.Choice(['none', 'basic', 'comprehensive']), 
              default='comprehensive', help='Mock generation level')
@click.option('--coverage', type=click.Choice(['happy_path', 'comprehensive', 'full']),
              default='comprehensive', help='Test coverage level')
@click.option('--include-private', is_flag=True, help='Include private methods in tests')
@click.option('--no-fixtures', is_flag=True, help='Disable fixture generation')
@click.option('--no-parametrize', is_flag=True, help='Disable parametrized tests')
@click.option('--max-lines', default=200, help='Maximum lines per test file')
@click.option('--split-files', is_flag=True, help='Split large test files')
@click.option('--dry-run', is_flag=True, help='Show what would be generated without creating files')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate(source, output, config, mock_level, coverage, include_private, 
             no_fixtures, no_parametrize, max_lines, split_files, dry_run, verbose):
    """Generate test files for Python code or API endpoints."""
    generate_command(source, output, config, mock_level, coverage, include_private,
                    no_fixtures, no_parametrize, max_lines, split_files, dry_run, verbose)


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(source, verbose):
    """Analyze source code and show what tests would be generated."""
    analyze_command(source, verbose)


@cli.command()
@click.option('--output', '-o', default='pytest_gen_config.json', help='Output config file path')
@click.option('--format', 'fmt', type=click.Choice(['json', 'yaml']), default='json', help='Config file format')
def init_config(output, fmt):
    """Create a default configuration file."""
    init_config_command(output, fmt)


@cli.command()
def info():
    """Show information about the pytest code generator."""
    info_command()


@cli.command()
@click.option('--port', default=5007, help='Port to serve the GUI on')
@click.option('--show/--no-show', default=True, help='Open browser automatically')
def gui(port: int, show: bool):
    """Launch the interactive Panel GUI."""
    try:
        from .panel_gui import launch_gui
        click.echo(f"Launching Panel GUI on port {port}...")
        click.echo("Close the browser tab or press Ctrl+C to stop the server.")
        launch_gui(port=port, show=show)
    except ImportError as e:
        click.echo(f"Error: Panel dependencies not installed. Please install with:")
        click.echo("pip install panel>=1.3.0")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error launching GUI: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli()