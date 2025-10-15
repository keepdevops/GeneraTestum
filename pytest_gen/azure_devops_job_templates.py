"""
Azure DevOps pipeline job templates.
"""

from typing import Dict, Any


class AzureDevOpsJobTemplates:
    """Templates for Azure DevOps pipeline jobs."""
    
    @staticmethod
    def get_python_test_job(project_info: Dict[str, Any]) -> str:
        """Get Python testing job template."""
        return f"""  - job: PythonTests
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
    
    @staticmethod
    def get_java_test_job(project_info: Dict[str, Any]) -> str:
        """Get Java testing job template."""
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
    
    @staticmethod
    def get_javascript_test_job(project_info: Dict[str, Any]) -> str:
        """Get JavaScript testing job template."""
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
    
    @staticmethod
    def get_security_job(project_info: Dict[str, Any]) -> str:
        """Get security scanning job template."""
        return f"""  - job: SecurityScan
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
    
    @staticmethod
    def get_build_job(project_info: Dict[str, Any]) -> str:
        """Get build job template."""
        return f"""  - job: Build
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
