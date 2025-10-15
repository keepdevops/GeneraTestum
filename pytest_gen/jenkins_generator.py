"""
Jenkins pipeline generator - refactored for 200LOC limit.
"""

from typing import Dict, Any
from .cicd_models import CIConfig
from .jenkins_stage_templates import JenkinsStageTemplates
from .jenkins_pipeline_structure import JenkinsPipelineStructure


class JenkinsGenerator:
    """Generates Jenkins pipeline configurations."""

    def __init__(self):
        self.stage_templates = JenkinsStageTemplates()
        self.pipeline_structure = JenkinsPipelineStructure()

    def generate_jenkins_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Jenkins pipeline configuration."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        
        # Build all stages
        stages = []
        
        # Add checkout stage
        stages.append(self.stage_templates.get_checkout_stage())
        
        # Add setup stage
        setup_stage = self.stage_templates.get_setup_stage(validated_info)
        stages.append(setup_stage)
        
        # Add lint stage
        lint_stage = self.stage_templates.get_lint_stage(validated_info)
        stages.append(lint_stage)
        
        # Add test stage
        test_stage = self.stage_templates.get_test_stage(validated_info)
        stages.append(test_stage)
        
        # Add build stage
        build_stage = self.stage_templates.get_build_stage(validated_info)
        stages.append(build_stage)
        
        # Add security stage
        security_stage = self.stage_templates.get_security_stage(validated_info)
        stages.append(security_stage)
        
        # Add deploy stage
        deploy_stage = self.stage_templates.get_deploy_stage()
        stages.append(deploy_stage)
        
        # Combine all stages
        stages_content = "\n\n".join(stages)
        
        # Generate complete pipeline
        pipeline_content = self.pipeline_structure.get_parallel_pipeline(validated_info, stages_content)

        return CIConfig(
            name="Jenkinsfile",
            content=pipeline_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )

    def generate_basic_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate a basic Jenkins pipeline."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        pipeline_content = self.pipeline_structure.get_basic_pipeline(validated_info)
        
        return CIConfig(
            name="Jenkinsfile",
            content=pipeline_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )

    def generate_minimal_pipeline(self) -> CIConfig:
        """Generate a minimal Jenkins pipeline."""
        pipeline_content = self.pipeline_structure.get_minimal_pipeline()
        
        return CIConfig(
            name="Jenkinsfile",
            content=pipeline_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )

    def generate_custom_pipeline(self, project_info: Dict[str, Any], 
                               stages: list) -> CIConfig:
        """Generate custom Jenkins pipeline with specific stages."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        pipeline_content = self.pipeline_structure.get_custom_pipeline(validated_info, stages)
        
        return CIConfig(
            name="Jenkinsfile",
            content=pipeline_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )

    def generate_multi_language_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate multi-language Jenkins pipeline."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        pipeline_content = self.pipeline_structure.get_multi_language_pipeline(validated_info)
        
        return CIConfig(
            name="Jenkinsfile",
            content=pipeline_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )

    def get_supported_stages(self) -> list:
        """Get list of supported pipeline stages."""
        return ['checkout', 'setup', 'lint', 'test', 'build', 'security', 'deploy']

    def get_supported_languages(self) -> list:
        """Get list of supported programming languages."""
        return ['python', 'java', 'javascript']

    def generate_pipeline_for_language(self, project_info: Dict[str, Any], 
                                     language: str) -> CIConfig:
        """Generate pipeline optimized for specific language."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        
        if language.lower() == 'python':
            return self.generate_basic_pipeline(validated_info)
        elif language.lower() == 'java':
            validated_info['has_java'] = True
            return self.generate_custom_pipeline(validated_info, ['checkout', 'setup', 'test', 'build'])
        elif language.lower() == 'javascript':
            validated_info['has_javascript'] = True
            return self.generate_custom_pipeline(validated_info, ['checkout', 'setup', 'test', 'build'])
        else:
            # Multi-language project
            return self.generate_jenkins_pipeline(validated_info)

    def generate_pipeline_with_docker(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Jenkins pipeline with Docker support."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        validated_info['has_docker'] = True
        
        return self.generate_jenkins_pipeline(validated_info)

    def generate_security_focused_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Jenkins pipeline with enhanced security scanning."""
        validated_info = self.pipeline_structure.validate_project_info(project_info)
        
        # Custom stages with enhanced security
        stages = ['checkout', 'setup', 'security', 'test', 'build']
        return self.generate_custom_pipeline(validated_info, stages)