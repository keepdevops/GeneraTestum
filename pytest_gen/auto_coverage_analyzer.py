"""
Automatic coverage analysis and gap detection for intelligent test generation.
"""

from typing import Dict, List, Any
from .coverage_models import CoverageReport
from .coverage_executor import CoverageExecutor
from .coverage_analyzer import CoverageGapAnalyzer
from .coverage_reporter import CoverageReporter


class AutoCoverageAnalyzer:
    """Automated coverage analysis and gap detection."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.min_coverage = self.config.get('min_coverage', 80)
        self.ignore_patterns = self.config.get('ignore_patterns', ['__init__.py', 'setup.py'])
        
        # Initialize components
        self.executor = CoverageExecutor()
        self.gap_analyzer = CoverageGapAnalyzer(self.min_coverage, self.ignore_patterns)
        self.reporter = CoverageReporter(self.min_coverage)

    def analyze_coverage(self, source_path: str, test_path: str = None) -> CoverageReport:
        """Analyze code coverage and identify gaps."""
        # Run coverage analysis
        coverage_data = self.executor.run_coverage_analysis(source_path, test_path)
        
        # Analyze coverage gaps
        gaps = self.gap_analyzer.analyze_coverage_gaps(coverage_data)
        
        # Generate recommendations
        recommendations = self.gap_analyzer.generate_recommendations(coverage_data, gaps)
        
        # Identify critical paths
        critical_paths = self.gap_analyzer.identify_critical_paths(coverage_data)
        
        return CoverageReport(
            total_coverage=coverage_data.get('total_coverage', 0),
            file_coverage=coverage_data.get('file_coverage', {}),
            gaps=gaps,
            recommendations=recommendations,
            critical_paths=critical_paths
        )

    def generate_coverage_report(self, report: CoverageReport) -> str:
        """Generate a comprehensive coverage report."""
        return self.reporter.generate_coverage_report(report)

    def auto_generate_missing_tests(self, gaps: List) -> List[str]:
        """Automatically generate test suggestions for missing coverage."""
        return self.reporter.auto_generate_missing_tests(gaps)
