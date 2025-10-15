"""
Automatic test documentation and README generation (refactored).
"""

import os
from typing import Dict, List, Any
from .doc_models import TestDocumentation, ProjectInfo
from .readme_generator import ReadmeGenerator
from .api_docs_generator import APIDocsGenerator
from .test_guide_generator import TestGuideGenerator
from .coverage_report_generator import CoverageReportGenerator


class DocumentationGenerator:
    """Generates comprehensive test documentation."""

    def __init__(self):
        self.template_dir = "templates"
        self.output_dir = "docs"
        self.readme_generator = ReadmeGenerator()
        self.api_docs_generator = APIDocsGenerator()
        self.test_guide_generator = TestGuideGenerator()
        self.coverage_report_generator = CoverageReportGenerator()

    def generate_all_documentation(self, project_info: Dict[str, Any]) -> List[TestDocumentation]:
        """Generate all documentation files."""
        docs = []
        
        # Generate README
        docs.append(self.readme_generator.generate_readme(project_info))
        
        # Generate API documentation
        docs.append(self.api_docs_generator.generate_api_docs(project_info))
        
        # Generate test guide
        docs.append(self.test_guide_generator.generate_test_guide(project_info))
        
        # Generate coverage report
        docs.append(self.coverage_report_generator.generate_coverage_report(project_info))
        
        return docs

    def save_documentation(self, docs: List[TestDocumentation], output_dir: str = "docs"):
        """Save documentation files to disk."""
        os.makedirs(output_dir, exist_ok=True)
        
        for doc in docs:
            file_path = os.path.join(output_dir, doc.file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(doc.content)
            
            print(f"📄 Generated: {file_path}")


class AutoDocumentationGenerator:
    """Main class for automatic documentation generation."""

    def __init__(self):
        self.generator = DocumentationGenerator()

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze project to gather information for documentation."""
        project_info = {
            'name': os.path.basename(project_path),
            'description': 'Automatically generated test suite with comprehensive coverage.',
            'version': '1.0.0',
            'repository_url': '<repository-url>',
            'wiki_url': '<wiki-url>',
            'issues_url': '<issues-url>',
            'discussions_url': '<discussions-url>',
            'license': 'MIT License',
            'dashboard_url': 'http://localhost:8080/dashboard',
            'coverage_percentage': 85,
            'test_count': 25,
            'pass_rate': 96,
            'avg_duration': 0.15,
            'fastest_test': 'test_simple_add',
            'fastest_time': '0.001',
            'slowest_test': 'test_large_dataset',
            'slowest_time': '2.5',
            'total_duration': '15.2'
        }
        
        # Try to extract more information from the project
        try:
            # Look for setup.py or pyproject.toml
            setup_file = os.path.join(project_path, 'setup.py')
            if os.path.exists(setup_file):
                with open(setup_file, 'r') as f:
                    content = f.read()
                    if 'name=' in content:
                        project_info['name'] = content.split('name=')[1].split(',')[0].strip().strip('"\'')
            
            # Count test files
            test_files = []
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.startswith('test_') and file.endswith('.py'):
                        test_files.append(file)
            project_info['test_count'] = len(test_files)
            
        except Exception:
            pass
        
        return project_info

    def generate_documentation(self, project_path: str, output_dir: str = "docs") -> List[TestDocumentation]:
        """Generate comprehensive documentation for a project."""
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Generate all documentation
        docs = self.generator.generate_all_documentation(project_info)
        
        # Save documentation
        self.generator.save_documentation(docs, output_dir)
        
        return docs

    def generate_documentation_report(self, docs: List[TestDocumentation]) -> str:
        """Generate a report of generated documentation."""
        if not docs:
            return "✅ No documentation generated."
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("📚 AUTOMATIC DOCUMENTATION GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n📄 DOCUMENTATION FILES GENERATED: {len(docs)}")
        
        for doc in docs:
            report_lines.append(f"\n📋 {doc.title.upper()}:")
            report_lines.append(f"  • File: {doc.file_path}")
            report_lines.append(f"  • Type: {doc.doc_type}")
            report_lines.append(f"  • Size: {len(doc.content)} characters")
        
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        report_lines.append(f"  • Review and customize generated documentation")
        report_lines.append(f"  • Add project-specific examples and screenshots")
        report_lines.append(f"  • Update configuration examples for your environment")
        report_lines.append(f"  • Add troubleshooting section for common issues")
        report_lines.append(f"  • Include contribution guidelines and code of conduct")
        
        return "\n".join(report_lines)
