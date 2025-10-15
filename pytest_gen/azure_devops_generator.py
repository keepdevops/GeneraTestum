"""
Azure DevOps pipeline generator - refactored for 200LOC limit.
"""

from typing import Dict, Any
from .cicd_models import CIConfig
from .azure_devops_job_templates import AzureDevOpsJobTemplates
from .azure_devops_stage_templates import AzureDevOpsStageTemplates


class AzureDevOpsGenerator:
    """Generates Azure DevOps pipeline configurations."""

    def __init__(self):
        self.job_templates = AzureDevOpsJobTemplates()
        self.stage_templates = AzureDevOpsStageTemplates()

    def generate_azure_devops(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Azure DevOps pipeline configuration."""
        # Start with pipeline header
        pipeline_content = self.stage_templates.get_pipeline_header(project_info)
        
        # Build test stage jobs
        test_jobs = []
        
        # Add Python testing job
        python_job = self.job_templates.get_python_test_job(project_info)
        test_jobs.append(python_job)
        
        # Add Java testing if project has Java
        if project_info.get('has_java', False):
            java_job = self.job_templates.get_java_test_job(project_info)
            test_jobs.append(java_job)
        
        # Add JavaScript testing if project has JavaScript
        if project_info.get('has_javascript', False):
            js_job = self.job_templates.get_javascript_test_job(project_info)
            test_jobs.append(js_job)
        
        # Add test stage
        test_jobs_content = "\n".join(test_jobs)
        test_stage = self.stage_templates.get_test_stage(project_info, test_jobs_content)
        pipeline_content += test_stage
        
        # Add security stage
        security_stage = self.stage_templates.get_security_stage(project_info)
        pipeline_content += security_stage
        
        # Add build stage
        build_stage = self.stage_templates.get_build_stage(project_info)
        pipeline_content += build_stage
        
        # Add deployment stage
        deployment_stage = self.stage_templates.get_deployment_stage(project_info)
        pipeline_content += deployment_stage

        return CIConfig(
            name="azure-pipelines.yml",
            content=pipeline_content,
            file_path="azure-pipelines.yml",
            config_type="azure_devops"
        )

    def generate_basic_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate a basic Azure DevOps pipeline."""
        pipeline_content = self.stage_templates.get_basic_pipeline(project_info)
        
        return CIConfig(
            name="azure-pipelines.yml",
            content=pipeline_content,
            file_path="azure-pipelines.yml",
            config_type="azure_devops"
        )

    def generate_custom_pipeline(self, project_info: Dict[str, Any], 
                               stages: list) -> CIConfig:
        """Generate custom Azure DevOps pipeline with specific stages."""
        pipeline_content = self.stage_templates.get_pipeline_header(project_info)
        
        for stage in stages:
            if stage == 'test':
                test_jobs = [self.job_templates.get_python_test_job(project_info)]
                if project_info.get('has_java', False):
                    test_jobs.append(self.job_templates.get_java_test_job(project_info))
                test_jobs_content = "\n".join(test_jobs)
                test_stage = self.stage_templates.get_test_stage(project_info, test_jobs_content)
                pipeline_content += test_stage
            
            elif stage == 'security':
                security_stage = self.stage_templates.get_security_stage(project_info)
                pipeline_content += security_stage
            
            elif stage == 'build':
                build_stage = self.stage_templates.get_build_stage(project_info)
                pipeline_content += build_stage
            
            elif stage == 'deploy':
                deployment_stage = self.stage_templates.get_deployment_stage(project_info)
                pipeline_content += deployment_stage
        
        return CIConfig(
            name="azure-pipelines.yml",
            content=pipeline_content,
            file_path="azure-pipelines.yml",
            config_type="azure_devops"
        )

    def get_supported_stages(self) -> list:
        """Get list of supported pipeline stages."""
        return ['test', 'security', 'build', 'deploy']

    def get_supported_languages(self) -> list:
        """Get list of supported programming languages."""
        return ['python', 'java', 'javascript']

    def validate_project_info(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default values for project info."""
        defaults = {
            'python_version': '3.9',
            'java_version': '11',
            'node_version': '16',
            'has_java': False,
            'has_javascript': False
        }
        
        validated_info = defaults.copy()
        validated_info.update(project_info)
        
        return validated_info

    def generate_pipeline_for_language(self, project_info: Dict[str, Any], 
                                     language: str) -> CIConfig:
        """Generate pipeline optimized for specific language."""
        validated_info = self.validate_project_info(project_info)
        
        if language.lower() == 'python':
            return self.generate_basic_pipeline(validated_info)
        elif language.lower() == 'java':
            validated_info['has_java'] = True
            return self.generate_custom_pipeline(validated_info, ['test', 'build'])
        elif language.lower() == 'javascript':
            validated_info['has_javascript'] = True
            return self.generate_custom_pipeline(validated_info, ['test', 'build'])
        else:
            # Multi-language project
            return self.generate_azure_devops(validated_info)