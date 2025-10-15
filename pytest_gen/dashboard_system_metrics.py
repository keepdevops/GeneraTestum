"""
System metrics collection for dashboard.
"""

import psutil
from datetime import datetime
from typing import List
from .dashboard_models import SystemMetric, MetricStatus, MetricCategory


class SystemMetricsCollector:
    """Collects system performance metrics."""
    
    def __init__(self):
        self.metric_history = {}
    
    def collect_system_metrics(self) -> List[SystemMetric]:
        """Collect system performance metrics."""
        metrics = []
        now = datetime.now()

        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics.append(SystemMetric(
            name="CPU Usage",
            value=cpu_percent,
            unit="%",
            timestamp=now,
            status=self._get_metric_status(cpu_percent, 80, 95),
            trend=self._get_trend("cpu", cpu_percent),
            threshold_warning=80.0,
            threshold_critical=95.0,
            category=MetricCategory.SYSTEM
        ))

        # Memory Usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        metrics.append(SystemMetric(
            name="Memory Usage",
            value=memory_percent,
            unit="%",
            timestamp=now,
            status=self._get_metric_status(memory_percent, 85, 95),
            trend=self._get_trend("memory", memory_percent),
            threshold_warning=85.0,
            threshold_critical=95.0,
            category=MetricCategory.SYSTEM
        ))

        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        metrics.append(SystemMetric(
            name="Disk Usage",
            value=disk_percent,
            unit="%",
            timestamp=now,
            status=self._get_metric_status(disk_percent, 80, 90),
            trend=self._get_trend("disk", disk_percent),
            threshold_warning=80.0,
            threshold_critical=90.0,
            category=MetricCategory.SYSTEM
        ))

        # Network I/O
        network = psutil.net_io_counters()
        metrics.append(SystemMetric(
            name="Network Bytes Sent",
            value=network.bytes_sent,
            unit="bytes",
            timestamp=now,
            status=MetricStatus.HEALTHY,
            trend=self._get_trend("network_sent", network.bytes_sent),
            category=MetricCategory.NETWORK
        ))

        metrics.append(SystemMetric(
            name="Network Bytes Received",
            value=network.bytes_recv,
            unit="bytes",
            timestamp=now,
            status=MetricStatus.HEALTHY,
            trend=self._get_trend("network_recv", network.bytes_recv),
            category=MetricCategory.NETWORK
        ))

        # Process Count
        process_count = len(psutil.pids())
        metrics.append(SystemMetric(
            name="Active Processes",
            value=process_count,
            unit="count",
            timestamp=now,
            status=self._get_metric_status(process_count, 200, 300),
            trend=self._get_trend("processes", process_count),
            threshold_warning=200,
            threshold_critical=300,
            category=MetricCategory.SYSTEM
        ))

        return metrics

    def _get_metric_status(self, value: float, warning_threshold: float, critical_threshold: float) -> MetricStatus:
        """Determine metric status based on thresholds."""
        if value >= critical_threshold:
            return MetricStatus.CRITICAL
        elif value >= warning_threshold:
            return MetricStatus.WARNING
        else:
            return MetricStatus.HEALTHY

    def _get_trend(self, metric_name: str, current_value: float) -> str:
        """Calculate trend for a metric."""
        if metric_name not in self.metric_history:
            self.metric_history[metric_name] = []
        
        history = self.metric_history[metric_name]
        history.append(current_value)
        
        # Keep only last 10 values
        if len(history) > 10:
            history.pop(0)
        
        if len(history) < 2:
            return "stable"
        
        # Calculate trend
        recent_avg = sum(history[-3:]) / len(history[-3:])
        older_avg = sum(history[:-3]) / len(history[:-3]) if len(history) > 3 else history[0]
        
        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
