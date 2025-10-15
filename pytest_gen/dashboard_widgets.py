"""
Dashboard widget generators.
"""

from typing import Dict, List, Any


class DashboardWidgets:
    """Dashboard widget content generators."""
    
    @staticmethod
    def generate_metrics_widget(metrics: List[Dict[str, Any]]) -> str:
        """Generate system metrics widget content."""
        if not metrics:
            return '<div class="loading">No metrics available</div>'
        
        metric_cards = ""
        for metric in metrics:
            status_class = metric.get('status', 'healthy')
            metric_cards += f"""
            <div class="metric-card">
                <div class="metric-value">{metric.get('value', 0)}{metric.get('unit', '')}</div>
                <div class="metric-label">{metric.get('name', 'Unknown')}</div>
                <div class="status-indicator {status_class}"></div>
            </div>
            """
        
        return metric_cards

    @staticmethod
    def generate_jobs_widget(jobs: List[Dict[str, Any]]) -> str:
        """Generate automation jobs widget content."""
        if not jobs:
            return '<div class="loading">No active jobs</div>'
        
        job_items = ""
        for job in jobs:
            status_class = job.get('status', 'unknown')
            progress = job.get('progress', 0)
            job_items += f"""
            <div class="job-item {status_class}">
                <div>
                    <strong>{job.get('job_type', 'Unknown').replace('_', ' ').title()}</strong>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {progress}%"></div>
                    </div>
                    <small>Progress: {progress}%</small>
                </div>
                <div>
                    <span class="status-indicator {status_class}"></span>
                </div>
            </div>
            """
        
        return job_items

    @staticmethod
    def generate_alerts_widget(alerts: List[Dict[str, Any]]) -> str:
        """Generate alerts widget content."""
        if not alerts:
            return '<div class="loading">No alerts</div>'
        
        alert_items = ""
        for alert in alerts:
            severity = alert.get('severity', 'info')
            alert_items += f"""
            <div class="alert-item {severity}">
                <div class="alert-title">{alert.get('title', 'Unknown Alert')}</div>
                <div class="alert-message">{alert.get('message', 'No message')}</div>
                <small>Source: {alert.get('source', 'Unknown')}</small>
            </div>
            """
        
        return alert_items

    @staticmethod
    def generate_test_stats_widget(stats: Dict[str, Any]) -> str:
        """Generate test generation statistics widget content."""
        if not stats:
            return '<div class="loading">No data available</div>', ''
        
        stats_content = f"""
                <div class="stat-item">
                    <div class="stat-number">{stats.get('total_tests_generated', 0)}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('tests_generated_today', 0)}</div>
                    <div class="stat-label">Today</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('success_rate', 0):.1f}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('average_generation_time', 0):.1f}s</div>
                    <div class="stat-label">Avg Time</div>
                </div>
            """
        
        additional_info = f"""
            <strong>Languages:</strong> {', '.join(stats.get('languages_supported', []))}<br>
            <strong>Frameworks:</strong> {', '.join(stats.get('frameworks_supported', []))}
        """
        
        return stats_content, additional_info

    @staticmethod
    def generate_security_stats_widget(stats: Dict[str, Any]) -> str:
        """Generate security statistics widget content."""
        if not stats:
            return '<div class="loading">No data available</div>', '', 'healthy'
        
        status_class = 'error' if stats.get('critical_vulnerabilities', 0) > 0 else 'healthy'
        
        stats_content = f"""
                <div class="stat-item">
                    <div class="stat-number">{stats.get('total_vulnerabilities_found', 0)}</div>
                    <div class="stat-label">Found</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('vulnerabilities_fixed', 0)}</div>
                    <div class="stat-label">Fixed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('critical_vulnerabilities', 0)}</div>
                    <div class="stat-label">Critical</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('security_tests_generated', 0)}</div>
                    <div class="stat-label">Tests</div>
                </div>
            """
        
        additional_info = f"""
            <strong>Coverage:</strong> {stats.get('scan_coverage', 0):.1f}%<br>
            <strong>Last Scan:</strong> {stats.get('last_scan', 'Never')}
        """
        
        return stats_content, additional_info, status_class

    @staticmethod
    def generate_cicd_stats_widget(stats: Dict[str, Any]) -> str:
        """Generate CI/CD statistics widget content."""
        if not stats:
            return '<div class="loading">No data available</div>', '', 'healthy'
        
        success_rate = (stats.get('successful_builds', 0) / max(stats.get('total_builds', 1), 1)) * 100
        status_class = 'healthy' if success_rate > 80 else 'warning'
        
        stats_content = f"""
                <div class="stat-item">
                    <div class="stat-number">{stats.get('total_builds', 0)}</div>
                    <div class="stat-label">Total Builds</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('successful_builds', 0)}</div>
                    <div class="stat-label">Successful</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('failed_builds', 0)}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{success_rate:.1f}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            """
        
        additional_info = f"""
            <strong>Avg Build Time:</strong> {stats.get('average_build_time', 0):.1f}s<br>
            <strong>Active Pipelines:</strong> {stats.get('active_pipelines', 0)}
        """
        
        return stats_content, additional_info, status_class

    @staticmethod
    def generate_performance_widget(performance: Dict[str, Any]) -> str:
        """Generate performance metrics widget content."""
        if not performance:
            return '<div class="loading">No data available</div>', '', 'healthy'
        
        status_class = 'warning' if performance.get('cpu_usage', 0) > 80 else 'healthy'
        
        stats_content = f"""
                <div class="stat-item">
                    <div class="stat-number">{performance.get('cpu_usage', 0):.1f}%</div>
                    <div class="stat-label">CPU</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{performance.get('memory_usage', 0):.1f}%</div>
                    <div class="stat-label">Memory</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{performance.get('response_time', 0):.3f}s</div>
                    <div class="stat-label">Response</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{performance.get('error_rate', 0):.1f}%</div>
                    <div class="stat-label">Error Rate</div>
                </div>
            """
        
        additional_info = f"""
            <strong>Disk Usage:</strong> {performance.get('disk_usage', 0):.1f}%<br>
            <strong>Throughput:</strong> {performance.get('throughput', 0):.0f} req/s
        """
        
        return stats_content, additional_info, status_class
