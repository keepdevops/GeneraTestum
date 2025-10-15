"""
Dashboard widget component generators.
"""

from typing import Dict, List, Any


class DashboardWidgetComponents:
    """Individual dashboard widget component generators."""
    
    @staticmethod
    def generate_metric_card(metric: Dict[str, Any]) -> str:
        """Generate a single metric card."""
        status_class = metric.get('status', 'healthy')
        value = metric.get('value', 0)
        unit = metric.get('unit', '')
        name = metric.get('name', 'Unknown')
        
        return f"""
        <div class="metric-card">
            <div class="metric-value">{value}{unit}</div>
            <div class="metric-label">{name}</div>
            <div class="status-indicator {status_class}"></div>
        </div>
        """
    
    @staticmethod
    def generate_job_item(job: Dict[str, Any]) -> str:
        """Generate a single job item."""
        status_class = job.get('status', 'unknown')
        progress = job.get('progress', 0)
        job_type = job.get('job_type', 'Unknown').replace('_', ' ').title()
        
        return f"""
        <div class="job-item {status_class}">
            <div>
                <strong>{job_type}</strong>
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
    
    @staticmethod
    def generate_alert_item(alert: Dict[str, Any]) -> str:
        """Generate a single alert item."""
        level = alert.get('level', 'info')
        message = alert.get('message', 'Unknown alert')
        timestamp = alert.get('timestamp', '')
        
        return f"""
        <div class="alert-item alert-{level}">
            <div class="alert-message">{message}</div>
            <div class="alert-timestamp">{timestamp}</div>
        </div>
        """
    
    @staticmethod
    def generate_status_indicator(status: str) -> str:
        """Generate a status indicator."""
        return f'<span class="status-indicator status-{status}"></span>'
    
    @staticmethod
    def generate_progress_bar(progress: int, label: str = "") -> str:
        """Generate a progress bar."""
        return f"""
        <div class="progress-container">
            {f'<div class="progress-label">{label}</div>' if label else ''}
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <div class="progress-text">{progress}%</div>
        </div>
        """
    
    @staticmethod
    def generate_chart_bar(data: List[Dict[str, Any]]) -> str:
        """Generate a bar chart."""
        if not data:
            return '<div class="chart-container">No data available</div>'
        
        bars = ""
        max_value = max([item.get('value', 0) for item in data])
        
        for item in data:
            value = item.get('value', 0)
            label = item.get('label', '')
            height_percent = (value / max_value * 100) if max_value > 0 else 0
            
            bars += f"""
            <div class="chart-bar-item" style="height: {height_percent}%" title="{label}: {value}">
            </div>
            """
        
        return f"""
        <div class="chart-container">
            <div class="chart-bar">
                {bars}
            </div>
        </div>
        """
    
    @staticmethod
    def generate_gauge(value: int, max_value: int = 100, label: str = "") -> str:
        """Generate a gauge chart."""
        percentage = (value / max_value * 100) if max_value > 0 else 0
        
        return f"""
        <div class="gauge-container">
            <div class="gauge-circle">
                <div class="gauge-inner">
                    {percentage:.0f}%
                </div>
            </div>
            {f'<div class="gauge-label">{label}</div>' if label else ''}
        </div>
        """
    
    @staticmethod
    def generate_stat_card(title: str, value: Any, subtitle: str = "", status: str = "") -> str:
        """Generate a statistics card."""
        status_html = f'<div class="status-indicator status-{status}"></div>' if status else ''
        
        return f"""
        <div class="stat-card">
            <div class="stat-header">
                <h3>{title}</h3>
                {status_html}
            </div>
            <div class="stat-value">{value}</div>
            {f'<div class="stat-subtitle">{subtitle}</div>' if subtitle else ''}
        </div>
        """
    
    @staticmethod
    def generate_list_item(text: str, icon: str = "", status: str = "") -> str:
        """Generate a list item."""
        icon_html = f'<span class="item-icon">{icon}</span>' if icon else ''
        status_html = f'<span class="status-indicator status-{status}"></span>' if status else ''
        
        return f"""
        <div class="list-item">
            {icon_html}
            <span class="item-text">{text}</span>
            {status_html}
        </div>
        """
