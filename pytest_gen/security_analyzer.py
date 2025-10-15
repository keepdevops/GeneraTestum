"""
Security vulnerability analyzer.
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from .security_models import SecurityVulnerability, SecurityAnalysisResult
from .security_patterns import SecurityPatterns


class SecurityAnalyzer:
    """Analyzes code to identify potential security vulnerabilities."""

    def __init__(self):
        self.patterns = SecurityPatterns.get_vulnerability_patterns()
        self.severity_levels = SecurityPatterns.get_severity_levels()

    def analyze_code(self, source_code: str, file_path: str = "") -> SecurityAnalysisResult:
        """Analyze source code for security vulnerabilities."""
        vulnerabilities = []
        
        # Parse the code into an AST
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            # If code can't be parsed, return empty result
            return SecurityAnalysisResult(
                vulnerabilities=[],
                total_vulnerabilities=0,
                critical_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                analysis_summary="Code could not be parsed"
            )
        
        # Analyze using pattern matching
        pattern_vulnerabilities = self._analyze_patterns(source_code, file_path)
        vulnerabilities.extend(pattern_vulnerabilities)
        
        # Analyze using AST traversal
        ast_vulnerabilities = self._analyze_ast(tree, file_path)
        vulnerabilities.extend(ast_vulnerabilities)
        
        # Count vulnerabilities by severity
        critical_count = sum(1 for v in vulnerabilities if v.severity == 'critical')
        high_count = sum(1 for v in vulnerabilities if v.severity == 'high')
        medium_count = sum(1 for v in vulnerabilities if v.severity == 'medium')
        low_count = sum(1 for v in vulnerabilities if v.severity == 'low')
        
        # Generate analysis summary
        summary = self._generate_summary(vulnerabilities, critical_count, high_count, medium_count, low_count)
        
        return SecurityAnalysisResult(
            vulnerabilities=vulnerabilities,
            total_vulnerabilities=len(vulnerabilities),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            analysis_summary=summary
        )

    def _analyze_patterns(self, source_code: str, file_path: str) -> List[SecurityVulnerability]:
        """Analyze code using regex patterns."""
        vulnerabilities = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for vuln_type, pattern_info in self.patterns.items():
                for pattern in pattern_info.patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Extract function name if possible
                        function_name = self._extract_function_name(lines, line_num)
                        
                        vulnerability = SecurityVulnerability(
                            vulnerability_type=vuln_type,
                            severity=pattern_info.severity,
                            description=pattern_info.description,
                            affected_function=function_name,
                            line_number=line_num,
                            mitigation=pattern_info.mitigation
                        )
                        vulnerabilities.append(vulnerability)
                        break  # Only report one vulnerability per line
        
        return vulnerabilities

    def _analyze_ast(self, tree: ast.AST, file_path: str) -> List[SecurityVulnerability]:
        """Analyze code using AST traversal."""
        vulnerabilities = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                vulns = self._analyze_function_call(node, file_path)
                vulnerabilities.extend(vulns)
            elif isinstance(node, ast.FunctionDef):
                vulns = self._analyze_function_definition(node, file_path)
                vulnerabilities.extend(vulns)
        
        return vulnerabilities

    def _analyze_function_call(self, node: ast.Call, file_path: str) -> List[SecurityVulnerability]:
        """Analyze function calls for security issues."""
        vulnerabilities = []
        
        # Check for dangerous function calls
        dangerous_functions = {
            'eval': ('code_injection', 'critical', 'Use of eval() is dangerous'),
            'exec': ('code_injection', 'critical', 'Use of exec() is dangerous'),
            'compile': ('code_injection', 'critical', 'Use of compile() is dangerous'),
            '__import__': ('code_injection', 'critical', 'Use of __import__() is dangerous')
        }
        
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in dangerous_functions:
                vuln_type, severity, description = dangerous_functions[func_name]
                vulnerability = SecurityVulnerability(
                    vulnerability_type=vuln_type,
                    severity=severity,
                    description=description,
                    affected_function=func_name,
                    line_number=node.lineno,
                    mitigation='Avoid dynamic code execution'
                )
                vulnerabilities.append(vulnerability)
        
        return vulnerabilities

    def _analyze_function_definition(self, node: ast.FunctionDef, file_path: str) -> List[SecurityVulnerability]:
        """Analyze function definitions for security issues."""
        vulnerabilities = []
        
        # Check for missing input validation
        has_input_validation = False
        for stmt in node.body:
            if isinstance(stmt, (ast.If, ast.Assert)):
                has_input_validation = True
                break
        
        if not has_input_validation and any('request' in str(arg) for arg in node.args.args):
            vulnerability = SecurityVulnerability(
                vulnerability_type='missing_input_validation',
                severity='medium',
                description='Function appears to lack input validation',
                affected_function=node.name,
                line_number=node.lineno,
                mitigation='Add proper input validation'
            )
            vulnerabilities.append(vulnerability)
        
        return vulnerabilities

    def _extract_function_name(self, lines: List[str], line_num: int) -> str:
        """Extract function name from context."""
        # Look backwards from the current line to find function definition
        for i in range(line_num - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('def '):
                # Extract function name
                match = re.match(r'def\s+(\w+)', line)
                if match:
                    return match.group(1)
        return 'unknown_function'

    def _generate_summary(self, vulnerabilities: List[SecurityVulnerability], 
                         critical: int, high: int, medium: int, low: int) -> str:
        """Generate analysis summary."""
        total = len(vulnerabilities)
        
        if total == 0:
            return "No security vulnerabilities detected."
        
        summary_parts = [f"Found {total} security vulnerabilities:"]
        
        if critical > 0:
            summary_parts.append(f"- {critical} critical")
        if high > 0:
            summary_parts.append(f"- {high} high")
        if medium > 0:
            summary_parts.append(f"- {medium} medium")
        if low > 0:
            summary_parts.append(f"- {low} low")
        
        # Get top vulnerability types
        vuln_types = {}
        for vuln in vulnerabilities:
            vuln_types[vuln.vulnerability_type] = vuln_types.get(vuln.vulnerability_type, 0) + 1
        
        top_types = sorted(vuln_types.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_types:
            summary_parts.append(f"Most common: {', '.join([f'{t} ({c})' for t, c in top_types])}")
        
        return " ".join(summary_parts)
