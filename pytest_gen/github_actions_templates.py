"""
GitHub Actions workflow templates.
"""

from typing import Dict, Any


def get_java_job_template(project_info: Dict[str, Any]) -> str:
    """Get Java testing job template."""
    return f"""

  test-java:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up JDK {project_info.get('java_version', '11')}
      uses: actions/setup-java@v3
      with:
        java-version: '{project_info.get('java_version', '11')}'
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
    
    - name: Make gradlew executable
      run: chmod +x ./gradlew
    
    - name: Run tests
      run: ./gradlew test
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: java-test-results
        path: build/test-results/test/TEST-*.xml"""


def get_javascript_job_template(project_info: Dict[str, Any]) -> str:
    """Get JavaScript testing job template."""
    return f"""

  test-javascript:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '{project_info.get('node_version', '16')}'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linting
      run: |
        npm run lint || echo "No lint script found"
        npm run format:check || echo "No format check script found"
    
    - name: Run tests
      run: |
        npm test
        npm run test:coverage || echo "No coverage script found"
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      if: success()
      with:
        file: ./coverage/lcov.info
        flags: javascript
        fail_ci_if_error: false"""


def get_docker_job_template(project_info: Dict[str, Any]) -> str:
    """Get Docker testing job template."""
    return f"""

  test-docker:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Build Docker image
      run: docker build -t test-image .
    
    - name: Test Docker image
      run: |
        docker run --rm test-image python -m pytest tests/
        docker run --rm test-image python -c "import src; print('Import successful')"
    
    - name: Scan Docker image
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: test-image
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'"""


def get_deployment_job_template(project_info: Dict[str, Any]) -> str:
    """Get deployment job template."""
    return f"""

  deploy:
    needs: [test-python]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment..."
        # Add your deployment commands here
    
    - name: Run smoke tests
      run: |
        echo "Running smoke tests..."
        # Add your smoke test commands here
    
    - name: Deploy to production
      if: success()
      run: |
        echo "Deploying to production environment..."
        # Add your production deployment commands here"""
