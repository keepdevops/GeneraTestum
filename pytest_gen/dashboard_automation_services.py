"""
Automation services integration for dashboard data collection.
"""

import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .dashboard_models import (
    AutomationJob, AutomationType, JobStatus, TestGenerationStats, 
    SecurityStats, CICDStats, PerformanceMetrics, Alert, AlertLevel
)


class AutomationServicesCollector:
    """Collects data from automation services."""
    
    def __init__(self):
        self.job_history = []
        self.alert_history = []
        self.start_time = datetime.now()
    
    def get_active_jobs(self) -> List[AutomationJob]:
        """Get currently active automation jobs."""
        jobs = []
        
        # Simulate active jobs (in real implementation, this would query actual services)
        jobs.extend(self._get_test_generation_jobs())
        jobs.extend(self._get_security_testing_jobs())
        jobs.extend(self._get_cicd_jobs())
        
        return jobs
    
    def _get_test_generation_jobs(self) -> List[AutomationJob]:
        """Get test generation jobs."""
        jobs = []
        
        # Check for files in test directories
        test_dirs = ["tests_generated", "tests", "test_output"]
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                files = os.listdir(test_dir)
                if files:
                    jobs.append(AutomationJob(
                        id=f"test_gen_{test_dir}",
                        name=f"Test Generation - {test_dir}",
                        type=AutomationType.TEST_GENERATION,
                        status=JobStatus.RUNNING,
                        progress=min(len(files) * 10, 100),
                        started_at=datetime.now() - timedelta(minutes=5),
                        estimated_completion=datetime.now() + timedelta(minutes=2)
                    ))
        
        return jobs
    
    def _get_security_testing_jobs(self) -> List[AutomationJob]:
        """Get security testing jobs."""
        jobs = []
        
        # Check for security analysis files
        if os.path.exists("security_analysis.txt"):
            jobs.append(AutomationJob(
                id="security_scan_001",
                name="Security Analysis Scan",
                type=AutomationType.SECURITY_TESTING,
                status=JobStatus.COMPLETED,
                progress=100,
                started_at=datetime.now() - timedelta(hours=1),
                estimated_completion=datetime.now()
            ))
        
        return jobs
    
    def _get_cicd_jobs(self) -> List[AutomationJob]:
        """Get CI/CD pipeline jobs."""
        jobs = []
        
        # Check for CI/CD configuration files
        cicd_files = ["azure-pipelines.yml", "Jenkinsfile", ".gitlab-ci.yml", ".github/workflows"]
        for cicd_file in cicd_files:
            if os.path.exists(cicd_file):
                jobs.append(AutomationJob(
                    id=f"cicd_{cicd_file.replace('.', '_').replace('/', '_')}",
                    name=f"CI/CD Pipeline - {cicd_file}",
                    type=AutomationType.CICD,
                    status=JobStatus.RUNNING,
                    progress=75,
                    started_at=datetime.now() - timedelta(minutes=15),
                    estimated_completion=datetime.now() + timedelta(minutes=5)
                ))
        
        return jobs
    
    def get_test_statistics(self) -> TestGenerationStats:
        """Get test generation statistics."""
        stats = {
            "tests_generated": 0,
            "total_files_processed": 0,
            "success_rate": 0.0,
            "average_generation_time": 0.0,
            "coverage_percentage": 0.0
        }
        
        # Count generated test files
        test_dirs = ["tests_generated", "tests", "test_output", "tests_python", "tests_java"]
        total_tests = 0
        total_files = 0
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                files = os.listdir(test_dir)
                test_files = [f for f in files if f.startswith("test_") and f.endswith(".py")]
                total_tests += len(test_files)
                total_files += len(files)
        
        if total_files > 0:
            stats["tests_generated"] = total_tests
            stats["total_files_processed"] = total_files
            stats["success_rate"] = (total_tests / total_files) * 100 if total_files > 0 else 0
            stats["average_generation_time"] = 2.5  # Simulated
            stats["coverage_percentage"] = 85.5  # Simulated
        
        return stats
    
    def get_security_statistics(self) -> SecurityStats:
        """Get security testing statistics."""
        stats = {
            "vulnerabilities_found": 0,
            "files_analyzed": 0,
            "critical_issues": 0,
            "security_score": 0.0
        }
        
        # Check security analysis file
        if os.path.exists("security_analysis.txt"):
            try:
                with open("security_analysis.txt", "r") as f:
                    content = f.read()
                    if "critical" in content.lower():
                        stats["critical_issues"] = 1
                    stats["vulnerabilities_found"] = content.count("vulnerability")
                    stats["files_analyzed"] = content.count("file")
                    stats["security_score"] = 95.0 if stats["critical_issues"] == 0 else 75.0
            except Exception:
                pass
        
        return stats
    
    def get_cicd_statistics(self) -> CICDStats:
        """Get CI/CD pipeline statistics."""
        stats = {
            "pipelines_active": 0,
            "builds_today": 0,
            "success_rate": 0.0,
            "average_build_time": 0.0
        }
        
        # Check for CI/CD files
        cicd_files = ["azure-pipelines.yml", "Jenkinsfile", ".gitlab-ci.yml"]
        active_pipelines = 0
        
        for cicd_file in cicd_files:
            if os.path.exists(cicd_file):
                active_pipelines += 1
        
        stats["pipelines_active"] = active_pipelines
        stats["builds_today"] = active_pipelines * 3  # Simulated
        stats["success_rate"] = 95.0  # Simulated
        stats["average_build_time"] = 8.5  # Simulated
        
        return stats
    
    def get_alerts(self) -> List[Alert]:
        """Get system alerts."""
        alerts = []
        
        # Check for recent errors or issues
        if os.path.exists("error.log"):
            alerts.append(Alert(
                id="error_log_001",
                message="Error log file detected",
                level=AlertLevel.WARNING,
                timestamp=datetime.now() - timedelta(hours=2),
                category="system",
                resolved=False
            ))
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            free_percent = (free / total) * 100
            
            if free_percent < 10:
                alerts.append(Alert(
                    id="disk_space_001",
                    message=f"Low disk space: {free_percent:.1f}% free",
                    level=AlertLevel.CRITICAL,
                    timestamp=datetime.now(),
                    category="system",
                    resolved=False
                ))
        except Exception:
            pass
        
        return alerts
    
    def get_uptime(self) -> str:
        """Get system uptime."""
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
