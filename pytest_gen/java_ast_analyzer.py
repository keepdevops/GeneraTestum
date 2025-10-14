"""
AST visitor for analyzing Java code using javalang.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from .java_models import JavaMethod, JavaClass, JavaAnnotation, JavaFile


class JavaASTAnalyzer:
    """AST visitor for analyzing Java code."""
    
    def __init__(self, framework_indicators: Dict[str, List[str]]):
        self.framework_indicators = framework_indicators
        self.package = ""
        self.imports = []
        self.classes = []
        self.annotations = []
        self.dependencies = set()
        self.detected_framework = None
        self.current_class = None
    
    def visit_compilation_unit(self, node):
        """Visit compilation unit (file level)."""
        if node.package:
            self.package = '.'.join(node.package.name)
        
        for import_decl in node.imports:
            import_name = '.'.join(import_decl.path)
            self.imports.append(import_name)
            self.dependencies.add(import_name.split('.')[0])
        
        for type_decl in node.types:
            if hasattr(type_decl, 'name'):
                self.visit(type_decl)
    
    def visit_class_declaration(self, node):
        """Visit class declaration."""
        class_name = node.name
        access_modifier = self._get_access_modifier(node.modifiers)
        
        # Extract class annotations
        class_annotations = self._extract_annotations(node.annotations)
        
        # Extract fields
        fields = []
        if hasattr(node, 'fields'):
            for field in node.fields:
                field_name = field.declarators[0].name
                field_type = self._get_type_string(field.type)
                fields.append((field_name, field_type))
        
        # Extract methods
        methods = []
        if hasattr(node, 'methods'):
            for method in node.methods:
                method_info = self._extract_method_info(method)
                if method_info:
                    methods.append(method_info)
        
        # Determine superclass and interfaces
        superclass = None
        interfaces = []
        if hasattr(node, 'extends') and node.extends:
            superclass = '.'.join(node.extends.name)
        if hasattr(node, 'implements') and node.implements:
            for impl in node.implements:
                interfaces.append('.'.join(impl.name))
        
        java_class = JavaClass(
            name=class_name,
            package=self.package,
            imports=self.imports.copy(),
            methods=methods,
            fields=fields,
            annotations=class_annotations,
            superclass=superclass,
            interfaces=interfaces,
            access_modifier=access_modifier,
            docstring=None,
            line_number=getattr(node, 'position', {}).get('line', 0),
            is_abstract='abstract' in node.modifiers,
            is_final='final' in node.modifiers
        )
        
        self.classes.append(java_class)
        self.current_class = java_class
        
        # Detect framework
        self._detect_framework_from_class(java_class)
    
    def visit_method_declaration(self, node):
        """Visit method declaration."""
        method_info = self._extract_method_info(node)
        if method_info and self.current_class:
            self.current_class.methods.append(method_info)
    
    def _extract_method_info(self, node) -> Optional[JavaMethod]:
        """Extract method information from AST node."""
        method_name = node.name
        access_modifier = self._get_access_modifier(node.modifiers)
        return_type = self._get_type_string(node.return_type) if hasattr(node, 'return_type') else 'void'
        
        # Extract parameters
        parameters = []
        if hasattr(node, 'parameters'):
            for param in node.parameters:
                param_name = param.name
                param_type = self._get_type_string(param.type)
                parameters.append((param_name, param_type))
        
        # Extract annotations
        annotations = self._extract_annotations(node.annotations)
        
        return JavaMethod(
            name=method_name,
            parameters=parameters,
            return_type=return_type,
            access_modifier=access_modifier,
            annotations=annotations,
            docstring=None,
            line_number=getattr(node, 'position', {}).get('line', 0),
            is_static='static' in node.modifiers,
            is_abstract='abstract' in node.modifiers
        )
    
    def _extract_annotations(self, annotations) -> List[str]:
        """Extract annotation names from AST nodes."""
        if not annotations:
            return []
        
        annotation_names = []
        for annotation in annotations:
            if hasattr(annotation, 'name'):
                annotation_names.append('.'.join(annotation.name))
        
        return annotation_names
    
    def _get_access_modifier(self, modifiers) -> str:
        """Get access modifier from modifier list."""
        if 'public' in modifiers:
            return 'public'
        elif 'protected' in modifiers:
            return 'protected'
        elif 'private' in modifiers:
            return 'private'
        else:
            return 'package-private'
    
    def _get_type_string(self, type_node) -> str:
        """Convert type AST node to string."""
        if not type_node:
            return 'void'
        
        if hasattr(type_node, 'name'):
            return '.'.join(type_node.name)
        elif hasattr(type_node, 'element_type'):
            return f"{self._get_type_string(type_node.element_type)}[]"
        else:
            return str(type_node)
    
    def _detect_framework_from_class(self, java_class: JavaClass):
        """Detect framework from class annotations and methods."""
        all_annotations = java_class.annotations.copy()
        for method in java_class.methods:
            all_annotations.extend(method.annotations)
        
        for framework, indicators in self.framework_indicators.items():
            if any(indicator in all_annotations for indicator in indicators):
                self.detected_framework = framework
                break
