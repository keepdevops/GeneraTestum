"""
Dashboard backend services - refactored for 200LOC limit.
"""

from datetime import datetime
from typing import Dict, List, Any
from .dashboard_models import DashboardData, SystemStatus
from .dashboard_system_metrics import SystemMetricsCollector
from .dashboard_automation_services import AutomationServicesCollector


class DashboardDataCollector:
    """Collects data from various automation systems."""

    def __init__(self):
        self.system_metrics = SystemMetricsCollector()
        self.automation_services = AutomationServicesCollector()

    def collect_all_data(self) -> DashboardData:
        """Collect all dashboard data."""
        return DashboardData(
            system_status=self.get_system_status(),
            last_updated=datetime.now(),
            metrics=self.system_metrics.collect_system_metrics(),
            active_jobs=self.automation_services.get_active_jobs(),
            alerts=self.automation_services.get_alerts(),
            test_stats=self.automation_services.get_test_statistics(),
            security_stats=self.automation_services.get_security_statistics(),
            cicd_stats=self.automation_services.get_cicd_statistics(),
            performance=self._get_performance_metrics()
        )

    def get_system_status(self) -> SystemStatus:
        """Get overall system status."""
        # Check for critical alerts
        alerts = self.automation_services.get_alerts()
        critical_alerts = [a for a in alerts if a.level.value == "critical" and not a.resolved]
        
        if critical_alerts:
            return SystemStatus.CRITICAL
        
        # Check for warnings
        warning_alerts = [a for a in alerts if a.level.value == "warning" and not a.resolved]
        if warning_alerts:
            return SystemStatus.WARNING
        
        # Check system metrics
        metrics = self.system_metrics.collect_system_metrics()
        critical_metrics = [m for m in metrics if m.status.value == "critical"]
        
        if critical_metrics:
            return SystemStatus.WARNING
        
        return SystemStatus.HEALTHY

    def get_metrics(self):
        """Get system metrics."""
        return self.system_metrics.collect_system_metrics()

    def get_active_jobs(self):
        """Get active automation jobs."""
        return self.automation_services.get_active_jobs()

    def get_alerts(self):
        """Get system alerts."""
        return self.automation_services.get_alerts()

    def get_test_statistics(self):
        """Get test generation statistics."""
        return self.automation_services.get_test_statistics()

    def get_security_statistics(self):
        """Get security testing statistics."""
        return self.automation_services.get_security_statistics()

    def get_cicd_statistics(self):
        """Get CI/CD pipeline statistics."""
        return self.automation_services.get_cicd_statistics()

    def get_uptime(self) -> str:
        """Get system uptime."""
        return self.automation_services.get_uptime()

    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics summary."""
        return {
            "average_response_time": 0.15,
            "throughput": 150.0,
            "error_rate": 0.02,
            "availability": 99.8
        }

    def refresh_data(self):
        """Force refresh of all data."""
        # This could trigger immediate data collection
        pass

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of collected data."""
        data = self.collect_all_data()
        
        return {
            "system_status": data.system_status.value,
            "metrics_count": len(data.metrics),
            "active_jobs": len(data.active_jobs),
            "alerts_count": len(data.alerts),
            "unresolved_alerts": len([a for a in data.alerts if not a.resolved]),
            "last_updated": data.last_updated.isoformat()
        }