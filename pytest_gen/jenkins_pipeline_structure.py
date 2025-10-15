"""
Jenkins pipeline structure and post-processing templates.
"""

from typing import Dict, Any


class JenkinsPipelineStructure:
    """Jenkins pipeline structure and configuration templates."""
    
    @staticmethod
    def get_pipeline_header(project_info: Dict[str, Any]) -> str:
        """Get pipeline header with environment variables."""
        return f"""pipeline {{
    agent any
    
    environment {{
        PYTHON_VERSION = '{project_info.get('python_version', '3.9')}'
        JAVA_VERSION = '{project_info.get('java_version', '11')}'
        NODE_VERSION = '{project_info.get('node_version', '16')}'
    }}"""
    
    @staticmethod
    def get_stages_section(stages_content: str) -> str:
        """Get stages section wrapper."""
        return f"""    
    stages {{
{stages_content}
    }}"""
    
    @staticmethod
    def get_post_section() -> str:
        """Get post-processing section."""
        return """    
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
    
    @staticmethod
    def get_basic_pipeline(project_info: Dict[str, Any]) -> str:
        """Get basic pipeline template."""
        header = JenkinsPipelineStructure.get_pipeline_header(project_info)
        basic_stages = """
        stage('Checkout') {{
            steps {{
                checkout scm
            }}
        }}
        
        stage('Setup') {{
            steps {{
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }}
        }}
        
        stage('Test') {{
            steps {{
                sh '''
                    pytest tests/
                '''
            }}
        }}"""
        
        stages_section = JenkinsPipelineStructure.get_stages_section(basic_stages)
        post_section = JenkinsPipelineStructure.get_post_section()
        
        return f"{header}\n{stages_section}\n{post_section}"
    
    @staticmethod
    def get_parallel_pipeline(project_info: Dict[str, Any], stages_content: str) -> str:
        """Get pipeline with parallel stages."""
        header = JenkinsPipelineStructure.get_pipeline_header(project_info)
        stages_section = JenkinsPipelineStructure.get_stages_section(stages_content)
        post_section = JenkinsPipelineStructure.get_post_section()
        
        return f"{header}\n{stages_section}\n{post_section}"
    
    @staticmethod
    def get_custom_pipeline(project_info: Dict[str, Any], 
                          stages: list, 
                          include_post: bool = True) -> str:
        """Get custom pipeline with specified stages."""
        header = JenkinsPipelineStructure.get_pipeline_header(project_info)
        
        # Build stages content based on requested stages
        stages_list = []
        for stage in stages:
            if stage == 'checkout':
                stages_list.append("        stage('Checkout') {steps {checkout scm}}")
            elif stage == 'setup':
                stages_list.append("        stage('Setup') {steps {sh 'pip install -r requirements.txt'}}")
            elif stage == 'test':
                stages_list.append("        stage('Test') {steps {sh 'pytest tests/'}}")
            elif stage == 'build':
                stages_list.append("        stage('Build') {steps {sh 'python setup.py build'}}")
            elif stage == 'deploy':
                stages_list.append("        stage('Deploy') {when {branch 'main'} steps {sh 'echo Deploying...'}}")
        
        stages_content = "\n".join(stages_list)
        stages_section = JenkinsPipelineStructure.get_stages_section(stages_content)
        
        result = f"{header}\n{stages_section}"
        if include_post:
            post_section = JenkinsPipelineStructure.get_post_section()
            result += f"\n{post_section}"
        
        return result
    
    @staticmethod
    def get_minimal_pipeline() -> str:
        """Get minimal pipeline template."""
        return """pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/'
            }
        }
    }
}"""
    
    @staticmethod
    def get_multi_language_pipeline(project_info: Dict[str, Any]) -> str:
        """Get multi-language pipeline template."""
        header = JenkinsPipelineStructure.get_pipeline_header(project_info)
        
        stages = [
            "        stage('Checkout') {steps {checkout scm}}",
            "        stage('Setup') {parallel {stage('Python') {steps {sh 'pip install -r requirements.txt'}} stage('Java') {when {expression {params.hasJava == true}} steps {sh './gradlew dependencies'}} stage('Node') {when {expression {params.hasJavaScript == true}} steps {sh 'npm install'}}}}}",
            "        stage('Test') {parallel {stage('Python') {steps {sh 'pytest tests/'}} stage('Java') {when {expression {params.hasJava == true}} steps {sh './gradlew test'}} stage('Node') {when {expression {params.hasJavaScript == true}} steps {sh 'npm test'}}}}}",
            "        stage('Build') {parallel {stage('Python') {steps {sh 'python setup.py build'}} stage('Java') {when {expression {params.hasJava == true}} steps {sh './gradlew build'}}}}}"
        ]
        
        stages_content = "\n".join(stages)
        stages_section = JenkinsPipelineStructure.get_stages_section(stages_content)
        post_section = JenkinsPipelineStructure.get_post_section()
        
        return f"{header}\n{stages_section}\n{post_section}"
    
    @staticmethod
    def validate_project_info(project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default values for project info."""
        defaults = {
            'python_version': '3.9',
            'java_version': '11',
            'node_version': '16',
            'has_java': False,
            'has_javascript': False,
            'has_docker': False
        }
        
        validated_info = defaults.copy()
        validated_info.update(project_info)
        
        return validated_info
