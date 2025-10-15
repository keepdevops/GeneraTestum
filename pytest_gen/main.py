"""
CLI interface for pytest code generator.
"""

import click
from .cli_core_commands import generate, analyze, init_config, info
from .cli_ai_commands import ask, explain, suggest, review, assistant, ai_status, smart_suggest
from .cli_gui_commands import gui, web_gui
from .cli_dashboard_commands import dashboard
from .library_commands import library
from .automation_commands import automation


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Pytest Code Generator - Generate comprehensive test cases from Python code."""
    pass


# Core Commands
cli.add_command(generate)
cli.add_command(analyze)
cli.add_command(init_config)
cli.add_command(info)

# AI Assistant Commands
cli.add_command(ask)
cli.add_command(explain)
cli.add_command(suggest)
cli.add_command(review)
cli.add_command(assistant)
cli.add_command(ai_status)
cli.add_command(smart_suggest)

# GUI Commands
cli.add_command(gui)
cli.add_command(web_gui)

# Dashboard Command
cli.add_command(dashboard)

# Library Commands
cli.add_command(library)

# Automation Commands
cli.add_command(automation)


if __name__ == '__main__':
    cli()