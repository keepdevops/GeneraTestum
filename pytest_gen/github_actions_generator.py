"""
GitHub Actions workflow generator.
"""

from typing import Dict, Any
from .cicd_models import CIConfig


class GitHubActionsGenerator:
    """Generates GitHub Actions workflow configurations."""

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
    - uses: actions/checkout@v4
    
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
        pip install pytest pytest-cov pytest-xdist
    
    - name: Run linting
      run: |
        pip install flake8 black isort
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check src/
        isort --check-only src/
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false"""

        # Add Java testing if project has Java
        if project_info.get('has_java', False):
            workflow_content += self._add_java_job(project_info)
        
        # Add JavaScript testing if project has JavaScript
        if project_info.get('has_javascript', False):
            workflow_content += self._add_javascript_job(project_info)
        
        # Add Docker job if project has Docker
        if project_info.get('has_docker', False):
            workflow_content += self._add_docker_job(project_info)
        
        # Add deployment job
        workflow_content += self._add_deployment_job(project_info)

        return CIConfig(
            name="ci.yml",
            content=workflow_content,
            file_path=".github/workflows/ci.yml",
            config_type="github_actions"
        )

    def _add_java_job(self, project_info: Dict[str, Any]) -> str:
        """Add Java testing job to workflow."""
        from .github_actions_templates import get_java_job_template
        return get_java_job_template(project_info)

    def _add_javascript_job(self, project_info: Dict[str, Any]) -> str:
        """Add JavaScript testing job to workflow."""
        from .github_actions_templates import get_javascript_job_template
        return get_javascript_job_template(project_info)

    def _add_docker_job(self, project_info: Dict[str, Any]) -> str:
        """Add Docker testing job to workflow."""
        from .github_actions_templates import get_docker_job_template
        return get_docker_job_template(project_info)

    def _add_deployment_job(self, project_info: Dict[str, Any]) -> str:
        """Add deployment job to workflow."""
        from .github_actions_templates import get_deployment_job_template
        return get_deployment_job_template(project_info)