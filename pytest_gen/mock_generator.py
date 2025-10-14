"""
Mock generation for external dependencies and external calls.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass
from .config import GeneratorConfig, MockLevel
from .code_analyzer import FunctionInfo, ClassInfo, ModuleInfo


@dataclass
class MockInfo:
    """Information about a mock to be generated."""
    target: str  # What to mock (e.g., "requests.get", "database.query")
    mock_name: str  # Variable name for the mock
    return_value: Optional[Any] = None
    side_effect: Optional[Any] = None
    is_patch: bool = True
    patch_path: Optional[str] = None
    mock_type: str = "MagicMock"  # MagicMock, Mock, AsyncMock


class MockGenerator:
    """Generates mock configurations for external dependencies."""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self._common_mocks = {
            'requests': {
                'requests.get': {'return_value': 'mock_response'},
                'requests.post': {'return_value': 'mock_response'},
                'requests.put': {'return_value': 'mock_response'},
                'requests.delete': {'return_value': 'mock_response'},
            },
            'database': {
                'database.query': {'return_value': 'mock_result'},
                'database.execute': {'return_value': 'mock_result'},
                'database.commit': {'return_value': None},
            },
            'file_io': {
                'open': {'return_value': 'mock_file'},
                'os.path.exists': {'return_value': True},
                'os.path.join': {'return_value': 'mock_path'},
            },
            'datetime': {
                'datetime.now': {'return_value': 'mock_datetime'},
                'datetime.today': {'return_value': 'mock_date'},
            }
        }
    
    def generate_mocks_for_function(self, func_info: FunctionInfo) -> List[MockInfo]:
        """Generate mocks needed for a specific function."""
        if self.config.mock_level == MockLevel.NONE:
            return []
        
        mocks = []
        
        # Generate mocks based on function dependencies
        for dep in func_info.dependencies:
            mock = self._create_mock_for_dependency(dep)
            if mock:
                mocks.append(mock)
        
        # Generate mocks for external calls
        if self.config.mock_external_calls:
            mocks.extend(self._generate_external_call_mocks(func_info))
        
        return mocks
    
    def generate_mocks_for_module(self, module_info: ModuleInfo) -> List[MockInfo]:
        """Generate mocks for an entire module."""
        if self.config.mock_level == MockLevel.NONE:
            return []
        
        mocks = []
        
        # Collect all dependencies from the module
        all_deps = set(module_info.dependencies)
        for func in module_info.functions:
            all_deps.update(func.dependencies)
        for cls in module_info.classes:
            all_deps.update(cls.dependencies)
            for method in cls.methods:
                all_deps.update(method.dependencies)
        
        # Generate mocks for common dependencies
        for dep in all_deps:
            mock = self._create_mock_for_dependency(dep)
            if mock:
                mocks.append(mock)
        
        return self._deduplicate_mocks(mocks)
    
    def generate_mocks_for_api_endpoint(self, endpoint) -> List[MockInfo]:
        """Generate mocks needed for an API endpoint test."""
        if self.config.mock_level == MockLevel.NONE:
            return []
        
        mocks = []
        
        # Mock HTTP requests
        if hasattr(endpoint, 'method') and endpoint.method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
            method = endpoint.method.lower()
            mocks.append(MockInfo(
                target=f'requests.{method}',
                mock_name=f'mock_requests_{method}',
                return_value={
                    'status_code': 200,
                    'json': lambda: {'success': True, 'data': 'mock_data'},
                    'text': 'mock response'
                },
                is_patch=True,
                patch_path=f'requests.{method}'
            ))
        
        # Mock common API dependencies
        api_mocks = [
            ('requests.get', 'mock_requests_get'),
            ('requests.post', 'mock_requests_post'),
            ('requests.put', 'mock_requests_put'),
            ('requests.delete', 'mock_requests_delete'),
            ('json.loads', 'mock_json_loads'),
            ('json.dumps', 'mock_json_dumps'),
        ]
        
        for target, mock_name in api_mocks:
            mocks.append(MockInfo(
                target=target,
                mock_name=mock_name,
                return_value='mock_result' if 'json' not in target else '{"mock": "data"}',
                is_patch=True,
                patch_path=target
            ))
        
        return self._deduplicate_mocks(mocks)
    
    def get_mock_imports(self, mocks: List[MockInfo]) -> Set[str]:
        """Get import statements needed for the given mocks."""
        imports = set()
        
        for mock in mocks:
            if mock.is_patch:
                imports.add('from unittest.mock import patch')
                imports.add('from unittest.mock import Mock, MagicMock')
            
            # Add specific imports based on mock targets
            if 'requests' in mock.target:
                imports.add('import requests')
            if 'json' in mock.target:
                imports.add('import json')
            if 'datetime' in mock.target:
                imports.add('from datetime import datetime')
            if 'os' in mock.target:
                imports.add('import os')
        
        return imports
    
    def _create_mock_for_dependency(self, dependency: str) -> Optional[MockInfo]:
        """Create a mock for a specific dependency."""
        dependency_lower = dependency.lower()
        
        # Check for common mock patterns
        for category, mock_configs in self._common_mocks.items():
            if self._should_mock_category(category, dependency_lower):
                for target, config in mock_configs.items():
                    if any(keyword in dependency_lower for keyword in target.split('.')):
                        return MockInfo(
                            target=target,
                            mock_name=f"mock_{target.replace('.', '_')}",
                            return_value=config.get('return_value'),
                            side_effect=config.get('side_effect'),
                            is_patch=True,
                            patch_path=target
                        )
        
        return None
    
    def _generate_external_call_mocks(self, func_info: FunctionInfo) -> List[MockInfo]:
        """Generate mocks for external function calls."""
        mocks = []
        
        # Look for common external call patterns
        external_patterns = [
            'requests.', 'urllib.', 'http.',
            'database.', 'db.', 'sql.',
            'open(', 'file(', 'os.',
            'datetime.', 'time.',
        ]
        
        for pattern in external_patterns:
            if pattern in func_info.name.lower() or any(pattern in dep.lower() for dep in func_info.dependencies):
                mock = MockInfo(
                    target=pattern.rstrip('.()'),
                    mock_name=f"mock_{pattern.replace('.', '_').replace('(', '').replace(')', '')}",
                    return_value='mock_result',
                    is_patch=True,
                    patch_path=pattern.rstrip('.()')
                )
                mocks.append(mock)
        
        return mocks
    
    def _should_mock_category(self, category: str, dependency: str) -> bool:
        """Check if a dependency category should be mocked based on config."""
        if category == 'requests' and self.config.mock_network:
            return True
        elif category == 'database' and self.config.mock_database:
            return True
        elif category == 'file_io' and self.config.mock_file_io:
            return True
        elif category == 'datetime':
            return True  # Always mock datetime for reproducible tests
        return False
    
    def _deduplicate_mocks(self, mocks: List[MockInfo]) -> List[MockInfo]:
        """Remove duplicate mocks based on target."""
        seen = set()
        unique_mocks = []
        
        for mock in mocks:
            if mock.target not in seen:
                seen.add(mock.target)
                unique_mocks.append(mock)
        
        return unique_mocks
    
    def generate_mock_code(self, mock_info: MockInfo) -> str:
        """Generate the actual mock code."""
        if mock_info.is_patch:
            return f"@patch('{mock_info.patch_path}')\n"
        else:
            return f"{mock_info.mock_name} = {mock_info.mock_type}()\n"
    
    def get_mock_imports(self, mocks: List[MockInfo]) -> Set[str]:
        """Get required imports for mocks."""
        imports = set()
        
        if any(mock.is_patch for mock in mocks):
            imports.add('from unittest.mock import patch')
        
        if any(mock.mock_type != 'MagicMock' for mock in mocks):
            imports.add('from unittest.mock import Mock')
        
        return imports