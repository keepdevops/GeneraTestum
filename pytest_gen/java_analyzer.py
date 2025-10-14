"""
Java code analysis using javalang library.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from .config import GeneratorConfig
from .java_models import JavaMethod, JavaClass, JavaAnnotation, JavaFile
from .java_ast_analyzer import JavaASTAnalyzer


class JavaAnalyzer:
    """Analyzes Java files to extract classes, methods, and annotations."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.framework_indicators = {
            'spring': ['@Controller', '@Service', '@Repository', '@Component', '@Autowired'],
            'junit': ['@Test', '@BeforeEach', '@AfterEach', '@BeforeAll', '@AfterAll'],
            'mockito': ['@Mock', '@InjectMocks', '@Spy', '@Captor'],
            'jpa': ['@Entity', '@Table', '@Column', '@Id', '@GeneratedValue']
        }
    
    def analyze_file(self, file_path: str) -> Optional[JavaFile]:
        """Analyze a Java file and extract information."""
        try:
            import javalang
        except ImportError:
            raise ImportError("javalang library not installed. Install with: pip install javalang")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.analyze_code(content, file_path)
    
    def analyze_code(self, code: str, file_path: str = "<string>") -> Optional[JavaFile]:
        """Analyze Java code string."""
        try:
            import javalang
            tree = javalang.parse.parse(code)
        except Exception:
            return None
        
        analyzer = JavaASTAnalyzer(self.framework_indicators)
        analyzer.visit(tree)
        
        return JavaFile(
            file_path=file_path,
            package=analyzer.package,
            imports=analyzer.imports,
            classes=analyzer.classes,
            annotations=analyzer.annotations,
            dependencies=analyzer.dependencies,
            framework=analyzer.detected_framework
        )
    
    def detect_framework(self, java_file: JavaFile) -> Optional[str]:
        """Detect which framework is being used."""
        all_annotations = []
        for cls in java_file.classes:
            all_annotations.extend(cls.annotations)
            for method in cls.methods:
                all_annotations.extend(method.annotations)
        
        for framework, indicators in self.framework_indicators.items():
            if any(indicator in all_annotations for indicator in indicators):
                return framework
        
        return None
