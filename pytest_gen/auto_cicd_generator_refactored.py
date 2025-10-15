"""
Automatic CI/CD pipeline configuration generation (refactored).
"""

import os
from typing import Dict, List, Any
from .cicd_models import CIConfig, ProjectInfo
from .github_actions_generator import GitHubActionsGenerator
from .jenkins_generator import JenkinsGenerator
from .gitlab_ci_generator import GitLabCIGenerator
from .azure_devops_generator import AzureDevOpsGenerator


class CICDGenerator:
    """Generates CI/CD pipeline configurations."""

    def __init__(self):
        self.output_dir = ".github/workflows"
        self.github_generator = GitHubActionsGenerator()
        self.jenkins_generator = JenkinsGenerator()
        self.gitlab_generator = GitLabCIGenerator()
        self.azure_generator = AzureDevOpsGenerator()

    def generate_all_cicd_configs(self, project_info: Dict[str, Any]) -> List[CIConfig]:
        """Generate all CI/CD configurations."""
        configs = []
        
        # Generate GitHub Actions
        configs.append(self.github_generator.generate_workflow(project_info))
        
        # Generate Jenkins pipeline
        configs.append(self.jenkins_generator.generate_pipeline(project_info))
        
        # Generate GitLab CI
        configs.append(self.gitlab_generator.generate_pipeline(project_info))
        
        # Generate Azure DevOps
        configs.append(self.azure_generator.generate_pipeline(project_info))
        
        return configs

    def save_cicd_configs(self, configs: List[CIConfig], output_dir: str = ".github/workflows"):
        """Save CI/CD configurations to disk."""
        for config in configs:
            if config.config_type == "github_actions":
                config_dir = ".github/workflows"
            elif config.config_type == "jenkins":
                config_dir = "."
            elif config.config_type == "gitlab_ci":
                config_dir = "."
            elif config.config_type == "azure_devops":
                config_dir = "."
            else:
                config_dir = output_dir
            
            os.makedirs(config_dir, exist_ok=True)
            file_path = os.path.join(config_dir, config.file_path)
            
            with open(file_path, 'w') as f:
                f.write(config.content)
            
            print(f"🔧 Generated: {file_path}")


class AutoCICDGenerator:
    """Main class for automatic CI/CD pipeline generation."""

    def __init__(self):
        self.generator = CICDGenerator()

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze project to gather information for CI/CD configuration."""
        project_info = {
            'name': os.path.basename(project_path),
            'python_version': '3.9',
            'java_version': '11',
            'node_version': '16',
            'has_java': False,
            'has_python': False,
            'has_node': False,
            'has_docker': False,
            'has_database': False
        }
        
        # Analyze project structure
        try:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        project_info['has_python'] = True
                    elif file.endswith('.java'):
                        project_info['has_java'] = True
                    elif file.endswith('.js') or file.endswith('.ts'):
                        project_info['has_node'] = True
                    elif file == 'Dockerfile' or file == 'docker-compose.yml':
                        project_info['has_docker'] = True
                    elif file.endswith('.sql'):
                        project_info['has_database'] = True
                
                # Check for specific files
                if 'requirements.txt' in files:
                    project_info['has_python'] = True
                if 'build.gradle' in files or 'pom.xml' in files:
                    project_info['has_java'] = True
                if 'package.json' in files:
                    project_info['has_node'] = True
        except Exception:
            pass
        
        return project_info

    def generate_cicd_configs(self, project_path: str, output_dir: str = ".github/workflows") -> List[CIConfig]:
        """Generate comprehensive CI/CD configurations for a project."""
        # Analyze project
        project_info = self.analyze_project(project_path)
        
        # Generate all CI/CD configurations
        configs = self.generator.generate_all_cicd_configs(project_info)
        
        # Save configurations
        self.generator.save_cicd_configs(configs, output_dir)
        
        return configs

    def generate_cicd_report(self, configs: List[CIConfig]) -> str:
        """Generate a report of generated CI/CD configurations."""
        if not configs:
            return "✅ No CI/CD configurations generated."
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔧 AUTOMATIC CI/CD PIPELINE GENERATION REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"\n🚀 CI/CD CONFIGURATIONS GENERATED: {len(configs)}")
        
        for config in configs:
            report_lines.append(f"\n🔧 {config.name.upper()}:")
            report_lines.append(f"  • File: {config.file_path}")
            report_lines.append(f"  • Type: {config.config_type}")
            report_lines.append(f"  • Size: {len(config.content)} characters")
        
        report_lines.append(f"\n💡 RECOMMENDATIONS:")
        report_lines.append(f"  • Review and customize generated configurations for your environment")
        report_lines.append(f"  • Add your specific deployment commands and environment variables")
        report_lines.append(f"  • Configure secrets and environment variables in your CI/CD platform")
        report_lines.append(f"  • Set up branch protection rules and required status checks")
        report_lines.append(f"  • Configure notifications for build failures and deployments")
        report_lines.append(f"  • Add additional stages for security scanning, performance testing, etc.")
        
        return "\n".join(report_lines)
