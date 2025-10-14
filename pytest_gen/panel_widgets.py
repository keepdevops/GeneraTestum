"""
Legacy import compatibility for Panel widgets.
"""

# Import the refactored components
from .config_widgets import ConfigWidgets
from .ui_widgets import ActionWidgets, PreviewWidget, FileTreeWidget

# Maintain backward compatibility
__all__ = ['ConfigWidgets', 'ActionWidgets', 'PreviewWidget', 'FileTreeWidget']
