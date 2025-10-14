"""
CLI commands for managing the test library.
"""

import click
import json
from typing import Dict, Any
from .test_library_manager import TestLibraryManager


@click.group()
def library():
    """Manage test library patterns, templates, and examples."""
    pass


@library.command()
def list():
    """List all available patterns, templates, and examples."""
    manager = TestLibraryManager()
    stats = manager.get_library_stats()
    
    click.echo("📚 Test Library Contents:")
    click.echo(f"  Patterns: {stats['patterns']}")
    click.echo(f"  Templates: {stats['templates']}")
    click.echo(f"  Examples: {stats['examples']}")
    
    if stats['patterns'] > 0:
        click.echo("\n🔍 Available Patterns:")
        for pattern_name in manager.patterns.keys():
            click.echo(f"  - {pattern_name}")
    
    if stats['templates'] > 0:
        click.echo("\n📝 Available Templates:")
        for template_name in manager.templates.keys():
            click.echo(f"  - {template_name}")
    
    if stats['examples'] > 0:
        click.echo("\n💡 Available Examples:")
        for example_name in manager.examples.keys():
            click.echo(f"  - {example_name}")


@library.command()
@click.argument('pattern_name')
def show_pattern(pattern_name: str):
    """Show details of a specific pattern."""
    manager = TestLibraryManager()
    
    if pattern_name in manager.patterns:
        pattern = manager.patterns[pattern_name]
        click.echo(f"📋 Pattern: {pattern_name}")
        click.echo(f"Description: {pattern.get('description', 'No description')}")
        
        if 'test_cases' in pattern:
            click.echo("\nTest Cases:")
            for test_case in pattern['test_cases']:
                click.echo(f"  - {test_case.get('name', 'Unnamed')}: {test_case.get('description', 'No description')}")
        
        if 'examples' in pattern:
            click.echo("\nExamples:")
            for example_name, example_data in pattern['examples'].items():
                click.echo(f"  - {example_name}")
                if isinstance(example_data, dict) and 'template' in example_data:
                    click.echo(f"    Template: {example_data['template'][:100]}...")
    else:
        click.echo(f"❌ Pattern '{pattern_name}' not found")


@library.command()
@click.argument('template_name')
def show_template(template_name: str):
    """Show content of a specific template."""
    manager = TestLibraryManager()
    
    template = manager.get_template(template_name)
    if template:
        click.echo(f"📝 Template: {template_name}")
        click.echo("=" * 50)
        click.echo(template)
    else:
        click.echo(f"❌ Template '{template_name}' not found")


@library.command()
@click.argument('example_name')
def show_example(example_name: str):
    """Show content of a specific example."""
    manager = TestLibraryManager()
    
    example = manager.get_example(example_name)
    if example:
        click.echo(f"💡 Example: {example_name}")
        click.echo("=" * 50)
        click.echo(example)
    else:
        click.echo(f"❌ Example '{example_name}' not found")


@library.command()
@click.argument('function_name')
@click.option('--type', 'function_type', default='basic', help='Function type (basic, api, validation, etc.)')
def suggest(function_name: str, function_type: str):
    """Suggest test cases for a function based on patterns."""
    manager = TestLibraryManager()
    
    suggestions = manager.suggest_test_cases(function_name, function_type)
    
    if suggestions:
        click.echo(f"💡 Test suggestions for {function_name} ({function_type}):")
        for i, suggestion in enumerate(suggestions, 1):
            click.echo(f"  {i}. {suggestion}")
    else:
        click.echo(f"❌ No suggestions found for {function_name} ({function_type})")


@library.command()
@click.argument('template_name')
@click.argument('output_file')
@click.option('--function-name', help='Function name to substitute')
@click.option('--class-name', help='Class name to substitute')
@click.option('--module-name', help='Module name to substitute')
def generate(template_name: str, output_file: str, **kwargs):
    """Generate test file from a template."""
    manager = TestLibraryManager()
    
    # Remove None values
    substitutions = {k: v for k, v in kwargs.items() if v is not None}
    
    test_content = manager.generate_test_from_template(template_name, **substitutions)
    
    if test_content:
        with open(output_file, 'w') as f:
            f.write(test_content)
        click.echo(f"✅ Generated test file: {output_file}")
    else:
        click.echo(f"❌ Template '{template_name}' not found or generation failed")


@library.command()
@click.argument('pattern_file', type=click.Path(exists=True))
def add_pattern(pattern_file: str):
    """Add a new pattern from a JSON file."""
    manager = TestLibraryManager()
    
    try:
        with open(pattern_file, 'r') as f:
            pattern_data = json.load(f)
        
        pattern_name = pattern_data.get('name', 'unnamed_pattern')
        manager.add_pattern(pattern_name, pattern_data)
        manager.save_library()
        
        click.echo(f"✅ Added pattern: {pattern_name}")
    except Exception as e:
        click.echo(f"❌ Error adding pattern: {e}")


@library.command()
@click.argument('template_file', type=click.Path(exists=True))
@click.argument('template_name')
def add_template(template_file: str, template_name: str):
    """Add a new template from a file."""
    manager = TestLibraryManager()
    
    try:
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        manager.add_template(template_name, template_content)
        manager.save_library()
        
        click.echo(f"✅ Added template: {template_name}")
    except Exception as e:
        click.echo(f"❌ Error adding template: {e}")


@library.command()
@click.argument('example_file', type=click.Path(exists=True))
@click.argument('example_name')
def add_example(example_file: str, example_name: str):
    """Add a new example from a file."""
    manager = TestLibraryManager()
    
    try:
        with open(example_file, 'r') as f:
            example_content = f.read()
        
        manager.add_example(example_name, example_content)
        manager.save_library()
        
        click.echo(f"✅ Added example: {example_name}")
    except Exception as e:
        click.echo(f"❌ Error adding example: {e}")


@library.command()
def stats():
    """Show detailed statistics about the test library."""
    manager = TestLibraryManager()
    stats = manager.get_library_stats()
    
    click.echo("📊 Test Library Statistics:")
    click.echo(f"  Total Patterns: {stats['patterns']}")
    click.echo(f"  Total Templates: {stats['templates']}")
    click.echo(f"  Total Examples: {stats['examples']}")
    
    if stats['patterns'] > 0:
        click.echo("\nPattern Categories:")
        pattern_categories = {}
        for pattern_name, pattern_data in manager.patterns.items():
            category = pattern_data.get('category', 'general')
            if category not in pattern_categories:
                pattern_categories[category] = 0
            pattern_categories[category] += 1
        
        for category, count in pattern_categories.items():
            click.echo(f"  {category}: {count}")


if __name__ == '__main__':
    library()
