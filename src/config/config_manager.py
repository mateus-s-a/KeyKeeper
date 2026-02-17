"""
Configuration Manager Module
Handles loading, saving, and managing application configuration.
"""

import os
import json
from pathlib import Path


class ConfigManager:
    """
    Manages application configuration settings.
    Handles loading from files and providing default values.
    """
    
    DEFAULT_CONFIG = {
        "keys_to_monitor": ["d", "f", "j", "k"],
        "overlay": {
            "width": 400,
            "height": 150,
            "position": {
                "x": 100,
                "y": 100
            },
            "always_on_top": True,
            "transparent": True,
            "opacity": 0.9
        },
        "appearance": {
            "background_color": "#1a1a1a",
            "active_key_color": "#00ff00",
            "inactive_key_color": "#333333",
            "text_color": "#ffffff",
            "font_family": "Arial",
            "font_size": 24,
            "key_padding": 10,
            "border_width": 2,
            "border_color": "#666666"
        },
        "statistics": {
            "enabled": True,
            "show_kps": True,
            "show_press_count": True,
            "kps_update_interval": 0.1
        }
    }
    
    def __init__(self, config_path=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        if config_path is None:
            # Use default config path in config directory
            self.config_path = Path(__file__).parent / "default_config.json"
        else:
            self.config_path = Path(config_path)
            
        self.config = None
        
    def load_config(self):
        """
        Load configuration from file or use defaults.
        
        Returns:
            dict: Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.config = self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
                    print(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                self.config = self.DEFAULT_CONFIG.copy()
        else:
            print(f"No config file found. Using defaults.")
            self.config = self.DEFAULT_CONFIG.copy()
            # Save default config for user reference
            self.save_config()
            
        return self.config
    
    def save_config(self, config=None):
        """
        Save configuration to file.
        
        Args:
            config: Optional configuration dict to save. Uses current if None.
        """
        if config is not None:
            self.config = config
            
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if self.config is None:
            self.load_config()
        return self.config.get(key, default)
    
    def _merge_configs(self, default, loaded):
        """
        Recursively merge loaded config with defaults.
        
        Args:
            default: Default configuration
            loaded: Loaded configuration
            
        Returns:
            Merged configuration
        """
        merged = default.copy()
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
