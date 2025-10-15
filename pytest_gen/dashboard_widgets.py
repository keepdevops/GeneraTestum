"""
Dashboard widgets - refactored for 200LOC limit.
"""

from typing import Dict, List, Any
from .dashboard_widget_generators import DashboardWidgetGenerators


class DashboardWidgets:
    """Dashboard widget content generators."""
    
    def __init__(self):
        self.generators = DashboardWidgetGenerators()
    
    def generate_metrics_widget(self, metrics: List[Dict[str, Any]]) -> str:
        """Generate system metrics widget content."""
        return self.generators.generate_metrics_widget(metrics)
    
    def generate_jobs_widget(self, jobs: List[Dict[str, Any]]) -> str:
        """Generate automation jobs widget content."""
        return self.generators.generate_jobs_widget(jobs)
    
    def generate_alerts_widget(self, alerts: List[Dict[str, Any]]) -> str:
        """Generate alerts widget content."""
        return self.generators.generate_alerts_widget(alerts)
    
    def generate_test_stats_widget(self, test_stats: Dict[str, Any]) -> str:
        """Generate test statistics widget."""
        return self.generators.generate_test_stats_widget(test_stats)
    
    def generate_security_stats_widget(self, security_stats: Dict[str, Any]) -> str:
        """Generate security statistics widget."""
        return self.generators.generate_security_stats_widget(security_stats)
    
    def generate_cicd_stats_widget(self, cicd_stats: Dict[str, Any]) -> str:
        """Generate CI/CD statistics widget."""
        return self.generators.generate_cicd_stats_widget(cicd_stats)
    
    def generate_performance_widget(self, performance: Dict[str, Any]) -> str:
        """Generate performance metrics widget."""
        return self.generators.generate_performance_widget(performance)
    
    def generate_system_overview_widget(self, data: Dict[str, Any]) -> str:
        """Generate system overview widget."""
        system_status = data.get('system_status', 'unknown')
        last_updated = data.get('last_updated', '')
        metrics_count = len(data.get('metrics', []))
        jobs_count = len(data.get('active_jobs', []))
        alerts_count = len(data.get('alerts', []))
        
        return f"""
        <div class="system-overview-widget">
            <div class="widget-header">
                <h2 class="widget-title">System Overview</h2>
                <div class="system-status status-{system_status}">
                    <span class="status-indicator status-{system_status}"></span>
                    {system_status.title()}
                </div>
            </div>
            <div class="widget-content">
                <div class="overview-stats">
                    <div class="stat-item">
                        <div class="stat-number">{metrics_count}</div>
                        <div class="stat-label">Metrics</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{jobs_count}</div>
                        <div class="stat-label">Active Jobs</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{alerts_count}</div>
                        <div class="stat-label">Alerts</div>
                    </div>
                </div>
                <div class="last-updated">
                    Last updated: {last_updated}
                </div>
            </div>
        </div>
        """
    
    def generate_quick_actions_widget(self) -> str:
        """Generate quick actions widget."""
        return """
        <div class="quick-actions-widget">
            <div class="widget-header">
                <h2 class="widget-title">Quick Actions</h2>
            </div>
            <div class="widget-content">
                <div class="action-buttons">
                    <button class="action-btn" onclick="refreshDashboard()">
                        <span class="btn-icon">🔄</span>
                        Refresh
                    </button>
                    <button class="action-btn" onclick="runTests()">
                        <span class="btn-icon">🧪</span>
                        Run Tests
                    </button>
                    <button class="action-btn" onclick="generateReports()">
                        <span class="btn-icon">📊</span>
                        Generate Reports
                    </button>
                    <button class="action-btn" onclick="checkSecurity()">
                        <span class="btn-icon">🔒</span>
                        Security Check
                    </button>
                </div>
            </div>
        </div>
        """
    
    def generate_all_widgets(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate all dashboard widgets."""
        return {
            "system_overview": self.generate_system_overview_widget(data),
            "metrics": self.generate_metrics_widget(data.get('metrics', [])),
            "jobs": self.generate_jobs_widget(data.get('active_jobs', [])),
            "alerts": self.generate_alerts_widget(data.get('alerts', [])),
            "test_stats": self.generate_test_stats_widget(data.get('test_stats', {})),
            "security_stats": self.generate_security_stats_widget(data.get('security_stats', {})),
            "cicd_stats": self.generate_cicd_stats_widget(data.get('cicd_stats', {})),
            "performance": self.generate_performance_widget(data.get('performance', {})),
            "quick_actions": self.generate_quick_actions_widget()
        }