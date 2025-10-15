"""
README generator - refactored for 200LOC limit.
"""

from typing import Dict, Any
from .doc_models import TestDocumentation
from .readme_template_sections import ReadmeTemplateSections
from .readme_config_sections import ReadmeConfigSections


class ReadmeGenerator:
    """Generates comprehensive project README documentation."""

    def __init__(self):
        self.template_sections = ReadmeTemplateSections()
        self.config_sections = ReadmeConfigSections()

    def generate_project_readme(self, project_info: Dict[str, Any]) -> TestDocumentation:
        """Generate comprehensive project README."""
        content = f"""{self.template_sections.get_header_section(project_info)}

{self.template_sections.get_project_structure_section(project_info)}

{self.template_sections.get_installation_section(project_info)}

{self.template_sections.get_testing_section()}

{self.template_sections.get_coverage_section()}

{self.config_sections.get_configuration_section()}

{self.config_sections.get_development_section()}

{self.config_sections.get_contributing_section(project_info)}

{self.config_sections.get_footer_section(project_info)}
"""

        return TestDocumentation(
            title="README",
            content=content,
            file_path="README.md",
            doc_type="readme"
        )

    def generate_minimal_readme(self, project_info: Dict[str, Any]) -> TestDocumentation:
        """Generate a minimal README."""
        content = f"""# {project_info.get('name', 'Project')}

{project_info.get('description', 'A Python project with automated testing.')}

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest
```

## License

{project_info.get('license', 'MIT')}
"""

        return TestDocumentation(
            title="README",
            content=content,
            file_path="README.md",
            doc_type="readme"
        )

    def generate_readme_section(self, section_name: str, project_info: Dict[str, Any]) -> str:
        """Generate a specific README section."""
        section_generators = {
            'header': self.template_sections.get_header_section,
            'structure': self.template_sections.get_project_structure_section,
            'installation': self.template_sections.get_installation_section,
            'testing': self.template_sections.get_testing_section,
            'coverage': self.template_sections.get_coverage_section,
            'configuration': self.config_sections.get_configuration_section,
            'development': self.config_sections.get_development_section,
            'contributing': self.config_sections.get_contributing_section,
            'footer': self.config_sections.get_footer_section
        }
        
        generator = section_generators.get(section_name)
        if generator:
            return generator(project_info)
        else:
            return f"# {section_name.title()}\n\nSection not found."

    def generate_custom_readme(self, project_info: Dict[str, Any], sections: list) -> TestDocumentation:
        """Generate README with custom sections."""
        content_parts = []
        
        for section in sections:
            section_content = self.generate_readme_section(section, project_info)
            content_parts.append(section_content)
        
        content = "\n\n".join(content_parts)
        
        return TestDocumentation(
            title="README",
            content=content,
            file_path="README.md",
            doc_type="readme"
        )

    def get_readme_template_variables(self, project_info: Dict[str, Any]) -> Dict[str, str]:
        """Get template variables for README generation."""
        return {
            'project_name': project_info.get('name', 'Test Generator Project'),
            'description': project_info.get('description', 'Automatically generated test suite'),
            'python_version': project_info.get('python_version', '3.9'),
            'repository': project_info.get('repository', 'https://github.com/your-org/your-project.git'),
            'author': project_info.get('author', 'Your Name'),
            'email': project_info.get('email', 'your.email@example.com'),
            'license': project_info.get('license', 'MIT'),
            'version': project_info.get('version', '1.0.0'),
            'last_updated': project_info.get('last_updated', '2024-01-01')
        }

    def validate_project_info(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default values for project info."""
        defaults = {
            'name': 'Test Generator Project',
            'description': 'Automatically generated test suite with comprehensive coverage.',
            'python_version': '3.9',
            'repository': 'https://github.com/your-org/your-project.git',
            'author': 'Your Name',
            'email': 'your.email@example.com',
            'license': 'MIT',
            'version': '1.0.0',
            'last_updated': '2024-01-01'
        }
        
        validated_info = defaults.copy()
        validated_info.update(project_info)
        
        return validated_info

    def generate_readme_with_custom_sections(self, project_info: Dict[str, Any], 
                                           custom_sections: Dict[str, str]) -> TestDocumentation:
        """Generate README with additional custom sections."""
        # Generate base README
        base_readme = self.generate_project_readme(project_info)
        
        # Add custom sections
        custom_content = []
        for section_name, section_content in custom_sections.items():
            custom_content.append(f"## {section_name}\n\n{section_content}")
        
        # Insert custom sections before footer
        content = base_readme.content
        footer_start = content.find("## 📚 API Documentation")
        
        if footer_start != -1:
            before_footer = content[:footer_start]
            after_footer = content[footer_start:]
            full_content = before_footer + "\n\n" + "\n\n".join(custom_content) + "\n\n" + after_footer
        else:
            full_content = content + "\n\n" + "\n\n".join(custom_content)
        
        return TestDocumentation(
            title="README",
            content=full_content,
            file_path="README.md",
            doc_type="readme"
        )