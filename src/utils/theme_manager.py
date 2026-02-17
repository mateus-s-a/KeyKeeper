"""
Theme Manager Module
Manages application themes and provides theme loading/switching functionality.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


class ThemeManager:
    """
    Manages themes for the keyboard overlay.
    Loads, validates, and applies themes.
    """
    
    def __init__(self, themes_directory: Optional[str] = None):
        """
        Initialize the theme manager.
        
        Args:
            themes_directory: Optional custom themes directory path
        """
        if themes_directory is None:
            # Default to assets/themes directory
            self.themes_dir = Path(__file__).parent.parent.parent / "assets" / "themes"
        else:
            self.themes_dir = Path(themes_directory)
        
        self.themes = {}
        self.current_theme = None
        self.load_themes()
    
    def load_themes(self):
        """Load all themes from the themes directory."""
        if not self.themes_dir.exists():
            print(f"Themes directory not found: {self.themes_dir}")
            return
        
        # Load all .json files in themes directory
        for theme_file in self.themes_dir.glob("*.json"):
            try:
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                
                theme_name = theme_data.get('theme_name', theme_file.stem)
                self.themes[theme_name] = theme_data
                print(f"Loaded theme: {theme_name}")
                
            except Exception as e:
                print(f"Error loading theme {theme_file}: {e}")
    
    def get_theme(self, theme_name: str) -> Optional[Dict]:
        """
        Get a theme by name.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Theme dictionary or None if not found
        """
        return self.themes.get(theme_name)
    
    def get_theme_names(self) -> List[str]:
        """
        Get list of available theme names.
        
        Returns:
            List of theme names
        """
        return sorted(self.themes.keys())
    
    def apply_theme(self, theme_name: str, config: Dict) -> Dict:
        """
        Apply a theme to the configuration.
        
        Args:
            theme_name: Name of theme to apply
            config: Current configuration dictionary
            
        Returns:
            Updated configuration dictionary
        """
        theme = self.get_theme(theme_name)
        
        if not theme:
            print(f"Theme not found: {theme_name}")
            return config
        
        # Update appearance settings from theme
        if 'appearance' in theme:
            config['appearance'].update(theme['appearance'])
            self.current_theme = theme_name
            print(f"Applied theme: {theme_name}")
        
        return config
    
    def create_theme_from_config(self, theme_name: str, 
                                  config: Dict,
                                  description: str = "") -> bool:
        """
        Create a new theme from current configuration.
        
        Args:
            theme_name: Name for the new theme
            config: Configuration to extract theme from
            description: Optional theme description
            
        Returns:
            True if successful, False otherwise
        """
        try:
            theme_data = {
                "theme_name": theme_name,
                "description": description,
                "appearance": config.get('appearance', {})
            }
            
            # Save theme file
            theme_file = self.themes_dir / f"{theme_name.lower().replace(' ', '_')}.json"
            
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=4)
            
            # Add to loaded themes
            self.themes[theme_name] = theme_data
            
            print(f"Created theme: {theme_name}")
            return True
            
        except Exception as e:
            print(f"Error creating theme: {e}")
            return False
    
    def delete_theme(self, theme_name: str) -> bool:
        """
        Delete a theme.
        
        Args:
            theme_name: Name of theme to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            theme = self.get_theme(theme_name)
            if not theme:
                return False
            
            # Find and delete theme file
            theme_file = self.themes_dir / f"{theme_name.lower().replace(' ', '_')}.json"
            
            if theme_file.exists():
                theme_file.unlink()
            
            # Remove from loaded themes
            if theme_name in self.themes:
                del self.themes[theme_name]
            
            print(f"Deleted theme: {theme_name}")
            return True
            
        except Exception as e:
            print(f"Error deleting theme: {e}")
            return False
    
    def get_theme_preview(self, theme_name: str) -> Dict:
        """
        Get preview information for a theme.
        
        Args:
            theme_name: Name of theme
            
        Returns:
            Dictionary with preview information
        """
        theme = self.get_theme(theme_name)
        
        if not theme:
            return {}
        
        appearance = theme.get('appearance', {})
        
        return {
            'name': theme_name,
            'description': theme.get('description', 'No description'),
            'background': appearance.get('background_color', '#1a1a1a'),
            'active_key': appearance.get('active_key_color', '#00ff00'),
            'inactive_key': appearance.get('inactive_key_color', '#333333'),
            'text': appearance.get('text_color', '#ffffff'),
            'border': appearance.get('border_color', '#666666')
        }
    
    def export_theme(self, theme_name: str, export_path: str) -> bool:
        """
        Export a theme to a file.
        
        Args:
            theme_name: Name of theme to export
            export_path: Path to export to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            theme = self.get_theme(theme_name)
            if not theme:
                return False
            
            with open(export_path, 'w') as f:
                json.dump(theme, f, indent=4)
            
            print(f"Exported theme to: {export_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting theme: {e}")
            return False
    
    def import_theme(self, theme_file_path: str) -> Optional[str]:
        """
        Import a theme from a file.
        
        Args:
            theme_file_path: Path to theme file
            
        Returns:
            Theme name if successful, None otherwise
        """
        try:
            with open(theme_file_path, 'r') as f:
                theme_data = json.load(f)
            
            theme_name = theme_data.get('theme_name', Path(theme_file_path).stem)
            
            # Save to themes directory
            theme_file = self.themes_dir / f"{theme_name.lower().replace(' ', '_')}.json"
            
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=4)
            
            # Add to loaded themes
            self.themes[theme_name] = theme_data
            
            print(f"Imported theme: {theme_name}")
            return theme_name
            
        except Exception as e:
            print(f"Error importing theme: {e}")
            return None
