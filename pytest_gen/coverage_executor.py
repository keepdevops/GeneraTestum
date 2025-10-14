"""
Coverage analysis execution functionality.
"""

import subprocess
import json
import os
from typing import Dict, Any


class CoverageExecutor:
    """Handles coverage analysis execution and parsing."""

    def run_coverage_analysis(self, source_path: str, test_path: str = None) -> Dict[str, Any]:
        """Run coverage analysis and return structured data."""
        try:
            # Run coverage
            if test_path:
                cmd = ['python', '-m', 'coverage', 'run', '-m', 'pytest', test_path]
            else:
                cmd = ['python', '-m', 'coverage', 'run', '--source', source_path, '-m', 'pytest']
            
            subprocess.run(cmd, capture_output=True)
            
            # Generate coverage report
            result = subprocess.run(
                ['python', '-m', 'coverage', 'report', '--show-missing', '--skip-covered'],
                capture_output=True,
                text=True
            )
            
            # Parse coverage output
            coverage_data = self._parse_coverage_output(result.stdout)
            
            # Get detailed coverage data
            json_result = subprocess.run(
                ['python', '-m', 'coverage', 'json', '--show-contexts'],
                capture_output=True,
                text=True
            )
            
            if json_result.returncode == 0:
                coverage_data.update(json.loads(json_result.stdout))
            
            return coverage_data
            
        except Exception as e:
            return {'error': str(e), 'total_coverage': 0, 'file_coverage': {}, 'missing_lines': []}

    def _parse_coverage_output(self, output: str) -> Dict[str, Any]:
        """Parse coverage command output."""
        lines = output.split('\n')
        coverage_data = {
            'total_coverage': 0,
            'file_coverage': {},
            'missing_lines': []
        }
        
        for line in lines:
            if '%' in line and 'TOTAL' in line:
                # Extract total coverage
                parts = line.split()
                for part in parts:
                    if part.endswith('%'):
                        coverage_data['total_coverage'] = float(part.replace('%', ''))
                        break
            
            elif '%' in line and not line.startswith('-'):
                # Extract file coverage
                parts = line.split()
                if len(parts) >= 4:
                    file_path = parts[0]
                    coverage_str = parts[-1].replace('%', '')
                    try:
                        coverage_data['file_coverage'][file_path] = float(coverage_str)
                    except ValueError:
                        pass
        
        return coverage_data
