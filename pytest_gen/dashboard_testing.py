"""
Dashboard testing and validation utilities.
"""

import asyncio
from typing import Dict, Any
from .dashboard_backend import DashboardDataCollector
from .dashboard_models import DashboardData


class DashboardTester:
    """Tests dashboard functionality and data collection."""
    
    def __init__(self):
        self.data_collector = DashboardDataCollector()
    
    async def test_dashboard_functionality(self) -> Dict[str, Any]:
        """Test complete dashboard functionality."""
        test_results = {
            "status": "success",
            "tests_passed": 0,
            "tests_failed": 0,
            "test_details": {},
            "data_summary": {}
        }
        
        try:
            # Test 1: Data Collection
            data_result = await self._test_data_collection()
            test_results["test_details"]["data_collection"] = data_result
            if data_result["success"]:
                test_results["tests_passed"] += 1
                test_results["data_summary"] = data_result["data_summary"]
            else:
                test_results["tests_failed"] += 1
            
            # Test 2: System Status
            status_result = await self._test_system_status()
            test_results["test_details"]["system_status"] = status_result
            if status_result["success"]:
                test_results["tests_passed"] += 1
            else:
                test_results["tests_failed"] += 1
            
            # Test 3: Metrics Collection
            metrics_result = await self._test_metrics_collection()
            test_results["test_details"]["metrics_collection"] = metrics_result
            if metrics_result["success"]:
                test_results["tests_passed"] += 1
            else:
                test_results["tests_failed"] += 1
            
            # Test 4: Jobs and Alerts
            jobs_result = await self._test_jobs_and_alerts()
            test_results["test_details"]["jobs_and_alerts"] = jobs_result
            if jobs_result["success"]:
                test_results["tests_passed"] += 1
            else:
                test_results["tests_failed"] += 1
            
            # Overall status
            if test_results["tests_failed"] > 0:
                test_results["status"] = "partial_failure"
            if test_results["tests_failed"] == test_results["tests_passed"]:
                test_results["status"] = "failure"
            
        except Exception as e:
            test_results["status"] = "error"
            test_results["error"] = str(e)
        
        return test_results
    
    async def _test_data_collection(self) -> Dict[str, Any]:
        """Test data collection functionality."""
        try:
            data = self.data_collector.collect_all_data()
            
            return {
                "success": True,
                "message": "Data collection successful",
                "data_summary": {
                    "system_status": data.system_status.value,
                    "metrics_count": len(data.metrics),
                    "active_jobs": len(data.active_jobs),
                    "alerts_count": len(data.alerts)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Data collection failed: {str(e)}",
                "data_summary": {}
            }
    
    async def _test_system_status(self) -> Dict[str, Any]:
        """Test system status functionality."""
        try:
            status = self.data_collector.get_system_status()
            
            return {
                "success": True,
                "message": "System status check successful",
                "status": status.value
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"System status check failed: {str(e)}",
                "status": "unknown"
            }
    
    async def _test_metrics_collection(self) -> Dict[str, Any]:
        """Test metrics collection functionality."""
        try:
            metrics = self.data_collector.get_metrics()
            
            return {
                "success": True,
                "message": "Metrics collection successful",
                "metrics_count": len(metrics),
                "metric_types": list(set([m.category.value for m in metrics]))
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Metrics collection failed: {str(e)}",
                "metrics_count": 0
            }
    
    async def _test_jobs_and_alerts(self) -> Dict[str, Any]:
        """Test jobs and alerts functionality."""
        try:
            jobs = self.data_collector.get_active_jobs()
            alerts = self.data_collector.get_alerts()
            
            return {
                "success": True,
                "message": "Jobs and alerts collection successful",
                "jobs_count": len(jobs),
                "alerts_count": len(alerts),
                "unresolved_alerts": len([a for a in alerts if not a.resolved])
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Jobs and alerts collection failed: {str(e)}",
                "jobs_count": 0,
                "alerts_count": 0
            }
    
    def validate_dashboard_data(self, data: DashboardData) -> Dict[str, Any]:
        """Validate dashboard data integrity."""
        issues = []
        
        # Check required fields
        if not data.system_status:
            issues.append("Missing system status")
        
        if not data.metrics:
            issues.append("No metrics available")
        
        if data.last_updated is None:
            issues.append("Missing last updated timestamp")
        
        # Check data consistency
        critical_alerts = [a for a in data.alerts if a.level.value == "critical" and not a.resolved]
        if critical_alerts and data.system_status.value == "healthy":
            issues.append("System shows healthy despite critical alerts")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "data_integrity_score": max(0, 100 - len(issues) * 10)
        }
