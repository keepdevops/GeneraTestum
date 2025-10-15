"""
Complex test guide templates.
"""

from .test_guide_basic_templates import TestGuideBasicTemplates
from .test_guide_advanced_templates import TestGuideAdvancedTemplates


class TestGuideTemplatesComplex:
    """Complex test guide templates."""
    
    def __init__(self):
        self.basic_templates = TestGuideBasicTemplates()
        self.advanced_templates = TestGuideAdvancedTemplates()
    
    def get_test_structure_template(self) -> str:
        """Get test structure template."""
        return self.basic_templates.get_test_structure_template()

    def get_test_types_template(self) -> str:
        """Get test types template."""
        return self.basic_templates.get_test_types_template()

    def get_test_patterns_template(self) -> str:
        """Get test patterns template."""
        return self.basic_templates.get_test_patterns_template()

    def get_mocking_guide_template(self) -> str:
        """Get mocking guide template."""
        return self.basic_templates.get_mocking_guide_template()

    def get_testing_best_practices_template(self) -> str:
        """Get testing best practices template."""
        return self.advanced_templates.get_testing_best_practices_template()

    def get_debugging_guide_template(self) -> str:
        """Get debugging guide template."""
        return self.advanced_templates.get_debugging_guide_template()

    def get_ci_cd_integration_template(self) -> str:
        """Get CI/CD integration template."""
        return self.advanced_templates.get_ci_cd_integration_template()

    def get_advanced_testing_template(self) -> str:
        """Get advanced testing template."""
        return self.advanced_templates.get_advanced_testing_template()
