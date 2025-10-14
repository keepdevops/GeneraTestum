"""
Coverage gap analysis and report generation functionality.
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from .coverage_models import CoverageGap, CoverageReport


class CoverageGapAnalyzer:
    """Analyzes coverage gaps and generates insights."""

    def __init__(self, min_coverage: int = 80, ignore_patterns: List[str] = None):
        self.min_coverage = min_coverage
        self.ignore_patterns = ignore_patterns or ['__init__.py', 'setup.py']

    def analyze_coverage_gaps(self, coverage_data: Dict[str, Any]) -> List[CoverageGap]:
        """Identify specific coverage gaps in the code."""
        gaps = []
        
        if 'files' not in coverage_data:
            return gaps
        
        for file_path, file_data in coverage_data['files'].items():
            # Skip ignored files
            if any(pattern in file_path for pattern in self.ignore_patterns):
                continue
            
            if 'missing_lines' in file_data:
                gaps.extend(self._analyze_file_gaps(file_path, file_data))
        
        # Sort gaps by priority
        gaps.sort(key=lambda gap: self._get_priority_score(gap.priority), reverse=True)
        
        return gaps

    def _analyze_file_gaps(self, file_path: str, file_data: Dict[str, Any]) -> List[CoverageGap]:
        """Analyze coverage gaps for a specific file."""
        gaps = []
        
        if not os.path.exists(file_path):
            return gaps
        
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
            
            lines = file_content.split('\n')
            missing_lines = file_data.get('missing_lines', [])
            
            for line_num in missing_lines:
                if line_num <= len(lines):
                    code_line = lines[line_num - 1].strip()
                    
                    # Skip empty lines and comments
                    if not code_line or code_line.startswith('#'):
                        continue
                    
                    gap = CoverageGap(
                        file_path=file_path,
                        line_number=line_num,
                        code_line=code_line,
                        priority=self._assess_gap_priority(code_line, file_path)
                    )
                    
                    # Analyze function/class context
                    gap.function_name = self._find_function_context(lines, line_num)
                    gap.class_name = self._find_class_context(lines, line_num)
                    
                    # Generate test suggestion
                    gap.test_suggestion = self._generate_test_suggestion(gap)
                    
                    gaps.append(gap)
        
        except Exception:
            pass
        
        return gaps

    def _assess_gap_priority(self, code_line: str, file_path: str) -> str:
        """Assess the priority of a coverage gap."""
        # High priority patterns
        high_priority_patterns = [
            'raise', 'except', 'return', 'yield',
            'if __name__', 'def main', 'def test_',
            'class ', 'def __init__'
        ]
        
        # Low priority patterns
        low_priority_patterns = [
            'import ', 'from ', 'pass', '...',
            'logger.', 'print(', 'debug('
        ]
        
        code_lower = code_line.lower()
        
        if any(pattern in code_lower for pattern in high_priority_patterns):
            return "high"
        elif any(pattern in code_lower for pattern in low_priority_patterns):
            return "low"
        else:
            return "medium"

    def _find_function_context(self, lines: List[str], line_num: int) -> str:
        """Find the function that contains the given line."""
        for i in range(line_num - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('def '):
                # Extract function name
                parts = line.split()
                if len(parts) > 1:
                    func_name = parts[1].split('(')[0]
                    return func_name
        return None

    def _find_class_context(self, lines: List[str], line_num: int) -> str:
        """Find the class that contains the given line."""
        for i in range(line_num - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('class '):
                # Extract class name
                parts = line.split()
                if len(parts) > 1:
                    class_name = parts[1].split('(')[0].split(':')[0]
                    return class_name
        return None

    def _generate_test_suggestion(self, gap: CoverageGap) -> str:
        """Generate a test suggestion for a coverage gap."""
        if gap.function_name:
            if gap.priority == "high":
                return f"Add comprehensive tests for {gap.function_name}() including edge cases and error conditions"
            else:
                return f"Add basic test for {gap.function_name}()"
        elif gap.class_name:
            return f"Add tests for {gap.class_name} class methods and initialization"
        else:
            return "Add integration or end-to-end tests for this code path"

    def _get_priority_score(self, priority: str) -> int:
        """Get numerical score for priority sorting."""
        scores = {'low': 1, 'medium': 2, 'high': 3}
        return scores.get(priority, 2)

    def generate_recommendations(self, coverage_data: Dict[str, Any], gaps: List[CoverageGap]) -> List[str]:
        """Generate recommendations based on coverage analysis."""
        recommendations = []
        
        total_coverage = coverage_data.get('total_coverage', 0)
        
        if total_coverage < self.min_coverage:
            recommendations.append(f"Increase overall coverage from {total_coverage:.1f}% to at least {self.min_coverage}%")
        
        # Analyze file coverage
        low_coverage_files = [
            file_path for file_path, coverage in coverage_data.get('file_coverage', {}).items()
            if coverage < self.min_coverage
        ]
        
        if low_coverage_files:
            recommendations.append(f"Focus on files with low coverage: {', '.join(low_coverage_files[:5])}")
        
        # Analyze gap priorities
        high_priority_gaps = [gap for gap in gaps if gap.priority == "high"]
        if high_priority_gaps:
            recommendations.append(f"Address {len(high_priority_gaps)} high-priority coverage gaps")
        
        # Suggest test types
        if any('def ' in gap.code_line for gap in gaps):
            recommendations.append("Add unit tests for uncovered functions")
        
        if any('class ' in gap.code_line for gap in gaps):
            recommendations.append("Add class tests for uncovered classes")
        
        if any('if ' in gap.code_line or 'except ' in gap.code_line for gap in gaps):
            recommendations.append("Add conditional and exception handling tests")
        
        return recommendations

    def identify_critical_paths(self, coverage_data: Dict[str, Any]) -> List[str]:
        """Identify critical code paths that need testing."""
        critical_paths = []
        
        if 'files' not in coverage_data:
            return critical_paths
        
        for file_path, file_data in coverage_data['files'].items():
            # Look for critical patterns
            if any(pattern in file_path.lower() for pattern in ['main', 'core', 'engine', 'handler']):
                missing_lines = file_data.get('missing_lines', [])
                if missing_lines:
                    critical_paths.append(f"{file_path}: {len(missing_lines)} uncovered lines")
        
        return critical_paths
