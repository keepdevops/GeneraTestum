"""
Dashboard CSS styles - refactored for 200LOC limit.
"""

from .dashboard_base_styles import DashboardBaseStyles
from .dashboard_advanced_styles import DashboardAdvancedStyles


class DashboardCSS:
    """Dashboard CSS styles and styling utilities."""
    
    def __init__(self):
        self.base_styles = DashboardBaseStyles()
        self.advanced_styles = DashboardAdvancedStyles()
    
    def get_all_styles(self) -> str:
        """Get all CSS styles."""
        return f"""
        <style>
        {self.base_styles.get_base_styles()}
        {self.base_styles.get_responsive_styles()}
        {self.advanced_styles.get_animation_styles()}
        {self.advanced_styles.get_chart_styles()}
        {self.advanced_styles.get_glassmorphism_styles()}
        {self.advanced_styles.get_dark_mode_styles()}
        </style>
        """
    
    def get_base_styles(self) -> str:
        """Get base CSS styles."""
        return self.base_styles.get_base_styles()
    
    def get_responsive_styles(self) -> str:
        """Get responsive CSS styles."""
        return self.base_styles.get_responsive_styles()
    
    def get_animation_styles(self) -> str:
        """Get animation styles."""
        return self.advanced_styles.get_animation_styles()
    
    def get_chart_styles(self) -> str:
        """Get chart styles."""
        return self.advanced_styles.get_chart_styles()
    
    def get_glassmorphism_styles(self) -> str:
        """Get glassmorphism styles."""
        return self.advanced_styles.get_glassmorphism_styles()
    
    def get_dark_mode_styles(self) -> str:
        """Get dark mode styles."""
        return self.advanced_styles.get_dark_mode_styles()
    
    def get_compact_styles(self) -> str:
        """Get compact version of all styles."""
        return f"""
        <style>
        {self.base_styles.get_base_styles()}
        {self.advanced_styles.get_animation_styles()}
        </style>
        """
    
    def get_mobile_styles(self) -> str:
        """Get mobile-optimized styles."""
        return f"""
        <style>
        {self.base_styles.get_base_styles()}
        {self.base_styles.get_responsive_styles()}
        {self.advanced_styles.get_animation_styles()}
        </style>
        """
    
    def get_theme_styles(self, theme: str = "light") -> str:
        """Get theme-specific styles."""
        base_css = self.base_styles.get_base_styles()
        
        if theme == "dark":
            theme_css = self.advanced_styles.get_dark_mode_styles()
        elif theme == "glassmorphism":
            theme_css = self.advanced_styles.get_glassmorphism_styles()
        else:
            theme_css = ""
        
        return f"""
        <style>
        {base_css}
        {theme_css}
        {self.advanced_styles.get_animation_styles()}
        </style>
        """