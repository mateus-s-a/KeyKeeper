"""
Core Application Module
Main application controller that orchestrates all components.
"""

import tkinter as tk
from config.config_manager import ConfigManager
from input.keyboard_listener import KeyboardListener
from gui.overlay_window import OverlayWindow


class KeyboardOverlayApp:
    """
    Main application class that manages the keyboard overlay.
    Coordinates between input handling, configuration, and GUI display.
    """
    
    def __init__(self):
        """Initialize the application components."""
        print("Initializing Keyboard Overlay Application...")
        
        # Load configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Initialize GUI root
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        
        # Create overlay window
        self.overlay = OverlayWindow(self.root, self.config)
        
        # Initialize keyboard listener
        self.keyboard_listener = KeyboardListener(
            keys_to_monitor=self.config.get('keys_to_monitor', ['d', 'f', 'j', 'k']),
            callback=self.on_key_event
        )
        
        print("Application initialized successfully!")
        
    def on_key_event(self, key, pressed):
        """
        Callback for keyboard events.
        
        Args:
            key: The key that was pressed/released
            pressed: True if pressed, False if released
        """
        self.overlay.update_key_state(key, pressed)
        
    def run(self):
        """Start the application."""
        print("Starting Keyboard Overlay...")
        print(f"Monitoring keys: {self.config.get('keys_to_monitor', [])}")
        print("Press Ctrl+C to exit")
        
        # Start keyboard listener
        self.keyboard_listener.start()
        
        # Run the GUI main loop
        try:
            self.root.mainloop()
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources before exit."""
        print("\nCleaning up...")
        self.keyboard_listener.stop()
        print("Application closed.")
