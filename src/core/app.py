"""
Core Application Module
Main application controller that orchestrates all components.
"""

import tkinter as tk
from config.config_manager import ConfigManager
from input.keyboard_listener import KeyboardListener
from gui.overlay_window import OverlayWindow
from core.statistics import StatisticsTracker
from core.profile_manager import ProfileManager


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
        
        # Initialize profile manager
        self.profile_manager = ProfileManager()
        print(f"Profile Manager initialized - {len(self.profile_manager.list_profiles())} profiles loaded")
        
        # Check for active profile
        active_profile = self.profile_manager.get_active_profile()
        if active_profile:
            print(f"Active profile: {active_profile.name}")
            # Apply active profile config
            self.config_manager.update(active_profile.config)
            self.config = self.config_manager.get_all()
        
        # Initialize statistics tracker if enabled
        stats_config = self.config.get('statistics', {})
        self.statistics = None
        if stats_config.get('enabled', False):
            kps_interval = stats_config.get('kps_update_interval', 1.0)
            self.statistics = StatisticsTracker(kps_window=kps_interval)
            print(f"Statistics tracking enabled (KPS window: {kps_interval}s)")
        
        # Initialize GUI root
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        
        # Create overlay window
        self.overlay = OverlayWindow(self.root, self.config, self.statistics, self.config_manager)
        
        # Set profile manager in overlay for menu access
        self.overlay.profile_manager = self.profile_manager
        
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
        # Update overlay visual state
        self.overlay.update_key_state(key, pressed)
        
        # Record press in statistics (only on press, not release)
        if pressed and self.statistics:
            self.statistics.record_press(key)
        
    def run(self):
        """Start the application."""
        print("Starting Keyboard Overlay...")
        print(f"Monitoring keys: {self.config.get('keys_to_monitor', [])}")
        
        if self.statistics:
            print("Statistics tracking: ENABLED")
            stats_config = self.config.get('statistics', {})
            if stats_config.get('show_kps', False):
                print("  - KPS display: ON")
            if stats_config.get('show_press_count', False):
                print("  - Press counter: ON")
        else:
            print("Statistics tracking: DISABLED")
        
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
        
        # Print session statistics if enabled
        if self.statistics:
            print("\n=== Session Statistics ===")
            stats = self.statistics.get_statistics()
            print(f"Total key presses: {stats['total_presses']}")
            print(f"Session duration: {stats['session_duration']}s")
            print(f"Peak KPS: {stats['peak_kps']}")
            print(f"Average KPS: {stats['average_kps']}")
            
            if stats['key_press_counts']:
                print("\nTop pressed keys:")
                for key, count in self.statistics.get_top_keys(5):
                    print(f"  {key.upper()}: {count} presses")
        
        print("Application closed.")
