"""
Auto documentation generator - refactored for 200LOC limit.
"""

import os
from typing import Dict, List, Any
from .doc_models import TestDocumentation
from .project_analyzer import ProjectAnalyzer
from .documentation_manager import DocumentationManager


class AutoDocumentationGenerator:
    """Main class for automatic documentation generation."""

    def __init__(self):
        self.project_analyzer = ProjectAnalyzer()
        self.doc_manager = DocumentationManager()

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze project to gather information for documentation."""
        # Get basic project info
        project_info = self.project_analyzer.analyze_project_structure(project_path)
        
        # Find API files
        api_files = self.project_analyzer.find_api_files(project_path)
        
        # Find test files
        test_files, test_directories = self.project_analyzer.find_test_files(project_path)
        
        # Generate structured information
        api_info = self.project_analyzer.generate_api_info(project_info)
        test_info = self.project_analyzer.generate_test_info(project_info, test_files, test_directories)
        coverage_info = self.project_analyzer.generate_coverage_info()
        
        return {
            'project': project_info,
            'api': api_info,
            'test': test_info,
            'coverage': coverage_info
        }

    def generate_all_documentation(self, project_info: Dict[str, Any]) -> List[TestDocumentation]:
        """Generate all documentation files."""
        return self.doc_manager.generate_all_documentation(project_info)

    def save_documentation(self, docs: List[TestDocumentation], output_dir: str = "docs") -> None:
        """Save documentation files to disk."""
        self.doc_manager.save_documentation(docs, output_dir)

    def generate_documentation(self, project_path: str, output_dir: str = "docs") -> List[TestDocumentation]:
        """Generate comprehensive documentation for a project."""
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Generate documentation
        docs = self.generate_all_documentation(project_info)
        
        # Save documentation
        self.save_documentation(docs, output_dir)
        
        return docs

    def generate_documentation_report(self, docs: List[TestDocumentation]) -> str:
        """Generate a report of generated documentation."""
        return self.doc_manager.generate_documentation_report(docs)

    def generate_custom_documentation(self, project_path: str, output_dir: str = "docs", 
                                    doc_types: List[str] = None) -> List[TestDocumentation]:
        """Generate specific types of documentation."""
        if doc_types is None:
            doc_types = ['readme', 'api', 'test_guide', 'coverage']
        
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Generate custom documentation
        docs = self.doc_manager.generate_custom_documentation(project_info, doc_types)
        
        # Save documentation
        self.save_documentation(docs, output_dir)
        
        return docs

    def generate_minimal_documentation(self, project_path: str, output_dir: str = "docs") -> List[TestDocumentation]:
        """Generate minimal documentation (README only)."""
        return self.generate_custom_documentation(project_path, output_dir, ['readme'])

    def validate_project_structure(self, project_path: str) -> Dict[str, Any]:
        """Validate project structure for documentation generation."""
        validation_results = {
            'valid': True,
            'issues': [],
            'recommendations': []
        }
        
        if not os.path.exists(project_path):
            validation_results['valid'] = False
            validation_results['issues'].append(f"Project path does not exist: {project_path}")
            return validation_results
        
        # Check for common project files
        expected_files = ['requirements.txt', 'setup.py']
        for file in expected_files:
            if not os.path.exists(os.path.join(project_path, file)):
                validation_results['recommendations'].append(f"Consider adding {file}")
        
        # Check for source code
        src_dirs = ['src', 'lib', 'app']
        has_src = any(os.path.exists(os.path.join(project_path, d)) for d in src_dirs)
        if not has_src:
            validation_results['recommendations'].append("Consider organizing code in a src/ directory")
        
        return validation_results

    def get_documentation_options(self) -> Dict[str, List[str]]:
        """Get available documentation generation options."""
        return {
            'documentation_types': ['readme', 'api', 'test_guide', 'coverage'],
            'output_formats': ['markdown', 'html', 'pdf'],
            'customization_options': [
                'project_name',
                'description',
                'author',
                'license',
                'repository_url',
                'python_version'
            ]
        }

    def generate_documentation_with_custom_info(self, project_path: str, 
                                              custom_info: Dict[str, Any], 
                                              output_dir: str = "docs") -> List[TestDocumentation]:
        """Generate documentation with custom project information."""
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Override with custom info
        if 'project' in custom_info:
            project_info['project'].update(custom_info['project'])
        if 'api' in custom_info:
            project_info['api'].update(custom_info['api'])
        if 'test' in custom_info:
            project_info['test'].update(custom_info['test'])
        if 'coverage' in custom_info:
            project_info['coverage'].update(custom_info['coverage'])
        
        # Generate documentation
        docs = self.generate_all_documentation(project_info)
        
        # Save documentation
        self.save_documentation(docs, output_dir)
        
        return docs