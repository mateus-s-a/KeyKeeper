"""
Overlay Window Module
Creates and manages the transparent overlay window for displaying key states.
"""

import tkinter as tk
from tkinter import font as tkfont, Menu
from gui.animations import AnimationController


class OverlayWindow:
    """
    Transparent overlay window that displays keyboard key states.
    Always stays on top and shows which keys are currently pressed.
    Optionally displays statistics like KPS and press counts.
    """
    
    def __init__(self, parent, config, statistics=None, config_manager=None):
        """
        Initialize the overlay window.
        
        Args:
            parent: Parent Tk root window
            config: Configuration dictionary
            statistics: Optional StatisticsTracker instance
            config_manager: Optional ConfigManager instance
        """
        self.config = config
        self.parent = parent
        self.statistics = statistics
        self.config_manager = config_manager
        
        # Animation controller
        self.animation_controller = AnimationController()
        self.animations_enabled = config.get('animations', {}).get('enabled', True)
        self.animation_type = config.get('animations', {}).get('type', 'pulse')
        
        # Create toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("KeyKeeper Overlay")
        
        # Create context menu
        self._create_context_menu()
        
        # Configure window properties
        self._setup_window()
        
        # Key display widgets
        self.key_widgets = {}
        
        # Statistics widgets
        self.stats_widgets = {}
        
        # Create the UI
        self._create_ui()
        
        # Setup statistics update timer if enabled
        if self.statistics:
            self._setup_statistics_update()
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_context_menu(self):
        """Create right-click context menu."""
        self.context_menu = Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Settings", command=self._open_settings)
        self.context_menu.add_command(label="Profile Manager", command=self._open_profile_manager)
        self.context_menu.add_command(label="Heatmap Viewer", command=self._open_heatmap)
        self.context_menu.add_separator()
        
        # Animation submenu
        animation_menu = Menu(self.context_menu, tearoff=0)
        animation_menu.add_checkbutton(
            label="Enable Animations",
            command=self._toggle_animations
        )
        animation_menu.add_separator()
        animation_menu.add_radiobutton(label="Pulse", command=lambda: self._set_animation('pulse'))
        animation_menu.add_radiobutton(label="Scale", command=lambda: self._set_animation('scale'))
        animation_menu.add_radiobutton(label="Glow", command=lambda: self._set_animation('glow'))
        animation_menu.add_radiobutton(label="Fade", command=lambda: self._set_animation('fade'))
        self.context_menu.add_cascade(label="Animations", menu=animation_menu)
        
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Reset Statistics", command=self._reset_stats)
        self.context_menu.add_command(label="Exit", command=self._on_close)
        
        # Bind right-click
        self.window.bind("<Button-3>", self._show_context_menu)
        
        # Store references to heatmap and profile manager windows
        self.heatmap_window = None
        self.profile_manager_window = None
        self.profile_manager = None  # Will be set by app
    
    def _show_context_menu(self, event):
        """Show context menu."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _open_settings(self):
        """Open settings window."""
        from gui.settings_window import SettingsWindow
        settings = SettingsWindow(
            self.parent,
            self.config,
            self.config_manager,
            update_callback=self.apply_config_changes
        )
        settings.show()
    
    def _toggle_animations(self):
        """Toggle animations on/off."""
        self.animations_enabled = not self.animations_enabled
    
    def _set_animation(self, animation_type):
        """Set animation type."""
        self.animation_type = animation_type
    
    def _reset_stats(self):
        """Reset statistics."""
        if self.statistics:
            self.statistics.reset_statistics()
    
    def _open_heatmap(self):
        """Open heatmap viewer window."""
        if self.heatmap_window is None or not self.heatmap_window.window.winfo_exists():
            from gui.heatmap import HeatmapWindow
            self.heatmap_window = HeatmapWindow(
                parent=self.window,
                statistics_tracker=self.statistics
            )
        else:
            self.heatmap_window.show()
    
    def _open_profile_manager(self):
        """Open profile manager window."""
        if self.profile_manager is None:
            print("Profile Manager not available")
            return
        
        if self.profile_manager_window is None or not self.profile_manager_window.window.winfo_exists():
            from gui.profile_manager_window import ProfileManagerWindow
            self.profile_manager_window = ProfileManagerWindow(
                parent=self.window,
                profile_manager=self.profile_manager,
                config_manager=self.config_manager,
                on_profile_change=self._on_profile_changed
            )
        else:
            self.profile_manager_window.show()
    
    def _on_profile_changed(self, profile):
        """Handle profile change event."""
        # Apply new config and recreate UI
        self.config = profile.config
        self.apply_config_changes(self.config)
        print(f"Switched to profile: {profile.name}")
    
    def apply_config_changes(self, new_config):
        """
        Apply configuration changes from settings window.
        
        Args:
            new_config: New configuration dictionary
        """
        self.config = new_config
        # Recreate UI with new config
        # For now, just update what we can without recreating
        self._update_from_config()
    
    def _update_from_config(self):
        """Update window from current config."""
        # Update appearance
        appearance = self.config.get('appearance', {})
        
        # Update background
        bg_color = appearance.get('background_color', '#1a1a1a')
        self.window.configure(bg=bg_color)
        if hasattr(self, 'main_frame'):
            self.main_frame.configure(bg=bg_color)
            self.keys_frame.configure(bg=bg_color)
        
        # Update key widgets
        for key, widget in self.key_widgets.items():
            widget['label'].configure(
                font=(
                    appearance.get('font_family', 'Arial'),
                    appearance.get('font_size', 24),
                    'bold'
                )
            )
        
        # Update window properties
        overlay_config = self.config.get('overlay', {})
        if overlay_config.get('always_on_top'):
            self.window.attributes('-topmost', True)
        else:
            self.window.attributes('-topmost', False)
        
        self.window.attributes('-alpha', overlay_config.get('opacity', 0.9))
        
    def _setup_window(self):
        """Configure window properties (transparency, always on top, etc.)"""
        overlay_config = self.config.get('overlay', {})
        stats_config = self.config.get('statistics', {})
        
        # Adjust height if statistics are enabled
        width = overlay_config.get('width', 400)
        base_height = overlay_config.get('height', 150)
        
        # Add extra height for statistics display
        if self.statistics and (stats_config.get('show_kps') or stats_config.get('show_press_count')):
            height = base_height + 80  # Extra space for stats
        else:
            height = base_height
        
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
        
        # Create statistics display if enabled
        if self.statistics:
            self._create_statistics_ui()
            
    def _create_key_widget(self, key):
        """
        Create a widget for displaying a single key.
        
        Args:
            key: The key character to display
            
        Returns:
            Dictionary containing the key's widgets
        """
        appearance = self.config.get('appearance', {})
        stats_config = self.config.get('statistics', {})
        show_per_key_kps = stats_config.get('show_per_key_kps', True)
        
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
        
        # Create per-key KPS label if enabled
        kps_label = None
        if self.statistics and show_per_key_kps:
            kps_label = tk.Label(
                key_frame,
                text="0.0 KPS",
                font=(appearance.get('font_family', 'Arial'), 9),
                fg=appearance.get('text_color', '#ffffff'),
                bg=appearance.get('inactive_key_color', '#333333')
            )
            kps_label.pack(padx=2, pady=(0, 2))
        
        return {
            'frame': key_frame,
            'label': key_label,
            'kps_label': kps_label,
            'pressed': False
        }
    
    def _create_statistics_ui(self):
        """Create the statistics display UI."""
        stats_config = self.config.get('statistics', {})
        appearance = self.config.get('appearance', {})
        bg_color = appearance.get('background_color', '#1a1a1a')
        text_color = appearance.get('text_color', '#ffffff')
        
        # Create statistics frame
        self.stats_frame = tk.Frame(
            self.main_frame,
            bg=bg_color
        )
        self.stats_frame.pack(side='bottom', fill='x', pady=(10, 0))
        
        # Create separator line
        separator = tk.Frame(
            self.stats_frame,
            bg=appearance.get('border_color', '#666666'),
            height=2
        )
        separator.pack(fill='x', pady=(0, 10))
        
        # Create stats display frame
        stats_display = tk.Frame(self.stats_frame, bg=bg_color)
        stats_display.pack()
        
        # KPS display
        if stats_config.get('show_kps', False):
            kps_frame = tk.Frame(stats_display, bg=bg_color)
            kps_frame.pack(side='left', padx=20)
            
            kps_label = tk.Label(
                kps_frame,
                text="KPS:",
                font=('Arial', 10, 'bold'),
                fg=text_color,
                bg=bg_color
            )
            kps_label.pack(side='left', padx=(0, 5))
            
            kps_value = tk.Label(
                kps_frame,
                text="0.00",
                font=('Arial', 12, 'bold'),
                fg=appearance.get('active_key_color', '#00ff00'),
                bg=bg_color
            )
            kps_value.pack(side='left')
            
            self.stats_widgets['kps_label'] = kps_value
        
        # Press count display
        if stats_config.get('show_press_count', False):
            count_frame = tk.Frame(stats_display, bg=bg_color)
            count_frame.pack(side='left', padx=20)
            
            count_label = tk.Label(
                count_frame,
                text="Total:",
                font=('Arial', 10, 'bold'),
                fg=text_color,
                bg=bg_color
            )
            count_label.pack(side='left', padx=(0, 5))
            
            count_value = tk.Label(
                count_frame,
                text="0",
                font=('Arial', 12, 'bold'),
                fg=appearance.get('active_key_color', '#00ff00'),
                bg=bg_color
            )
            count_value.pack(side='left')
            
            self.stats_widgets['count_label'] = count_value
        
        # Peak KPS display
        if stats_config.get('show_kps', False):
            peak_frame = tk.Frame(stats_display, bg=bg_color)
            peak_frame.pack(side='left', padx=20)
            
            peak_label = tk.Label(
                peak_frame,
                text="Peak:",
                font=('Arial', 10, 'bold'),
                fg=text_color,
                bg=bg_color
            )
            peak_label.pack(side='left', padx=(0, 5))
            
            peak_value = tk.Label(
                peak_frame,
                text="0.00",
                font=('Arial', 12, 'bold'),
                fg=appearance.get('active_key_color', '#00ff00'),
                bg=bg_color
            )
            peak_value.pack(side='left')
            
            self.stats_widgets['peak_label'] = peak_value
    
    def _setup_statistics_update(self):
        """Setup periodic statistics updates."""
        update_interval = int(self.config.get('statistics', {}).get('kps_update_interval', 1.0) * 100)  # Convert to ms
        self._update_statistics()
        self.window.after(update_interval, self._periodic_statistics_update)
    
    def _periodic_statistics_update(self):
        """Periodically update statistics display."""
        self._update_statistics()
        update_interval = int(self.config.get('statistics', {}).get('kps_update_interval', 1.0) * 100)
        self.window.after(update_interval, self._periodic_statistics_update)
    
    def _update_statistics(self):
        """Update statistics display with current values."""
        if not self.statistics:
            return
        
        stats = self.statistics.get_statistics()
        
        # Update KPS
        if 'kps_label' in self.stats_widgets:
            self.stats_widgets['kps_label'].config(text=f"{stats['current_kps']:.2f}")
        
        # Update total count
        if 'count_label' in self.stats_widgets:
            self.stats_widgets['count_label'].config(text=str(stats['total_presses']))
        
        # Update peak KPS
        if 'peak_label' in self.stats_widgets:
            self.stats_widgets['peak_label'].config(text=f"{stats['peak_kps']:.2f}")
        
        # Update per-key KPS
        per_key_kps = stats.get('per_key_kps', {})
        for key, widget_data in self.key_widgets.items():
            kps_label = widget_data.get('kps_label')
            if kps_label:
                key_kps = per_key_kps.get(key, 0.0)
                kps_label.config(text=f"{key_kps:.1f} KPS")
        
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
            
            # Trigger animation if enabled
            if self.animations_enabled:
                self.animation_controller.animate_key_press(
                    key,
                    widget,
                    animation_type=self.animation_type,
                    duration=0.3
                )
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
