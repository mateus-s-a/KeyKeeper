# Development Guide

## Architecture Overview

The Keyboard Overlay application follows a modular architecture with clear separation of concerns:

### Module Structure

```
src/
├── core/           # Application core and orchestration
├── gui/            # User interface components
├── input/          # Keyboard input handling
├── config/         # Configuration management
└── utils/          # Shared utilities
```

### Key Components

#### 1. Core Module (`src/core/`)
- **app.py**: Main application controller
  - Orchestrates all components
  - Manages application lifecycle
  - Handles communication between modules

#### 2. GUI Module (`src/gui/`)
- **overlay_window.py**: Overlay window implementation
  - Creates transparent, always-on-top window
  - Displays key states visually
  - Handles window configuration

#### 3. Input Module (`src/input/`)
- **keyboard_listener.py**: Keyboard event handling
  - Uses pynput to capture keyboard events
  - Filters events for monitored keys only
  - Thread-safe key state management

#### 4. Config Module (`src/config/`)
- **config_manager.py**: Configuration management
  - Loads/saves JSON configuration
  - Provides default values
  - Merges user config with defaults

## Configuration

### Configuration File Structure

The application uses a JSON configuration file (`src/config/default_config.json`):

```json
{
    "keys_to_monitor": ["d", "f", "j", "k"],
    "overlay": {
        "width": 400,
        "height": 150,
        "position": {"x": 100, "y": 100},
        "always_on_top": true,
        "transparent": true,
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
        "enabled": false,
        "show_kps": false,
        "show_press_count": false,
        "kps_update_interval": 1.0
    }
}
```

### Customization Options

#### Keys to Monitor
Edit the `keys_to_monitor` array to change which keys are displayed:
```json
"keys_to_monitor": ["a", "s", "d", "w"]  // WASD keys for gaming
```

#### Visual Appearance
- `background_color`: Overlay background (hex color)
- `active_key_color`: Color when key is pressed
- `inactive_key_color`: Color when key is not pressed
- `text_color`: Key letter color
- `font_family`: Font name (must be installed on system)
- `font_size`: Size of key letters

#### Window Position
- `overlay.position.x`: X coordinate on screen
- `overlay.position.y`: Y coordinate on screen
- `overlay.width`: Window width in pixels
- `overlay.height`: Window height in pixels

## Adding New Features

### Adding Statistics Module (Future)

To add KPS (Keys Per Second) tracking:

1. Create `src/core/statistics.py`:
```python
class StatisticsTracker:
    def __init__(self):
        self.key_presses = []
        
    def record_press(self, key):
        # Record timestamp of key press
        pass
        
    def calculate_kps(self):
        # Calculate keys per second
        pass
```

2. Integrate into `app.py`:
```python
from core.statistics import StatisticsTracker

class KeyboardOverlayApp:
    def __init__(self):
        # ...existing code...
        if self.config.get('statistics', {}).get('enabled'):
            self.stats = StatisticsTracker()
```

3. Update `overlay_window.py` to display statistics.

### Adding New Keys

The system automatically supports any keyboard key recognized by pynput:
- Alphanumeric: a-z, 0-9
- Special keys: space, enter, shift, ctrl, alt, etc.
- Function keys: f1-f12
- Arrow keys: up, down, left, right

Just add them to the `keys_to_monitor` array in the config.

## Testing

### Running Tests
```bash
pytest tests/
```

### Writing Tests
Create test files in the `tests/` directory:

```python
# tests/test_config.py
import pytest
from src.config.config_manager import ConfigManager

def test_load_default_config():
    cm = ConfigManager()
    config = cm.load_config()
    assert 'keys_to_monitor' in config
    assert len(config['keys_to_monitor']) > 0
```

## Linux-Specific Notes

### Permissions
On Linux, the application needs permission to capture keyboard events:
- Run with appropriate permissions if needed
- May require adding user to input group

### X11 vs Wayland
- The application is designed for X11
- Wayland may require additional configuration
- Transparency and always-on-top work best on X11

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-xlib

# For development
sudo apt-get install python3-pip python3-venv
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document all public methods
- Keep functions focused and single-purpose
- Use meaningful variable names

## Future Enhancements

### Planned Features
1. **Statistics Module**
   - Keys per second (KPS)
   - Total key press counter
   - Per-key press counts
   - Historical data tracking

2. **Profile System**
   - Multiple configuration profiles
   - Quick profile switching
   - Per-application profiles

3. **Visual Enhancements**
   - Theme system with presets
   - Key press animations
   - Heat map visualization
   - Customizable key shapes

4. **Advanced Features**
   - Recording and replay
   - Key combination tracking
   - Macro detection
   - Export statistics to CSV

### Contributing
When adding features:
1. Create feature branch
2. Follow existing code structure
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

## Troubleshooting

### Common Issues

**Keys not being detected:**
- Check if keys are listed in `keys_to_monitor`
- Verify pynput is installed correctly
- Check console for error messages

**Overlay not visible:**
- Check `overlay.always_on_top` setting
- Verify window position is on screen
- Check opacity setting (should be > 0)

**Poor performance:**
- Reduce `opacity` value
- Decrease `font_size`
- Disable statistics if enabled

### Debug Mode
To enable verbose logging, modify `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
