"""
Main automation dashboard orchestrator - refactored for 200LOC limit.
"""

import asyncio
from typing import Dict, Any, Optional
from fastapi.responses import HTMLResponse
from .dashboard_server_manager import DashboardServerManager
from .dashboard_testing import DashboardTester
from .dashboard_ui import DashboardUI
from .dashboard_backend import DashboardDataCollector


class AutomationDashboard:
    """Main automation dashboard orchestrator."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.server_manager = DashboardServerManager(host, port)
        self.tester = DashboardTester()
        self.ui = DashboardUI()
        self.data_collector = DashboardDataCollector()
        self.app = self._create_app()

    def _create_app(self):
        """Create the main FastAPI application."""
        app = self.server_manager.get_app()
        
        # Add custom dashboard route
        @app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard():
            """Serve the main dashboard."""
            try:
                data = self.data_collector.collect_all_data()
                html = self.ui.generate_dashboard_html(self._serialize_data(data))
                return HTMLResponse(content=html)
            except Exception as e:
                error_html = self.ui.generate_error_html(f"Dashboard error: {str(e)}")
                return HTMLResponse(content=error_html, status_code=500)
        
        return app

    def _serialize_data(self, data) -> Dict[str, Any]:
        """Serialize dashboard data for UI."""
        return {
            "system_status": data.system_status.value,
            "last_updated": data.last_updated.isoformat(),
            "metrics": [
                {
                    "name": m.name,
                    "value": m.value,
                    "unit": m.unit,
                    "status": m.status.value,
                    "category": m.category.value
                }
                for m in data.metrics
            ],
            "active_jobs": [
                {
                    "id": j.id,
                    "name": j.name,
                    "status": j.status.value,
                    "progress": j.progress,
                    "type": j.type.value
                }
                for j in data.active_jobs
            ],
            "alerts": [
                {
                    "id": a.id,
                    "message": a.message,
                    "level": a.level.value,
                    "category": a.category,
                    "resolved": a.resolved
                }
                for a in data.alerts
            ],
            "test_stats": data.test_stats,
            "security_stats": data.security_stats,
            "cicd_stats": data.cicd_stats,
            "performance": data.performance
        }

    def run_dashboard(self):
        """Run the dashboard server."""
        import uvicorn
        
        # Start periodic updates in background
        asyncio.create_task(self._start_background_tasks())
        
        # Run the server
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )

    async def _start_background_tasks(self):
        """Start background tasks."""
        # This would start periodic data updates, health checks, etc.
        pass

    async def test_dashboard(self) -> Dict[str, Any]:
        """Test dashboard functionality."""
        return await self.tester.test_dashboard_functionality()

    def get_dashboard_info(self) -> Dict[str, Any]:
        """Get dashboard information."""
        server_info = self.server_manager.get_server_info()
        
        return {
            "name": "Test Generator Automation Dashboard",
            "version": "1.0.0",
            "description": "Real-time monitoring dashboard for all automation systems",
            "host": self.host,
            "port": self.port,
            "endpoints": {
                "Dashboard": server_info["dashboard_url"],
                "API": server_info["api_url"],
                "Health": server_info["health_url"],
                "WebSocket": server_info["websocket_url"]
            },
            "features": [
                "Real-time system monitoring",
                "Performance metrics tracking",
                "Automation job management",
                "Security testing status",
                "CI/CD pipeline monitoring",
                "Alert system",
                "WebSocket live updates"
            ]
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current dashboard status."""
        try:
            data = self.data_collector.collect_all_data()
            return {
                "status": "running",
                "system_status": data.system_status.value,
                "last_update": data.last_updated.isoformat(),
                "metrics_count": len(data.metrics),
                "active_jobs": len(data.active_jobs),
                "alerts_count": len(data.alerts)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }