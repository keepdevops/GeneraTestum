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
    
    def generate_tests_for_file(self, java_file: JavaFile) -> List[str]:
        """Generate tests for a complete Java file and write to disk."""
        import os
        
        tests = []
        
        for java_class in java_file.classes:
            class_tests = self._generate_class_tests(java_class, java_file)
            # Tag each test with the class name for grouping
            for test in class_tests:
                test.class_name = java_class.name
            tests.extend(class_tests)
        
        # Group tests by class and write complete test files
        written_files = []
        test_groups = {}
        
        for test in tests:
            # Group tests by the class being tested using the class name tag
            class_name = getattr(test, 'class_name', 'Unknown')
            
            if class_name not in test_groups:
                test_groups[class_name] = []
            test_groups[class_name].append(test)
        
        # Write complete test files
        for class_name, class_tests in test_groups.items():
            test_filename = f"Test{class_name}.java"
            output_path = os.path.join(self.config.output_dir, test_filename)
            
            # Generate complete test file content
            file_content = self._generate_complete_test_file(class_name, class_tests)
            
            # Write the test file
            with open(output_path, 'w') as f:
                f.write(file_content)
            
            written_files.append(output_path)
        
        return written_files
    
    def _generate_complete_test_file(self, class_name: str, tests: List[GeneratedTest]) -> str:
        """Generate a complete Java test file with imports and class structure."""
        # Collect all unique imports
        all_imports = set()
        for test in tests:
            all_imports.update(test.imports)
        
        # Add standard JUnit and AssertJ imports
        all_imports.update(self.junit_imports)
        all_imports.add('org.assertj.core.api.Assertions.assertThat')
        all_imports.add('org.assertj.core.api.Assertions.assertThatCode')
        all_imports.add(f'com.example.{class_name}')
        
        # Generate file content
        content = []
        
        # Add package declaration
        content.append("package com.example;")
        content.append("")
        
        # Add imports
        for import_stmt in sorted(all_imports):
            content.append(f"import {import_stmt};")
        content.append("")
        
        # Add class declaration
        content.append(f"class Test{class_name} {{")
        content.append("")
        
        # Add test methods
        for test in tests:
            content.append(f"    {test.content}")
            content.append("")
        
        # Close class
        content.append("}")
        
        return "\n".join(content)
    
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
