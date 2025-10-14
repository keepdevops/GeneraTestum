"""
Preview generation methods for GUI.
"""

from typing import Dict, Any
from .config import GeneratorConfig


class GUIPreviewHandlers:
    """Preview generation methods for GUI."""
    
    def __init__(self, preview_widget):
        self.preview_widget = preview_widget
    
    def generate_preview_content(self, file_path: str, analysis: Dict[str, Any], config: GeneratorConfig) -> str:
        """Generate preview content for test generation."""
        content = f"# Test Preview for {file_path}\n\n"
        content += f"**File Type:** {analysis.get('file_type', 'unknown')}\n\n"
        
        # Functions
        functions = analysis.get('functions', [])
        if functions:
            content += f"**Functions ({len(functions)}):**\n"
            for func in functions:
                content += f"- {func['name']} ({func['parameters']} parameters)\n"
            content += "\n"
        
        # Classes
        classes = analysis.get('classes', [])
        if classes:
            content += f"**Classes ({len(classes)}):**\n"
            for cls in classes:
                content += f"- {cls['name']} ({cls['methods']} methods)\n"
            content += "\n"
        
        # Endpoints
        endpoints = analysis.get('endpoints', [])
        if endpoints:
            content += f"**API Endpoints ({len(endpoints)}):**\n"
            for endpoint in endpoints:
                content += f"- {endpoint['method']} {endpoint['path']}\n"
            content += "\n"
        
        # Configuration
        content += "**Configuration:**\n"
        content += f"- Mock Level: {config.mock_level}\n"
        content += f"- Coverage Type: {config.coverage_type}\n"
        content += f"- Include Private Methods: {config.include_private_methods}\n"
        content += f"- Generate Fixtures: {config.generate_fixtures}\n"
        content += f"- Max Lines Per File: {config.max_lines_per_file}\n\n"
        
        # Sample test
        content += "**Sample Generated Test:**\n"
        content += "```python\n"
        content += "import pytest\n"
        content += "from example_module import sample_function\n\n"
        content += "def test_sample_function():\n"
        content += "    \"\"\"Test sample_function.\"\"\"\n"
        content += "    # Arrange\n"
        content += "    input_value = \"test\"\n\n"
        content += "    # Act\n"
        content += "    result = sample_function(input_value)\n\n"
        content += "    # Assert\n"
        content += "    assert result is not None\n"
        content += "    assert isinstance(result, str)\n"
        content += "```\n\n"
        content += f"**Estimated Tests:** {analysis.get('estimated_tests', 0)}"
        
        return content
