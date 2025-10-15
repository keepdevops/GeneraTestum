"""
CLI interface for pytest code generator.
"""

import click
import sys
from .cli_commands import (
    generate_command, analyze_command, init_config_command, info_command
)
from .ai_commands import (
    ask_command, explain_command, suggest_command, review_command, 
    assistant_command, ai_status_command
)
from .library_commands import library
from .automation_commands import automation
from .automation_dashboard import AutomationDashboard


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

@cli.command()
@click.option('--port', default=5007, help='Port to serve the web GUI on')
@click.option('--host', default='localhost', help='Host to serve the web GUI on')
@click.option('--debug', is_flag=True, help='Run in debug mode')
def web_gui(port: int, host: str, debug: bool):
    """Launch the web-based GUI (Flask)."""
    try:
        from .web_gui import launch_web_gui
        launch_web_gui(port=port, host=host, debug=debug)
    except ImportError as e:
        click.echo(f"Error: Flask dependencies not installed. Please install with:")
        click.echo("pip install flask")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error launching web GUI: {e}")
        sys.exit(1)


# AI Assistant Commands
@cli.command()
@click.argument('question', required=True)
@click.option('--file', '-f', help='File to provide as context for the question')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed response information')
def ask(question, file, verbose):
    """Ask the AI assistant a question about testing."""
    ask_command(question, file, verbose)


@cli.command()
@click.argument('test_file', required=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed explanation')
def explain(test_file, verbose):
    """Explain what tests will be generated or what existing tests do."""
    explain_command(test_file, verbose)


@cli.command()
@click.argument('source_file', required=True)
@click.option('--tests', '-t', help='Existing test file to compare against')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed suggestions')
def suggest(source_file, tests, verbose):
    """Suggest test improvements or new tests for source code."""
    suggest_command(source_file, tests, verbose)


@cli.command()
@click.argument('test_directory', default='tests/')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed review')
@click.option('--verbose', '-v', is_flag=True, help='Show token usage')
def review(test_directory, detailed, verbose):
    """Review all tests in a directory and provide feedback."""
    review_command(test_directory, detailed, verbose)


@cli.command()
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
def assistant(interactive):
    """Launch AI assistant in interactive mode."""
    assistant_command(interactive)


@cli.command(name='ai-status')
def ai_status():
    """Check AI assistant configuration and status."""
    ai_status_command()


# Add library commands as a subcommand group
cli.add_command(library, name='library')

# Add automation commands as a subcommand group
cli.add_command(automation, name='automation')


@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind the dashboard to')
@click.option('--port', type=int, default=8000, help='Port to bind the dashboard to')
@click.option('--test', is_flag=True, help='Test dashboard functionality')
@click.option('--info', is_flag=True, help='Show dashboard information')
def dashboard(host, port, test, info):
    """🎛️ Launch the Test Generator Automation Dashboard.
    
    Provides real-time monitoring of all automation systems including:
    - System performance metrics
    - Test generation statistics  
    - Security testing status
    - CI/CD pipeline monitoring
    - Active automation jobs
    - System alerts and notifications
    
    Examples:
        pytest-gen dashboard                    # Start dashboard on default port 8000
        pytest-gen dashboard --port 9000       # Start dashboard on port 9000
        pytest-gen dashboard --test            # Test dashboard functionality
        pytest-gen dashboard --info            # Show dashboard information
    """
    dashboard_instance = AutomationDashboard(host=host, port=port)
    
    if info:
        info_data = dashboard_instance.get_dashboard_info()
        click.echo("🎛️ Test Generator Automation Dashboard")
        click.echo("=" * 50)
        click.echo(f"Name: {info_data['name']}")
        click.echo(f"Version: {info_data['version']}")
        click.echo(f"Description: {info_data['description']}")
        click.echo(f"Host: {info_data['host']}")
        click.echo(f"Port: {info_data['port']}")
        click.echo("\n📍 Endpoints:")
        for name, url in info_data['endpoints'].items():
            click.echo(f"  {name}: {url}")
        click.echo("\n✨ Features:")
        for feature in info_data['features']:
            click.echo(f"  • {feature}")
        return
    
    if test:
        import asyncio
        result = asyncio.run(dashboard_instance.test_dashboard())
        if result['status'] == 'success':
            click.echo("✅ Dashboard functionality test passed!")
            click.echo(f"📊 System Status: {result['data_summary']['system_status']}")
            click.echo(f"📈 Metrics: {result['data_summary']['metrics_count']}")
            click.echo(f"⚙️ Active Jobs: {result['data_summary']['active_jobs']}")
            click.echo(f"🚨 Alerts: {result['data_summary']['alerts_count']}")
        else:
            click.echo(f"❌ Dashboard test failed: {result['message']}")
            sys.exit(1)
        return
    
    click.echo("🎛️ Starting Test Generator Automation Dashboard...")
    click.echo(f"📍 Dashboard URL: http://{host}:{port}/dashboard")
    click.echo(f"🔗 API Base URL: http://{host}:{port}/api/dashboard/")
    click.echo(f"❤️ Health Check: http://{host}:{port}/api/dashboard/health")
    click.echo(f"🌐 WebSocket: ws://{host}:{port}/ws/dashboard")
    click.echo("Press Ctrl+C to stop the dashboard")
    
    try:
        dashboard_instance.run_dashboard()
    except KeyboardInterrupt:
        click.echo("\n👋 Dashboard stopped.")
    except Exception as e:
        click.echo(f"❌ Error starting dashboard: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli()