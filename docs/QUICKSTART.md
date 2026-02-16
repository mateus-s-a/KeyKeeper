# Quick Start Guide

## Installation

### 1. System Requirements
- Linux Ubuntu 20.04+ (or similar distribution)
- Python 3.8 or higher
- X11 window system (for best compatibility)

### 2. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk python3-xlib
```

### 3. Install Python Dependencies
```bash
cd /path/to/keyboard-overlay
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pynput pyyaml numpy
```

## Running the Application

### Basic Usage
```bash
python main.py
```

The overlay window will appear showing the default keys: D, F, J, K

### First Run
On the first run, the application will:
1. Create a default configuration file at `src/config/default_config.json`
2. Display an overlay window at position (100, 100)
3. Monitor the keys specified in the configuration

## Customization

### Changing Monitored Keys

Edit `src/config/default_config.json`:
```json
{
    "keys_to_monitor": ["a", "s", "d", "w"]
}
```

Common key layouts:
- **Rhythm games (4K)**: `["d", "f", "j", "k"]`
- **Rhythm games (7K)**: `["s", "d", "f", "space", "j", "k", "l"]`
- **WASD gaming**: `["w", "a", "s", "d"]`
- **Arrow keys**: `["up", "down", "left", "right"]`
- **Custom combo**: Any combination of keys!

### Changing Colors

Edit the `appearance` section in the config file:
```json
{
    "appearance": {
        "background_color": "#1a1a1a",
        "active_key_color": "#00ff00",
        "inactive_key_color": "#333333",
        "text_color": "#ffffff"
    }
}
```

Color suggestions:
- **Green theme**: Active: `#00ff00`, Inactive: `#003300`
- **Blue theme**: Active: `#00aaff`, Inactive: `#001133`
- **Red theme**: Active: `#ff0000`, Inactive: `#330000`
- **Purple theme**: Active: `#aa00ff`, Inactive: `#220033`
- **Cyberpunk**: Active: `#ff00ff`, Inactive: `#0a0a0a`

### Moving the Overlay

Edit the `overlay.position` section:
```json
{
    "overlay": {
        "position": {
            "x": 100,
            "y": 100
        }
    }
}
```

Tips:
- Bottom center: `{"x": 800, "y": 900}` (adjust for your screen)
- Top right: `{"x": 1400, "y": 50}`
- Top left: `{"x": 50, "y": 50}`

### Adjusting Size

```json
{
    "overlay": {
        "width": 400,
        "height": 150
    }
}
```

### Changing Font

```json
{
    "appearance": {
        "font_family": "Arial",
        "font_size": 24
    }
}
```

Available fonts (Ubuntu): Arial, Helvetica, Courier, Times, DejaVu Sans, Ubuntu, etc.

### Adjusting Transparency

```json
{
    "overlay": {
        "opacity": 0.9
    }
}
```

Values: 0.0 (completely transparent) to 1.0 (completely opaque)

## Usage Examples

### Example 1: Osu! Mania Player
```json
{
    "keys_to_monitor": ["d", "f", "j", "k"],
    "appearance": {
        "active_key_color": "#ff00ff",
        "font_size": 28
    }
}
```

### Example 2: FPS Gamer (WASD)
```json
{
    "keys_to_monitor": ["w", "a", "s", "d"],
    "overlay": {
        "position": {"x": 50, "y": 900}
    },
    "appearance": {
        "active_key_color": "#00ff00"
    }
}
```

### Example 3: Streamer Setup
```json
{
    "keys_to_monitor": ["q", "w", "e", "r", "space"],
    "overlay": {
        "width": 600,
        "opacity": 0.85
    },
    "appearance": {
        "background_color": "#000000",
        "active_key_color": "#00ffff",
        "font_size": 32
    }
}
```

## Troubleshooting

### Keys Not Responding
**Problem**: Keys are pressed but overlay doesn't update

**Solutions**:
1. Check that keys are in `keys_to_monitor` array
2. Make sure keys are lowercase in config: `"d"` not `"D"`
3. For special keys, use full name: `"space"`, `"shift"`, `"ctrl"`
4. Verify pynput is installed: `pip install pynput`

### Overlay Not Visible
**Problem**: Application runs but no window appears

**Solutions**:
1. Check window position is on your screen
2. Try changing position to `{"x": 100, "y": 100}`
3. Increase opacity: `"opacity": 1.0`
4. Disable transparency temporarily: `"transparent": false`

### Permission Errors
**Problem**: Cannot capture keyboard events

**Solutions**:
```bash
# Add user to input group
sudo usermod -a -G input $USER

# Log out and log back in for changes to take effect
```

### Application Crashes on Start
**Problem**: Error messages when running

**Solutions**:
1. Check Python version: `python3 --version` (should be 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check config file syntax (must be valid JSON)
4. Try deleting config file and let it regenerate

## Advanced Tips

### Running on Startup
Create a desktop entry:
```bash
# Create autostart directory
mkdir -p ~/.config/autostart

# Create desktop entry
cat > ~/.config/autostart/keyboard-overlay.desktop << EOF
[Desktop Entry]
Type=Application
Name=Keyboard Overlay
Exec=python3 /path/to/keyboard-overlay/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```

### Running in Background
```bash
# Run and detach from terminal
nohup python main.py &

# Check if running
ps aux | grep main.py

# Kill process
pkill -f main.py
```

## Getting Help

- Check the documentation in `docs/DEVELOPMENT.md`
- Review configuration examples in this guide
- Check console output for error messages
- Verify all dependencies are installed

## Next Steps

Now that you have the basics working:
1. Experiment with different color schemes
2. Try different key combinations for your use case
3. Adjust position and size for your screen
4. Explore the code to understand how it works
5. Consider contributing new features!

Enjoy your keyboard overlay! 🎮⌨️
