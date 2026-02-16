# Project Structure Overview

## Complete File Tree

```
keyboard-overlay/
├── main.py                              # Application entry point
├── requirements.txt                     # Python dependencies
├── README.md                            # Project overview
├── .gitignore                          # Git ignore rules
│
├── src/                                # Source code directory
│   ├── core/                           # Core application logic
│   │   ├── __init__.py
│   │   └── app.py                      # Main application controller
│   │
│   ├── gui/                            # GUI components
│   │   ├── __init__.py
│   │   └── overlay_window.py           # Overlay window implementation
│   │
│   ├── input/                          # Input handling
│   │   ├── __init__.py
│   │   └── keyboard_listener.py        # Keyboard event capture
│   │
│   ├── config/                         # Configuration management
│   │   ├── __init__.py
│   │   ├── config_manager.py           # Config loader/saver
│   │   └── default_config.json         # Default configuration
│   │
│   └── utils/                          # Utility functions
│       └── __init__.py
│
├── assets/                             # Static assets
│   ├── fonts/                          # Custom fonts (empty for now)
│   └── themes/                         # Theme configurations
│       ├── cyberpunk.json              # Cyberpunk neon theme
│       ├── matrix.json                 # Matrix green theme
│       └── minimal_dark.json           # Minimal dark theme
│
├── tests/                              # Test suite
│   ├── __init__.py
│   └── test_config.py                  # Configuration tests
│
└── docs/                               # Documentation
    ├── DEVELOPMENT.md                  # Developer guide
    └── QUICKSTART.md                   # Quick start guide
```

## Module Descriptions

### Core Modules

#### `main.py`
- Application entry point
- Handles startup and error handling
- Sets up Python path for imports

#### `src/core/app.py`
- Main application controller
- Orchestrates all components
- Manages application lifecycle
- Coordinates between input, config, and GUI

### GUI Module

#### `src/gui/overlay_window.py`
- Creates transparent overlay window
- Displays key states visually
- Handles window configuration (position, size, transparency)
- Updates key visuals in real-time

### Input Module

#### `src/input/keyboard_listener.py`
- Captures keyboard events using pynput
- Filters events for monitored keys
- Thread-safe key state tracking
- Provides callbacks for key press/release

### Config Module

#### `src/config/config_manager.py`
- Loads and saves JSON configuration
- Provides default configuration values
- Merges user config with defaults
- Handles config validation

#### `src/config/default_config.json`
- Default configuration template
- Defines all available settings
- Used as fallback if no user config exists

### Assets

#### `assets/themes/*.json`
- Pre-configured visual themes
- Easy to apply different looks
- Can be loaded into config

### Tests

#### `tests/test_config.py`
- Unit tests for configuration manager
- Validates config structure
- Tests default values

### Documentation

#### `docs/DEVELOPMENT.md`
- Architecture overview
- Development guidelines
- Feature implementation guide
- Troubleshooting guide

#### `docs/QUICKSTART.md`
- Installation instructions
- Basic usage guide
- Customization examples
- Common issues and solutions

## Key Design Patterns

### 1. Modular Architecture
- Each module has a single responsibility
- Clear interfaces between modules
- Easy to extend and maintain

### 2. Configuration-Driven
- Most behavior controlled by config file
- No need to modify code for customization
- Easy to create and share configurations

### 3. Event-Driven GUI
- Keyboard listener triggers callbacks
- Callbacks update GUI state
- Separates input handling from display

### 4. Observer Pattern
- KeyboardListener observes keyboard events
- Notifies app.py through callbacks
- app.py updates OverlayWindow

## Data Flow

```
Keyboard Input
    ↓
KeyboardListener (filters & captures)
    ↓
on_key_event callback
    ↓
KeyboardOverlayApp (processes)
    ↓
OverlayWindow.update_key_state
    ↓
Visual Update (GUI)
```

## Extension Points

### Adding New Features

1. **Statistics Module** (Future)
   - Create `src/core/statistics.py`
   - Track key presses over time
   - Calculate KPS, totals, etc.
   - Integrate into app.py

2. **Theme Manager** (Future)
   - Create `src/utils/theme_manager.py`
   - Load themes from assets/themes/
   - Apply themes to overlay window
   - Add theme switcher UI

3. **Profile System** (Future)
   - Create `src/config/profile_manager.py`
   - Support multiple configurations
   - Quick profile switching
   - Per-application profiles

4. **GUI Settings** (Future)
   - Create `src/gui/settings_window.py`
   - Visual configuration editor
   - Real-time preview
   - Save/load profiles

## Technology Stack

- **Python 3.8+**: Main programming language
- **Tkinter**: GUI framework (included with Python)
- **pynput**: Keyboard event capture
- **JSON**: Configuration format
- **pytest**: Testing framework (optional)

## File Sizes (Approximate)

- Total: ~23 KB (source code)
- Largest file: overlay_window.py (~5.7 KB)
- Configuration: ~800 bytes
- All documentation: ~14 KB

## Lines of Code

- Source code: ~500 LOC
- Documentation: ~400 lines
- Tests: ~100 LOC
- Total: ~1000 lines

## Current Status

✅ **Completed**:
- Project structure
- Core application logic
- Configuration system
- Keyboard input handling
- Overlay window display
- Basic visual customization
- Documentation
- Sample themes
- Basic tests

🔄 **Ready for Development**:
- Statistics tracking (KPS, counters)
- Theme manager
- Profile system
- GUI settings panel
- Advanced animations
- Recording/replay

## Next Steps

1. **Test the basic functionality**:
   ```bash
   python main.py
   ```

2. **Customize configuration**:
   - Edit `src/config/default_config.json`
   - Change keys, colors, position

3. **Begin feature development**:
   - Start with statistics module
   - Add KPS calculation
   - Display stats in overlay

4. **Enhance GUI**:
   - Add animations for key presses
   - Improve visual feedback
   - Add more customization options
