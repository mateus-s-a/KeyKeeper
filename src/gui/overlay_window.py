"""
Overlay Window Module
Creates and manages the transparent overlay window for displaying key states.
"""

import tkinter as tk
from tkinter import font as tkfont


class OverlayWindow:
    """
    Transparent overlay window that displays keyboard key states.
    Always stays on top and shows which keys are currently pressed.
    """
    
    def __init__(self, parent, config):
        """
        Initialize the overlay window.
        
        Args:
            parent: Parent Tk root window
            config: Configuration dictionary
        """
        self.config = config
        self.parent = parent
        
        # Create toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Keyboard Overlay")
        
        # Configure window properties
        self._setup_window()
        
        # Key display widgets
        self.key_widgets = {}
        
        # Create the UI
        self._create_ui()
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _setup_window(self):
        """Configure window properties (transparency, always on top, etc.)"""
        overlay_config = self.config.get('overlay', {})
        
        # Set window size
        width = overlay_config.get('width', 400)
        height = overlay_config.get('height', 150)
        pos_x = overlay_config.get('position', {}).get('x', 100)
        pos_y = overlay_config.get('position', {}).get('y', 100)
        
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        
        # Always on top
        if overlay_config.get('always_on_top', True):
            self.window.attributes('-topmost', True)
        
        # Transparency
        if overlay_config.get('transparent', True):
            opacity = overlay_config.get('opacity', 0.9)
            self.window.attributes('-alpha', opacity)
            
        # Remove window decorations (optional)
        # self.window.overrideredirect(True)
        
        # Set background color
        bg_color = self.config.get('appearance', {}).get('background_color', '#1a1a1a')
        self.window.configure(bg=bg_color)
        
    def _create_ui(self):
        """Create the user interface elements."""
        appearance = self.config.get('appearance', {})
        keys_to_monitor = self.config.get('keys_to_monitor', ['d', 'f', 'j', 'k'])
        
        # Create main container
        self.main_frame = tk.Frame(
            self.window,
            bg=appearance.get('background_color', '#1a1a1a')
        )
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create key display frame
        self.keys_frame = tk.Frame(
            self.main_frame,
            bg=appearance.get('background_color', '#1a1a1a')
        )
        self.keys_frame.pack(expand=True)
        
        # Create key widgets
        for key in keys_to_monitor:
            key_widget = self._create_key_widget(key)
            self.key_widgets[key.lower()] = key_widget
            
    def _create_key_widget(self, key):
        """
        Create a widget for displaying a single key.
        
        Args:
            key: The key character to display
            
        Returns:
            Dictionary containing the key's widgets
        """
        appearance = self.config.get('appearance', {})
        
        # Create frame for the key
        key_frame = tk.Frame(
            self.keys_frame,
            bg=appearance.get('inactive_key_color', '#333333'),
            highlightbackground=appearance.get('border_color', '#666666'),
            highlightthickness=appearance.get('border_width', 2)
        )
        key_frame.pack(side='left', padx=appearance.get('key_padding', 10))
        
        # Create label for the key
        key_label = tk.Label(
            key_frame,
            text=key.upper(),
            font=(
                appearance.get('font_family', 'Arial'),
                appearance.get('font_size', 24),
                'bold'
            ),
            fg=appearance.get('text_color', '#ffffff'),
            bg=appearance.get('inactive_key_color', '#333333'),
            width=4,
            height=2
        )
        key_label.pack(padx=5, pady=5)
        
        return {
            'frame': key_frame,
            'label': key_label,
            'pressed': False
        }
        
    def update_key_state(self, key, pressed):
        """
        Update the visual state of a key.
        
        Args:
            key: The key to update
            pressed: True if pressed, False if released
        """
        key = key.lower()
        
        if key not in self.key_widgets:
            return
            
        widget = self.key_widgets[key]
        appearance = self.config.get('appearance', {})
        
        if pressed:
            # Key is pressed - highlight it
            color = appearance.get('active_key_color', '#00ff00')
            widget['frame'].configure(bg=color)
            widget['label'].configure(bg=color)
            widget['pressed'] = True
        else:
            # Key is released - return to normal
            color = appearance.get('inactive_key_color', '#333333')
            widget['frame'].configure(bg=color)
            widget['label'].configure(bg=color)
            widget['pressed'] = False
            
    def _on_close(self):
        """Handle window close event."""
        self.parent.quit()
        
    def show(self):
        """Show the overlay window."""
        self.window.deiconify()
        
    def hide(self):
        """Hide the overlay window."""
        self.window.withdraw()
