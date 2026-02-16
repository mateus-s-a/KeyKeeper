# KeyKeeper (Keyboard Overlay Application)

A highly customizable keyboard overlay application, designed to display keypresses in real-time on screen. Perfect for rhythm game players, streamers, and anyone who wants to visualize their keyboard input.

## Features

- **Real-time Key Display**: Shows keypresses as they happen
- **Highly Customizable**: Configure which keys to monitor and display
- **Transparent Overlay**: Always-on-top window that doesn't interfere with your applications
- **Statistics Tracking** (Future): Keys per second (KPS), key press counts, and more
- **Theme Support**: Customize colors, fonts, and visual styles

## Project Structure

```
keyboard-overlay/
├── src/
│   ├── core/           # Core application logic
│   ├── gui/            # GUI components and overlay window
│   ├── input/          # Keyboard input handling
│   ├── config/         # Configuration management
│   └── utils/          # Utility functions and helpers
├── assets/
│   ├── fonts/          # Custom fonts
│   └── themes/         # Theme configurations
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
4. Use the configuration file or GUI settings to customize

## Development

This project is structured for easy expansion and maintenance:

- **Modular Design**: Each component is separated into its own module
- **Scalable Architecture**: Easy to add new features and statistics
- **Theme System**: Simple to create and apply new visual themes
- **Configuration-Driven**: Most behavior can be modified without code changes

## Future Features

- [ ] Keys per second (KPS) display
- [ ] Key press counter
- [ ] Heat map visualization
- [ ] Profile system for different applications
- [ ] GUI configuration tool
- [ ] Recording and replay functionality

## License

[To be determined]
