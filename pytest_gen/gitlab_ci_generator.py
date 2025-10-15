"""
GitLab CI pipeline generator.
"""

from typing import Dict, Any
from .cicd_models import CIConfig


class GitLabCIGenerator:
    """Generates GitLab CI pipeline configurations."""

    def generate_gitlab_ci(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate GitLab CI configuration."""
        pipeline_content = f"""stages:
  - test
  - build
  - security
  - deploy

variables:
  PYTHON_VERSION: "{project_info.get('python_version', '3.9')}"
  JAVA_VERSION: "{project_info.get('java_version', '11')}"
  NODE_VERSION: "{project_info.get('node_version', '16')}"

# Python testing
test:python:
  stage: test
  image: python:${{PYTHON_VERSION}}
  before_script:
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt
    - pip install pytest pytest-cov pytest-xdist flake8 black isort
  script:
    - flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
    - black --check src/
    - isort --check-only src/
    - pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml
  artifacts:
    reports:
      junit: test-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - coverage.xml
      - htmlcov/
    expire_in: 1 week
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  only:
    - merge_requests
    - main
    - develop"""

        # Add Java testing if project has Java
        if project_info.get('has_java', False):
            pipeline_content += self._add_java_job(project_info)
        
        # Add JavaScript testing if project has JavaScript
        if project_info.get('has_javascript', False):
            pipeline_content += self._add_javascript_job(project_info)
        
        # Add Docker job if project has Docker
        if project_info.get('has_docker', False):
            pipeline_content += self._add_docker_job(project_info)
        
        # Add security scanning
        pipeline_content += self._add_security_jobs(project_info)
        
        # Add deployment
        pipeline_content += self._add_deployment_jobs(project_info)

        return CIConfig(
            name=".gitlab-ci.yml",
            content=pipeline_content,
            file_path=".gitlab-ci.yml",
            config_type="gitlab_ci"
        )

    def _add_java_job(self, project_info: Dict[str, Any]) -> str:
        """Add Java testing job."""
        return f"""

# Java testing
test:java:
  stage: test
  image: openjdk:{project_info.get('java_version', '11')}-jdk
  before_script:
    - chmod +x ./gradlew
  script:
    - ./gradlew dependencies
    - ./gradlew checkstyleMain checkstyleTest
    - ./gradlew test jacocoTestReport
  artifacts:
    reports:
      junit: build/test-results/test/TEST-*.xml
      coverage_report:
        coverage_format: jacoco
        path: build/reports/jacoco/test/jacocoTestReport.xml
    paths:
      - build/reports/
    expire_in: 1 week
  only:
    - merge_requests
    - main
    - develop"""

    def _add_javascript_job(self, project_info: Dict[str, Any]) -> str:
        """Add JavaScript testing job."""
        return f"""

# JavaScript testing
test:javascript:
  stage: test
  image: node:{project_info.get('node_version', '16')}
  cache:
    paths:
      - node_modules/
  before_script:
    - npm ci
  script:
    - npm run lint || echo "No lint script found"
    - npm run format:check || echo "No format check script found"
    - npm test
    - npm run test:coverage || echo "No coverage script found"
  artifacts:
    paths:
      - coverage/
    expire_in: 1 week
  only:
    - merge_requests
    - main
    - develop"""

    def _add_docker_job(self, project_info: Dict[str, Any]) -> str:
        """Add Docker testing job."""
        return f"""

# Docker testing
test:docker:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker info
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker run --rm $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA python -m pytest tests/
    - docker run --rm $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA python -c "import src; print('Import successful')"
  only:
    - merge_requests
    - main
    - develop"""

    def _add_security_jobs(self, project_info: Dict[str, Any]) -> str:
        """Add security scanning jobs."""
        return f"""

# Security scanning
security:python:
  stage: security
  image: python:${{PYTHON_VERSION}}
  before_script:
    - pip install bandit safety
  script:
    - bandit -r src/ -f json -o bandit-report.json
    - safety check --json --output safety-report.json
  artifacts:
    reports:
      sast: bandit-report.json
    paths:
      - bandit-report.json
      - safety-report.json
    expire_in: 1 week
  only:
    - merge_requests
    - main
    - develop

security:docker:
  stage: security
  image: aquasec/trivy:latest
  dependencies:
    - test:docker
  script:
    - trivy image --format template --template "@contrib/gitlab.tpl" -o gl-container-scanning-report.json $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json
  only:
    - merge_requests
    - main
    - develop"""

    def _add_deployment_jobs(self, project_info: Dict[str, Any]) -> str:
        """Add deployment jobs."""
        return f"""

# Build stage
build:docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - develop

# Deployment
deploy:staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - echo "Deploying to staging environment..."
    - curl -X POST "$STAGING_DEPLOY_URL" -H "Authorization: Bearer $STAGING_TOKEN"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy:production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - echo "Deploying to production environment..."
    - curl -X POST "$PRODUCTION_DEPLOY_URL" -H "Authorization: Bearer $PRODUCTION_TOKEN"
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main"""