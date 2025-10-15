"""
Azure DevOps pipeline generator.
"""

from typing import Dict, Any
from .cicd_models import CIConfig


class AzureDevOpsGenerator:
    """Generates Azure DevOps pipeline configurations."""

    def generate_azure_devops(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Azure DevOps pipeline configuration."""
        pipeline_content = f"""trigger:
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

stages:
- stage: Test
  displayName: 'Test Stage'
  jobs:
  - job: PythonTests
    displayName: 'Python Tests'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
      displayName: 'Use Python $(pythonVersion)'
    
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-xdist flake8 black isort
      displayName: 'Install dependencies'
    
    - script: |
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check src/
        isort --check-only src/
      displayName: 'Run linting'
    
    - script: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml
      displayName: 'Run tests'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFiles: 'test-results.xml'
        testRunTitle: 'Python Tests'
      condition: always()
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'Cobertura'
        summaryFileLocation: 'coverage.xml'
        reportDirectory: 'htmlcov'
      condition: always()"""

        # Add Java testing if project has Java
        if project_info.get('has_java', False):
            pipeline_content += self._add_java_job(project_info)
        
        # Add JavaScript testing if project has JavaScript
        if project_info.get('has_javascript', False):
            pipeline_content += self._add_javascript_job(project_info)
        
        # Add security scanning
        pipeline_content += self._add_security_stage(project_info)
        
        # Add build stage
        pipeline_content += self._add_build_stage(project_info)
        
        # Add deployment stage
        pipeline_content += self._add_deployment_stage(project_info)

        return CIConfig(
            name="azure-pipelines.yml",
            content=pipeline_content,
            file_path="azure-pipelines.yml",
            config_type="azure_devops"
        )

    def _add_java_job(self, project_info: Dict[str, Any]) -> str:
        """Add Java testing job."""
        return f"""

  - job: JavaTests
    displayName: 'Java Tests'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: JavaToolInstaller@0
      inputs:
        versionSpec: '$(javaVersion)'
        jdkArchitectureOption: 'x64'
        jdkSourceOption: 'PreInstalled'
      displayName: 'Use Java $(javaVersion)'
    
    - script: |
        chmod +x ./gradlew
        ./gradlew dependencies
      displayName: 'Setup Gradle'
    
    - script: |
        ./gradlew checkstyleMain checkstyleTest
      displayName: 'Run linting'
    
    - script: |
        ./gradlew test jacocoTestReport
      displayName: 'Run tests'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFiles: 'build/test-results/test/TEST-*.xml'
        testRunTitle: 'Java Tests'
      condition: always()
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'JaCoCo'
        summaryFileLocation: 'build/reports/jacoco/test/jacocoTestReport.xml'
      condition: always()"""

    def _add_javascript_job(self, project_info: Dict[str, Any]) -> str:
        """Add JavaScript testing job."""
        return f"""

  - job: JavaScriptTests
    displayName: 'JavaScript Tests'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: NodeTool@0
      inputs:
        versionSpec: '$(nodeVersion)'
      displayName: 'Use Node.js $(nodeVersion)'
    
    - script: |
        npm ci
      displayName: 'Install dependencies'
    
    - script: |
        npm run lint || echo "No lint script found"
        npm run format:check || echo "No format check script found"
      displayName: 'Run linting'
    
    - script: |
        npm test
        npm run test:coverage || echo "No coverage script found"
      displayName: 'Run tests'"""

    def _add_security_stage(self, project_info: Dict[str, Any]) -> str:
        """Add security scanning stage."""
        return f"""

- stage: Security
  displayName: 'Security Stage'
  dependsOn: Test
  condition: succeeded()
  jobs:
  - job: SecurityScan
    displayName: 'Security Scanning'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
      displayName: 'Use Python $(pythonVersion)'
    
    - script: |
        pip install bandit safety
        bandit -r src/ -f json -o bandit-report.json
        safety check --json --output safety-report.json
      displayName: 'Run security scans'
    
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: 'bandit-report.json'
        artifactName: 'security-reports'
      condition: always()"""

    def _add_build_stage(self, project_info: Dict[str, Any]) -> str:
        """Add build stage."""
        return f"""

- stage: Build
  displayName: 'Build Stage'
  dependsOn: Security
  condition: succeeded()
  jobs:
  - job: Build
    displayName: 'Build Application'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
      displayName: 'Use Python $(pythonVersion)'
    
    - script: |
        python setup.py sdist bdist_wheel
      displayName: 'Build Python package'
    
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: 'dist/'
        artifactName: 'python-package'
    
    - script: |
        docker build -t $(Build.Repository.Name):$(Build.BuildId) .
      displayName: 'Build Docker image'
      condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')"""

    def _add_deployment_stage(self, project_info: Dict[str, Any]) -> str:
        """Add deployment stage."""
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
              echo "Running smoke tests..."
              # Add your smoke test commands here
            displayName: 'Run Smoke Tests'"""