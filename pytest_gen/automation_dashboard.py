"""
Main automation dashboard orchestrator.
"""

import uvicorn
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .dashboard_api import DashboardAPIService
from .dashboard_ui import DashboardUI
from .dashboard_backend import DashboardDataCollector
from .dashboard_models import DashboardData


class AutomationDashboard:
    """Main automation dashboard orchestrator."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.api_service = DashboardAPIService()
        self.ui = DashboardUI()
        self.data_collector = DashboardDataCollector()
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """Create the main FastAPI application."""
        app = self.api_service.get_app()
        
        # Add dashboard UI route
        @app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard():
            """Serve the main dashboard."""
            try:
                data = self.data_collector.collect_all_data()
                html = self.ui.generate_dashboard_html(self._serialize_data(data))
                return HTMLResponse(content=html)
            except Exception as e:
                error_html = f"""
                <html>
                <head><title>Dashboard Error</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1>Dashboard Error</h1>
                    <p>Error: {str(e)}</p>
                    <p><a href="/api/dashboard/health">Check API Health</a></p>
                </body>
                </html>
                """
                return HTMLResponse(content=error_html, status_code=500)

        @app.get("/", response_class=HTMLResponse)
        async def root():
            """Redirect to dashboard."""
            return HTMLResponse(content="""
            <html>
            <head><title>Test Generator Dashboard</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>🎛️ Test Generator Automation Dashboard</h1>
                <p>Welcome to the Test Generator Automation Dashboard</p>
                <p><a href="/dashboard" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Open Dashboard</a></p>
                <p><a href="/api/dashboard/data">API Data</a> | <a href="/api/dashboard/health">Health Check</a></p>
            </body>
            </html>
            """)

        return app

    def _serialize_data(self, data: DashboardData) -> Dict[str, Any]:
        """Serialize dashboard data for UI."""
        return {
            'system_status': data.system_status.value,
            'last_updated': data.last_updated.isoformat(),
            'metrics': [
                {
                    'name': m.name,
                    'value': m.value,
                    'unit': m.unit,
                    'status': m.status.value,
                    'trend': m.trend,
                    'threshold_warning': m.threshold_warning,
                    'threshold_critical': m.threshold_critical
                } for m in data.metrics
            ],
            'active_jobs': [
                {
                    'job_id': j.job_id,
                    'job_type': j.job_type.value,
                    'status': j.status,
                    'progress': j.progress,
                    'started_at': j.started_at.isoformat(),
                    'error_message': j.error_message,
                    'result_summary': j.result_summary
                } for j in data.active_jobs
            ],
            'alerts': [
                {
                    'alert_id': a.alert_id,
                    'severity': a.severity,
                    'title': a.title,
                    'message': a.message,
                    'source': a.source,
                    'timestamp': a.timestamp.isoformat(),
                    'acknowledged': a.acknowledged,
                    'resolved': a.resolved
                } for a in data.alerts
            ],
            'test_stats': {
                'total_tests_generated': data.test_stats.total_tests_generated,
                'tests_generated_today': data.test_stats.tests_generated_today,
                'success_rate': data.test_stats.success_rate,
                'average_generation_time': data.test_stats.average_generation_time,
                'languages_supported': data.test_stats.languages_supported,
                'frameworks_supported': data.test_stats.frameworks_supported,
                'last_generation': data.test_stats.last_generation.isoformat() if data.test_stats.last_generation else None
            },
            'security_stats': {
                'total_vulnerabilities_found': data.security_stats.total_vulnerabilities_found,
                'vulnerabilities_fixed': data.security_stats.vulnerabilities_fixed,
                'critical_vulnerabilities': data.security_stats.critical_vulnerabilities,
                'security_tests_generated': data.security_stats.security_tests_generated,
                'last_scan': data.security_stats.last_scan.isoformat() if data.security_stats.last_scan else None,
                'scan_coverage': data.security_stats.scan_coverage
            },
            'cicd_stats': {
                'total_builds': data.cicd_stats.total_builds,
                'successful_builds': data.cicd_stats.successful_builds,
                'failed_builds': data.cicd_stats.failed_builds,
                'average_build_time': data.cicd_stats.average_build_time,
                'last_build': data.cicd_stats.last_build.isoformat() if data.cicd_stats.last_build else None,
                'active_pipelines': data.cicd_stats.active_pipelines
            },
            'performance': {
                'cpu_usage': data.performance.cpu_usage,
                'memory_usage': data.performance.memory_usage,
                'disk_usage': data.performance.disk_usage,
                'network_io': data.performance.network_io,
                'response_time': data.performance.response_time,
                'throughput': data.performance.throughput,
                'error_rate': data.performance.error_rate,
                'timestamp': data.performance.timestamp.isoformat()
            }
        }

    async def start_dashboard(self):
        """Start the dashboard server."""
        print(f"🎛️ Starting Test Generator Automation Dashboard...")
        print(f"📍 Dashboard URL: http://{self.host}:{self.port}/dashboard")
        print(f"🔗 API Base URL: http://{self.host}:{self.port}/api/dashboard/")
        print(f"❤️ Health Check: http://{self.host}:{self.port}/api/dashboard/health")
        print(f"🌐 WebSocket: ws://{self.host}:{self.port}/ws/dashboard")
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        await server.serve()

    def run_dashboard(self):
        """Run the dashboard (blocking)."""
        print(f"🎛️ Starting Test Generator Automation Dashboard...")
        print(f"📍 Dashboard URL: http://{self.host}:{self.port}/dashboard")
        print(f"🔗 API Base URL: http://{self.host}:{self.port}/api/dashboard/")
        print(f"❤️ Health Check: http://{self.host}:{self.port}/api/dashboard/health")
        print(f"🌐 WebSocket: ws://{self.host}:{self.port}/ws/dashboard")
        print(f"Press Ctrl+C to stop the dashboard")
        
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=True
        )

    def get_dashboard_info(self) -> Dict[str, Any]:
        """Get dashboard information."""
        return {
            'name': 'Test Generator Automation Dashboard',
            'version': '1.0.0',
            'description': 'Real-time monitoring of all automation systems',
            'host': self.host,
            'port': self.port,
            'endpoints': {
                'dashboard': f'http://{self.host}:{self.port}/dashboard',
                'api_base': f'http://{self.host}:{self.port}/api/dashboard/',
                'health_check': f'http://{self.host}:{self.port}/api/dashboard/health',
                'websocket': f'ws://{self.host}:{self.port}/ws/dashboard'
            },
            'features': [
                'Real-time system monitoring',
                'Automation job tracking',
                'Security testing status',
                'CI/CD pipeline monitoring',
                'Performance metrics',
                'Alert management',
                'WebSocket live updates'
            ]
        }

    async def test_dashboard(self) -> Dict[str, Any]:
        """Test dashboard functionality."""
        try:
            # Test data collection
            data = self.data_collector.collect_all_data()
            
            # Test UI generation
            html = self.ui.generate_dashboard_html(self._serialize_data(data))
            
            # Test API service
            app = self.api_service.get_app()
            
            return {
                'status': 'success',
                'message': 'Dashboard functionality test passed',
                'components': {
                    'data_collector': 'working',
                    'ui_generator': 'working',
                    'api_service': 'working',
                    'main_app': 'working'
                },
                'data_summary': {
                    'system_status': data.system_status.value,
                    'metrics_count': len(data.metrics),
                    'active_jobs': len(data.active_jobs),
                    'alerts_count': len(data.alerts)
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Dashboard test failed: {str(e)}',
                'error': str(e)
            }


def create_dashboard(host: str = "0.0.0.0", port: int = 8000) -> AutomationDashboard:
    """Create and return a dashboard instance."""
    return AutomationDashboard(host=host, port=port)


def run_dashboard_cli():
    """CLI entry point for running the dashboard."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Generator Automation Dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--test', action='store_true', help='Test dashboard functionality')
    
    args = parser.parse_args()
    
    dashboard = AutomationDashboard(host=args.host, port=args.port)
    
    if args.test:
        import asyncio
        result = asyncio.run(dashboard.test_dashboard())
        print(f"Dashboard test result: {result}")
    else:
        dashboard.run_dashboard()


if __name__ == "__main__":
    run_dashboard_cli()
