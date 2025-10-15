"""
Core CLI commands for test generation and analysis.
"""

import click
from .cli_commands import (
    generate_command, analyze_command, init_config_command, info_command
)


@click.command()
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


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(source, verbose):
    """Analyze code structure and dependencies."""
    analyze_command(source, verbose)


@click.command()
@click.option('--config-path', type=click.Path(), help='Path to save configuration file')
@click.option('--interactive', '-i', is_flag=True, help='Interactive configuration setup')
def init_config(config_path, interactive):
    """Initialize configuration file."""
    init_config_command(config_path, interactive)


@click.command()
def info():
    """Show information about the test generator."""
    info_command()
