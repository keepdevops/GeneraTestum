"""
Dashboard data models and structures.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum


class SystemStatus(Enum):
    """System status enumeration."""
    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class AutomationType(Enum):
    """Automation type enumeration."""
    TEST_GENERATION = "test_generation"
    SECURITY_TESTING = "security_testing"
    CI_CD = "ci_cd"
    DOCUMENTATION = "documentation"
    OPTIMIZATION = "optimization"
    INTEGRATION_TESTING = "integration_testing"


@dataclass
class SystemMetric:
    """System metric data."""
    name: str
    value: Union[int, float, str]
    unit: str
    timestamp: datetime
    status: SystemStatus
    trend: Optional[str] = None  # 'up', 'down', 'stable'
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None


@dataclass
class AutomationJob:
    """Automation job status."""
    job_id: str
    job_type: AutomationType
    status: str  # 'running', 'completed', 'failed', 'queued'
    progress: float  # 0.0 to 100.0
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result_summary: Optional[Dict[str, Any]] = None


@dataclass
class TestGenerationStats:
    """Test generation statistics."""
    total_tests_generated: int
    tests_generated_today: int
    success_rate: float
    average_generation_time: float
    languages_supported: List[str]
    frameworks_supported: List[str]
    last_generation: Optional[datetime] = None


@dataclass
class SecurityStats:
    """Security testing statistics."""
    total_vulnerabilities_found: int
    vulnerabilities_fixed: int
    critical_vulnerabilities: int
    security_tests_generated: int
    last_scan: Optional[datetime] = None
    scan_coverage: float = 0.0


@dataclass
class CICDStats:
    """CI/CD pipeline statistics."""
    total_builds: int
    successful_builds: int
    failed_builds: int
    average_build_time: float
    last_build: Optional[datetime] = None
    active_pipelines: int = 0


@dataclass
class PerformanceMetrics:
    """Performance metrics."""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: float
    response_time: float
    throughput: float
    error_rate: float
    timestamp: datetime


@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""
    widget_id: str
    widget_type: str  # 'metric', 'chart', 'table', 'status', 'alert'
    title: str
    position: Dict[str, int]  # x, y, width, height
    data_source: str
    refresh_interval: int = 30  # seconds
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""
    layout_id: str
    name: str
    description: str
    widgets: List[DashboardWidget]
    theme: str = "dark"
    auto_refresh: bool = True
    refresh_interval: int = 30


@dataclass
class Alert:
    """System alert."""
    alert_id: str
    severity: str  # 'info', 'warning', 'error', 'critical'
    title: str
    message: str
    source: str
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False
    actions: List[str] = field(default_factory=list)


@dataclass
class DashboardData:
    """Complete dashboard data."""
    system_status: SystemStatus
    metrics: List[SystemMetric]
    active_jobs: List[AutomationJob]
    recent_jobs: List[AutomationJob]
    test_stats: TestGenerationStats
    security_stats: SecurityStats
    cicd_stats: CICDStats
    performance: PerformanceMetrics
    alerts: List[Alert]
    last_updated: datetime


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    title: str = "Test Generator Automation Dashboard"
    description: str = "Real-time monitoring of all automation systems"
    version: str = "1.0.0"
    default_layout: str = "default"
    layouts: List[DashboardLayout] = field(default_factory=list)
    auto_refresh: bool = True
    refresh_interval: int = 30
    max_history: int = 1000
    alert_retention_days: int = 30


@dataclass
class UserPreference:
    """User dashboard preferences."""
    user_id: str
    preferred_layout: str
    widget_configs: Dict[str, Dict[str, Any]]
    theme: str = "dark"
    notifications_enabled: bool = True
    email_alerts: bool = False
    refresh_interval: int = 30


@dataclass
class DashboardEvent:
    """Dashboard event for real-time updates."""
    event_type: str  # 'metric_update', 'job_status', 'alert', 'system_status'
    event_data: Dict[str, Any]
    timestamp: datetime
    source: str
    priority: int = 0  # 0=low, 1=medium, 2=high, 3=critical
