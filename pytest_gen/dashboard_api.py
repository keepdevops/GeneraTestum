"""
Dashboard API service for real-time data and control.
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .dashboard_backend import DashboardDataCollector
from .dashboard_models import DashboardData, DashboardEvent, SystemStatus


class DashboardAPIService:
    """Dashboard API service with WebSocket support."""

    def __init__(self):
        self.app = FastAPI(title="Test Generator Dashboard API", version="1.0.0")
        self.data_collector = DashboardDataCollector()
        self.connected_clients: List[WebSocket] = []
        self.setup_routes()
        self.setup_middleware()

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
            """Root endpoint."""
            return {"message": "Test Generator Dashboard API", "status": "running"}

        @self.app.get("/api/dashboard/data")
        async def get_dashboard_data():
            """Get complete dashboard data."""
            try:
                data = self.data_collector.collect_all_data()
                return self._serialize_dashboard_data(data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/status")
        async def get_system_status():
            """Get system status."""
            try:
                data = self.data_collector.collect_all_data()
                return {
                    "status": data.system_status.value,
                    "last_updated": data.last_updated.isoformat(),
                    "active_jobs": len(data.active_jobs),
                    "alerts": len([a for a in data.alerts if not a.acknowledged])
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/metrics")
        async def get_system_metrics():
            """Get system metrics."""
            try:
                metrics = self.data_collector.collect_system_metrics()
                return [self._serialize_metric(m) for m in metrics]
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/jobs")
        async def get_jobs():
            """Get automation jobs."""
            try:
                active_jobs = self.data_collector.get_active_jobs()
                recent_jobs = self.data_collector.get_recent_jobs()
                return {
                    "active": [self._serialize_job(j) for j in active_jobs],
                    "recent": [self._serialize_job(j) for j in recent_jobs]
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/alerts")
        async def get_alerts():
            """Get system alerts."""
            try:
                alerts = self.data_collector.get_alerts()
                return [self._serialize_alert(a) for a in alerts]
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/dashboard/alerts/{alert_id}/acknowledge")
        async def acknowledge_alert(alert_id: str):
            """Acknowledge an alert."""
            try:
                # This would typically update a database
                return {"message": f"Alert {alert_id} acknowledged", "success": True}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/stats/test-generation")
        async def get_test_generation_stats():
            """Get test generation statistics."""
            try:
                stats = self.data_collector.collect_test_generation_stats()
                return self._serialize_test_stats(stats)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/stats/security")
        async def get_security_stats():
            """Get security testing statistics."""
            try:
                stats = self.data_collector.collect_security_stats()
                return self._serialize_security_stats(stats)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/stats/cicd")
        async def get_cicd_stats():
            """Get CI/CD statistics."""
            try:
                stats = self.data_collector.collect_cicd_stats()
                return self._serialize_cicd_stats(stats)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/performance")
        async def get_performance_metrics():
            """Get performance metrics."""
            try:
                metrics = self.data_collector.collect_performance_metrics()
                return self._serialize_performance_metrics(metrics)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.websocket("/ws/dashboard")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await websocket.accept()
            self.connected_clients.append(websocket)
            
            try:
                while True:
                    # Send periodic updates
                    data = self.data_collector.collect_all_data()
                    event = DashboardEvent(
                        event_type="data_update",
                        event_data=self._serialize_dashboard_data(data),
                        timestamp=datetime.now(),
                        source="dashboard_api",
                        priority=0
                    )
                    await websocket.send_text(json.dumps(self._serialize_event(event)))
                    await asyncio.sleep(30)  # Update every 30 seconds
                    
            except WebSocketDisconnect:
                self.connected_clients.remove(websocket)

        @self.app.get("/api/dashboard/health")
        async def health_check():
            """Health check endpoint."""
            try:
                data = self.data_collector.collect_all_data()
                return {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "connected_clients": len(self.connected_clients),
                    "system_status": data.system_status.value
                }
            except Exception as e:
                return {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

    def _serialize_dashboard_data(self, data: DashboardData) -> Dict[str, Any]:
        """Serialize dashboard data for JSON response."""
        return {
            "system_status": data.system_status.value,
            "metrics": [self._serialize_metric(m) for m in data.metrics],
            "active_jobs": [self._serialize_job(j) for j in data.active_jobs],
            "recent_jobs": [self._serialize_job(j) for j in data.recent_jobs],
            "test_stats": self._serialize_test_stats(data.test_stats),
            "security_stats": self._serialize_security_stats(data.security_stats),
            "cicd_stats": self._serialize_cicd_stats(data.cicd_stats),
            "performance": self._serialize_performance_metrics(data.performance),
            "alerts": [self._serialize_alert(a) for a in data.alerts],
            "last_updated": data.last_updated.isoformat()
        }

    def _serialize_metric(self, metric) -> Dict[str, Any]:
        """Serialize system metric."""
        return {
            "name": metric.name,
            "value": metric.value,
            "unit": metric.unit,
            "timestamp": metric.timestamp.isoformat(),
            "status": metric.status.value,
            "trend": metric.trend,
            "threshold_warning": metric.threshold_warning,
            "threshold_critical": metric.threshold_critical
        }

    def _serialize_job(self, job) -> Dict[str, Any]:
        """Serialize automation job."""
        return {
            "job_id": job.job_id,
            "job_type": job.job_type.value,
            "status": job.status,
            "progress": job.progress,
            "started_at": job.started_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "error_message": job.error_message,
            "result_summary": job.result_summary
        }

    def _serialize_alert(self, alert) -> Dict[str, Any]:
        """Serialize system alert."""
        return {
            "alert_id": alert.alert_id,
            "severity": alert.severity,
            "title": alert.title,
            "message": alert.message,
            "source": alert.source,
            "timestamp": alert.timestamp.isoformat(),
            "acknowledged": alert.acknowledged,
            "resolved": alert.resolved,
            "actions": alert.actions
        }

    def _serialize_test_stats(self, stats) -> Dict[str, Any]:
        """Serialize test generation statistics."""
        return {
            "total_tests_generated": stats.total_tests_generated,
            "tests_generated_today": stats.tests_generated_today,
            "success_rate": stats.success_rate,
            "average_generation_time": stats.average_generation_time,
            "languages_supported": stats.languages_supported,
            "frameworks_supported": stats.frameworks_supported,
            "last_generation": stats.last_generation.isoformat() if stats.last_generation else None
        }

    def _serialize_security_stats(self, stats) -> Dict[str, Any]:
        """Serialize security statistics."""
        return {
            "total_vulnerabilities_found": stats.total_vulnerabilities_found,
            "vulnerabilities_fixed": stats.vulnerabilities_fixed,
            "critical_vulnerabilities": stats.critical_vulnerabilities,
            "security_tests_generated": stats.security_tests_generated,
            "last_scan": stats.last_scan.isoformat() if stats.last_scan else None,
            "scan_coverage": stats.scan_coverage
        }

    def _serialize_cicd_stats(self, stats) -> Dict[str, Any]:
        """Serialize CI/CD statistics."""
        return {
            "total_builds": stats.total_builds,
            "successful_builds": stats.successful_builds,
            "failed_builds": stats.failed_builds,
            "average_build_time": stats.average_build_time,
            "last_build": stats.last_build.isoformat() if stats.last_build else None,
            "active_pipelines": stats.active_pipelines
        }

    def _serialize_performance_metrics(self, metrics) -> Dict[str, Any]:
        """Serialize performance metrics."""
        return {
            "cpu_usage": metrics.cpu_usage,
            "memory_usage": metrics.memory_usage,
            "disk_usage": metrics.disk_usage,
            "network_io": metrics.network_io,
            "response_time": metrics.response_time,
            "throughput": metrics.throughput,
            "error_rate": metrics.error_rate,
            "timestamp": metrics.timestamp.isoformat()
        }

    def _serialize_event(self, event: DashboardEvent) -> Dict[str, Any]:
        """Serialize dashboard event."""
        return {
            "event_type": event.event_type,
            "event_data": event.event_data,
            "timestamp": event.timestamp.isoformat(),
            "source": event.source,
            "priority": event.priority
        }

    async def broadcast_event(self, event: DashboardEvent):
        """Broadcast event to all connected clients."""
        if self.connected_clients:
            message = json.dumps(self._serialize_event(event))
            disconnected_clients = []
            
            for client in self.connected_clients:
                try:
                    await client.send_text(message)
                except:
                    disconnected_clients.append(client)
            
            # Remove disconnected clients
            for client in disconnected_clients:
                self.connected_clients.remove(client)

    def get_app(self) -> FastAPI:
        """Get the FastAPI application."""
        return self.app
