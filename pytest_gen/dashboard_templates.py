"""
Dashboard HTML templates.
"""

from typing import Dict, Any
from .dashboard_css import DashboardCSS


class DashboardTemplates:
    """Dashboard HTML templates."""
    
    @staticmethod
    def get_base_template() -> str:
        """Get the base HTML template."""
        css = DashboardCSS()
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {css.get_base_styles()}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎛️ Test Generator Automation Dashboard</h1>
        <div class="subtitle">Real-time monitoring of all automation systems</div>
        <div class="status-indicator {{system_status}}"></div>
        <span style="margin-left: 10px;">System Status: <strong>{{system_status}}</strong></span>
    </div>
    
    <div class="dashboard">
        {{metrics_widget}}
        {{jobs_widget}}
        {{alerts_widget}}
        {{test_stats_widget}}
        {{security_stats_widget}}
        {{cicd_stats_widget}}
        {{performance_widget}}
    </div>
    
    <div class="refresh-info">
        Last updated: {{timestamp}} | Auto-refresh every 30 seconds
    </div>
    
    <script>
        {css.get_javascript()}
    </script>
</body>
</html>
"""

    @staticmethod
    def get_widget_template(widget_type: str) -> str:
        """Get widget template by type."""
        templates = {
            'metrics': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">📊 System Metrics</h3>
                <div class="status-indicator healthy"></div>
            </div>
            <div class="metric-grid">
                {content}
            </div>
        </div>
            """,
            'jobs': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">⚙️ Active Jobs</h3>
                <div class="status-indicator healthy"></div>
            </div>
            <div class="job-list">
                {content}
            </div>
        </div>
            """,
            'alerts': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">🚨 Alerts ({count})</h3>
                <div class="status-indicator warning"></div>
            </div>
            <div class="job-list">
                {content}
            </div>
        </div>
            """,
            'test_stats': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">🧪 Test Generation</h3>
                <div class="status-indicator healthy"></div>
            </div>
            <div class="stats-grid">
                {content}
            </div>
            <div style="margin-top: 15px;">
                {additional_info}
            </div>
        </div>
            """,
            'security_stats': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">🔒 Security Testing</h3>
                <div class="status-indicator {status_class}"></div>
            </div>
            <div class="stats-grid">
                {content}
            </div>
            <div style="margin-top: 15px;">
                {additional_info}
            </div>
        </div>
            """,
            'cicd_stats': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">🚀 CI/CD Pipeline</h3>
                <div class="status-indicator {status_class}"></div>
            </div>
            <div class="stats-grid">
                {content}
            </div>
            <div style="margin-top: 15px;">
                {additional_info}
            </div>
        </div>
            """,
            'performance': """
        <div class="widget">
            <div class="widget-header">
                <h3 class="widget-title">⚡ Performance</h3>
                <div class="status-indicator {status_class}"></div>
            </div>
            <div class="stats-grid">
                {content}
            </div>
            <div style="margin-top: 15px;">
                {additional_info}
            </div>
        </div>
            """
        }
        return templates.get(widget_type, "")
