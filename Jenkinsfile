pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        JAVA_VERSION = '11'
        NODE_VERSION = '16'
        PIP_CACHE_DIR = "${WORKSPACE}/.pip_cache"
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Setup Environment') {
            parallel {
                stage('Setup Python') {
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    python${env.PYTHON_VERSION} --version
                                    python${env.PYTHON_VERSION} -m pip install --upgrade pip
                                    python${env.PYTHON_VERSION} -m pip install -r requirements.txt
                                    python${env.PYTHON_VERSION} -m pip install -r requirements-dev.txt
                                '''
                            } else {
                                bat '''
                                    python --version
                                    python -m pip install --upgrade pip
                                    python -m pip install -r requirements.txt
                                    python -m pip install -r requirements-dev.txt
                                '''
                            }
                        }
                    }
                }
                
                stage('Setup Java') {
                    when {
                        anyOf {
                            changeset "**/*.java"
                            changeset "**/build.gradle"
                            changeset "**/pom.xml"
                        }
                    }
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    java -version
                                    ./gradlew --version
                                '''
                            } else {
                                bat '''
                                    java -version
                                    gradlew.bat --version
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Python Linting') {
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    python${env.PYTHON_VERSION} -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
                                    python${env.PYTHON_VERSION} -m flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                                '''
                            } else {
                                bat '''
                                    python -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
                                    python -m flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                                '''
                            }
                        }
                    }
                }
                
                stage('Type Checking') {
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    python${env.PYTHON_VERSION} -m mypy src/ --ignore-missing-imports
                                '''
                            } else {
                                bat '''
                                    python -m mypy src/ --ignore-missing-imports
                                '''
                            }
                        }
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    python${env.PYTHON_VERSION} -m bandit -r src/ -f json -o bandit-report.json || true
                                    python${env.PYTHON_VERSION} -m safety check --json --output safety-report.json || true
                                '''
                            } else {
                                bat '''
                                    python -m bandit -r src/ -f json -o bandit-report.json || true
                                    python -m safety check --json --output safety-report.json || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: '.',
                                reportFiles: 'bandit-report.json',
                                reportName: 'Security Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Testing') {
            parallel {
                stage('Python Tests') {
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    python${env.PYTHON_VERSION} -m pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
                                '''
                            } else {
                                bat '''
                                    python -m pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            publishTestResults testResultsPattern: 'test-results.xml'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
                
                stage('Java Tests') {
                    when {
                        anyOf {
                            changeset "**/*.java"
                            changeset "**/build.gradle"
                            changeset "**/pom.xml"
                        }
                    }
                    steps {
                        script {
                            if (isUnix()) {
                                sh '''
                                    ./gradlew test jacocoTestReport
                                '''
                            } else {
                                bat '''
                                    gradlew.bat test jacocoTestReport
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            publishTestResults testResultsPattern: 'build/test-results/test/**/*.xml'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'build/reports/jacoco/test/html',
                                reportFiles: 'index.html',
                                reportName: 'Java Coverage Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            # Start services
                            docker-compose -f docker-compose.test.yml up -d
                            sleep 30
                            
                            # Run integration tests
                            python${env.PYTHON_VERSION} -m pytest tests/integration/ --verbose
                            
                            # Stop services
                            docker-compose -f docker-compose.test.yml down
                        '''
                    } else {
                        bat '''
                            docker-compose -f docker-compose.test.yml up -d
                            timeout /t 30
                            python -m pytest tests/integration/ --verbose
                            docker-compose -f docker-compose.test.yml down
                        '''
                    }
                }
            }
        }
        
        stage('Performance Tests') {
            when {
                anyOf {
                    branch 'main'
                    expression { return params.RUN_PERFORMANCE_TESTS == true }
                }
            }
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python${env.PYTHON_VERSION} -m pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
                        '''
                    } else {
                        bat '''
                            python -m pytest tests/performance/ --benchmark-only --benchmark-json=benchmark-results.json
                        '''
                    }
                }
            }
        }
        
        stage('Deploy Staging') {
            when {
                branch 'develop'
                not { changeRequest() }
            }
            steps {
                script {
                    echo "Deploying to staging environment..."
                    // Add your staging deployment commands here
                }
            }
        }
        
        stage('Deploy Production') {
            when {
                branch 'main'
                not { changeRequest() }
            }
            steps {
                script {
                    echo "Deploying to production environment..."
                    // Add your production deployment commands here
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Archive artifacts
                archiveArtifacts artifacts: 'test-results.xml,bandit-report.json,safety-report.json,benchmark-results.json', fingerprint: true
                
                // Clean workspace
                cleanWs()
            }
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed. Please check the logs."
            }
        }
        
        unstable {
            script {
                echo "⚠️ Pipeline completed with warnings."
            }
        }
    }
}
