"""
Dashboard backend services and data collection.
"""

import os
import time
import json
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .dashboard_models import (
    DashboardData, SystemStatus, SystemMetric, AutomationJob, AutomationType,
    TestGenerationStats, SecurityStats, CICDStats, PerformanceMetrics,
    Alert, DashboardEvent
)
from .auto_security_testing import AutoSecurityTesting
from .auto_test_optimizer import AutoTestOptimizer
from .auto_integration_testing import AutoIntegrationTesting
from .auto_cicd_generator import AutoCICDGenerator
from .auto_documentation_generator import AutoDocumentationGenerator


class DashboardDataCollector:
    """Collects data from various automation systems."""

    def __init__(self):
        self.security_testing = AutoSecurityTesting()
        self.test_optimizer = AutoTestOptimizer()
        self.integration_testing = AutoIntegrationTesting()
        self.cicd_generator = AutoCICDGenerator()
        self.doc_generator = AutoDocumentationGenerator()
        self.job_history = []
        self.alert_history = []

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
            trend=self._get_trend("cpu"),
            threshold_warning=80.0,
            threshold_critical=95.0
        ))

        # Memory Usage
        memory = psutil.virtual_memory()
        metrics.append(SystemMetric(
            name="Memory Usage",
            value=memory.percent,
            unit="%",
            timestamp=now,
            status=self._get_metric_status(memory.percent, 80, 90),
            trend=self._get_trend("memory"),
            threshold_warning=80.0,
            threshold_critical=90.0
        ))

        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        metrics.append(SystemMetric(
            name="Disk Usage",
            value=disk_percent,
            unit="%",
            timestamp=now,
            status=self._get_metric_status(disk_percent, 80, 95),
            trend=self._get_trend("disk"),
            threshold_warning=80.0,
            threshold_critical=95.0
        ))

        # Network I/O
        network = psutil.net_io_counters()
        metrics.append(SystemMetric(
            name="Network I/O",
            value=network.bytes_sent + network.bytes_recv,
            unit="bytes",
            timestamp=now,
            status=SystemStatus.HEALTHY,
            trend=self._get_trend("network")
        ))

        return metrics

    def collect_test_generation_stats(self) -> TestGenerationStats:
        """Collect test generation statistics."""
        # Count generated test files
        test_dirs = ['tests_generated', 'tests_python', 'tests_java', 'tests_mixed_python', 'tests_mixed_java']
        total_tests = 0
        today_tests = 0
        today = datetime.now().date()

        for test_dir in test_dirs:
            test_path = os.path.join('.', test_dir)
            if os.path.exists(test_path):
                for root, dirs, files in os.walk(test_path):
                    for file in files:
                        if file.startswith('test_') and file.endswith('.py'):
                            total_tests += 1
                            file_path = os.path.join(root, file)
                            if os.path.exists(file_path):
                                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                                if file_time.date() == today:
                                    today_tests += 1

        return TestGenerationStats(
            total_tests_generated=total_tests,
            tests_generated_today=today_tests,
            success_rate=95.0,  # Placeholder - would be calculated from actual data
            average_generation_time=2.5,  # Placeholder
            languages_supported=['Python', 'Java'],
            frameworks_supported=['pytest', 'JUnit', 'Flask', 'FastAPI', 'Django'],
            last_generation=datetime.now() - timedelta(minutes=30)
        )

    def collect_security_stats(self) -> SecurityStats:
        """Collect security testing statistics."""
        # Check for security analysis files
        security_files = ['security_analysis.txt', 'security_example.py']
        vulnerabilities_found = 0
        vulnerabilities_fixed = 0
        critical_vulnerabilities = 0

        for security_file in security_files:
            if os.path.exists(security_file):
                try:
                    with open(security_file, 'r') as f:
                        content = f.read()
                        if 'VULNERABILITIES FOUND:' in content:
                            # Parse vulnerability count
                            lines = content.split('\n')
                            for line in lines:
                                if 'VULNERABILITIES FOUND:' in line:
                                    try:
                                        vulnerabilities_found = int(line.split(':')[1].strip())
                                    except:
                                        vulnerabilities_found = 0
                                elif 'CRITICAL VULNERABILITIES FIXED' in line:
                                    try:
                                        vulnerabilities_fixed = int(line.split(':')[1].strip())
                                    except:
                                        vulnerabilities_fixed = 0
                        break
                except Exception:
                    pass

        return SecurityStats(
            total_vulnerabilities_found=vulnerabilities_found,
            vulnerabilities_fixed=vulnerabilities_fixed,
            critical_vulnerabilities=critical_vulnerabilities,
            security_tests_generated=1,  # Placeholder
            last_scan=datetime.now() - timedelta(hours=2),
            scan_coverage=85.0
        )

    def collect_cicd_stats(self) -> CICDStats:
        """Collect CI/CD pipeline statistics."""
        # Check for CI/CD configuration files
        cicd_files = ['.github/workflows', 'Jenkinsfile', '.gitlab-ci.yml', 'azure-pipelines.yml']
        total_configs = 0
        
        for cicd_file in cicd_files:
            if os.path.exists(cicd_file):
                total_configs += 1

        return CICDStats(
            total_builds=total_configs * 10,  # Placeholder
            successful_builds=int(total_configs * 10 * 0.85),  # 85% success rate
            failed_builds=int(total_configs * 10 * 0.15),  # 15% failure rate
            average_build_time=5.2,  # Placeholder
            last_build=datetime.now() - timedelta(hours=1),
            active_pipelines=total_configs
        )

    def collect_performance_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()

        return PerformanceMetrics(
            cpu_usage=cpu_percent,
            memory_usage=memory.percent,
            disk_usage=(disk.used / disk.total) * 100,
            network_io=network.bytes_sent + network.bytes_recv,
            response_time=0.15,  # Placeholder - would be measured
            throughput=1000.0,  # Placeholder
            error_rate=0.02,  # 2% error rate
            timestamp=datetime.now()
        )

    def get_active_jobs(self) -> List[AutomationJob]:
        """Get currently active automation jobs."""
        # This would typically connect to a job queue or database
        # For now, return placeholder data
        return [
            AutomationJob(
                job_id="job_001",
                job_type=AutomationType.TEST_GENERATION,
                status="running",
                progress=75.0,
                started_at=datetime.now() - timedelta(minutes=5),
                result_summary={"tests_generated": 15, "coverage": 85.0}
            ),
            AutomationJob(
                job_id="job_002",
                job_type=AutomationType.SECURITY_TESTING,
                status="completed",
                progress=100.0,
                started_at=datetime.now() - timedelta(minutes=10),
                completed_at=datetime.now() - timedelta(minutes=2),
                result_summary={"vulnerabilities_found": 0, "security_tests": 5}
            )
        ]

    def get_recent_jobs(self, limit: int = 10) -> List[AutomationJob]:
        """Get recent automation jobs."""
        # This would typically query a database
        # For now, return placeholder data
        recent_jobs = []
        job_types = list(AutomationType)
        
        for i in range(min(limit, len(job_types))):
            job_type = job_types[i]
            recent_jobs.append(AutomationJob(
                job_id=f"job_{i+1:03d}",
                job_type=job_type,
                status="completed",
                progress=100.0,
                started_at=datetime.now() - timedelta(hours=i),
                completed_at=datetime.now() - timedelta(hours=i-1),
                result_summary={"status": "success", "items_processed": 10 + i}
            ))
        
        return recent_jobs

    def get_alerts(self) -> List[Alert]:
        """Get current system alerts."""
        alerts = []
        now = datetime.now()

        # Check system metrics for alerts
        metrics = self.collect_system_metrics()
        for metric in metrics:
            if metric.status == SystemStatus.WARNING:
                alerts.append(Alert(
                    alert_id=f"warning_{metric.name.lower().replace(' ', '_')}",
                    severity="warning",
                    title=f"{metric.name} Warning",
                    message=f"{metric.name} is at {metric.value}{metric.unit}",
                    source="system_monitor",
                    timestamp=now,
                    actions=["investigate", "scale_resources"]
                ))
            elif metric.status == SystemStatus.ERROR:
                alerts.append(Alert(
                    alert_id=f"error_{metric.name.lower().replace(' ', '_')}",
                    severity="error",
                    title=f"{metric.name} Critical",
                    message=f"{metric.name} is critically high at {metric.value}{metric.unit}",
                    source="system_monitor",
                    timestamp=now,
                    actions=["immediate_action", "alert_team"]
                ))

        return alerts

    def _get_metric_status(self, value: float, warning_threshold: float, critical_threshold: float) -> SystemStatus:
        """Determine metric status based on thresholds."""
        if value >= critical_threshold:
            return SystemStatus.ERROR
        elif value >= warning_threshold:
            return SystemStatus.WARNING
        else:
            return SystemStatus.HEALTHY

    def _get_trend(self, metric_name: str) -> Optional[str]:
        """Get trend for a metric (placeholder implementation)."""
        # This would typically compare with historical data
        trends = ["up", "down", "stable"]
        return trends[hash(metric_name) % len(trends)]

    def collect_all_data(self) -> DashboardData:
        """Collect all dashboard data."""
        return DashboardData(
            system_status=SystemStatus.HEALTHY,
            metrics=self.collect_system_metrics(),
            active_jobs=self.get_active_jobs(),
            recent_jobs=self.get_recent_jobs(),
            test_stats=self.collect_test_generation_stats(),
            security_stats=self.collect_security_stats(),
            cicd_stats=self.collect_cicd_stats(),
            performance=self.collect_performance_metrics(),
            alerts=self.get_alerts(),
            last_updated=datetime.now()
        )
