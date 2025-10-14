"""
Database and file system mock generation functionality.
"""

from typing import Dict, List, Any
from .mock_models import DependencyInfo, MockConfig


class DatabaseMockGenerator:
    """Generates mocks for database dependencies."""

    def generate_mock(self, dep: DependencyInfo, config: MockConfig) -> str:
        """Generate mock for database dependencies."""
        mock_code = []
        
        mock_code.append("from unittest.mock import Mock, MagicMock")
        mock_code.append("")
        
        mock_code.append(f"class {dep.name.title()}Mock:")
        mock_code.append(f'    """Mock for {dep.name} database."""')
        mock_code.append("")
        
        mock_code.append("    def __init__(self):")
        mock_code.append("        self.connection = MagicMock()")
        mock_code.append("        self.cursor = MagicMock()")
        mock_code.append("        self.connection.cursor.return_value = self.cursor")
        mock_code.append("")
        
        # Common database operations
        mock_code.extend([
            "    def execute(self, query, params=None):",
            "        # Mock query execution",
            "        if 'SELECT' in query.upper():",
            "            return self._mock_select_result(query)",
            "        elif 'INSERT' in query.upper():",
            "            return self._mock_insert_result()",
            "        elif 'UPDATE' in query.upper():",
            "            return self._mock_update_result()",
            "        elif 'DELETE' in query.upper():",
            "            return self._mock_delete_result()",
            "        return None",
            "",
            "    def _mock_select_result(self, query):",
            "        # Return mock data based on query",
            "        if 'users' in query.lower():",
            "            return [{'id': 1, 'name': 'Test User', 'email': 'test@example.com'}]",
            "        elif 'products' in query.lower():",
            "            return [{'id': 1, 'name': 'Test Product', 'price': 99.99}]",
            "        return []",
            "",
            "    def _mock_insert_result(self):",
            "        return {'lastrowid': 1}",
            "",
            "    def _mock_update_result(self):",
            "        return {'rowcount': 1}",
            "",
            "    def _mock_delete_result(self):",
            "        return {'rowcount': 1}",
            ""
        ])
        
        return "\n".join(mock_code)


class FileMockGenerator:
    """Generates mocks for file system dependencies."""

    def generate_mock(self, dep: DependencyInfo, config: MockConfig) -> str:
        """Generate mock for file system dependencies."""
        mock_code = []
        
        mock_code.append("import tempfile")
        mock_code.append("import os")
        mock_code.append("from unittest.mock import patch, mock_open")
        mock_code.append("")
        
        mock_code.append(f"class {dep.name.title()}Mock:")
        mock_code.append(f'    """Mock for {dep.name} file operations."""')
        mock_code.append("")
        
        mock_code.extend([
            "    @staticmethod",
            "    def mock_file_operations():",
            "        # Mock file read/write operations",
            "        with patch('builtins.open', mock_open(read_data='mock file content')):",
            "            yield",
            "",
            "    @staticmethod",
            "    def create_temp_file(content='test content'):",
            "        # Create temporary file for testing",
            "        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:",
            "            f.write(content.encode())",
            "            return f.name",
            "",
            "    @staticmethod",
            "    def cleanup_temp_file(file_path):",
            "        # Clean up temporary file",
            "        if os.path.exists(file_path):",
            "            os.unlink(file_path)",
            ""
        ])
        
        return "\n".join(mock_code)
