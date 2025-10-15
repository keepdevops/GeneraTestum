"""
Main CI/CD pipeline configuration generator.
"""

import os
from typing import Dict, List, Any
from .cicd_models import CIConfig, ProjectInfo
from .github_actions_generator import GitHubActionsGenerator
from .jenkins_generator import JenkinsGenerator
from .gitlab_ci_generator import GitLabCIGenerator
from .azure_devops_generator import AzureDevOpsGenerator


class AutoCICDGenerator:
    """Main class for automatic CI/CD configuration generation."""

    def __init__(self):
        self.github_generator = GitHubActionsGenerator()
        self.jenkins_generator = JenkinsGenerator()
        self.gitlab_generator = GitLabCIGenerator()
        self.azure_generator = AzureDevOpsGenerator()

    def analyze_project(self, project_path: str) -> ProjectInfo:
        """Analyze project to gather information for CI/CD configuration."""
        project_info = {
            'name': os.path.basename(project_path),
            'description': 'Automated CI/CD pipeline',
            'python_version': '3.9',
            'java_version': '11',
            'node_version': '16',
            'test_framework': 'pytest',
            'has_java': False,
            'has_javascript': False,
            'has_docker': False,
            'has_database': False,
            'has_api': False,
            'dependencies': [],
            'test_directories': ['tests'],
            'source_directories': ['src']
        }
        
        # Check for Java files
        for root, dirs, files in os.walk(project_path):
            if any(f.endswith('.java') for f in files):
                project_info['has_java'] = True
                break
        
        # Check for JavaScript files
        for root, dirs, files in os.walk(project_path):
            if any(f.endswith(('.js', '.ts', '.jsx', '.tsx')) for f in files):
                project_info['has_javascript'] = True
                break
        
        # Check for Docker files
        for root, dirs, files in os.walk(project_path):
            if any(f in ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'] for f in files):
                project_info['has_docker'] = True
                break
        
        # Check for requirements.txt or package.json
        if os.path.exists(os.path.join(project_path, 'requirements.txt')):
            with open(os.path.join(project_path, 'requirements.txt'), 'r') as f:
                project_info['dependencies'] = [line.strip() for line in f if line.strip()]
        
        # Check for API-related files
        for root, dirs, files in os.walk(project_path):
            if any('api' in f.lower() or 'flask' in f.lower() or 'django' in f.lower() for f in files):
                project_info['has_api'] = True
                break
        
        # Check for database files
        for root, dirs, files in os.walk(project_path):
            if any('db' in f.lower() or 'database' in f.lower() or 'sql' in f.lower() for f in files):
                project_info['has_database'] = True
                break
        
        return ProjectInfo(**project_info)

    def generate_all_cicd_configs(self, project_info: ProjectInfo) -> List[CIConfig]:
        """Generate all CI/CD configurations."""
        configs = []
        
        # Generate GitHub Actions
        github_config = self.github_generator.generate_github_actions(project_info.__dict__)
        configs.append(github_config)
        
        # Generate Jenkins
        jenkins_config = self.jenkins_generator.generate_jenkins_pipeline(project_info.__dict__)
        configs.append(jenkins_config)
        
        # Generate GitLab CI
        gitlab_config = self.gitlab_generator.generate_gitlab_ci(project_info.__dict__)
        configs.append(gitlab_config)
        
        # Generate Azure DevOps
        azure_config = self.azure_generator.generate_azure_devops(project_info.__dict__)
        configs.append(azure_config)
        
        return configs

    def save_cicd_configs(self, configs: List[CIConfig], output_dir: str = ".github/workflows"):
        """Save CI/CD configurations to disk."""
        os.makedirs(output_dir, exist_ok=True)
        
        for config in configs:
            # Create subdirectory for each config type
            config_dir = output_dir
            if config.config_type != 'github_actions':
                config_dir = os.path.join(output_dir, '..', '..', config.config_type)
                os.makedirs(config_dir, exist_ok=True)
            
            file_path = os.path.join(config_dir, config.name)
            with open(file_path, 'w') as f:
                f.write(config.content)
            print(f"Generated {config.config_type} configuration: {file_path}")

    def generate_cicd_configs(self, project_path: str, output_dir: str = ".github/workflows") -> List[CIConfig]:
        """Generate comprehensive CI/CD configurations for a project."""
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Generate configurations
        configs = self.generate_all_cicd_configs(project_info)
        
        # Save configurations
        self.save_cicd_configs(configs, output_dir)
        
        return configs

    def generate_cicd_report(self, configs: List[CIConfig]) -> str:
        """Generate a report of generated CI/CD configurations."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🚀 AUTOMATIC CI/CD CONFIGURATION GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n📊 GENERATED CONFIGURATIONS: {len(configs)}")
        
        for config in configs:
            report_lines.append(f"\n🔧 {config.config_type.upper()}:")
            report_lines.append(f"  • File: {config.name}")
            report_lines.append(f"  • Path: {config.file_path}")
            report_lines.append(f"  • Size: {len(config.content)} characters")
        
        report_lines.append(f"\n💡 FEATURES INCLUDED:")
        report_lines.append(f"  • Multi-language support (Python, Java, JavaScript)")
        report_lines.append(f"  • Comprehensive testing (unit, integration, security)")
        report_lines.append(f"  • Code quality checks (linting, formatting)")
        report_lines.append(f"  • Security scanning (SAST, dependency scanning)")
        report_lines.append(f"  • Coverage reporting")
        report_lines.append(f"  • Automated deployment")
        report_lines.append(f"  • Docker support")
        
        report_lines.append(f"\n🎯 NEXT STEPS:")
        report_lines.append(f"  • Review generated configurations")
        report_lines.append(f"  • Customize for your specific needs")
        report_lines.append(f"  • Set up secrets and environment variables")
        report_lines.append(f"  • Enable the desired CI/CD platform")
        report_lines.append(f"  • Test the pipeline with a sample commit")
        
        return "\n".join(report_lines)