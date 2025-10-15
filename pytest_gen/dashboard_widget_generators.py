"""
Dashboard widget generators for complete widget sections.
"""

from typing import Dict, List, Any
from .dashboard_widget_components import DashboardWidgetComponents


class DashboardWidgetGenerators:
    """Generates complete dashboard widget sections."""
    
    def __init__(self):
        self.components = DashboardWidgetComponents()
    
    def generate_metrics_widget(self, metrics: List[Dict[str, Any]]) -> str:
        """Generate system metrics widget content."""
        if not metrics:
            return '<div class="loading">No metrics available</div>'
        
        metric_cards = ""
        for metric in metrics:
            metric_cards += self.components.generate_metric_card(metric)
        
        return f"""
        <div class="metrics-widget">
            <div class="widget-header">
                <h2 class="widget-title">System Metrics</h2>
                <div class="widget-actions">
                    <button class="refresh-btn">Refresh</button>
                </div>
            </div>
            <div class="widget-content">
                {metric_cards}
            </div>
        </div>
        """
    
    def generate_jobs_widget(self, jobs: List[Dict[str, Any]]) -> str:
        """Generate automation jobs widget content."""
        if not jobs:
            return '<div class="loading">No active jobs</div>'
        
        job_items = ""
        for job in jobs:
            job_items += self.components.generate_job_item(job)
        
        return f"""
        <div class="jobs-widget">
            <div class="widget-header">
                <h2 class="widget-title">Active Jobs</h2>
                <div class="widget-actions">
                    <span class="job-count">{len(jobs)} active</span>
                </div>
            </div>
            <div class="widget-content">
                {job_items}
            </div>
        </div>
        """
    
    def generate_alerts_widget(self, alerts: List[Dict[str, Any]]) -> str:
        """Generate alerts widget content."""
        if not alerts:
            return '<div class="loading">No alerts</div>'
        
        alert_items = ""
        for alert in alerts:
            alert_items += self.components.generate_alert_item(alert)
        
        return f"""
        <div class="alerts-widget">
            <div class="widget-header">
                <h2 class="widget-title">System Alerts</h2>
                <div class="widget-actions">
                    <span class="alert-count">{len(alerts)} total</span>
                </div>
            </div>
            <div class="widget-content">
                {alert_items}
            </div>
        </div>
        """
    
    def generate_test_stats_widget(self, test_stats: Dict[str, Any]) -> str:
        """Generate test statistics widget."""
        stats_cards = ""
        
        # Generate stat cards for key metrics
        stats_data = [
            ("Tests Generated", test_stats.get("tests_generated", 0), "Total test files"),
            ("Success Rate", f"{test_stats.get('success_rate', 0):.1f}%", "Generation success"),
            ("Coverage", f"{test_stats.get('coverage_percentage', 0):.1f}%", "Test coverage"),
            ("Avg Time", f"{test_stats.get('average_generation_time', 0):.1f}s", "Generation time")
        ]
        
        for title, value, subtitle in stats_data:
            stats_cards += self.components.generate_stat_card(title, value, subtitle)
        
        return f"""
        <div class="test-stats-widget">
            <div class="widget-header">
                <h2 class="widget-title">Test Statistics</h2>
            </div>
            <div class="widget-content">
                <div class="stats-grid">
                    {stats_cards}
                </div>
            </div>
        </div>
        """
    
    def generate_security_stats_widget(self, security_stats: Dict[str, Any]) -> str:
        """Generate security statistics widget."""
        vulnerabilities = security_stats.get("vulnerabilities_found", 0)
        critical_issues = security_stats.get("critical_issues", 0)
        security_score = security_stats.get("security_score", 0)
        
        # Generate security gauge
        gauge_html = self.components.generate_gauge(
            int(security_score), 
            100, 
            "Security Score"
        )
        
        # Generate stats
        stats_html = ""
        stats_data = [
            ("Vulnerabilities", vulnerabilities, "critical" if vulnerabilities > 0 else "healthy"),
            ("Critical Issues", critical_issues, "critical" if critical_issues > 0 else "healthy"),
            ("Files Analyzed", security_stats.get("files_analyzed", 0), "info")
        ]
        
        for title, value, status in stats_data:
            stats_html += self.components.generate_stat_card(title, value, "", status)
        
        return f"""
        <div class="security-stats-widget">
            <div class="widget-header">
                <h2 class="widget-title">Security Statistics</h2>
            </div>
            <div class="widget-content">
                <div class="security-gauge">
                    {gauge_html}
                </div>
                <div class="security-stats">
                    {stats_html}
                </div>
            </div>
        </div>
        """
    
    def generate_cicd_stats_widget(self, cicd_stats: Dict[str, Any]) -> str:
        """Generate CI/CD statistics widget."""
        active_pipelines = cicd_stats.get("pipelines_active", 0)
        builds_today = cicd_stats.get("builds_today", 0)
        success_rate = cicd_stats.get("success_rate", 0)
        
        # Generate progress bars
        progress_bars = ""
        progress_data = [
            ("Success Rate", success_rate),
            ("Pipeline Health", 95),  # Simulated
            ("Build Efficiency", 88)  # Simulated
        ]
        
        for label, progress in progress_data:
            progress_bars += self.components.generate_progress_bar(progress, label)
        
        return f"""
        <div class="cicd-stats-widget">
            <div class="widget-header">
                <h2 class="widget-title">CI/CD Statistics</h2>
            </div>
            <div class="widget-content">
                <div class="cicd-overview">
                    <div class="stat-card">
                        <div class="stat-value">{active_pipelines}</div>
                        <div class="stat-label">Active Pipelines</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{builds_today}</div>
                        <div class="stat-label">Builds Today</div>
                    </div>
                </div>
                <div class="cicd-progress">
                    {progress_bars}
                </div>
            </div>
        </div>
        """
    
    def generate_performance_widget(self, performance: Dict[str, Any]) -> str:
        """Generate performance metrics widget."""
        response_time = performance.get("average_response_time", 0)
        throughput = performance.get("throughput", 0)
        error_rate = performance.get("error_rate", 0)
        availability = performance.get("availability", 0)
        
        # Generate performance chart
        chart_data = [
            {"label": "Response Time", "value": response_time * 1000},  # Convert to ms
            {"label": "Throughput", "value": throughput},
            {"label": "Error Rate", "value": error_rate * 100},
            {"label": "Availability", "value": availability}
        ]
        
        chart_html = self.components.generate_chart_bar(chart_data)
        
        return f"""
        <div class="performance-widget">
            <div class="widget-header">
                <h2 class="widget-title">Performance Metrics</h2>
            </div>
            <div class="widget-content">
                <div class="performance-chart">
                    {chart_html}
                </div>
                <div class="performance-summary">
                    <div class="stat-card">
                        <div class="stat-value">{response_time:.2f}s</div>
                        <div class="stat-label">Avg Response</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{throughput:.0f}</div>
                        <div class="stat-label">Throughput</div>
                    </div>
                </div>
            </div>
        </div>
        """
