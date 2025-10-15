"""
Azure DevOps pipeline stage templates.
"""

from typing import Dict, Any


class AzureDevOpsStageTemplates:
    """Templates for Azure DevOps pipeline stages."""
    
    @staticmethod
    def get_test_stage(project_info: Dict[str, Any], jobs_content: str) -> str:
        """Get test stage template."""
        return f"""stages:
- stage: Test
  displayName: 'Test Stage'
  jobs:
{jobs_content}"""
    
    @staticmethod
    def get_security_stage(project_info: Dict[str, Any]) -> str:
        """Get security stage template."""
        return f"""
- stage: Security
  displayName: 'Security Stage'
  dependsOn: Test
  condition: succeeded()
  jobs:
    job_template = AzureDevOpsJobTemplates.get_security_job(project_info)
    return f"""
- stage: Security
  displayName: 'Security Stage'
  dependsOn: Test
  condition: succeeded()
  jobs:
{job_template}"""
    
    @staticmethod
    def get_build_stage(project_info: Dict[str, Any]) -> str:
        """Get build stage template."""
        return f"""
- stage: Build
  displayName: 'Build Stage'
  dependsOn: Security
  condition: succeeded()
  jobs:
{job_template}"""
    
    @staticmethod
    def get_deployment_stage(project_info: Dict[str, Any]) -> str:
        """Get deployment stage template."""
        return f"""
- stage: Deploy
  displayName: 'Deploy Stage'
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployToProduction
    displayName: 'Deploy to Production'
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Deploying to production environment..."
              # Add your deployment commands here
            displayName: 'Deploy to Production'
          
          - script: |
              echo "Running post-deployment tests..."
              # Add your post-deployment test commands here
            displayName: 'Post-deployment Tests'"""
    
    @staticmethod
    def get_pipeline_header(project_info: Dict[str, Any]) -> str:
        """Get pipeline header template."""
        return f"""trigger:
- main
- develop

pr:
- main
- develop

schedules:
- cron: "0 2 * * *"
  displayName: Nightly build
  branches:
    include:
    - main
  always: true

variables:
  pythonVersion: '{project_info.get('python_version', '3.9')}'
  javaVersion: '{project_info.get('java_version', '11')}'
  nodeVersion: '{project_info.get('node_version', '16')}'
"""
    
    @staticmethod
    def get_minimal_test_stage() -> str:
        """Get minimal test stage template."""
        return """stages:
- stage: Test
  displayName: 'Test Stage'
  jobs:
  - job: RunTests
    displayName: 'Run Tests'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.9'
      displayName: 'Use Python 3.9'
    
    - script: |
        pip install -r requirements.txt
        pip install pytest
      displayName: 'Install dependencies'
    
    - script: |
        pytest tests/
      displayName: 'Run tests'"""
    
    @staticmethod
    def get_basic_pipeline(project_info: Dict[str, Any]) -> str:
        """Get basic pipeline template."""
        header = AzureDevOpsStageTemplates.get_pipeline_header(project_info)
        minimal_stage = AzureDevOpsStageTemplates.get_minimal_test_stage()
        return f"{header}\n{minimal_stage}"
