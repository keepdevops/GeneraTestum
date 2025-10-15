"""
Dashboard API service - refactored for 200LOC limit.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .dashboard_backend import DashboardDataCollector
from .dashboard_models import DashboardData, DashboardEvent, SystemStatus
from .dashboard_api_routes import DashboardAPIRoutes
from .dashboard_websocket import DashboardWebSocketManager
from .dashboard_ui import DashboardUI


class DashboardAPIService:
    """Dashboard API service with WebSocket support."""

    def __init__(self):
        self.app = FastAPI(title="Test Generator Dashboard API", version="1.0.0")
        self.data_collector = DashboardDataCollector()
        self.websocket_manager = DashboardWebSocketManager(self.data_collector)
        self.routes = DashboardAPIRoutes(self.data_collector)
        self.ui = DashboardUI()
        
        self.setup_middleware()
        self.setup_routes()
        self.setup_static_files()

    def setup_middleware(self):
        """Setup CORS and other middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/")
        async def root():
            return await self.routes.root()

        @self.app.get("/api/dashboard/data")
        async def get_dashboard_data():
            return await self.routes.get_dashboard_data()

        @self.app.get("/api/dashboard/status")
        async def get_system_status():
            return await self.routes.get_system_status()

        @self.app.get("/api/dashboard/metrics")
        async def get_metrics():
            return await self.routes.get_metrics()

        @self.app.get("/api/dashboard/jobs")
        async def get_active_jobs():
            return await self.routes.get_active_jobs()

        @self.app.get("/api/dashboard/alerts")
        async def get_alerts():
            return await self.routes.get_alerts()

        @self.app.get("/api/dashboard/test-stats")
        async def get_test_statistics():
            return await self.routes.get_test_statistics()

        @self.app.get("/api/dashboard/security-stats")
        async def get_security_statistics():
            return await self.routes.get_security_statistics()

        @self.app.get("/api/dashboard/cicd-stats")
        async def get_cicd_statistics():
            return await self.routes.get_cicd_statistics()

        @self.app.get("/api/dashboard/health")
        async def health_check():
            return await self.routes.health_check()

        @self.app.get("/dashboard")
        async def dashboard():
            """Serve the dashboard UI."""
            try:
                data = self.data_collector.collect_all_data()
                html_content = self.ui.generate_dashboard_html(data.__dict__)
                return HTMLResponse(content=html_content)
            except Exception as e:
                error_html = self.ui.generate_error_html(f"Failed to load dashboard: {str(e)}")
                return HTMLResponse(content=error_html, status_code=500)

        @self.app.websocket("/ws/dashboard")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await self.websocket_manager.handle_websocket(websocket)

    def setup_static_files(self):
        """Setup static file serving."""
        try:
            import os
            static_dir = os.path.join(os.path.dirname(__file__), "static")
            if os.path.exists(static_dir):
                self.app.mount("/static", StaticFiles(directory=static_dir), name="static")
        except Exception:
            # Static files are optional
            pass

    async def start_periodic_updates(self):
        """Start periodic data updates."""
        await self.websocket_manager.start_periodic_updates()

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app

    async def run_server(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the dashboard server."""
        import uvicorn
        
        # Start periodic updates in background
        asyncio.create_task(self.start_periodic_updates())
        
        # Run the server
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

    def get_dashboard_info(self) -> Dict[str, Any]:
        """Get dashboard information."""
        return {
            "name": "Test Generator Automation Dashboard",
            "version": "1.0.0",
            "description": "Real-time monitoring dashboard for all automation systems",
            "host": "0.0.0.0",
            "port": 8000,
            "endpoints": {
                "Dashboard": "http://0.0.0.0:8000/dashboard",
                "API": "http://0.0.0.0:8000/api/dashboard/",
                "Health": "http://0.0.0.0:8000/api/dashboard/health",
                "WebSocket": "ws://0.0.0.0:8000/ws/dashboard"
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