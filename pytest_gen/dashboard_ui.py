"""
Dashboard UI components and HTML templates.
"""

from typing import Dict, List, Any
from datetime import datetime
from .dashboard_templates import DashboardTemplates
from .dashboard_widgets import DashboardWidgets


class DashboardUI:
    """Dashboard UI components and templates."""

    def __init__(self):
        self.templates = DashboardTemplates()
        self.widgets = DashboardWidgets()

    def generate_dashboard_html(self, data: Dict[str, Any]) -> str:
        """Generate complete dashboard HTML."""
        # Generate widget content
        metrics_content = self.widgets.generate_metrics_widget(data.get('metrics', []))
        jobs_content = self.widgets.generate_jobs_widget(data.get('active_jobs', []))
        alerts_content = self.widgets.generate_alerts_widget(data.get('alerts', []))
        
        test_stats_content, test_additional = self.widgets.generate_test_stats_widget(data.get('test_stats', {}))
        security_content, security_additional, security_status = self.widgets.generate_security_stats_widget(data.get('security_stats', {}))
        cicd_content, cicd_additional, cicd_status = self.widgets.generate_cicd_stats_widget(data.get('cicd_stats', {}))
        perf_content, perf_additional, perf_status = self.widgets.generate_performance_widget(data.get('performance', {}))
        
        # Generate widget HTML using templates
        metrics_widget = self.templates.get_widget_template('metrics').format(content=metrics_content)
        jobs_widget = self.templates.get_widget_template('jobs').format(content=jobs_content)
        alerts_widget = self.templates.get_widget_template('alerts').format(
            content=alerts_content, 
            count=len(data.get('alerts', []))
        )
        test_stats_widget = self.templates.get_widget_template('test_stats').format(
            content=test_stats_content,
            additional_info=test_additional
        )
        security_stats_widget = self.templates.get_widget_template('security_stats').format(
            content=security_content,
            additional_info=security_additional,
            status_class=security_status
        )
        cicd_stats_widget = self.templates.get_widget_template('cicd_stats').format(
            content=cicd_content,
            additional_info=cicd_additional,
            status_class=cicd_status
        )
        performance_widget = self.templates.get_widget_template('performance').format(
            content=perf_content,
            additional_info=perf_additional,
            status_class=perf_status
        )
        
        # Generate complete HTML
        html = self.templates.get_base_template().format(
            title="Test Generator Automation Dashboard",
            timestamp=data.get('last_updated', datetime.now().isoformat()),
            system_status=data.get('system_status', 'healthy'),
            metrics_widget=metrics_widget,
            jobs_widget=jobs_widget,
            alerts_widget=alerts_widget,
            test_stats_widget=test_stats_widget,
            security_stats_widget=security_stats_widget,
            cicd_stats_widget=cicd_stats_widget,
            performance_widget=performance_widget
        )
        return html

    def _create_widget_templates(self) -> Dict[str, str]:
        """Create widget templates."""
        return {
            'metrics': self.widgets.generate_metrics_widget,
            'jobs': self.widgets.generate_jobs_widget,
            'alerts': self.widgets.generate_alerts_widget,
            'test_stats': self.widgets.generate_test_stats_widget,
            'security_stats': self.widgets.generate_security_stats_widget,
            'cicd_stats': self.widgets.generate_cicd_stats_widget,
            'performance': self.widgets.generate_performance_widget
        }