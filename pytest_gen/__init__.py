"""
Pytest Code Generator

A comprehensive tool for generating pytest test cases from Python code,
APIs, and other code types with automatic mocking and fixtures.
"""

__version__ = "1.0.0"
__author__ = "Pytest Generator"

from .generator_core import generate_tests, GeneratorCore
from .config import DEFAULT_CONFIG, GeneratorConfig
from .panel_gui import launch_gui
from .ai_assistant import AIAssistant

__all__ = [
    "generate_tests",
    "GeneratorCore",
    "GeneratorConfig", 
    "DEFAULT_CONFIG",
    "launch_gui",
    "AIAssistant"
]
