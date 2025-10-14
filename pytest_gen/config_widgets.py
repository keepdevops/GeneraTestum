"""
Configuration widgets for test generation settings.
"""

import panel as pn
from panel.widgets import TextInput, Select, Checkbox, IntInput, Accordion
from typing import Dict, Any
from .config import GeneratorConfig, MockLevel, TestCoverage


class ConfigWidgets:
    """Configuration widgets for test generation settings."""
    
    def __init__(self, config: GeneratorConfig = None):
        self.config = config or GeneratorConfig()
        self.widgets = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all configuration widgets."""
        # Language selection
        self.widgets['language'] = Select(
            name="Language",
            options=["Python", "Java", "Panel"],
            value="Python",
            width=200
        )
        
        # Mock level
        self.widgets['mock_level'] = Select(
            name="Mock Level",
            options=[level.value for level in MockLevel],
            value=MockLevel.COMPREHENSIVE.value,
            width=200
        )
        
        # Coverage type
        self.widgets['coverage'] = Select(
            name="Test Coverage",
            options=[coverage.value for coverage in TestCoverage],
            value=TestCoverage.COMPREHENSIVE.value,
            width=200
        )
        
        # Output directory
        self.widgets['output_dir'] = TextInput(
            name="Output Directory",
            value=self.config.output_dir,
            width=300
        )
        
        # Max lines per file
        self.widgets['max_lines'] = IntInput(
            name="Max Lines Per File",
            value=self.config.max_lines_per_file,
            start=50,
            end=500,
            width=150
        )
        
        # Boolean options
        self.widgets['include_private'] = Checkbox(
            name="Include Private Methods",
            value=self.config.include_private_methods
        )
        
        self.widgets['generate_fixtures'] = Checkbox(
            name="Generate Fixtures",
            value=self.config.generate_fixtures
        )
        
        self.widgets['generate_parametrize'] = Checkbox(
            name="Generate Parametrized Tests",
            value=self.config.generate_parametrize
        )
        
        self.widgets['split_files'] = Checkbox(
            name="Split Large Files",
            value=self.config.split_large_tests
        )
        
        # Mock options
        self.widgets['mock_external'] = Checkbox(
            name="Mock External Calls",
            value=self.config.mock_external_calls
        )
        
        self.widgets['mock_database'] = Checkbox(
            name="Mock Database",
            value=self.config.mock_database
        )
        
        self.widgets['mock_file_io'] = Checkbox(
            name="Mock File I/O",
            value=self.config.mock_file_io
        )
        
        self.widgets['mock_network'] = Checkbox(
            name="Mock Network",
            value=self.config.mock_network
        )
    
    def get_config_from_widgets(self) -> GeneratorConfig:
        """Get configuration from widget values."""
        config = GeneratorConfig()
        
        # Map widget values to config
        config.mock_level = MockLevel(self.widgets['mock_level'].value)
        config.coverage_type = TestCoverage(self.widgets['coverage'].value)
        config.output_dir = self.widgets['output_dir'].value
        config.max_lines_per_file = self.widgets['max_lines'].value
        config.include_private_methods = self.widgets['include_private'].value
        config.generate_fixtures = self.widgets['generate_fixtures'].value
        config.generate_parametrize = self.widgets['generate_parametrize'].value
        config.split_large_tests = self.widgets['split_files'].value
        config.mock_external_calls = self.widgets['mock_external'].value
        config.mock_database = self.widgets['mock_database'].value
        config.mock_file_io = self.widgets['mock_file_io'].value
        config.mock_network = self.widgets['mock_network'].value
        
        return config
    
    def update_widgets_from_config(self, config: GeneratorConfig):
        """Update widgets from configuration object."""
        self.widgets['mock_level'].value = config.mock_level.value
        self.widgets['coverage'].value = config.coverage_type.value
        self.widgets['output_dir'].value = config.output_dir
        self.widgets['max_lines'].value = config.max_lines_per_file
        self.widgets['include_private'].value = config.include_private_methods
        self.widgets['generate_fixtures'].value = config.generate_fixtures
        self.widgets['generate_parametrize'].value = config.generate_parametrize
        self.widgets['split_files'].value = config.split_large_tests
        self.widgets['mock_external'].value = config.mock_external_calls
        self.widgets['mock_database'].value = config.mock_database
        self.widgets['mock_file_io'].value = config.mock_file_io
        self.widgets['mock_network'].value = config.mock_network
    
    def get_layout(self):
        """Get the complete configuration layout."""
        # Group widgets into sections
        basic_section = pn.Column(
            pn.pane.HTML("<h3>Basic Settings</h3>"),
            pn.Row(self.widgets['language'], self.widgets['output_dir']),
            pn.Row(self.widgets['mock_level'], self.widgets['coverage']),
            pn.Row(self.widgets['max_lines']),
        )
        
        options_section = pn.Column(
            pn.pane.HTML("<h3>Test Options</h3>"),
            self.widgets['include_private'],
            self.widgets['generate_fixtures'],
            self.widgets['generate_parametrize'],
            self.widgets['split_files']
        )
        
        mock_section = pn.Column(
            pn.pane.HTML("<h3>Mock Settings</h3>"),
            self.widgets['mock_external'],
            self.widgets['mock_database'],
            self.widgets['mock_file_io'],
            self.widgets['mock_network']
        )
        
        return Accordion(
            ("Basic Settings", basic_section),
            ("Test Options", options_section),
            ("Mock Settings", mock_section),
            active=[0, 1, 2]
        )
