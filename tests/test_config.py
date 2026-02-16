"""
Test suite for configuration manager.
"""

import pytest
import json
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager class."""
    
    def test_default_config_exists(self):
        """Test that default configuration has all required keys."""
        cm = ConfigManager()
        config = cm.load_config()
        
        assert 'keys_to_monitor' in config
        assert 'overlay' in config
        assert 'appearance' in config
        assert 'statistics' in config
        
    def test_keys_to_monitor_is_list(self):
        """Test that keys_to_monitor is a list."""
        cm = ConfigManager()
        config = cm.load_config()
        
        assert isinstance(config['keys_to_monitor'], list)
        assert len(config['keys_to_monitor']) > 0
        
    def test_default_keys(self):
        """Test default monitored keys."""
        cm = ConfigManager()
        config = cm.load_config()
        
        expected_keys = ['d', 'f', 'j', 'k']
        assert config['keys_to_monitor'] == expected_keys
        
    def test_overlay_config_structure(self):
        """Test overlay configuration structure."""
        cm = ConfigManager()
        config = cm.load_config()
        
        overlay = config['overlay']
        assert 'width' in overlay
        assert 'height' in overlay
        assert 'position' in overlay
        assert 'always_on_top' in overlay
        assert 'transparent' in overlay
        
    def test_appearance_config_structure(self):
        """Test appearance configuration structure."""
        cm = ConfigManager()
        config = cm.load_config()
        
        appearance = config['appearance']
        assert 'background_color' in appearance
        assert 'active_key_color' in appearance
        assert 'inactive_key_color' in appearance
        assert 'text_color' in appearance
        assert 'font_family' in appearance
        assert 'font_size' in appearance
        
    def test_get_method(self):
        """Test ConfigManager get method."""
        cm = ConfigManager()
        cm.load_config()
        
        keys = cm.get('keys_to_monitor')
        assert keys is not None
        assert isinstance(keys, list)
        
    def test_get_method_with_default(self):
        """Test ConfigManager get method with default value."""
        cm = ConfigManager()
        cm.load_config()
        
        value = cm.get('nonexistent_key', 'default_value')
        assert value == 'default_value'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
