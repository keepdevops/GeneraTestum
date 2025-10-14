"""
Main template manager for test code generation.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from jinja2 import Template, Environment
from .config import GeneratorConfig
from .code_analyzer import FunctionInfo, ClassInfo, ModuleInfo
from .mock_generator import MockInfo
from .fixture_generator import FixtureInfo
from .parametrize_generator import ParametrizeInfo
from .template_loader import TemplateLoader
from .template_models import TestTemplate


class TemplateManager:
    """Manages test templates and code generation."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.env = Environment(loader=TemplateLoader())
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
    
    def generate_function_test(self, func_info: FunctionInfo, mocks: List[MockInfo] = None, fixtures: List[FixtureInfo] = None) -> str:
        """Generate test code for a function."""
        template = self.env.get_template('test_function')
        
        context = {
            'function': func_info,
            'mocks': mocks or [],
            'fixtures': fixtures or [],
            'config': self.config
        }
        
        return template.render(**context)
    
    def generate_class_test(self, class_info: ClassInfo, methods: List[FunctionInfo] = None) -> str:
        """Generate test code for a class."""
        template = self.env.get_template('test_class')
        
        context = {
            'class_name': f"{self.config.test_class_prefix}{class_info.name}",
            'methods': methods or class_info.methods,
            'config': self.config
        }
        
        return template.render(**context)
    
    def generate_api_test(self, endpoint_info, mocks: List[MockInfo] = None) -> str:
        """Generate test code for an API endpoint."""
        template = self.env.get_template('test_api_endpoint')
        
        context = {
            'endpoint': endpoint_info,
            'mocks': mocks or [],
            'config': self.config
        }
        
        return template.render(**context)
    
    def generate_fixture_code(self, fixture_info: FixtureInfo) -> str:
        """Generate fixture code."""
        template = self.env.get_template('fixture')
        
        context = {
            'fixture': fixture_info,
            'config': self.config
        }
        
        return template.render(**context)
    
    def generate_mock_code(self, mock_info: MockInfo) -> str:
        """Generate mock code."""
        template = self.env.get_template('mock')
        
        context = {
            'mock': mock_info,
            'config': self.config
        }
        
        return template.render(**context)
    
    def generate_parametrize_code(self, parametrize_info: ParametrizeInfo) -> str:
        """Generate parametrize code."""
        template = self.env.get_template('parametrize')
        
        context = {
            'parametrize': parametrize_info,
            'config': self.config
        }
        
        return template.render(**context)
    
    def generate_complete_test_file(self, module_info: ModuleInfo, test_functions: List[str], 
                                  fixtures: List[str] = None, imports: Set[str] = None) -> str:
        """Generate a complete test file."""
        file_content = []
        
        # Add imports
        if imports:
            for imp in sorted(imports):
                file_content.append(imp)
            file_content.append("")
        
        # Add fixtures
        if fixtures:
            file_content.append("# Fixtures")
            for fixture in fixtures:
                file_content.append(fixture)
                file_content.append("")
        
        # Add test functions
        if test_functions:
            file_content.append("# Test Functions")
            for test_func in test_functions:
                file_content.append(test_func)
                file_content.append("")
        
        return "\n".join(file_content)
    
    def format_test_name(self, name: str) -> str:
        """Format a test name according to config."""
        return f"{self.config.test_prefix}{name}"
    
    def format_class_name(self, name: str) -> str:
        """Format a class name according to config."""
        return f"{self.config.test_class_prefix}{name}"
    
    def create_custom_template(self, name: str, content: str, variables: Dict[str, Any] = None) -> TestTemplate:
        """Create a custom test template."""
        return TestTemplate(
            name=name,
            content=content,
            variables=variables or {}
        )
    
    def load_template_from_file(self, file_path: str) -> str:
        """Load a template from a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def save_template_to_file(self, template: TestTemplate, file_path: str) -> None:
        """Save a template to a file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template.content)
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names."""
        return list(TemplateLoader().templates.keys())
    
    def validate_template(self, template_content: str) -> Tuple[bool, List[str]]:
        """Validate a template for syntax errors."""
        errors = []
        
        try:
            template = Template(template_content)
            # Try to render with empty context to check syntax
            template.render()
        except Exception as e:
            errors.append(str(e))
        
        return len(errors) == 0, errors
    
    def generate_imports_section(self, imports: Set[str]) -> str:
        """Generate imports section for test files."""
        if not imports:
            return ""
        
        import_lines = []
        for imp in sorted(imports):
            import_lines.append(imp)
        
        return "\n".join(import_lines) + "\n"
    
    def generate_docstring(self, description: str) -> str:
        """Generate a docstring for test functions."""
        return f'"""Test {description}."""'
    
    def format_assertion(self, expected: Any, actual: Any = None, assertion_type: str = "equal") -> str:
        """Generate assertion statements."""
        if assertion_type == "equal":
            return f"assert {actual or 'result'} == {expected}"
        elif assertion_type == "not_equal":
            return f"assert {actual or 'result'} != {expected}"
        elif assertion_type == "is_none":
            return f"assert {actual or 'result'} is None"
        elif assertion_type == "is_not_none":
            return f"assert {actual or 'result'} is not None"
        elif assertion_type == "is_instance":
            return f"assert isinstance({actual or 'result'}, {expected})"
        elif assertion_type == "raises":
            return f"with pytest.raises({expected}):\n    # Test code here"
        else:
            return f"assert {actual or 'result'} {assertion_type} {expected}"