"""
Dashboard API route handlers.
"""

from fastapi import HTTPException
from typing import Dict, List, Any
from .dashboard_models import DashboardData


class DashboardAPIRoutes:
    """Route handlers for dashboard API endpoints."""
    
    def __init__(self, data_collector):
        self.data_collector = data_collector
    
    async def root(self):
        """Root endpoint."""
        return {"message": "Test Generator Dashboard API", "status": "running"}
    
    async def get_dashboard_data(self):
        """Get complete dashboard data."""
        try:
            data = self.data_collector.collect_all_data()
            return self._serialize_dashboard_data(data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to collect data: {str(e)}")
    
    async def get_system_status(self):
        """Get system status."""
        try:
            status = self.data_collector.get_system_status()
            return {
                "status": status.value,
                "timestamp": datetime.now().isoformat(),
                "uptime": self.data_collector.get_uptime()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")
    
    async def get_metrics(self):
        """Get system metrics."""
        try:
            metrics = self.data_collector.get_metrics()
            return {
                "metrics": [
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "timestamp": metric.timestamp.isoformat(),
                        "category": metric.category.value
                    }
                    for metric in metrics
                ],
                "total_metrics": len(metrics)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")
    
    async def get_active_jobs(self):
        """Get active automation jobs."""
        try:
            jobs = self.data_collector.get_active_jobs()
            return {
                "jobs": [
                    {
                        "id": job.id,
                        "name": job.name,
                        "status": job.status.value,
                        "progress": job.progress,
                        "started_at": job.started_at.isoformat(),
                        "estimated_completion": job.estimated_completion.isoformat() if job.estimated_completion else None
                    }
                    for job in jobs
                ],
                "total_jobs": len(jobs)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get jobs: {str(e)}")
    
    async def get_alerts(self):
        """Get system alerts."""
        try:
            alerts = self.data_collector.get_alerts()
            return {
                "alerts": [
                    {
                        "id": alert.id,
                        "message": alert.message,
                        "level": alert.level.value,
                        "timestamp": alert.timestamp.isoformat(),
                        "category": alert.category.value,
                        "resolved": alert.resolved
                    }
                    for alert in alerts
                ],
                "total_alerts": len(alerts),
                "unresolved_alerts": len([a for a in alerts if not a.resolved])
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")
    
    async def get_test_statistics(self):
        """Get test generation statistics."""
        try:
            stats = self.data_collector.get_test_statistics()
            return {
                "tests_generated": stats.get("tests_generated", 0),
                "total_files_processed": stats.get("total_files_processed", 0),
                "success_rate": stats.get("success_rate", 0.0),
                "average_generation_time": stats.get("average_generation_time", 0.0),
                "coverage_percentage": stats.get("coverage_percentage", 0.0)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get test stats: {str(e)}")
    
    async def get_security_statistics(self):
        """Get security testing statistics."""
        try:
            stats = self.data_collector.get_security_statistics()
            return {
                "vulnerabilities_found": stats.get("vulnerabilities_found", 0),
                "files_analyzed": stats.get("files_analyzed", 0),
                "critical_issues": stats.get("critical_issues", 0),
                "security_score": stats.get("security_score", 0.0)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get security stats: {str(e)}")
    
    async def get_cicd_statistics(self):
        """Get CI/CD pipeline statistics."""
        try:
            stats = self.data_collector.get_cicd_statistics()
            return {
                "pipelines_active": stats.get("pipelines_active", 0),
                "builds_today": stats.get("builds_today", 0),
                "success_rate": stats.get("success_rate", 0.0),
                "average_build_time": stats.get("average_build_time", 0.0)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get CI/CD stats: {str(e)}")
    
    async def health_check(self):
        """Health check endpoint."""
        try:
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "services": {
                    "data_collector": "healthy",
                    "websocket": "healthy",
                    "api": "healthy"
                }
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
    
    def _serialize_dashboard_data(self, data: DashboardData) -> Dict[str, Any]:
        """Serialize dashboard data for API response."""
        return {
            "system_status": data.system_status.value,
            "last_updated": data.last_updated.isoformat(),
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "category": metric.category.value
                }
                for metric in data.metrics
            ],
            "active_jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "status": job.status.value,
                    "progress": job.progress
                }
                for job in data.active_jobs
            ],
            "alerts": [
                {
                    "id": alert.id,
                    "message": alert.message,
                    "level": alert.level.value,
                    "category": alert.category.value
                }
                for alert in data.alerts
            ],
            "test_stats": data.test_stats,
            "security_stats": data.security_stats,
            "cicd_stats": data.cicd_stats,
            "performance": data.performance
        }
