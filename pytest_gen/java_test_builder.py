"""
JUnit 5 test generation for Java classes and methods.
"""

from typing import Dict, List, Set, Optional, Any
from .config import GeneratorConfig
from .java_models import JavaMethod, JavaClass, JavaFile
from .test_models import GeneratedTest
from .java_test_templates import JavaTestTemplates


class JavaTestBuilder:
    """Generates JUnit 5 tests for Java code."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.templates = JavaTestTemplates()
        self.mockito_imports = {
            'Mock', 'InjectMocks', 'Spy', 'Captor', 'when', 'verify', 'ArgumentCaptor'
        }
        self.junit_imports = {
            'Test', 'BeforeEach', 'AfterEach', 'BeforeAll', 'AfterAll', 
            'DisplayName', 'ParameterizedTest', 'ValueSource', 'MethodSource'
        }
    
    def generate_tests_for_file(self, java_file: JavaFile) -> List[GeneratedTest]:
        """Generate tests for a complete Java file."""
        tests = []
        
        for java_class in java_file.classes:
            class_tests = self._generate_class_tests(java_class, java_file)
            tests.extend(class_tests)
        
        return tests
    
    def _generate_class_tests(self, java_class: JavaClass, java_file: JavaFile) -> List[GeneratedTest]:
        """Generate tests for a Java class."""
        tests = []
        
        # Generate class-level test
        class_test = GeneratedTest(
            name=f"test_{java_class.name}_instantiation",
            content=self.templates.class_instantiation_test(java_class),
            imports=self._get_class_test_imports(java_class, java_file),
            fixtures=[],
            mocks=[],
            parametrize=[],
            file_path="",
            line_count=0
        )
        tests.append(class_test)
        
        # Generate method tests
        for method in java_class.methods:
            if self._should_test_method(method):
                method_test = GeneratedTest(
                    name=f"test_{method.name}",
                    content=self.templates.method_test(method, java_class),
                    imports=self._get_method_test_imports(method, java_class, java_file),
                    fixtures=[],
                    mocks=[],
                    parametrize=[],
                    file_path="",
                    line_count=0
                )
                tests.append(method_test)
        
        return tests
    
    def _should_test_method(self, method: JavaMethod) -> bool:
        """Determine if a method should be tested."""
        # Skip private methods unless configured otherwise
        if method.access_modifier == 'private' and not self.config.include_private_methods:
            return False
        
        # Skip abstract methods
        if method.is_abstract:
            return False
        
        # Skip main methods
        if method.name == 'main':
            return False
        
        # Skip getters and setters if configured
        if not self.config.generate_fixtures:
            if method.name.startswith(('get', 'set', 'is', 'has')):
                return False
        
        return True
    
    def _get_class_test_imports(self, java_class: JavaClass, java_file: JavaFile) -> Set[str]:
        """Get imports needed for class tests."""
        imports = {
            'org.junit.jupiter.api.Test',
            'org.junit.jupiter.api.DisplayName',
            'org.assertj.core.api.Assertions.assertThat'
        }
        
        # Add class import
        if java_class.package:
            imports.add(f"{java_class.package}.{java_class.name}")
        
        return imports
    
    def _get_method_test_imports(self, method: JavaMethod, java_class: JavaClass, java_file: JavaFile) -> Set[str]:
        """Get imports needed for method tests."""
        imports = {
            'org.junit.jupiter.api.Test',
            'org.junit.jupiter.api.DisplayName',
            'org.assertj.core.api.Assertions.assertThat',
            'org.assertj.core.api.Assertions.assertThatCode'
        }
        
        # Add class import
        if java_class.package:
            imports.add(f"{java_class.package}.{java_class.name}")
        
        # Add imports for parameter types
        for param_name, param_type in method.parameters:
            if 'list' in param_type.lower():
                imports.add('java.util.ArrayList')
            elif 'map' in param_type.lower():
                imports.add('java.util.HashMap')
            elif 'set' in param_type.lower():
                imports.add('java.util.HashSet')
        
        return imports
    
    def generate_mockito_tests(self, java_class: JavaClass, java_file: JavaFile) -> List[GeneratedTest]:
        """Generate tests with Mockito mocks."""
        tests = []
        
        for method in java_class.methods:
            if self._needs_mocking(method):
                mock_test = GeneratedTest(
                    name=f"test_{method.name}_with_mocks",
                    content=self.templates.mockito_test(method, java_class),
                    imports=self._get_mockito_imports(method, java_class, java_file),
                    fixtures=[],
                    mocks=[],
                    parametrize=[],
                    file_path="",
                    line_count=0
                )
                tests.append(mock_test)
        
        return tests
    
    def _needs_mocking(self, method: JavaMethod) -> bool:
        """Determine if a method needs mocking."""
        # Check for Spring annotations that indicate dependencies
        spring_annotations = ['@Autowired', '@Inject', '@Resource']
        return any(ann in method.annotations for ann in spring_annotations)
    
    def _get_mockito_imports(self, method: JavaMethod, java_class: JavaClass, java_file: JavaFile) -> Set[str]:
        """Get imports needed for Mockito tests."""
        imports = self._get_method_test_imports(method, java_class, java_file)
        imports.add('org.mockito.Mockito')
        
        return imports
