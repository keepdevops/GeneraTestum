"""
Test library manager for accessing and using test patterns and templates.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class TestLibraryManager:
    """Manages test patterns, templates, and examples."""

    def __init__(self, library_path: str = "test_library"):
        self.library_path = Path(library_path)
        self.patterns = {}
        self.templates = {}
        self.examples = {}
        self._load_library()

    def _load_library(self):
        """Load all patterns, templates, and examples from the library."""
        if not self.library_path.exists():
            return

        # Load patterns
        patterns_dir = self.library_path / "patterns"
        if patterns_dir.exists():
            for pattern_file in patterns_dir.glob("*.json"):
                with open(pattern_file, 'r') as f:
                    pattern_data = json.load(f)
                    self.patterns.update(pattern_data.get("patterns", {}))

        # Load templates
        templates_dir = self.library_path / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.py"):
                with open(template_file, 'r') as f:
                    template_name = template_file.stem
                    self.templates[template_name] = f.read()

        # Load examples
        examples_dir = self.library_path / "examples"
        if examples_dir.exists():
            for example_file in examples_dir.glob("*.py"):
                with open(example_file, 'r') as f:
                    example_name = example_file.stem
                    self.examples[example_name] = f.read()

    def get_patterns_for_function(self, function_name: str, function_type: str = "basic") -> List[Dict[str, Any]]:
        """Get test patterns for a specific function type."""
        patterns = []
        
        if function_type == "basic":
            basic_patterns = self.patterns.get("basic_function_patterns", {}).get("patterns", {})
            for pattern_name, pattern_data in basic_patterns.items():
                patterns.extend(pattern_data.get("test_cases", []))
        
        elif function_type == "api":
            api_patterns = self.patterns.get("api_patterns", {}).get("patterns", {})
            for pattern_name, pattern_data in api_patterns.items():
                patterns.extend(pattern_data.get("test_cases", []))
        
        return patterns

    def get_patterns_for_class(self, class_name: str) -> List[Dict[str, Any]]:
        """Get test patterns for a class."""
        patterns = []
        class_patterns = self.patterns.get("class_patterns", {}).get("patterns", {})
        
        for pattern_name, pattern_data in class_patterns.items():
            patterns.extend(pattern_data.get("test_cases", []))
        
        return patterns

    def get_template(self, template_name: str) -> Optional[str]:
        """Get a specific template by name."""
        return self.templates.get(template_name)

    def get_example(self, example_name: str) -> Optional[str]:
        """Get a specific example by name."""
        return self.examples.get(example_name)

    def get_matching_examples(self, function_name: str, function_type: str = "basic") -> List[str]:
        """Get examples that match the function type or name."""
        matching_examples = []
        
        for example_name, example_content in self.examples.items():
            if function_type in example_name.lower() or function_name.lower() in example_name.lower():
                matching_examples.append(example_name)
        
        return matching_examples

    def get_pattern_examples(self, pattern_name: str) -> Dict[str, Any]:
        """Get examples for a specific pattern."""
        # Search through all patterns for examples
        for pattern_category, patterns in self.patterns.items():
            if isinstance(patterns, dict):
                for name, pattern_data in patterns.items():
                    if name == pattern_name:
                        return pattern_data.get("examples", {})
        
        return {}

    def suggest_test_cases(self, function_name: str, function_type: str = "basic") -> List[str]:
        """Suggest test cases based on patterns and examples."""
        suggestions = []
        
        # Get patterns for this function type
        patterns = self.get_patterns_for_function(function_name, function_type)
        
        for pattern in patterns:
            pattern_name = pattern.get("name", "")
            pattern_desc = pattern.get("description", "")
            suggestions.append(f"{pattern_name}: {pattern_desc}")
        
        return suggestions

    def generate_test_from_template(self, template_name: str, **kwargs) -> str:
        """Generate test code from a template with substitutions."""
        template = self.get_template(template_name)
        if not template:
            return ""
        
        # Simple string substitution
        # In a more sophisticated implementation, you'd use a proper templating engine
        for key, value in kwargs.items():
            template = template.replace(f"{{{key}}}", str(value))
        
        return template

    def get_library_stats(self) -> Dict[str, int]:
        """Get statistics about the test library."""
        return {
            "patterns": len(self.patterns),
            "templates": len(self.templates),
            "examples": len(self.examples)
        }

    def add_pattern(self, pattern_name: str, pattern_data: Dict[str, Any]):
        """Add a new pattern to the library."""
        self.patterns[pattern_name] = pattern_data

    def add_template(self, template_name: str, template_content: str):
        """Add a new template to the library."""
        self.templates[template_name] = template_content

    def add_example(self, example_name: str, example_content: str):
        """Add a new example to the library."""
        self.examples[example_name] = example_content

    def save_library(self):
        """Save the library back to disk."""
        # Save patterns
        patterns_dir = self.library_path / "patterns"
        patterns_dir.mkdir(parents=True, exist_ok=True)
        
        # Group patterns by category and save as JSON files
        pattern_categories = {}
        for pattern_name, pattern_data in self.patterns.items():
            category = pattern_data.get("category", "general")
            if category not in pattern_categories:
                pattern_categories[category] = {"patterns": {}}
            pattern_categories[category]["patterns"][pattern_name] = pattern_data
        
        for category, data in pattern_categories.items():
            with open(patterns_dir / f"{category}_patterns.json", 'w') as f:
                json.dump(data, f, indent=2)

        # Save templates
        templates_dir = self.library_path / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        for template_name, template_content in self.templates.items():
            with open(templates_dir / f"{template_name}.py", 'w') as f:
                f.write(template_content)

        # Save examples
        examples_dir = self.library_path / "examples"
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        for example_name, example_content in self.examples.items():
            with open(examples_dir / f"{example_name}.py", 'w') as f:
                f.write(example_content)
