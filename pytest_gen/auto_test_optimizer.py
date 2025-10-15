"""
Automatic test suite performance optimization and execution time analysis.
"""

import ast
import os
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestPerformanceMetrics:
    """Test performance metrics."""
    test_name: str
    execution_time: float
    memory_usage: float
    complexity_score: int
    dependency_count: int
    mock_count: int
    assertion_count: int


@dataclass
class OptimizationSuggestion:
    """Test optimization suggestion."""
    test_name: str
    suggestion_type: str  # 'parallelize', 'mock_optimization', 'fixture_optimization', 'assertion_optimization'
    description: str
    potential_improvement: float  # percentage improvement
    implementation: str


@dataclass
class TestSuiteReport:
    """Test suite performance report."""
    total_tests: int
    total_execution_time: float
    average_execution_time: float
    slowest_tests: List[TestPerformanceMetrics]
    optimization_suggestions: List[OptimizationSuggestion]
    parallelization_potential: float


class TestPerformanceAnalyzer:
    """Analyzes test performance and identifies optimization opportunities."""

    def __init__(self):
        self.complexity_keywords = {
            'high_complexity': ['for', 'while', 'if', 'elif', 'else', 'try', 'except', 'with'],
            'medium_complexity': ['def', 'class', 'import', 'from'],
            'low_complexity': ['assert', 'return', 'pass', 'break', 'continue']
        }

    def analyze_test_performance(self, test_file: str) -> List[TestPerformanceMetrics]:
        """Analyze performance metrics for tests in a file."""
        metrics = []
        
        try:
            with open(test_file, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    metric = self._analyze_single_test(node, test_file)
                    if metric:
                        metrics.append(metric)
        
        except Exception:
            pass
        
        return metrics

    def _analyze_single_test(self, test_func: ast.FunctionDef, file_path: str) -> Optional[TestPerformanceMetrics]:
        """Analyze a single test function."""
        test_name = test_func.name
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity(test_func)
        
        # Count dependencies and mocks
        dependency_count = self._count_dependencies(test_func)
        mock_count = self._count_mocks(test_func)
        assertion_count = self._count_assertions(test_func)
        
        # Estimate execution time based on complexity
        estimated_time = self._estimate_execution_time(complexity_score, dependency_count, mock_count)
        
        # Estimate memory usage
        estimated_memory = self._estimate_memory_usage(complexity_score, dependency_count)
        
        return TestPerformanceMetrics(
            test_name=test_name,
            execution_time=estimated_time,
            memory_usage=estimated_memory,
            complexity_score=complexity_score,
            dependency_count=dependency_count,
            mock_count=mock_count,
            assertion_count=assertion_count
        )

    def _calculate_complexity(self, test_func: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a test function."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(test_func):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity

    def _count_dependencies(self, test_func: ast.FunctionDef) -> int:
        """Count external dependencies in a test function."""
        dependencies = set()
        
        for node in ast.walk(test_func):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['requests', 'urllib', 'http', 'sqlite3', 'psycopg2', 'pymongo']:
                        dependencies.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    if hasattr(node.func, 'value') and isinstance(node.func.value, ast.Name):
                        if node.func.value.id in ['requests', 'urllib', 'http', 'sqlite3', 'psycopg2', 'pymongo']:
                            dependencies.add(node.func.value.id)
        
        return len(dependencies)

    def _count_mocks(self, test_func: ast.FunctionDef) -> int:
        """Count mock objects in a test function."""
        mock_count = 0
        
        for node in ast.walk(test_func):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['Mock', 'MagicMock', 'patch', 'mock']:
                        mock_count += 1
                elif isinstance(node.func, ast.Attribute):
                    if hasattr(node.func, 'attr') and node.func.attr in ['Mock', 'MagicMock', 'patch']:
                        mock_count += 1
        
        return mock_count

    def _count_assertions(self, test_func: ast.FunctionDef) -> int:
        """Count assertion statements in a test function."""
        assertion_count = 0
        
        for node in ast.walk(test_func):
            if isinstance(node, ast.Assert):
                assertion_count += 1
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr.startswith('assert'):
                        assertion_count += 1
        
        return assertion_count

    def _estimate_execution_time(self, complexity: int, dependencies: int, mocks: int) -> float:
        """Estimate test execution time based on metrics."""
        base_time = 0.01  # Base execution time
        
        # Add time based on complexity
        complexity_time = complexity * 0.005
        
        # Add time based on dependencies (I/O operations)
        dependency_time = dependencies * 0.1
        
        # Subtract time saved by mocks
        mock_savings = mocks * 0.05
        
        return max(0.001, base_time + complexity_time + dependency_time - mock_savings)

    def _estimate_memory_usage(self, complexity: int, dependencies: int) -> float:
        """Estimate test memory usage based on metrics."""
        base_memory = 1.0  # Base memory in MB
        
        # Add memory based on complexity
        complexity_memory = complexity * 0.5
        
        # Add memory based on dependencies
        dependency_memory = dependencies * 2.0
        
        return base_memory + complexity_memory + dependency_memory


class TestOptimizer:
    """Generates optimization suggestions for test suites."""

    def __init__(self):
        self.optimization_strategies = {
            'parallelize': self._suggest_parallelization,
            'mock_optimization': self._suggest_mock_optimization,
            'fixture_optimization': self._suggest_fixture_optimization,
            'assertion_optimization': self._suggest_assertion_optimization,
            'dependency_optimization': self._suggest_dependency_optimization
        }

    def generate_optimization_suggestions(self, metrics: List[TestPerformanceMetrics]) -> List[OptimizationSuggestion]:
        """Generate optimization suggestions for test metrics."""
        suggestions = []
        
        for metric in metrics:
            # Analyze each test for optimization opportunities
            test_suggestions = []
            
            # Check for parallelization opportunities
            if metric.execution_time > 0.1:  # Tests taking more than 100ms
                test_suggestions.extend(self._suggest_parallelization(metric))
            
            # Check for mock optimization
            if metric.mock_count > 5:  # Tests with many mocks
                test_suggestions.extend(self._suggest_mock_optimization(metric))
            
            # Check for fixture optimization
            if metric.dependency_count > 3:  # Tests with many dependencies
                test_suggestions.extend(self._suggest_fixture_optimization(metric))
            
            # Check for assertion optimization
            if metric.assertion_count > 10:  # Tests with many assertions
                test_suggestions.extend(self._suggest_assertion_optimization(metric))
            
            # Check for dependency optimization
            if metric.dependency_count > 2:  # Tests with external dependencies
                test_suggestions.extend(self._suggest_dependency_optimization(metric))
            
            suggestions.extend(test_suggestions)
        
        return suggestions

    def _suggest_parallelization(self, metric: TestPerformanceMetrics) -> List[OptimizationSuggestion]:
        """Suggest parallelization opportunities."""
        if metric.execution_time > 0.5:  # Only for slow tests
            improvement = min(50, metric.execution_time * 100)  # Up to 50% improvement
            
            return [OptimizationSuggestion(
                test_name=metric.test_name,
                suggestion_type='parallelize',
                description=f"Test takes {metric.execution_time:.3f}s and could benefit from parallelization",
                potential_improvement=improvement,
                implementation=f"""
# Add to pytest.ini or conftest.py
[pytest]
addopts = -n auto  # or -n 4 for 4 parallel workers

# Or use pytest-xdist marker
@pytest.mark.parallel
def {metric.test_name}():
    # Test implementation
    pass
"""
            )]
        return []

    def _suggest_mock_optimization(self, metric: TestPerformanceMetrics) -> List[OptimizationSuggestion]:
        """Suggest mock optimization opportunities."""
        if metric.mock_count > 5:
            improvement = min(30, metric.mock_count * 5)  # Up to 30% improvement
            
            return [OptimizationSuggestion(
                test_name=metric.test_name,
                suggestion_type='mock_optimization',
                description=f"Test uses {metric.mock_count} mocks, consider consolidating or using fixtures",
                potential_improvement=improvement,
                implementation=f"""
# Instead of multiple individual mocks:
# @patch('module.function1')
# @patch('module.function2')
# @patch('module.function3')

# Use a single mock context manager:
@patch.multiple('module', function1=Mock(), function2=Mock(), function3=Mock())
def {metric.test_name}():
    # Test implementation
    pass

# Or create a fixture for common mocks:
@pytest.fixture
def mock_dependencies():
    with patch.multiple('module', function1=Mock(), function2=Mock(), function3=Mock()) as mocks:
        yield mocks
"""
            )]
        return []

    def _suggest_fixture_optimization(self, metric: TestPerformanceMetrics) -> List[OptimizationSuggestion]:
        """Suggest fixture optimization opportunities."""
        if metric.dependency_count > 3:
            improvement = min(40, metric.dependency_count * 10)  # Up to 40% improvement
            
            return [OptimizationSuggestion(
                test_name=metric.test_name,
                suggestion_type='fixture_optimization',
                description=f"Test has {metric.dependency_count} dependencies, consider using fixtures",
                potential_improvement=improvement,
                implementation=f"""
# Create fixtures for common setup:
@pytest.fixture
def test_data():
    return {{
        'user': User(name='test', email='test@example.com'),
        'database': TestDatabase(),
        'api_client': TestAPIClient()
    }}

@pytest.fixture
def mock_services():
    with patch.multiple('services', 
                       database_service=Mock(),
                       api_service=Mock(),
                       cache_service=Mock()) as mocks:
        yield mocks

def {metric.test_name}(test_data, mock_services):
    # Use fixtures instead of inline setup
    user = test_data['user']
    mock_db = mock_services['database_service']
    
    # Test implementation
    pass
"""
            )]
        return []

    def _suggest_assertion_optimization(self, metric: TestPerformanceMetrics) -> List[OptimizationSuggestion]:
        """Suggest assertion optimization opportunities."""
        if metric.assertion_count > 10:
            improvement = min(20, metric.assertion_count * 2)  # Up to 20% improvement
            
            return [OptimizationSuggestion(
                test_name=metric.test_name,
                suggestion_type='assertion_optimization',
                description=f"Test has {metric.assertion_count} assertions, consider consolidating",
                potential_improvement=improvement,
                implementation=f"""
# Instead of multiple individual assertions:
# assert result.status == 'success'
# assert result.code == 200
# assert result.message == 'OK'
# assert result.data is not None

# Use structured assertions:
expected_result = {{
    'status': 'success',
    'code': 200,
    'message': 'OK',
    'data': {'key': 'value'}
}}

assert result == expected_result

# Or use pytest's assert introspection:
assert result.status == 'success'
assert result.code == 200
assert result.message == 'OK'
assert result.data is not None
"""
            )]
        return []

    def _suggest_dependency_optimization(self, metric: TestPerformanceMetrics) -> List[OptimizationSuggestion]:
        """Suggest dependency optimization opportunities."""
        if metric.dependency_count > 2:
            improvement = min(60, metric.dependency_count * 20)  # Up to 60% improvement
            
            return [OptimizationSuggestion(
                test_name=metric.test_name,
                suggestion_type='dependency_optimization',
                description=f"Test has {metric.dependency_count} external dependencies, consider mocking",
                potential_improvement=improvement,
                implementation=f"""
# Mock external dependencies:
@patch('requests.get')
@patch('database.connect')
@patch('cache.get')
def {metric.test_name}(mock_cache, mock_db, mock_requests):
    # Configure mocks
    mock_requests.return_value.json.return_value = {{'status': 'success'}}
    mock_db.return_value.query.return_value = [{{'id': 1, 'name': 'test'}}]
    mock_cache.return_value = 'cached_value'
    
    # Test implementation
    result = function_under_test()
    
    # Verify mocks were called
    mock_requests.assert_called_once()
    mock_db.assert_called_once()
    mock_cache.assert_called_once()
"""
            )]
        return []


class AutoTestOptimizer:
    """Main class for automatic test suite optimization."""

    def __init__(self):
        self.analyzer = TestPerformanceAnalyzer()
        self.optimizer = TestOptimizer()

    def analyze_test_suite(self, test_directory: str) -> TestSuiteReport:
        """Analyze entire test suite for optimization opportunities."""
        all_metrics = []
        
        # Find all test files
        test_files = self._find_test_files(test_directory)
        
        # Analyze each test file
        for test_file in test_files:
            file_metrics = self.analyzer.analyze_test_performance(test_file)
            all_metrics.extend(file_metrics)
        
        # Calculate suite metrics
        total_tests = len(all_metrics)
        total_execution_time = sum(metric.execution_time for metric in all_metrics)
        average_execution_time = total_execution_time / total_tests if total_tests > 0 else 0
        
        # Find slowest tests
        slowest_tests = sorted(all_metrics, key=lambda x: x.execution_time, reverse=True)[:10]
        
        # Generate optimization suggestions
        optimization_suggestions = self.optimizer.generate_optimization_suggestions(all_metrics)
        
        # Calculate parallelization potential
        parallelization_potential = self._calculate_parallelization_potential(all_metrics)
        
        return TestSuiteReport(
            total_tests=total_tests,
            total_execution_time=total_execution_time,
            average_execution_time=average_execution_time,
            slowest_tests=slowest_tests,
            optimization_suggestions=optimization_suggestions,
            parallelization_potential=parallelization_potential
        )

    def _find_test_files(self, directory: str) -> List[str]:
        """Find all test files in a directory."""
        test_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(os.path.join(root, file))
        
        return test_files

    def _calculate_parallelization_potential(self, metrics: List[TestPerformanceMetrics]) -> float:
        """Calculate potential improvement from parallelization."""
        if not metrics:
            return 0.0
        
        # Calculate current sequential time
        sequential_time = sum(metric.execution_time for metric in metrics)
        
        # Calculate parallel time (assuming 4 cores)
        parallel_time = max(metric.execution_time for metric in metrics)
        
        # Calculate improvement percentage
        improvement = ((sequential_time - parallel_time) / sequential_time) * 100
        
        return min(improvement, 75.0)  # Cap at 75% improvement

    def generate_optimization_report(self, report: TestSuiteReport) -> str:
        """Generate comprehensive optimization report."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("⚡ AUTOMATIC TEST SUITE OPTIMIZATION REPORT")
        report_lines.append("=" * 60)
        
        # Summary
        report_lines.append(f"\n📊 TEST SUITE SUMMARY:")
        report_lines.append(f"  • Total Tests: {report.total_tests}")
        report_lines.append(f"  • Total Execution Time: {report.total_execution_time:.3f}s")
        report_lines.append(f"  • Average Execution Time: {report.average_execution_time:.3f}s")
        report_lines.append(f"  • Parallelization Potential: {report.parallelization_potential:.1f}%")
        
        # Slowest tests
        if report.slowest_tests:
            report_lines.append(f"\n🐌 SLOWEST TESTS (Top 10):")
            for i, test in enumerate(report.slowest_tests[:10], 1):
                report_lines.append(f"  {i:2d}. {test.test_name}")
                report_lines.append(f"      Time: {test.execution_time:.3f}s | Complexity: {test.complexity_score} | Dependencies: {test.dependency_count}")
        
        # Optimization suggestions
        if report.optimization_suggestions:
            report_lines.append(f"\n💡 OPTIMIZATION SUGGESTIONS ({len(report.optimization_suggestions)}):")
            
            # Group by type
            suggestions_by_type = {}
            for suggestion in report.optimization_suggestions:
                if suggestion.suggestion_type not in suggestions_by_type:
                    suggestions_by_type[suggestion.suggestion_type] = []
                suggestions_by_type[suggestion.suggestion_type].append(suggestion)
            
            for suggestion_type, suggestions in suggestions_by_type.items():
                report_lines.append(f"\n🔧 {suggestion_type.upper()} ({len(suggestions)} suggestions):")
                for suggestion in suggestions[:5]:  # Show top 5 per type
                    report_lines.append(f"  • {suggestion.test_name}")
                    report_lines.append(f"    {suggestion.description}")
                    report_lines.append(f"    Potential improvement: {suggestion.potential_improvement:.1f}%")
        
        # Recommendations
        report_lines.append(f"\n🚀 OPTIMIZATION RECOMMENDATIONS:")
        report_lines.append(f"  • Install pytest-xdist for parallel test execution")
        report_lines.append(f"  • Use pytest fixtures for common setup/teardown")
        report_lines.append(f"  • Mock external dependencies to reduce I/O time")
        report_lines.append(f"  • Consolidate similar tests to reduce duplication")
        report_lines.append(f"  • Use pytest markers to categorize tests")
        report_lines.append(f"  • Consider using pytest-benchmark for performance testing")
        
        # Configuration suggestions
        report_lines.append(f"\n⚙️ CONFIGURATION SUGGESTIONS:")
        report_lines.append(f"  • Add to pytest.ini:")
        report_lines.append(f"    [pytest]")
        report_lines.append(f"    addopts = -n auto --tb=short")
        report_lines.append(f"    markers =")
        report_lines.append(f"        slow: marks tests as slow")
        report_lines.append(f"        integration: marks tests as integration tests")
        report_lines.append(f"        unit: marks tests as unit tests")
        
        return "\n".join(report_lines)

    def generate_optimized_test_config(self, report: TestSuiteReport) -> str:
        """Generate optimized test configuration."""
        config_lines = []
        config_lines.append("# Optimized pytest configuration")
        config_lines.append("[pytest]")
        config_lines.append("addopts = -n auto --tb=short --strict-markers")
        config_lines.append("testpaths = tests")
        config_lines.append("python_files = test_*.py")
        config_lines.append("python_classes = Test*")
        config_lines.append("python_functions = test_*")
        config_lines.append("")
        config_lines.append("markers =")
        config_lines.append("    slow: marks tests as slow (deselect with '-m \"not slow\"')")
        config_lines.append("    integration: marks tests as integration tests")
        config_lines.append("    unit: marks tests as unit tests")
        config_lines.append("    performance: marks tests as performance tests")
        config_lines.append("    security: marks tests as security tests")
        config_lines.append("")
        config_lines.append("# Parallel execution configuration")
        config_lines.append("# Use: pytest -n auto (for automatic worker count)")
        config_lines.append("# Use: pytest -n 4 (for 4 parallel workers)")
        config_lines.append("")
        config_lines.append("# Coverage configuration")
        config_lines.append("[tool:pytest]")
        config_lines.append("addopts = --cov=src --cov-report=html --cov-report=term-missing")
        config_lines.append("")
        config_lines.append("# Performance testing")
        config_lines.append("# Install: pip install pytest-benchmark")
        config_lines.append("# Use: pytest --benchmark-only")
        
        return "\n".join(config_lines)
