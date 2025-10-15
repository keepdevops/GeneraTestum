"""
Automatic CI/CD pipeline configuration generation.
"""

import os
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CIConfig:
    """Generated CI/CD configuration."""
    name: str
    content: str
    file_path: str
    config_type: str  # 'github_actions', 'jenkins', 'gitlab_ci', 'azure_devops'


class CICDGenerator:
    """Generates CI/CD pipeline configurations."""

    def __init__(self):
        self.output_dir = ".github/workflows"

    def generate_github_actions(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate GitHub Actions workflow."""
        workflow_content = f"""name: Test Suite CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Nightly tests at 2 AM UTC

env:
  PYTHON_VERSION: '{project_info.get('python_version', '3.9')}'
  JAVA_VERSION: '{project_info.get('java_version', '11')}'
  NODE_VERSION: '{project_info.get('node_version', '16')}'

jobs:
  test-python:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ matrix.python-version }}}}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{{{ runner.os }}}}-pip-${{{{ hashFiles('**/requirements.txt') }}}}
        restore-keys: |
          ${{{{ runner.os }}}}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Type check with mypy
      run: |
        mypy src/ --ignore-missing-imports
    
    - name: Security scan with bandit
      run: |
        bandit -r src/ -f json -o bandit-report.json || true
    
    - name: Run tests with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{{{ matrix.python-version }}}}
        path: |
          test-results.xml
          htmlcov/
          bandit-report.json

  test-java:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '[java]') || contains(github.event.pull_request.title, '[java]')
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up JDK ${{{{ env.JAVA_VERSION }}}}
      uses: actions/setup-java@v3
      with:
        java-version: ${{{{ env.JAVA_VERSION }}}}
        distribution: 'temurin'
    
    - name: Cache Gradle packages
      uses: actions/cache@v3
      with:
        path: |
          ~/.gradle/caches
          ~/.gradle/wrapper
        key: ${{{{ runner.os }}}}-gradle-${{{{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}}}
        restore-keys: |
          ${{{{ runner.os }}}}-gradle-
    
    - name: Grant execute permission for gradlew
      run: chmod +x gradlew
    
    - name: Build with Gradle
      run: ./gradlew build
    
    - name: Run tests with Gradle
      run: ./gradlew test
    
    - name: Generate coverage report
      run: ./gradlew jacocoTestReport
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: java-test-results
        path: |
          build/test-results/
          build/reports/jacoco/test/html/

  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ env.PYTHON_VERSION }}}}
    
    - name: Install security tools
      run: |
        pip install bandit safety semgrep
    
    - name: Run Bandit security scan
      run: |
        bandit -r src/ -f json -o bandit-report.json
    
    - name: Run Safety dependency scan
      run: |
        safety check --json --output safety-report.json
    
    - name: Run Semgrep security scan
      run: |
        semgrep --config=auto --json --output=semgrep-report.json src/
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json
          semgrep-report.json

  performance-test:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule' || contains(github.event.head_commit.message, '[performance]')
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ env.PYTHON_VERSION }}}}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest-benchmark memory-profiler
    
    - name: Run performance tests
      run: |
        pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
    
    - name: Upload performance results
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: benchmark-results.json

  integration-test:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ env.PYTHON_VERSION }}}}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ --verbose
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test-python, test-java, security-scan]
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment..."
        # Add your staging deployment commands here
    
    - name: Run smoke tests
      run: |
        echo "Running smoke tests on staging..."
        # Add your smoke test commands here

  deploy-production:
    runs-on: ubuntu-latest
    needs: [test-python, test-java, security-scan, integration-test]
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        echo "Deploying to production environment..."
        # Add your production deployment commands here
    
    - name: Run health checks
      run: |
        echo "Running health checks..."
        # Add your health check commands here

  notify:
    runs-on: ubuntu-latest
    needs: [test-python, test-java, security-scan]
    if: always()
    
    steps:
    - name: Notify on success
      if: needs.test-python.result == 'success' && needs.test-java.result == 'success'
      run: |
        echo "✅ All tests passed successfully!"
    
    - name: Notify on failure
      if: needs.test-python.result == 'failure' || needs.test-java.result == 'failure'
      run: |
        echo "❌ Some tests failed. Please check the logs."
"""
        
        return CIConfig(
            name="GitHub Actions Workflow",
            content=workflow_content,
            file_path="test-pipeline.yml",
            config_type="github_actions"
        )

    def generate_jenkins_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Jenkins pipeline configuration."""
        jenkinsfile_content = f"""pipeline {{
    agent any
    
    environment {{
        PYTHON_VERSION = '{project_info.get('python_version', '3.9')}'
        JAVA_VERSION = '{project_info.get('java_version', '11')}'
        NODE_VERSION = '{project_info.get('node_version', '16')}'
        PIP_CACHE_DIR = "${{WORKSPACE}}/.pip_cache"
    }}
    
    options {{
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }}
    
    stages {{
        stage('Checkout') {{
            steps {{
                checkout scm
                script {{
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }}
            }}
        }}
        
        stage('Setup Environment') {{
            parallel {{
                stage('Setup Python') {{
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    python${{env.PYTHON_VERSION}} --version
                                    python${{env.PYTHON_VERSION}} -m pip install --upgrade pip
                                    python${{env.PYTHON_VERSION}} -m pip install -r requirements.txt
                                    python${{env.PYTHON_VERSION}} -m pip install -r requirements-dev.txt
                                '''
                            }} else {{
                                bat '''
                                    python --version
                                    python -m pip install --upgrade pip
                                    python -m pip install -r requirements.txt
                                    python -m pip install -r requirements-dev.txt
                                '''
                            }}
                        }}
                    }}
                }}
                
                stage('Setup Java') {{
                    when {{
                        anyOf {{
                            changeset "**/*.java"
                            changeset "**/build.gradle"
                            changeset "**/pom.xml"
                        }}
                    }}
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    java -version
                                    ./gradlew --version
                                '''
                            }} else {{
                                bat '''
                                    java -version
                                    gradlew.bat --version
                                '''
                            }}
                        }}
                    }}
                }}
            }}
        }}
        
        stage('Code Quality') {{
            parallel {{
                stage('Python Linting') {{
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    python${{env.PYTHON_VERSION}} -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
                                    python${{env.PYTHON_VERSION}} -m flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                                '''
                            }} else {{
                                bat '''
                                    python -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
                                    python -m flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                                '''
                            }}
                        }}
                    }}
                }}
                
                stage('Type Checking') {{
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    python${{env.PYTHON_VERSION}} -m mypy src/ --ignore-missing-imports
                                '''
                            }} else {{
                                bat '''
                                    python -m mypy src/ --ignore-missing-imports
                                '''
                            }}
                        }}
                    }}
                }}
                
                stage('Security Scan') {{
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    python${{env.PYTHON_VERSION}} -m bandit -r src/ -f json -o bandit-report.json || true
                                    python${{env.PYTHON_VERSION}} -m safety check --json --output safety-report.json || true
                                '''
                            }} else {{
                                bat '''
                                    python -m bandit -r src/ -f json -o bandit-report.json || true
                                    python -m safety check --json --output safety-report.json || true
                                '''
                            }}
                        }}
                    }}
                    post {{
                        always {{
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: '.',
                                reportFiles: 'bandit-report.json',
                                reportName: 'Security Report'
                            ])
                        }}
                    }}
                }}
            }}
        }}
        
        stage('Testing') {{
            parallel {{
                stage('Python Tests') {{
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    python${{env.PYTHON_VERSION}} -m pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
                                '''
                            }} else {{
                                bat '''
                                    python -m pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
                                '''
                            }}
                        }}
                    }}
                    post {{
                        always {{
                            publishTestResults testResultsPattern: 'test-results.xml'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }}
                    }}
                }}
                
                stage('Java Tests') {{
                    when {{
                        anyOf {{
                            changeset "**/*.java"
                            changeset "**/build.gradle"
                            changeset "**/pom.xml"
                        }}
                    }}
                    steps {{
                        script {{
                            if (isUnix()) {{
                                sh '''
                                    ./gradlew test jacocoTestReport
                                '''
                            }} else {{
                                bat '''
                                    gradlew.bat test jacocoTestReport
                                '''
                            }}
                        }}
                    }}
                    post {{
                        always {{
                            publishTestResults testResultsPattern: 'build/test-results/test/**/*.xml'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'build/reports/jacoco/test/html',
                                reportFiles: 'index.html',
                                reportName: 'Java Coverage Report'
                            ])
                        }}
                    }}
                }}
            }}
        }}
        
        stage('Integration Tests') {{
            when {{
                anyOf {{
                    branch 'main'
                    branch 'develop'
                }}
            }}
            steps {{
                script {{
                    if (isUnix()) {{
                        sh '''
                            # Start services
                            docker-compose -f docker-compose.test.yml up -d
                            sleep 30
                            
                            # Run integration tests
                            python${{env.PYTHON_VERSION}} -m pytest tests/integration/ --verbose
                            
                            # Stop services
                            docker-compose -f docker-compose.test.yml down
                        '''
                    }} else {{
                        bat '''
                            docker-compose -f docker-compose.test.yml up -d
                            timeout /t 30
                            python -m pytest tests/integration/ --verbose
                            docker-compose -f docker-compose.test.yml down
                        '''
                    }}
                }}
            }}
        }}
        
        stage('Performance Tests') {{
            when {{
                anyOf {{
                    branch 'main'
                    expression {{ return params.RUN_PERFORMANCE_TESTS == true }}
                }}
            }}
            steps {{
                script {{
                    if (isUnix()) {{
                        sh '''
                            python${{env.PYTHON_VERSION}} -m pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
                        '''
                    }} else {{
                        bat '''
                            python -m pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
                        '''
                    }}
                }}
            }}
        }}
        
        stage('Deploy Staging') {{
            when {{
                branch 'develop'
                not {{ changeRequest() }}
            }}
            steps {{
                script {{
                    echo "Deploying to staging environment..."
                    // Add your staging deployment commands here
                }}
            }}
        }}
        
        stage('Deploy Production') {{
            when {{
                branch 'main'
                not {{ changeRequest() }}
            }}
            steps {{
                script {{
                    echo "Deploying to production environment..."
                    // Add your production deployment commands here
                }}
            }}
        }}
    }}
    
    post {{
        always {{
            script {{
                // Archive artifacts
                archiveArtifacts artifacts: 'test-results.xml,bandit-report.json,safety-report.json,benchmark-results.json', fingerprint: true
                
                // Clean workspace
                cleanWs()
            }}
        }}
        
        success {{
            script {{
                echo "✅ Pipeline completed successfully!"
            }}
        }}
        
        failure {{
            script {{
                echo "❌ Pipeline failed. Please check the logs."
            }}
        }}
        
        unstable {{
            script {{
                echo "⚠️ Pipeline completed with warnings."
            }}
        }}
    }}
}}
"""
        
        return CIConfig(
            name="Jenkins Pipeline",
            content=jenkinsfile_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )

    def generate_gitlab_ci(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate GitLab CI configuration."""
        gitlab_ci_content = f"""stages:
  - setup
  - quality
  - test
  - security
  - performance
  - integration
  - deploy

variables:
  PYTHON_VERSION: "{project_info.get('python_version', '3.9')}"
  JAVA_VERSION: "{project_info.get('java_version', '11')}"
  NODE_VERSION: "{project_info.get('node_version', '16')}"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/
    - .gradle/caches/
    - .gradle/wrapper/

# Python setup
setup_python:
  stage: setup
  image: python:${{PYTHON_VERSION}}
  script:
    - python --version
    - pip install --upgrade pip
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt
  artifacts:
    paths:
      - .cache/pip/
    expire_in: 1 hour

# Java setup
setup_java:
  stage: setup
  image: openjdk:${{JAVA_VERSION}}
  script:
    - java -version
    - ./gradlew --version
  artifacts:
    paths:
      - .gradle/caches/
      - .gradle/wrapper/
    expire_in: 1 hour
  only:
    changes:
      - "**/*.java"
      - "**/build.gradle"
      - "**/pom.xml"

# Code quality checks
lint_python:
  stage: quality
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - setup_python
  script:
    - flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
    - flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
  allow_failure: true

type_check:
  stage: quality
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - setup_python
  script:
    - mypy src/ --ignore-missing-imports
  allow_failure: true

# Security scanning
security_scan:
  stage: security
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - setup_python
  script:
    - bandit -r src/ -f json -o bandit-report.json
    - safety check --json --output safety-report.json
  artifacts:
    reports:
      junit: bandit-report.json
    paths:
      - bandit-report.json
      - safety-report.json
    expire_in: 1 week
  allow_failure: true

# Python tests
test_python:
  stage: test
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - setup_python
  script:
    - pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      junit: test-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
      - coverage.xml
    expire_in: 1 week

# Java tests
test_java:
  stage: test
  image: openjdk:${{JAVA_VERSION}}
  dependencies:
    - setup_java
  script:
    - ./gradlew test jacocoTestReport
  artifacts:
    reports:
      junit: build/test-results/test/**/*.xml
    paths:
      - build/reports/jacoco/test/html/
    expire_in: 1 week
  only:
    changes:
      - "**/*.java"
      - "**/build.gradle"
      - "**/pom.xml"

# Performance tests
performance_test:
  stage: performance
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - setup_python
  script:
    - pip install pytest-benchmark memory-profiler
    - pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
  artifacts:
    paths:
      - benchmark-results.json
    expire_in: 1 week
  only:
    - main
    - develop
    - schedules

# Integration tests
integration_test:
  stage: integration
  image: python:${{PYTHON_VERSION}}
  services:
    - postgres:13
    - redis:6
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    REDIS_URL: redis://redis:6379/0
  dependencies:
    - setup_python
  script:
    - pip install pytest-django
    - pytest tests/integration/ --verbose
  only:
    - main
    - develop

# Deploy to staging
deploy_staging:
  stage: deploy
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - test_python
    - security_scan
  script:
    - echo "Deploying to staging environment..."
    - echo "Deployment commands would go here"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Deploy to production
deploy_production:
  stage: deploy
  image: python:${{PYTHON_VERSION}}
  dependencies:
    - test_python
    - security_scan
    - integration_test
  script:
    - echo "Deploying to production environment..."
    - echo "Deployment commands would go here"
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual

# Cleanup
cleanup:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Cleaning up temporary files..."
  when: always
"""
        
        return CIConfig(
            name="GitLab CI Pipeline",
            content=gitlab_ci_content,
            file_path=".gitlab-ci.yml",
            config_type="gitlab_ci"
        )

    def generate_azure_devops(self, project_info: Dict[str, Any]) -> CIConfig:
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

    def generate_all_cicd_configs(self, project_info: Dict[str, Any]) -> List[CIConfig]:
        """Generate all CI/CD configurations."""
        configs = []
        
        # Generate GitHub Actions
        configs.append(self.generate_github_actions(project_info))
        
        # Generate Jenkins pipeline
        configs.append(self.generate_jenkins_pipeline(project_info))
        
        # Generate GitLab CI
        configs.append(self.generate_gitlab_ci(project_info))
        
        # Generate Azure DevOps
        configs.append(self.generate_azure_devops(project_info))
        
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
