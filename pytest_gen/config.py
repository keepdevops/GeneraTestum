"""
Configuration management for pytest code generator.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum


class MockLevel(Enum):
    """Mock generation levels."""
    NONE = "none"
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"


class TestCoverage(Enum):
    """Test coverage types."""
    HAPPY_PATH = "happy_path"
    COMPREHENSIVE = "comprehensive"
    FULL = "full"


class CodeType(Enum):
    """Supported code types."""
    PYTHON = "python"
    API = "api"
    MIXED = "mixed"


@dataclass
class GeneratorConfig:
    """Configuration for test generation."""
    
    # Output settings
    output_dir: str = "tests"
    output_format: str = "pytest"
    
    # Code analysis settings
    code_type: CodeType = CodeType.PYTHON
    include_private_methods: bool = False
    max_depth: int = 3
    
    # Test generation settings
    coverage_type: TestCoverage = TestCoverage.COMPREHENSIVE
    mock_level: MockLevel = MockLevel.COMPREHENSIVE
    generate_fixtures: bool = True
    generate_parametrize: bool = True
    
    # Mock settings
    mock_external_calls: bool = True
    mock_database: bool = True
    mock_file_io: bool = True
    mock_network: bool = True
    
    # Fixture settings
    fixture_prefix: str = "test_"
    fixture_scope: str = "function"
    
    # Test naming
    test_prefix: str = "test_"
    test_class_prefix: str = "Test"
    
    # Dependencies to mock
    mock_dependencies: Set[str] = field(default_factory=lambda: {
        "requests", "urllib", "sqlite3", "psycopg2", "pymongo",
        "open", "file", "os", "pathlib", "json", "pickle"
    })
    
    # Templates
    test_template: str = "basic"
    fixture_template: str = "basic"
    
    # File settings
    max_lines_per_file: int = 200
    split_large_tests: bool = True
    
    # API specific settings
    api_frameworks: List[str] = field(default_factory=lambda: [
        "flask", "fastapi", "django", "tornado"
    ])
    
    # Edge case generation
    generate_edge_cases: bool = True
    generate_error_cases: bool = True
    generate_boundary_tests: bool = True


DEFAULT_CONFIG = GeneratorConfig()


def load_config_from_file(config_path: str) -> GeneratorConfig:
    """Load configuration from a JSON/YAML file."""
    import json
    import yaml
    
    with open(config_path, 'r') as f:
        if config_path.endswith('.json'):
            data = json.load(f)
        elif config_path.endswith(('.yaml', '.yml')):
            data = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported config file format")
    
    # Convert string enums back to enum values
    if 'code_type' in data:
        data['code_type'] = CodeType(data['code_type'])
    if 'coverage_type' in data:
        data['coverage_type'] = TestCoverage(data['coverage_type'])
    if 'mock_level' in data:
        data['mock_level'] = MockLevel(data['mock_level'])
    
    return GeneratorConfig(**data)


def save_config_to_file(config: GeneratorConfig, config_path: str) -> None:
    """Save configuration to a JSON/YAML file."""
    import json
    import yaml
    
    # Convert enums to strings for serialization
    data = {}
    for key, value in config.__dict__.items():
        if isinstance(value, Enum):
            data[key] = value.value
        elif isinstance(value, set):
            data[key] = list(value)
        else:
            data[key] = value
    
    with open(config_path, 'w') as f:
        if config_path.endswith('.json'):
            json.dump(data, f, indent=2)
        elif config_path.endswith(('.yaml', '.yml')):
            yaml.dump(data, f, default_flow_style=False)
        else:
            raise ValueError("Unsupported config file format")
