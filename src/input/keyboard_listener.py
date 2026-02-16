"""
Keyboard Listener Module
Handles keyboard input detection using pynput library.
"""

from pynput import keyboard
import threading


class KeyboardListener:
    """
    Listens for keyboard events and triggers callbacks.
    Monitors specific keys and reports their press/release state.
    """
    
    def __init__(self, keys_to_monitor, callback):
        """
        Initialize the keyboard listener.
        
        Args:
            keys_to_monitor: List of keys to monitor (e.g., ['d', 'f', 'j', 'k'])
            callback: Function to call on key events, signature: callback(key, pressed)
        """
        self.keys_to_monitor = [k.lower() for k in keys_to_monitor]
        self.callback = callback
        self.listener = None
        self.active_keys = set()
        self.lock = threading.Lock()
        
    def start(self):
        """Start listening for keyboard events."""
        if self.listener is not None:
            print("Listener already running")
            return
            
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        print("Keyboard listener started")
        
    def stop(self):
        """Stop listening for keyboard events."""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
            print("Keyboard listener stopped")
            
    def _on_press(self, key):
        """
        Internal handler for key press events.
        
        Args:
            key: The key that was pressed
        """
        key_str = self._get_key_string(key)
        
        if key_str and key_str.lower() in self.keys_to_monitor:
            with self.lock:
                if key_str not in self.active_keys:
                    self.active_keys.add(key_str)
                    self.callback(key_str, True)
                    
    def _on_release(self, key):
        """
        Internal handler for key release events.
        
        Args:
            key: The key that was released
        """
        key_str = self._get_key_string(key)
        
        if key_str and key_str.lower() in self.keys_to_monitor:
            with self.lock:
                if key_str in self.active_keys:
                    self.active_keys.remove(key_str)
                    self.callback(key_str, False)
                    
    def _get_key_string(self, key):
        """
        Convert pynput key object to string.
        
        Args:
            key: pynput key object
            
        Returns:
            String representation of the key, or None
        """
        try:
            # For alphanumeric keys
            if hasattr(key, 'char') and key.char:
                return key.char.lower()
            # For special keys
            elif hasattr(key, 'name'):
                return key.name.lower()
            else:
                return None
        except AttributeError:
            return None
            
    def is_key_pressed(self, key):
        """
        Check if a specific key is currently pressed.
        
        Args:
            key: Key to check
            
        Returns:
            bool: True if key is pressed, False otherwise
        """
        with self.lock:
            return key in self.active_keys
