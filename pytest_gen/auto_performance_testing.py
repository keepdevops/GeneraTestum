"""
Automatic performance test generation - refactored for 200LOC limit.
"""

import ast
import os
from typing import Dict, List, Any, Optional
from .performance_test_models import PerformanceRequirement, PerformanceTestSuite
from .performance_analyzer import PerformanceAnalyzer
from .performance_test_generator import PerformanceTestGenerator


class AutoPerformanceTesting:
    """Main orchestrator for automatic performance test generation."""

    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.generator = PerformanceTestGenerator()

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file for performance-critical functions."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Could not read file: {e}"
            }
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"Syntax error in file: {e}"
            }
        
        # Find functions
        functions = []
        requirements = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
                requirement = self.analyzer.analyze_function_performance(node)
                if requirement:
                    requirements.append(requirement)
        
        return {
            "success": True,
            "file_path": file_path,
            "total_functions": len(functions),
            "performance_critical_functions": len(requirements),
            "requirements": [
                {
                    "function_name": req.function_name,
                    "max_execution_time": req.max_execution_time,
                    "memory_limit": req.memory_limit,
                    "complexity_threshold": req.complexity_threshold
                }
                for req in requirements
            ]
        }

    def generate_performance_tests(self, file_path: str, output_dir: str = "tests") -> Dict[str, Any]:
        """Generate performance tests for a file."""
        # Analyze file first
        analysis = self.analyze_file(file_path)
        
        if not analysis["success"]:
            return analysis
        
        if not analysis["requirements"]:
            return {
                "success": True,
                "message": "No performance-critical functions found",
                "file_path": file_path,
                "tests_generated": 0
            }
        
        # Generate requirements
        requirements = []
        for req_data in analysis["requirements"]:
            requirements.append(PerformanceRequirement(
                function_name=req_data["function_name"],
                max_execution_time=req_data["max_execution_time"],
                memory_limit=req_data["memory_limit"],
                complexity_threshold=req_data["complexity_threshold"]
            ))
        
        # Generate tests
        test_suite = self.generator.generate_performance_tests(requirements)
        
        # Save test file
        test_file_path = self._save_test_file(file_path, test_suite, output_dir)
        
        return {
            "success": True,
            "file_path": file_path,
            "test_file_path": test_file_path,
            "tests_generated": test_suite.total_tests,
            "coverage_percentage": test_suite.coverage_percentage,
            "requirements_analyzed": len(requirements)
        }

    def _save_test_file(self, source_file_path: str, test_suite: PerformanceTestSuite, output_dir: str) -> str:
        """Save generated test file."""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate test filename
        source_filename = os.path.basename(source_file_path)
        test_filename = f"test_performance_{source_filename}"
        test_file_path = os.path.join(output_dir, test_filename)
        
        # Write test file
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_suite.test_file_content)
        
        return test_file_path

    def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """Analyze all Python files in a directory."""
        results = []
        total_files = 0
        total_requirements = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    file_path = os.path.join(root, file)
                    analysis = self.analyze_file(file_path)
                    
                    if analysis["success"]:
                        results.append(analysis)
                        total_files += 1
                        total_requirements += analysis["performance_critical_functions"]
        
        return {
            "success": True,
            "total_files_analyzed": total_files,
            "total_requirements_found": total_requirements,
            "files": results
        }

    def generate_directory_tests(self, directory_path: str, output_dir: str = "tests") -> Dict[str, Any]:
        """Generate performance tests for all Python files in a directory."""
        results = []
        total_tests = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    file_path = os.path.join(root, file)
                    result = self.generate_performance_tests(file_path, output_dir)
                    results.append(result)
                    
                    if result["success"] and "tests_generated" in result:
                        total_tests += result["tests_generated"]
        
        return {
            "success": True,
            "total_files_processed": len(results),
            "total_tests_generated": total_tests,
            "results": results
        }

    def get_performance_report(self, file_path: str) -> Dict[str, Any]:
        """Generate detailed performance report for a file."""
        analysis = self.analyze_file(file_path)
        
        if not analysis["success"]:
            return analysis
        
        # Generate detailed analysis for each requirement
        detailed_requirements = []
        for req_data in analysis["requirements"]:
            # This would require re-parsing the file to get the function AST
            # For now, return basic information
            detailed_requirements.append({
                "function_name": req_data["function_name"],
                "max_execution_time": req_data["max_execution_time"],
                "memory_limit": req_data["memory_limit"],
                "complexity_threshold": req_data["complexity_threshold"],
                "analysis": "Detailed analysis not implemented yet"
            })
        
        return {
            "success": True,
            "file_path": file_path,
            "summary": {
                "total_functions": analysis["total_functions"],
                "performance_critical": analysis["performance_critical_functions"],
                "coverage_percentage": (analysis["performance_critical_functions"] / analysis["total_functions"] * 100) if analysis["total_functions"] > 0 else 0
            },
            "detailed_requirements": detailed_requirements
        }