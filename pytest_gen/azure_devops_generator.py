"""
Azure DevOps pipeline generator.
"""

from typing import Dict, Any
from .cicd_models import CIConfig


class AzureDevOpsGenerator:
    """Generates Azure DevOps pipeline configurations."""

    def generate_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Azure DevOps pipeline configuration."""
        azure_pipeline_content = f"""trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - README.md
      - docs/*

pr:
  branches:
    include:
      - main
      - develop

variables:
  pythonVersion: '{project_info.get('python_version', '3.9')}'
  javaVersion: '{project_info.get('java_version', '11')}'
  nodeVersion: '{project_info.get('node_version', '16')}'

stages:
- stage: Quality
  displayName: 'Code Quality'
  jobs:
  - job: PythonQuality
    displayName: 'Python Code Quality'
    pool:
      vmImage: 'ubuntu-latest'
    
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
      displayName: 'Use Python $(pythonVersion)'
    
    - task: Cache@2
      inputs:
        key: 'pip | "$(Agent.OS)" | requirements.txt'
        path: '$(pip_cache_dir)'
      displayName: 'Cache pip packages'
    
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
      displayName: 'Install dependencies'
    
    - script: |
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      displayName: 'Lint with flake8'
      continueOnError: true
    
    - script: |
        mypy src/ --ignore-missing-imports
      displayName: 'Type check with mypy'
      continueOnError: true
    
    - script: |
        bandit -r src/ -f json -o bandit-report.json
        safety check --json --output safety-report.json
      displayName: 'Security scan'
      continueOnError: true
    
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/bandit-report.json'
        mergeTestResults: true
      displayName: 'Publish security test results'
      condition: always()
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'Cobertura'
        summaryFileLocation: '**/coverage.xml'
      displayName: 'Publish code coverage'
      condition: always()

- stage: Test
  displayName: 'Testing'
  dependsOn: Quality
  jobs:
  - job: PythonTests
    displayName: 'Python Tests'
    pool:
      vmImage: 'ubuntu-latest'
    
    strategy:
      matrix:
        Python38:
          python.version: '3.8'
        Python39:
          python.version: '3.9'
        Python310:
          python.version: '3.10'
        Python311:
          python.version: '3.11'
    
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(python.version)'
      displayName: 'Use Python $(python.version)'
    
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
      displayName: 'Install dependencies'
    
    - script: |
        pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
      displayName: 'Run tests with pytest'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/test-results.xml'
        mergeTestResults: true
      displayName: 'Publish test results'
      condition: always()
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'Cobertura'
        summaryFileLocation: '**/coverage.xml'
        reportDirectory: '**/htmlcov'
      displayName: 'Publish code coverage'
      condition: always()
  
  - job: JavaTests
    displayName: 'Java Tests'
    pool:
      vmImage: 'ubuntu-latest'
    condition: or(eq(variables['Build.SourceBranch'], 'refs/heads/main'), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
    
    steps:
    - task: JavaToolInstaller@0
      inputs:
        versionSpec: '$(javaVersion)'
        jdkArchitectureOption: 'x64'
      displayName: 'Install Java $(javaVersion)'
    
    - script: |
        chmod +x gradlew
        ./gradlew --version
      displayName: 'Setup Gradle'
    
    - script: |
        ./gradlew test jacocoTestReport
      displayName: 'Run tests with Gradle'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/build/test-results/test/**/*.xml'
        mergeTestResults: true
      displayName: 'Publish Java test results'
      condition: always()
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'JaCoCo'
        summaryFileLocation: '**/build/reports/jacoco/test/jacocoTestReport.xml'
        reportDirectory: '**/build/reports/jacoco/test/html'
      displayName: 'Publish Java coverage'
      condition: always()

- stage: Performance
  displayName: 'Performance Testing'
  dependsOn: Test
  condition: or(eq(variables['Build.SourceBranch'], 'refs/heads/main'), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
  jobs:
  - job: PerformanceTests
    displayName: 'Performance Tests'
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
        pip install pytest-benchmark memory-profiler
      displayName: 'Install dependencies'
    
    - script: |
        pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
      displayName: 'Run performance tests'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/benchmark-results.json'
        mergeTestResults: true
      displayName: 'Publish performance results'
      condition: always()

- stage: Integration
  displayName: 'Integration Testing'
  dependsOn: Test
  condition: or(eq(variables['Build.SourceBranch'], 'refs/heads/main'), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
  jobs:
  - job: IntegrationTests
    displayName: 'Integration Tests'
    pool:
      vmImage: 'ubuntu-latest'
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
    
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
      displayName: 'Use Python $(pythonVersion)'
    
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest-django
      displayName: 'Install dependencies'
    
    - script: |
        pytest tests/integration/ --verbose
      displayName: 'Run integration tests'
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db

- stage: Deploy
  displayName: 'Deployment'
  dependsOn: 
    - Test
    - Performance
    - Integration
  condition: and(succeeded(), or(eq(variables['Build.SourceBranch'], 'refs/heads/main'), eq(variables['Build.SourceBranch'], 'refs/heads/develop')))
  jobs:
  - deployment: DeployStaging
    displayName: 'Deploy to Staging'
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'staging'
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/develop')
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Deploying to staging environment..."
              echo "Deployment commands would go here"
            displayName: 'Deploy to staging'
  
  - deployment: DeployProduction
    displayName: 'Deploy to Production'
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'production'
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Deploying to production environment..."
              echo "Deployment commands would go here"
            displayName: 'Deploy to production'
"""
        
        return CIConfig(
            name="Azure DevOps Pipeline",
            content=azure_pipeline_content,
            file_path="azure-pipelines.yml",
            config_type="azure_devops"
        )
