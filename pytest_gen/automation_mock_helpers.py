"""
Helper functions for mock automation commands.
"""

import click
from .smart_mock_generator import SmartMockGenerator
from .mock_models import MockConfig


def generate_smart_mocks(source_file: str, mock_type: str, include_responses: bool, 
                         include_errors: bool, output: str):
    """Generate intelligent mocks for dependencies."""
    generator = SmartMockGenerator()
    
    click.echo(f"🎭 Generating intelligent mocks...")
    click.echo(f"Source file: {source_file}")
    click.echo(f"Mock type: {mock_type}")
    click.echo("")
    
    # Read source file
    try:
        with open(source_file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        click.echo(f"❌ File not found: {source_file}")
        return
    
    # Analyze dependencies
    dependencies = generator.analyze_dependencies(code, source_file)
    
    if not dependencies:
        click.echo("ℹ️  No external dependencies found in the code.")
        return
    
    click.echo(f"🔍 Found {len(dependencies)} dependencies:")
    for dep in dependencies:
        click.echo(f"  • {dep.name} ({dep.type})")
    
    click.echo("")
    
    # Generate mocks
    mock_config = MockConfig(
        mock_type=mock_type,
        include_responses=include_responses,
        include_error_cases=include_errors
    )
    
    mocks = generator.generate_smart_mocks(dependencies, mock_config)
    
    # Display generated mocks
    click.echo("🎯 Generated mocks:")
    for dep_name, mock_code in mocks.items():
        click.echo(f"\n📝 Mock for {dep_name}:")
        click.echo("-" * 40)
        click.echo(mock_code[:500] + "..." if len(mock_code) > 500 else mock_code)
    
    # Save mocks if requested
    if output:
        with open(output, 'w') as f:
            f.write("# Generated Smart Mocks\n\n")
            for dep_name, mock_code in mocks.items():
                f.write(f"# Mock for {dep_name}\n")
                f.write(mock_code)
                f.write("\n\n" + "="*50 + "\n\n")
        click.echo(f"\n📄 Mocks saved to: {output}")
