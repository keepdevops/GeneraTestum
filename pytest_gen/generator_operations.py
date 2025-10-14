"""
Generator operations and utilities.
"""

import os
from typing import List, Dict, Any, Optional
from .code_analyzer import CodeAnalyzer, ModuleInfo
from .api_analyzer import APIAnalyzer
from .api_models import APIModuleInfo
from .test_builder import TestBuilder, TestFile
from .source_analyzer import SourceAnalyzer
from .ai_assistant import AIAssistant


class GeneratorOperations:
    """Operations for test generation."""
    
    def __init__(self, config):
        self.config = config
        self.code_analyzer = CodeAnalyzer(self.config)
        self.api_analyzer = APIAnalyzer(self.config)
        self.test_builder = TestBuilder(self.config)
        self.source_analyzer = SourceAnalyzer(self.config)
        self.ai_assistant = None
        self._initialize_ai_assistant()
    
    def _initialize_ai_assistant(self):
        """Initialize AI assistant for recommendations."""
        try:
            self.ai_assistant = AIAssistant()
            init_result = self.ai_assistant.initialize()
            if not init_result["success"]:
                # AI assistant not available, continue without it
                self.ai_assistant = None
        except Exception:
            # AI assistant not available, continue without it
            self.ai_assistant = None
    
    def generate_tests_for_file(self, file_path: str) -> List[str]:
        """Generate tests for a single file."""
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Detect file type
        code_type = self.source_analyzer.detect_file_type(file_path)
        
        if code_type == "python":
            return self._generate_python_tests(file_path)
        elif code_type == "api":
            return self._generate_api_tests(file_path)
        else:
            # Try both analyzers
            test_files = []
            
            # Try Python analysis
            try:
                test_files.extend(self._generate_python_tests(file_path))
            except Exception:
                pass
            
            # Try API analysis
            try:
                test_files.extend(self._generate_api_tests(file_path))
            except Exception:
                pass
            
            return test_files
    
    def generate_tests_for_directory(self, dir_path: str) -> List[str]:
        """Generate tests for all files in a directory."""
        all_test_files = []
        
        for root, dirs, files in os.walk(dir_path):
            # Skip test directories
            if any(skip_dir in root for skip_dir in ['test', 'tests', '__pycache__']):
                continue
            
            for file in files:
                if self.source_analyzer._should_process_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        test_files = self.generate_tests_for_file(file_path)
                        all_test_files.extend(test_files)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        
        return all_test_files
    
    def generate_tests_from_code_string(self, code: str, file_path: str = "<string>") -> List[str]:
        """Generate tests from code string."""
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Try to detect code type
        code_type = self.source_analyzer.detect_code_type(code)
        
        if code_type.value == "python":
            module_info = self.code_analyzer.analyze_code(code, file_path)
            test_files = self.test_builder.build_tests_for_module(module_info)
        elif code_type.value == "api":
            api_info = self.api_analyzer.analyze_code(code, file_path)
            if api_info:
                test_files = self.test_builder.build_tests_for_api(api_info)
            else:
                return []
        else:
            # Try both analyzers
            test_files = []
            
            # Try Python analysis
            try:
                module_info = self.code_analyzer.analyze_code(code, file_path)
                test_files.extend(self.test_builder.build_tests_for_module(module_info))
            except Exception:
                pass
            
            # Try API analysis
            try:
                api_info = self.api_analyzer.analyze_code(code, file_path)
                if api_info:
                    test_files.extend(self.test_builder.build_tests_for_api(api_info))
            except Exception:
                pass
        
        return self.test_builder.save_test_files(test_files)
    
    def _generate_python_tests(self, file_path: str) -> List[str]:
        """Generate tests for Python code."""
        module_info = self.code_analyzer.analyze_file(file_path)
        test_files = self.test_builder.build_tests_for_module(module_info)
        return self.test_builder.save_test_files(test_files)
    
    def _generate_api_tests(self, file_path: str) -> List[str]:
        """Generate tests for API code."""
        api_info = self.api_analyzer.analyze_file(file_path)
        if not api_info:
            return []
        
        test_files = self.test_builder.build_tests_for_api(api_info)
        return self.test_builder.save_test_files(test_files)
    
    def get_ai_recommendations(self, source_path: str) -> Dict[str, Any]:
        """Get AI recommendations for test generation."""
        if not self.ai_assistant:
            return {"available": False, "message": "AI assistant not available"}
        
        try:
            # Analyze the source code
            analysis_result = self.ai_assistant.analyze_code(source_path)
            
            if analysis_result["success"]:
                return {
                    "available": True,
                    "analysis": analysis_result["analysis"],
                    "tokens_used": analysis_result.get("tokens_used", 0)
                }
            else:
                return {
                    "available": True,
                    "error": analysis_result["error"]
                }
        except Exception as e:
            return {
                "available": True,
                "error": f"Failed to get recommendations: {str(e)}"
            }
    
    def get_ai_test_suggestions(self, test_files: List[str]) -> Dict[str, Any]:
        """Get AI suggestions for improving existing tests."""
        if not self.ai_assistant:
            return {"available": False, "message": "AI assistant not available"}
        
        try:
            # Get suggestions for the test files
            suggestions_result = self.ai_assistant.suggest_tests({
                "code": "",  # No source code needed for existing tests
                "existing_tests": "\n".join([
                    f"File: {file}\n{open(file, 'r').read()}" 
                    for file in test_files if os.path.exists(file)
                ])
            })
            
            if suggestions_result["success"]:
                return {
                    "available": True,
                    "suggestions": suggestions_result["suggestions"],
                    "tokens_used": suggestions_result.get("tokens_used", 0)
                }
            else:
                return {
                    "available": True,
                    "error": suggestions_result["error"]
                }
        except Exception as e:
            return {
                "available": True,
                "error": f"Failed to get test suggestions: {str(e)}"
            }
    
    def ask_ai_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ask the AI assistant a question with optional context."""
        if not self.ai_assistant:
            return {"available": False, "message": "AI assistant not available"}
        
        try:
            response = self.ai_assistant.ask(question, context or {})
            return {
                "available": True,
                "response": response.get("response", ""),
                "success": response.get("success", False),
                "error": response.get("error", ""),
                "tokens_used": response.get("tokens_used", 0)
            }
        except Exception as e:
            return {
                "available": True,
                "error": f"Failed to ask question: {str(e)}"
            }
