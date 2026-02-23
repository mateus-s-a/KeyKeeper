# KeyKeeper (Keyboard Overlay Application)

A highly customizable keyboard overlay application, designed to display keypresses in real-time on screen. Perfect for rhythm game players, streamers, and anyone who wants to visualize their keyboard input.

## Features

- **Real-time Key Display**: Shows keypresses as they happen
- **Highly Customizable**: Configure which keys to monitor and display
- **Transparent Overlay**: Always-on-top window that doesn't interfere with your applications
- **Statistics Tracking**: Keys per second (KPS), key press counts, peak KPS, per-key KPS, and session statistics
- **Key Press Animations**: Visual feedback with multiple animation types (pulse, scale, glow, fade)
- **GUI Settings Window**: Comprehensive settings interface with live preview
- **Theme Support**: Full theme management with import/export capabilities
- **Profile Management**: Create and switch between multiple configuration profiles
- **Heatmap Visualization**: Visual representation of key press frequency and distribution
- **Per-Key Statistics**: Individual KPS tracking for each monitored key

## Project Structure

```
keyboard-overlay/
├── src/
│   ├── core/           # Core application logic, statistics, profile manager
│   ├── gui/            # GUI components, overlay, settings, heatmap
│   ├── input/          # Keyboard input handling
│   ├── config/         # Configuration management
│   └── utils/          # Utility functions, theme manager
├── assets/
│   ├── fonts/          # Custom fonts
│   └── themes/         # Theme configurations
├── profiles/           # Saved configuration profiles
├── tests/              # Unit and integration tests
├── docs/               # Additional documentation
└── main.py             # Application entry point
```

## Requirements

- Python 3.8+
- Required Python packages (see `requirements.txt`)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd keyboard-overlay

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Configuration

Edit `config/default_config.json` to customize:
- Keys to monitor
- Overlay position and size
- Visual appearance
- Statistics settings

## Usage

1. Run the application: `python main.py`
2. The overlay will appear on your screen
3. Press the configured keys to see them displayed
4. Right-click the overlay for quick access to:
   - **Settings**: Configure appearance, keys, animations, statistics
   - **Profile Manager**: Create and switch between different profiles
   - **Heatmap Viewer**: Visualize key press frequency and distribution
   - **Animations**: Toggle and select animation types
   - **Reset Statistics**: Clear current session data
5. Each key displays its individual KPS underneath the key label
6. Use the configuration file or GUI settings for advanced customization

## Future Features

- [x] Keys per second (KPS) display
- [x] Key press counter
- [x] Statistics module with peak tracking
- [x] Key press animations
- [x] GUI settings window
- [x] Theme selector and manager
- [x] Per-key KPS tracking
- [x] Profile system for different applications
- [x] Heatmap visualization
- [ ] Keyboard layout heatmap view

## License

[To be determined]
