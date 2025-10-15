"""
GUI and interface CLI commands.
"""

import click
import sys
from .panel_gui import TestGeneratorGUI


@click.command()
@click.option('--port', default=5007, help='Port for the GUI server')
@click.option('--host', default='127.0.0.1', help='Host for the GUI server')
@click.option('--show', is_flag=True, help='Automatically open browser')
def gui(port, host, show):
    """Launch the interactive Panel GUI."""
    try:
        gui_app = TestGeneratorGUI(port=port, host=host)
        gui_app.run(show=show)
    except Exception as e:
        click.echo(f"Error launching GUI: {e}")
        sys.exit(1)


@click.command()
@click.option('--host', default='127.0.0.1', help='Host for the web GUI')
@click.option('--port', default=5000, help='Port for the web GUI')
@click.option('--debug', is_flag=True, help='Run in debug mode')
def web_gui(host, port, debug):
    """Launch the web-based GUI."""
    try:
        from .web_gui import run_web_gui
        run_web_gui(host=host, port=port)
    except Exception as e:
        click.echo(f"Error launching web GUI: {e}")
        sys.exit(1)
