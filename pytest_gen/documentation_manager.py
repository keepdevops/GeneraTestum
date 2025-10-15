"""
Documentation generation and management utilities.
"""

import os
from typing import Dict, List, Any
from .doc_models import TestDocumentation
from .readme_generator import ReadmeGenerator
from .api_docs_generator import APIDocsGenerator
from .test_guide_generator import TestGuideGenerator
from .coverage_report_generator import CoverageReportGenerator


class DocumentationManager:
    """Manages documentation generation and file operations."""
    
    def __init__(self):
        self.readme_generator = ReadmeGenerator()
        self.api_generator = APIDocsGenerator()
        self.test_guide_generator = TestGuideGenerator()
        self.coverage_generator = CoverageReportGenerator()
    
    def generate_all_documentation(self, project_info: Dict[str, Any]) -> List[TestDocumentation]:
        """Generate all documentation files."""
        docs = []
        
        # Generate README
        readme_doc = self.readme_generator.generate_project_readme(project_info['project'])
        docs.append(readme_doc)
        
        # Generate API documentation
        api_doc = self.api_generator.generate_api_documentation(project_info['api'])
        docs.append(api_doc)
        
        # Generate test guide
        test_guide_doc = self.test_guide_generator.generate_test_guide(project_info['test'])
        docs.append(test_guide_doc)
        
        # Generate coverage report
        coverage_doc = self.coverage_generator.generate_coverage_report(project_info['coverage'])
        docs.append(coverage_doc)
        
        return docs
    
    def save_documentation(self, docs: List[TestDocumentation], output_dir: str = "docs") -> None:
        """Save documentation files to disk."""
        os.makedirs(output_dir, exist_ok=True)
        
        for doc in docs:
            # Create subdirectories as needed
            file_dir = os.path.dirname(os.path.join(output_dir, doc.file_path))
            if file_dir:
                os.makedirs(file_dir, exist_ok=True)
            
            file_path = os.path.join(output_dir, doc.file_path)
            with open(file_path, 'w') as f:
                f.write(doc.content)
            print(f"Generated {doc.doc_type} documentation: {file_path}")
    
    def generate_documentation_report(self, docs: List[TestDocumentation]) -> str:
        """Generate a report of generated documentation."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("📚 AUTOMATIC DOCUMENTATION GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n📊 GENERATED DOCUMENTATION: {len(docs)}")
        
        for doc in docs:
            report_lines.append(f"\n📄 {doc.doc_type.upper()}:")
            report_lines.append(f"  • Title: {doc.title}")
            report_lines.append(f"  • Path: {doc.file_path}")
            report_lines.append(f"  • Size: {len(doc.content)} characters")
        
        report_lines.append(f"\n💡 FEATURES INCLUDED:")
        report_lines.append(f"  • Comprehensive README with installation and usage")
        report_lines.append(f"  • API documentation with examples and testing")
        report_lines.append(f"  • Test guide with best practices")
        report_lines.append(f"  • Coverage report with recommendations")
        report_lines.append(f"  • Project structure and configuration")
        report_lines.append(f"  • CI/CD integration examples")
        
        report_lines.append(f"\n🎯 NEXT STEPS:")
        report_lines.append(f"  • Review generated documentation")
        report_lines.append(f"  • Customize content for your specific project")
        report_lines.append(f"  • Add project-specific examples and screenshots")
        report_lines.append(f"  • Update configuration files as needed")
        report_lines.append(f"  • Share documentation with your team")
        
        return "\n".join(report_lines)
    
    def generate_custom_documentation(self, project_info: Dict[str, Any], 
                                    doc_types: List[str]) -> List[TestDocumentation]:
        """Generate specific types of documentation."""
        docs = []
        
        if 'readme' in doc_types:
            readme_doc = self.readme_generator.generate_project_readme(project_info['project'])
            docs.append(readme_doc)
        
        if 'api' in doc_types:
            api_doc = self.api_generator.generate_api_documentation(project_info['api'])
            docs.append(api_doc)
        
        if 'test_guide' in doc_types:
            test_guide_doc = self.test_guide_generator.generate_test_guide(project_info['test'])
            docs.append(test_guide_doc)
        
        if 'coverage' in doc_types:
            coverage_doc = self.coverage_generator.generate_coverage_report(project_info['coverage'])
            docs.append(coverage_doc)
        
        return docs
    
    def validate_documentation(self, docs: List[TestDocumentation]) -> Dict[str, Any]:
        """Validate generated documentation."""
        validation_results = {
            'total_docs': len(docs),
            'valid_docs': 0,
            'invalid_docs': 0,
            'issues': []
        }
        
        for doc in docs:
            if doc.content and doc.title and doc.file_path:
                validation_results['valid_docs'] += 1
            else:
                validation_results['invalid_docs'] += 1
                validation_results['issues'].append(f"Invalid doc: {doc.title}")
        
        return validation_results
    
    def get_documentation_summary(self, docs: List[TestDocumentation]) -> Dict[str, Any]:
        """Get summary statistics for generated documentation."""
        total_chars = sum(len(doc.content) for doc in docs)
        doc_types = {}
        
        for doc in docs:
            doc_type = doc.doc_type
            if doc_type not in doc_types:
                doc_types[doc_type] = 0
            doc_types[doc_type] += 1
        
        return {
            'total_documents': len(docs),
            'total_characters': total_chars,
            'average_length': total_chars / len(docs) if docs else 0,
            'document_types': doc_types,
            'largest_doc': max(docs, key=lambda d: len(d.content)).title if docs else None,
            'smallest_doc': min(docs, key=lambda d: len(d.content)).title if docs else None
        }
