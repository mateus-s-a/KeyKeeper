# Phase 2 Features Documentation

## Overview

Phase 2 adds enhanced GUI features including animations, a comprehensive settings window, and theme management.

## Features

### 1. Key Press Animations

Visual feedback effects that trigger when keys are pressed.

#### Animation Types

- **Pulse**: Border thickness pulsates (default)
- **Scale**: Key text scales up and down
- **Glow**: Border glows with increasing thickness
- **Fade**: Subtle fade effect

#### Configuration

```json
{
    "animations": {
        "enabled": true,
        "type": "pulse",
        "duration": 0.3
    }
}
```

#### Usage

```python
from gui.animations import AnimationController

controller = AnimationController()
controller.animate_key_press(
    key='d',
    widget_info=widget_dict,
    animation_type=AnimationController.PULSE,
    duration=0.3
)
```

#### Available Animation Types

| Type | Description | Visual Effect |
|------|-------------|---------------|
| `pulse` | Pulsing border | Border thickness varies |
| `scale` | Size animation | Font size grows/shrinks |
| `glow` | Glowing effect | Border thickness increases |
| `fade` | Fade effect | Opacity change simulation |

### 2. GUI Settings Window

Comprehensive settings interface with live preview.

#### Features

- **Tabbed Interface**: Organized settings by category
- **Live Preview**: See changes in real-time
- **Color Pickers**: Visual color selection
- **Presets**: Quick key configurations
- **Apply/Save Options**: Flexible saving

#### Tabs

##### Appearance Tab
- Background color
- Active/inactive key colors
- Text color
- Border color
- Font family and size
- Key padding
- Border width

##### Keys Tab
- Custom key configuration
- Quick presets:
  - Rhythm 4K (D, F, J, K)
  - Rhythm 7K (S, D, F, Space, J, K, L)
  - WASD
  - Arrow keys
  - QWER

##### Overlay Tab
- Window size (width/height)
- Window position (X/Y)
- Always on top toggle
- Transparency toggle
- Opacity slider

##### Statistics Tab
- Enable/disable statistics
- Show KPS toggle
- Show press count toggle
- KPS update interval

##### Themes Tab
- Browse available themes
- Preview themes
- Apply themes
- Import/export themes

#### Opening Settings

**Method 1**: Right-click on overlay → Settings

**Method 2**: Programmatic:
```python
from gui.settings_window import SettingsWindow

settings = SettingsWindow(
    parent=root,
    config=config,
    config_manager=config_manager,
    update_callback=update_function
)
settings.show()
```

### 3. Theme Manager

Complete theme management system.

#### Features

- Load themes from `assets/themes/`
- Apply themes instantly
- Create custom themes
- Import/export themes
- Theme preview

#### Using ThemeManager

```python
from utils.theme_manager import ThemeManager

# Initialize
theme_mgr = ThemeManager()

# Get available themes
themes = theme_mgr.get_theme_names()
# Returns: ['Cyberpunk Neon', 'Matrix Green', 'Minimal Dark']

# Apply theme
config = theme_mgr.apply_theme('Matrix Green', config)

# Create new theme
theme_mgr.create_theme_from_config(
    theme_name='My Theme',
    config=current_config,
    description='Custom theme'
)

# Export theme
theme_mgr.export_theme('My Theme', '/path/to/export.json')

# Import theme
theme_name = theme_mgr.import_theme('/path/to/theme.json')
```

#### Theme File Format

```json
{
    "theme_name": "My Custom Theme",
    "description": "Description of the theme",
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
    }
}
```

#### Creating Custom Themes

1. **Via Settings Window**:
   - Configure appearance to your liking
   - Go to Themes tab
   - Click "Export Current"
   - Save as JSON file

2. **Manually**:
   - Create JSON file following the format above
   - Save to `assets/themes/` directory
   - Restart application or use Import feature

### 4. Context Menu

Right-click overlay for quick access:

- **Settings**: Open settings window
- **Animations**: Toggle and select animation type
  - Enable Animations
  - Pulse
  - Scale
  - Glow
  - Fade
- **Reset Statistics**: Clear current session stats
- **Exit**: Close application

## Configuration

### Complete Config Example

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
    "animations": {
        "enabled": true,
        "type": "pulse",
        "duration": 0.3
    },
    "statistics": {
        "enabled": true,
        "show_kps": true,
        "show_press_count": true,
        "kps_update_interval": 0.1
    }
}
```

## Usage Examples

### Example 1: Change Animation Type

```python
# In overlay_window.py
def _set_animation(self, animation_type):
    self.animation_type = animation_type
    # Now all key presses will use this animation
```

### Example 2: Apply Theme Programmatically

```python
from utils.theme_manager import ThemeManager

theme_mgr = ThemeManager()
config = theme_mgr.apply_theme('Cyberpunk Neon', config)

# Update overlay
overlay.apply_config_changes(config)
```

### Example 3: Custom Animation Callback

```python
def on_animation_complete():
    print("Animation finished!")

controller.animate_key_press(
    key='d',
    widget_info=widget,
    animation_type='pulse',
    callback=on_animation_complete
)
```

## Tips & Best Practices

### Animations
- Use **pulse** for general use (best performance)
- Use **scale** for dramatic effect
- Use **glow** for subtle feedback
- Disable animations if experiencing performance issues

### Settings Window
- Use **Apply** to test settings without saving
- Use **Save** to save without applying
- Use **Apply & Save** to do both
- **Reset to Defaults** reverts all settings

### Themes
- Export your favorite configurations as themes
- Share themes with others via JSON files
- Keep themes in `assets/themes/` for auto-loading
- Test themes before saving over defaults

### Performance
- Shorter animation duration = better performance
- Fewer monitored keys = better performance
- Disable animations for maximum performance

## Keyboard Shortcuts

- **Right-click**: Open context menu
- **Ctrl+S**: Save settings (in settings window)
- **Esc**: Close settings window

## Troubleshooting

### Animations not working
- Check `animations.enabled` is `true`
- Verify animation type is valid
- Check for console errors

### Settings window not opening
- Ensure `config_manager` is passed to overlay
- Check for tkinter errors in console
- Verify settings_window.py is imported correctly

### Theme not applying
- Verify theme file is valid JSON
- Check theme is in `assets/themes/` directory
- Ensure `appearance` section exists in theme

### Colors not updating
- Click "Apply" after changing colors
- Check color format is hex (e.g., #00ff00)
- Verify config is being saved correctly

## Future Enhancements

- [ ] Custom animation editor
- [ ] More animation types
- [ ] Animation speed control in GUI
- [ ] Theme marketplace/sharing
- [ ] Animated transitions between themes
- [ ] Keyboard shortcut customization
- [ ] Profile-based settings

## Related Documentation

- [Statistics Module](STATISTICS.md)
- [Development Guide](DEVELOPMENT.md)
- [Quick Start Guide](QUICKSTART.md)
