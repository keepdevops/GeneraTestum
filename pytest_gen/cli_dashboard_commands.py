"""
Dashboard CLI commands.
"""

import click
import sys
from .automation_dashboard import AutomationDashboard


@click.command()
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
