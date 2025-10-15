"""
Jenkins pipeline stage templates.
"""

from typing import Dict, Any


class JenkinsStageTemplates:
    """Templates for Jenkins pipeline stages."""
    
    @staticmethod
    def get_checkout_stage() -> str:
        """Get checkout stage template."""
        return """        stage('Checkout') {{
            steps {{
                checkout scm
            }}
        }}"""
    
    @staticmethod
    def get_setup_stage(project_info: Dict[str, Any]) -> str:
        """Get setup stage template."""
        stages = []
        
        # Python setup
        python_setup = """                stage('Python Setup') {{
                    steps {{
                        sh '''
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install pytest pytest-cov pytest-xdist
                        '''
                    }}
                }}"""
        stages.append(python_setup)
        
        # Java setup
        if project_info.get('has_java', False):
            java_setup = """                stage('Java Setup') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew dependencies
                        '''
                    }}
                }}"""
            stages.append(java_setup)
        
        # Node setup
        if project_info.get('has_javascript', False):
            node_setup = """                stage('Node Setup') {{
                    when {{
                        expression {{ params.hasJavaScript == true }}
                    }}
                    steps {{
                        sh '''
                            npm install
                        '''
                    }}
                }}"""
            stages.append(node_setup)
        
        stages_content = "\n".join(stages)
        return f"""        stage('Setup') {{
            parallel {{
{stages_content}
            }}
        }}"""
    
    @staticmethod
    def get_lint_stage(project_info: Dict[str, Any]) -> str:
        """Get lint stage template."""
        stages = []
        
        # Python lint
        python_lint = """                stage('Python Lint') {{
                    steps {{
                        sh '''
                            pip install flake8 black isort
                            flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
                            black --check src/
                            isort --check-only src/
                        '''
                    }}
                }}"""
        stages.append(python_lint)
        
        # Java lint
        if project_info.get('has_java', False):
            java_lint = """                stage('Java Lint') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew checkstyleMain checkstyleTest
                        '''
                    }}
                }}"""
            stages.append(java_lint)
        
        # JavaScript lint
        if project_info.get('has_javascript', False):
            js_lint = """                stage('JavaScript Lint') {{
                    when {{
                        expression {{ params.hasJavaScript == true }}
                    }}
                    steps {{
                        sh '''
                            npm run lint || echo "No lint script found"
                        '''
                    }}
                }}"""
            stages.append(js_lint)
        
        stages_content = "\n".join(stages)
        return f"""        stage('Lint') {{
            parallel {{
{stages_content}
            }}
        }}"""
    
    @staticmethod
    def get_test_stage(project_info: Dict[str, Any]) -> str:
        """Get test stage template."""
        stages = []
        
        # Python tests
        python_tests = """                stage('Python Tests') {{
                    steps {{
                        sh '''
                            pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml
                        '''
                    }}
                    post {{
                        always {{
                            publishTestResults testResultsPattern: 'test-results.xml'
                            publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                        }}
                    }}
                }}"""
        stages.append(python_tests)
        
        # Java tests
        if project_info.get('has_java', False):
            java_tests = """                stage('Java Tests') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew test jacocoTestReport
                        '''
                    }}
                    post {{
                        always {{
                            publishTestResults testResultsPattern: 'build/test-results/test/TEST-*.xml'
                            publishCoverage adapters: [jacocoAdapter('build/reports/jacoco/test/jacocoTestReport.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                        }}
                    }}
                }}"""
            stages.append(java_tests)
        
        # JavaScript tests
        if project_info.get('has_javascript', False):
            js_tests = """                stage('JavaScript Tests') {{
                    when {{
                        expression {{ params.hasJavaScript == true }}
                    }}
                    steps {{
                        sh '''
                            npm test
                            npm run test:coverage || echo "No coverage script found"
                        '''
                    }}
                    post {{
                        always {{
                            publishTestResults testResultsPattern: 'test-results.xml'
                        }}
                    }}
                }}"""
            stages.append(js_tests)
        
        stages_content = "\n".join(stages)
        return f"""        stage('Test') {{
            parallel {{
{stages_content}
            }}
        }}"""
    
    @staticmethod
    def get_build_stage(project_info: Dict[str, Any]) -> str:
        """Get build stage template."""
        stages = []
        
        # Python build
        python_build = """                stage('Python Build') {{
                    steps {{
                        sh '''
                            python setup.py sdist bdist_wheel
                        '''
                    }}
                }}"""
        stages.append(python_build)
        
        # Java build
        if project_info.get('has_java', False):
            java_build = """                stage('Java Build') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew build
                        '''
                    }}
                }}"""
            stages.append(java_build)
        
        # Docker build
        if project_info.get('has_docker', False):
            docker_build = """                stage('Docker Build') {{
                    when {{
                        expression {{ params.hasDocker == true }}
                    }}
                    steps {{
                        sh '''
                            docker build -t ${{BUILD_TAG}} .
                        '''
                    }}
                }}"""
            stages.append(docker_build)
        
        stages_content = "\n".join(stages)
        return f"""        stage('Build') {{
            parallel {{
{stages_content}
            }}
        }}"""
    
    @staticmethod
    def get_security_stage(project_info: Dict[str, Any]) -> str:
        """Get security stage template."""
        stages = []
        
        # Python security
        python_security = """                stage('Python Security') {{
                    steps {{
                        sh '''
                            pip install bandit safety
                            bandit -r src/
                            safety check
                        '''
                    }}
                }}"""
        stages.append(python_security)
        
        # Docker security
        if project_info.get('has_docker', False):
            docker_security = """                stage('Docker Security') {{
                    when {{
                        expression {{ params.hasDocker == true }}
                    }}
                    steps {{
                        sh '''
                            docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\
                                aquasec/trivy image ${{BUILD_TAG}}
                        '''
                    }}
                }}"""
            stages.append(docker_security)
        
        stages_content = "\n".join(stages)
        return f"""        stage('Security Scan') {{
            parallel {{
{stages_content}
            }}
        }}"""
    
    @staticmethod
    def get_deploy_stage() -> str:
        """Get deploy stage template."""
        return """        stage('Deploy') {{
            when {{
                branch 'main'
            }}
            steps {{
                script {{
                    if (env.BRANCH_NAME == 'main') {{
                        echo "Deploying to production..."
                        // Add your deployment logic here
                    }} else {{
                        echo "Deploying to staging..."
                        // Add your staging deployment logic here
                    }}
                }}
            }}
        }}"""
    
    @staticmethod
    def get_minimal_test_stage() -> str:
        """Get minimal test stage template."""
        return """        stage('Test') {{
            steps {{
                sh '''
                    pip install -r requirements.txt
                    pip install pytest
                    pytest tests/
                '''
            }}
        }}"""
