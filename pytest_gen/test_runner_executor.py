"""
Test execution functionality for automated test runner.
"""

import subprocess
import json
import os
import time
from typing import Dict, List, Any, Optional
from .test_runner_models import TestResult, TestSuiteResult


class TestExecutor:
    """Handles test execution and result parsing."""

    def __init__(self, timeout: int = 300):
        self.timeout = timeout

    def execute_pytest(self, test_path: str, **kwargs) -> Dict[str, Any]:
        """Execute pytest and capture results."""
        cmd = [
            'python', '-m', 'pytest',
            test_path,
            '--json-report',
            '--json-report-file=pytest_report.json',
            '-v',
            '--tb=short'
        ]
        
        # Add coverage if requested
        if kwargs.get('with_coverage', True):
            cmd.extend(['--cov', kwargs.get('source_path', '.')])
            cmd.extend(['--cov-report=term-missing', '--cov-report=json'])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # Parse JSON report if it exists
            if os.path.exists('pytest_report.json'):
                with open('pytest_report.json', 'r') as f:
                    return json.load(f)
            
            # Fallback to parsing stdout
            return self._parse_pytest_output(result.stdout, result.stderr)
            
        except subprocess.TimeoutExpired:
            return {
                'summary': {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'errors': 0
                },
                'tests': [],
                'error': 'Test execution timed out'
            }

    def _parse_pytest_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """Parse pytest output when JSON report is not available."""
        lines = stdout.split('\n')
        tests = []
        summary = {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 0}
        
        for line in lines:
            if '::' in line and ('PASSED' in line or 'FAILED' in line or 'SKIPPED' in line):
                parts = line.split('::')
                if len(parts) >= 2:
                    test_name = parts[-1].split()[0]
                    status = 'passed' if 'PASSED' in line else 'failed' if 'FAILED' in line else 'skipped'
                    
                    tests.append({
                        'nodeid': test_name,
                        'outcome': status,
                        'duration': 0.0,
                        'setup': {'outcome': 'passed'},
                        'call': {'outcome': status},
                        'teardown': {'outcome': 'passed'}
                    })
                    
                    summary[status] += 1
                    summary['total'] += 1
        
        return {
            'summary': summary,
            'tests': tests,
            'stderr': stderr
        }

    def run_coverage_analysis(self, test_path: str) -> Dict[str, Any]:
        """Run coverage analysis."""
        try:
            cmd = [
                'python', '-m', 'coverage', 'run', '-m', 'pytest', test_path
            ]
            
            subprocess.run(cmd, capture_output=True, timeout=60)
            
            # Generate coverage report
            result = subprocess.run(
                ['python', '-m', 'coverage', 'report', '--show-missing'],
                capture_output=True,
                text=True
            )
            
            # Parse coverage percentage
            coverage_lines = result.stdout.split('\n')
            for line in coverage_lines:
                if 'TOTAL' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        coverage_percentage = float(parts[-1].replace('%', ''))
                        return {'coverage_percentage': coverage_percentage}
            
            return {'coverage_percentage': 0.0}
            
        except Exception:
            return {'coverage_percentage': 0.0}
