"""
Jenkins pipeline generator.
"""

from typing import Dict, Any
from .cicd_models import CIConfig


class JenkinsGenerator:
    """Generates Jenkins pipeline configurations."""

    def generate_jenkins_pipeline(self, project_info: Dict[str, Any]) -> CIConfig:
        """Generate Jenkins pipeline configuration."""
        pipeline_content = f"""pipeline {{
    agent any
    
    environment {{
        PYTHON_VERSION = '{project_info.get('python_version', '3.9')}'
        JAVA_VERSION = '{project_info.get('java_version', '11')}'
        NODE_VERSION = '{project_info.get('node_version', '16')}'
    }}
    
    stages {{
        stage('Checkout') {{
            steps {{
                checkout scm
            }}
        }}
        
        stage('Setup') {{
            parallel {{
                stage('Python Setup') {{
                    steps {{
                        sh '''
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install pytest pytest-cov pytest-xdist
                        '''
                    }}
                }}
                stage('Java Setup') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew dependencies
                        '''
                    }}
                }}
                stage('Node Setup') {{
                    when {{
                        expression {{ params.hasJavaScript == true }}
                    }}
                    steps {{
                        sh '''
                            npm install
                        '''
                    }}
                }}
            }}
        }}
        
        stage('Lint') {{
            parallel {{
                stage('Python Lint') {{
                    steps {{
                        sh '''
                            pip install flake8 black isort
                            flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
                            black --check src/
                            isort --check-only src/
                        '''
                    }}
                }}
                stage('Java Lint') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew checkstyleMain checkstyleTest
                        '''
                    }}
                }}
                stage('JavaScript Lint') {{
                    when {{
                        expression {{ params.hasJavaScript == true }}
                    }}
                    steps {{
                        sh '''
                            npm run lint || echo "No lint script found"
                        '''
                    }}
                }}
            }}
        }}
        
        stage('Test') {{
            parallel {{
                stage('Python Tests') {{
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
                }}
                stage('Java Tests') {{
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
                }}
                stage('JavaScript Tests') {{
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
                }}
            }}
        }}
        
        stage('Build') {{
            parallel {{
                stage('Python Build') {{
                    steps {{
                        sh '''
                            python setup.py sdist bdist_wheel
                        '''
                    }}
                }}
                stage('Java Build') {{
                    when {{
                        expression {{ params.hasJava == true }}
                    }}
                    steps {{
                        sh '''
                            ./gradlew build
                        '''
                    }}
                }}
                stage('Docker Build') {{
                    when {{
                        expression {{ params.hasDocker == true }}
                    }}
                    steps {{
                        sh '''
                            docker build -t ${{BUILD_TAG}} .
                        '''
                    }}
                }}
            }}
        }}
        
        stage('Security Scan') {{
            parallel {{
                stage('Python Security') {{
                    steps {{
                        sh '''
                            pip install bandit safety
                            bandit -r src/
                            safety check
                        '''
                    }}
                }}
                stage('Docker Security') {{
                    when {{
                        expression {{ params.hasDocker == true }}
                    }}
                    steps {{
                        sh '''
                            docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\
                                aquasec/trivy image ${{BUILD_TAG}}
                        '''
                    }}
                }}
            }}
        }}
        
        stage('Deploy') {{
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
        }}
    }}
    
    post {{
        always {{
            cleanWs()
        }}
        success {{
            emailext (
                subject: "Build Successful: ${{env.JOB_NAME}} - ${{env.BUILD_NUMBER}}",
                body: "The build was successful. Please check the build details.",
                to: "${{env.CHANGE_AUTHOR_EMAIL}}"
            )
        }}
        failure {{
            emailext (
                subject: "Build Failed: ${{env.JOB_NAME}} - ${{env.BUILD_NUMBER}}",
                body: "The build failed. Please check the build details.",
                to: "${{env.CHANGE_AUTHOR_EMAIL}}"
            )
        }}
    }}
}}"""

        return CIConfig(
            name="Jenkinsfile",
            content=pipeline_content,
            file_path="Jenkinsfile",
            config_type="jenkins"
        )