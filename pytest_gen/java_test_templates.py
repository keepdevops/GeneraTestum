"""
JUnit 5 test templates for Java code generation.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from .java_models import JavaMethod, JavaClass


class JavaTestTemplates:
    """Templates for JUnit 5 test generation."""
    
    @staticmethod
    def class_instantiation_test(java_class: JavaClass) -> str:
        """Generate class instantiation test."""
        return f'''@Test
@DisplayName("Test {java_class.name} instantiation")
void test_{java_class.name}_instantiation() {{
    // Arrange & Act
    {java_class.name} instance = new {java_class.name}();
    
    // Assert
    assertThat(instance).isNotNull();
    assertThat(instance).isInstanceOf({java_class.name}.class);
}}'''
    
    @staticmethod
    def method_test(method: JavaMethod, java_class: JavaClass) -> str:
        """Generate test for a Java method."""
        test_content = f'''@Test
@DisplayName("Test {method.name} method")
void test_{method.name}() {{
    // Arrange
    {java_class.name} instance = new {java_class.name}();
'''
        
        # Add parameter setup
        for param_name, param_type in method.parameters:
            test_content += f"    {param_type} {param_name} = {JavaTestTemplates._get_default_value(param_type)};\n"
        
        # Add method call and assertion
        if method.return_type != 'void':
            test_content += f"\n    // Act\n"
            test_content += f"    {method.return_type} result = instance.{method.name}({', '.join([p[0] for p in method.parameters])});\n\n"
            test_content += f"    // Assert\n"
            test_content += f"    assertThat(result).isNotNull();\n"
        else:
            test_content += f"\n    // Act & Assert\n"
            test_content += f"    assertThatCode(() -> instance.{method.name}({', '.join([p[0] for p in method.parameters])}))\n"
            test_content += f"            .doesNotThrowAnyException();\n"
        
        test_content += "}"
        
        return test_content
    
    @staticmethod
    def mockito_test(method: JavaMethod, java_class: JavaClass) -> str:
        """Generate test with Mockito mocks."""
        test_content = f'''@Test
@DisplayName("Test {method.name} with mocks")
void test_{method.name}_with_mocks() {{
    // Arrange
    {java_class.name} instance = new {java_class.name}();
'''
        
        # Add mock setup for parameters
        for param_name, param_type in method.parameters:
            test_content += f"    {param_type} {param_name} = Mockito.mock({param_type}.class);\n"
        
        # Add method call and assertion
        if method.return_type != 'void':
            test_content += f"\n    // Act\n"
            test_content += f"    {method.return_type} result = instance.{method.name}({', '.join([p[0] for p in method.parameters])});\n\n"
            test_content += f"    // Assert\n"
            test_content += f"    assertThat(result).isNotNull();\n"
        else:
            test_content += f"\n    // Act & Assert\n"
            test_content += f"    assertThatCode(() -> instance.{method.name}({', '.join([p[0] for p in method.parameters])}))\n"
            test_content += f"            .doesNotThrowAnyException();\n"
        
        test_content += "}"
        
        return test_content
    
    @staticmethod
    def parameterized_test(method: JavaMethod, java_class: JavaClass) -> str:
        """Generate parametrized test for a method."""
        return f'''@ParameterizedTest
@ValueSource(strings = {{"test1", "test2", "test3"}})
@DisplayName("Test {method.name} with parameters")
void test_{method.name}_parameterized(String input) {{
    // Arrange
    {java_class.name} instance = new {java_class.name}();
    
    // Act
    {method.return_type} result = instance.{method.name}(input);
    
    // Assert
    assertThat(result).isNotNull();
}}'''
    
    @staticmethod
    def spring_test(method: JavaMethod, java_class: JavaClass) -> str:
        """Generate Spring integration test."""
        return f'''@SpringBootTest
@TestPropertySource(locations = "classpath:application-test.properties")
@DisplayName("Spring test for {method.name}")
class {java_class.name}SpringTest {{
    
    @Autowired
    private {java_class.name} {java_class.name.lower()};
    
    @Test
    void test_{method.name}_spring() {{
        // Arrange
        String input = "test";
        
        // Act
        {method.return_type} result = {java_class.name.lower()}.{method.name}(input);
        
        // Assert
        assertThat(result).isNotNull();
    }}
}}'''
    
    @staticmethod
    def _get_default_value(param_type: str) -> str:
        """Get default value for a parameter type."""
        type_lower = param_type.lower()
        
        if 'int' in type_lower or 'long' in type_lower or 'short' in type_lower or 'byte' in type_lower:
            return '0'
        elif 'double' in type_lower or 'float' in type_lower:
            return '0.0'
        elif 'boolean' in type_lower:
            return 'false'
        elif 'char' in type_lower:
            return "'a'"
        elif 'string' in type_lower:
            return '"test"'
        elif 'list' in type_lower:
            return 'new ArrayList<>()'
        elif 'map' in type_lower:
            return 'new HashMap<>()'
        elif 'set' in type_lower:
            return 'new HashSet<>()'
        else:
            return 'null'
