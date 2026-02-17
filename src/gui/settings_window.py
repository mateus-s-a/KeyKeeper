"""
Settings Window Module
Provides GUI settings window for configuration and theme management.
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from typing import Callable, Dict
from utils.theme_manager import ThemeManager


class SettingsWindow:
    """
    Settings window for KeyKeeper overlay configuration.
    Provides live preview and theme management.
    """
    
    def __init__(self, parent, config: Dict, config_manager, 
                 update_callback: Callable = None):
        """
        Initialize the settings window.
        
        Args:
            parent: Parent window
            config: Current configuration dictionary
            config_manager: ConfigManager instance
            update_callback: Callback to update main overlay
        """
        self.config = config.copy()  # Work with copy
        self.config_manager = config_manager
        self.update_callback = update_callback
        self.theme_manager = ThemeManager()
        
        # Preview timer to debounce rapid changes
        self.preview_timer = None
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("KeyKeeper Settings")
        self.window.geometry("700x600")
        self.window.resizable(True, True)
        
        # Make window stay on top but not always
        self.window.attributes('-topmost', False)
        
        # Create UI
        self._create_ui()
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_ui(self):
        """Create the settings UI."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.appearance_tab = ttk.Frame(self.notebook)
        self.keys_tab = ttk.Frame(self.notebook)
        self.overlay_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.themes_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.appearance_tab, text="Appearance")
        self.notebook.add(self.keys_tab, text="Keys")
        self.notebook.add(self.overlay_tab, text="Overlay")
        self.notebook.add(self.stats_tab, text="Statistics")
        self.notebook.add(self.themes_tab, text="Themes")
        
        # Build each tab
        self._create_appearance_tab()
        self._create_keys_tab()
        self._create_overlay_tab()
        self._create_stats_tab()
        self._create_themes_tab()
        
        # Create bottom button panel
        self._create_button_panel()
    
    def _create_appearance_tab(self):
        """Create appearance settings tab."""
        frame = ttk.Frame(self.appearance_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        appearance = self.config.get('appearance', {})
        
        # Background Color
        row = 0
        ttk.Label(frame, text="Background Color:").grid(row=row, column=0, sticky='w', pady=5)
        self.bg_color_btn = tk.Button(
            frame, 
            bg=appearance.get('background_color', '#1a1a1a'),
            width=10,
            command=lambda: self._choose_color('background_color', self.bg_color_btn)
        )
        self.bg_color_btn.grid(row=row, column=1, sticky='w', padx=5)
        
        # Active Key Color
        row += 1
        ttk.Label(frame, text="Active Key Color:").grid(row=row, column=0, sticky='w', pady=5)
        self.active_color_btn = tk.Button(
            frame,
            bg=appearance.get('active_key_color', '#00ff00'),
            width=10,
            command=lambda: self._choose_color('active_key_color', self.active_color_btn)
        )
        self.active_color_btn.grid(row=row, column=1, sticky='w', padx=5)
        
        # Inactive Key Color
        row += 1
        ttk.Label(frame, text="Inactive Key Color:").grid(row=row, column=0, sticky='w', pady=5)
        self.inactive_color_btn = tk.Button(
            frame,
            bg=appearance.get('inactive_key_color', '#333333'),
            width=10,
            command=lambda: self._choose_color('inactive_key_color', self.inactive_color_btn)
        )
        self.inactive_color_btn.grid(row=row, column=1, sticky='w', padx=5)
        
        # Text Color
        row += 1
        ttk.Label(frame, text="Text Color:").grid(row=row, column=0, sticky='w', pady=5)
        self.text_color_btn = tk.Button(
            frame,
            bg=appearance.get('text_color', '#ffffff'),
            width=10,
            command=lambda: self._choose_color('text_color', self.text_color_btn)
        )
        self.text_color_btn.grid(row=row, column=1, sticky='w', padx=5)
        
        # Border Color
        row += 1
        ttk.Label(frame, text="Border Color:").grid(row=row, column=0, sticky='w', pady=5)
        self.border_color_btn = tk.Button(
            frame,
            bg=appearance.get('border_color', '#666666'),
            width=10,
            command=lambda: self._choose_color('border_color', self.border_color_btn)
        )
        self.border_color_btn.grid(row=row, column=1, sticky='w', padx=5)
        
        # Font Family
        row += 1
        ttk.Label(frame, text="Font Family:").grid(row=row, column=0, sticky='w', pady=5)
        self.font_family = ttk.Combobox(
            frame,
            values=['Arial', 'Helvetica', 'Courier', 'Times', 'DejaVu Sans', 'Ubuntu'],
            width=15
        )
        self.font_family.set(appearance.get('font_family', 'Arial'))
        self.font_family.grid(row=row, column=1, sticky='w', padx=5)
        self.font_family.bind('<<ComboboxSelected>>', lambda e: self._update_live_preview())
        
        # Font Size
        row += 1
        ttk.Label(frame, text="Font Size:").grid(row=row, column=0, sticky='w', pady=5)
        self.font_size = tk.Scale(
            frame,
            from_=12,
            to=48,
            orient='horizontal',
            command=lambda v: self._update_live_preview()
        )
        self.font_size.set(appearance.get('font_size', 24))
        self.font_size.grid(row=row, column=1, sticky='w', padx=5)
        
        # Key Padding
        row += 1
        ttk.Label(frame, text="Key Padding:").grid(row=row, column=0, sticky='w', pady=5)
        self.key_padding = tk.Scale(
            frame,
            from_=5,
            to=30,
            orient='horizontal',
            command=lambda v: self._update_live_preview()
        )
        self.key_padding.set(appearance.get('key_padding', 10))
        self.key_padding.grid(row=row, column=1, sticky='w', padx=5)
        
        # Border Width
        row += 1
        ttk.Label(frame, text="Border Width:").grid(row=row, column=0, sticky='w', pady=5)
        self.border_width = tk.Scale(
            frame,
            from_=1,
            to=10,
            orient='horizontal',
            command=lambda v: self._update_live_preview()
        )
        self.border_width.set(appearance.get('border_width', 2))
        self.border_width.grid(row=row, column=1, sticky='w', padx=5)
    
    def _create_keys_tab(self):
        """Create keys configuration tab."""
        frame = ttk.Frame(self.keys_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Keys to Monitor:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        ttk.Label(frame, text="Enter keys separated by commas (e.g., d, f, j, k)").pack(anchor='w')
        
        # Keys entry
        self.keys_entry = tk.Text(frame, height=3, width=50)
        self.keys_entry.pack(pady=10, fill='x')
        
        current_keys = self.config.get('keys_to_monitor', ['d', 'f', 'j', 'k'])
        self.keys_entry.insert('1.0', ', '.join(current_keys))
        
        # Common presets
        ttk.Label(frame, text="Quick Presets:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(20, 5))
        
        presets_frame = ttk.Frame(frame)
        presets_frame.pack(fill='x')
        
        presets = [
            ("Rhythm 4K", ['d', 'f', 'j', 'k']),
            ("Rhythm 7K", ['s', 'd', 'f', 'space', 'j', 'k', 'l']),
            ("WASD", ['w', 'a', 's', 'd']),
            ("Arrow Keys", ['up', 'down', 'left', 'right']),
            ("QWER", ['q', 'w', 'e', 'r'])
        ]
        
        for preset_name, preset_keys in presets:
            btn = ttk.Button(
                presets_frame,
                text=preset_name,
                command=lambda k=preset_keys: self._apply_key_preset(k)
            )
            btn.pack(side='left', padx=5, pady=5)
    
    def _create_overlay_tab(self):
        """Create overlay settings tab."""
        frame = ttk.Frame(self.overlay_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        overlay = self.config.get('overlay', {})
        
        # Window Size
        ttk.Label(frame, text="Window Size:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        
        size_frame = ttk.Frame(frame)
        size_frame.pack(fill='x', pady=5)
        
        ttk.Label(size_frame, text="Width:").pack(side='left', padx=5)
        self.window_width = ttk.Spinbox(size_frame, from_=200, to=1000, width=10)
        self.window_width.set(overlay.get('width', 400))
        self.window_width.pack(side='left', padx=5)
        self.window_width.bind('<KeyRelease>', lambda e: self._schedule_live_preview())
        self.window_width.bind('<<Increment>>', lambda e: self._schedule_live_preview())
        self.window_width.bind('<<Decrement>>', lambda e: self._schedule_live_preview())
        
        ttk.Label(size_frame, text="Height:").pack(side='left', padx=5)
        self.window_height = ttk.Spinbox(size_frame, from_=100, to=500, width=10)
        self.window_height.set(overlay.get('height', 150))
        self.window_height.pack(side='left', padx=5)
        self.window_height.bind('<KeyRelease>', lambda e: self._schedule_live_preview())
        self.window_height.bind('<<Increment>>', lambda e: self._schedule_live_preview())
        self.window_height.bind('<<Decrement>>', lambda e: self._schedule_live_preview())
        
        # Window Position
        ttk.Label(frame, text="Window Position:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20, 5))
        
        pos_frame = ttk.Frame(frame)
        pos_frame.pack(fill='x', pady=5)
        
        position = overlay.get('position', {})
        
        ttk.Label(pos_frame, text="X:").pack(side='left', padx=5)
        self.pos_x = ttk.Spinbox(pos_frame, from_=0, to=3000, width=10)
        self.pos_x.set(position.get('x', 100))
        self.pos_x.pack(side='left', padx=5)
        self.pos_x.bind('<KeyRelease>', lambda e: self._schedule_live_preview())
        self.pos_x.bind('<<Increment>>', lambda e: self._schedule_live_preview())
        self.pos_x.bind('<<Decrement>>', lambda e: self._schedule_live_preview())
        
        ttk.Label(pos_frame, text="Y:").pack(side='left', padx=5)
        self.pos_y = ttk.Spinbox(pos_frame, from_=0, to=2000, width=10)
        self.pos_y.set(position.get('y', 100))
        self.pos_y.pack(side='left', padx=5)
        self.pos_y.bind('<KeyRelease>', lambda e: self._schedule_live_preview())
        self.pos_y.bind('<<Increment>>', lambda e: self._schedule_live_preview())
        self.pos_y.bind('<<Decrement>>', lambda e: self._schedule_live_preview())
        
        # Always on top
        self.always_on_top = tk.BooleanVar(value=overlay.get('always_on_top', True))
        ttk.Checkbutton(
            frame,
            text="Always on Top",
            variable=self.always_on_top,
            command=self._update_live_preview
        ).pack(anchor='w', pady=5)
        
        # Transparency
        self.transparent = tk.BooleanVar(value=overlay.get('transparent', True))
        ttk.Checkbutton(
            frame,
            text="Transparent Background",
            variable=self.transparent,
            command=self._update_live_preview
        ).pack(anchor='w', pady=5)
        
        # Opacity
        ttk.Label(frame, text="Opacity:").pack(anchor='w', pady=5)
        self.opacity = tk.Scale(
            frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient='horizontal',
            command=lambda v: self._update_live_preview()
        )
        self.opacity.set(overlay.get('opacity', 0.9))
        self.opacity.pack(fill='x', padx=5)
    
    def _create_stats_tab(self):
        """Create statistics settings tab."""
        frame = ttk.Frame(self.stats_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        stats = self.config.get('statistics', {})
        
        # Enable statistics
        self.stats_enabled = tk.BooleanVar(value=stats.get('enabled', True))
        ttk.Checkbutton(
            frame,
            text="Enable Statistics Tracking",
            variable=self.stats_enabled,
            command=self._toggle_stats
        ).pack(anchor='w', pady=5)
        
        # Show KPS
        self.show_kps = tk.BooleanVar(value=stats.get('show_kps', True))
        ttk.Checkbutton(
            frame,
            text="Show Keys Per Second (KPS)",
            variable=self.show_kps
        ).pack(anchor='w', pady=5)
        
        # Show press count
        self.show_count = tk.BooleanVar(value=stats.get('show_press_count', True))
        ttk.Checkbutton(
            frame,
            text="Show Total Press Count",
            variable=self.show_count
        ).pack(anchor='w', pady=5)
        
        # KPS update interval
        ttk.Label(frame, text="KPS Update Interval (seconds):").pack(anchor='w', pady=(20, 5))
        self.kps_interval = tk.Scale(
            frame,
            from_=0.05,
            to=2.0,
            resolution=0.05,
            orient='horizontal'
        )
        self.kps_interval.set(stats.get('kps_update_interval', 0.1))
        self.kps_interval.pack(fill='x', padx=5)
    
    def _create_themes_tab(self):
        """Create themes management tab."""
        frame = ttk.Frame(self.themes_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Theme list
        ttk.Label(frame, text="Available Themes:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill='both', expand=True, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox
        self.themes_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.themes_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.themes_list.yview)
        
        # Load themes
        for theme_name in self.theme_manager.get_theme_names():
            self.themes_list.insert('end', theme_name)
        
        # Theme preview button
        ttk.Button(
            frame,
            text="Preview Theme",
            command=self._preview_theme
        ).pack(side='left', padx=5, pady=5)
        
        # Apply theme button
        ttk.Button(
            frame,
            text="Apply Theme",
            command=self._apply_selected_theme
        ).pack(side='left', padx=5, pady=5)
        
        # Import theme button
        ttk.Button(
            frame,
            text="Import Theme",
            command=self._import_theme
        ).pack(side='left', padx=5, pady=5)
        
        # Export theme button
        ttk.Button(
            frame,
            text="Export Current",
            command=self._export_current_theme
        ).pack(side='left', padx=5, pady=5)
    
    def _create_button_panel(self):
        """Create bottom button panel."""
        button_frame = ttk.Frame(self.window)
        button_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        # Apply button
        ttk.Button(
            button_frame,
            text="Apply",
            command=self._apply_settings
        ).pack(side='left', padx=5)
        
        # Save button
        ttk.Button(
            button_frame,
            text="Save",
            command=self._save_settings
        ).pack(side='left', padx=5)
        
        # Apply & Save button
        ttk.Button(
            button_frame,
            text="Apply & Save",
            command=self._apply_and_save
        ).pack(side='left', padx=5)
        
        # Reset button
        ttk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_defaults
        ).pack(side='left', padx=5)
        
        # Close button
        ttk.Button(
            button_frame,
            text="Close",
            command=self._on_close
        ).pack(side='right', padx=5)
    
    def _choose_color(self, config_key: str, button):
        """Open color chooser dialog."""
        current_color = button.cget('bg')
        color = colorchooser.askcolor(color=current_color, title=f"Choose {config_key}")
        
        if color[1]:  # If color was selected
            button.configure(bg=color[1])
            self.config['appearance'][config_key] = color[1]
            self._update_live_preview()
    
    def _schedule_live_preview(self):
        """Schedule a live preview update with debouncing."""
        # Cancel existing timer if any
        if self.preview_timer:
            self.window.after_cancel(self.preview_timer)
        
        # Schedule new update after 300ms
        self.preview_timer = self.window.after(300, self._update_live_preview)
    
    def _update_live_preview(self):
        """Update live preview (if callback provided)."""
        if self.update_callback:
            # Extract current settings
            self._extract_settings()
            # Call update callback
            self.update_callback(self.config)
    
    def _extract_settings(self):
        """Extract settings from UI widgets into config."""
        # Appearance
        self.config['appearance']['font_family'] = self.font_family.get()
        self.config['appearance']['font_size'] = int(self.font_size.get())
        self.config['appearance']['key_padding'] = int(self.key_padding.get())
        self.config['appearance']['border_width'] = int(self.border_width.get())
        
        # Keys
        keys_text = self.keys_entry.get('1.0', 'end-1c')
        keys = [k.strip() for k in keys_text.split(',') if k.strip()]
        self.config['keys_to_monitor'] = keys
        
        # Overlay
        self.config['overlay']['width'] = int(self.window_width.get())
        self.config['overlay']['height'] = int(self.window_height.get())
        self.config['overlay']['position']['x'] = int(self.pos_x.get())
        self.config['overlay']['position']['y'] = int(self.pos_y.get())
        self.config['overlay']['always_on_top'] = self.always_on_top.get()
        self.config['overlay']['transparent'] = self.transparent.get()
        self.config['overlay']['opacity'] = self.opacity.get()
        
        # Statistics
        self.config['statistics']['enabled'] = self.stats_enabled.get()
        self.config['statistics']['show_kps'] = self.show_kps.get()
        self.config['statistics']['show_press_count'] = self.show_count.get()
        self.config['statistics']['kps_update_interval'] = self.kps_interval.get()
    
    def _apply_key_preset(self, keys):
        """Apply a key preset."""
        self.keys_entry.delete('1.0', 'end')
        self.keys_entry.insert('1.0', ', '.join(keys))
    
    def _toggle_stats(self):
        """Toggle statistics-related options."""
        enabled = self.stats_enabled.get()
        # Could enable/disable stat widgets here
    
    def _preview_theme(self):
        """Preview selected theme."""
        selection = self.themes_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a theme to preview")
            return
        
        theme_name = self.themes_list.get(selection[0])
        preview = self.theme_manager.get_theme_preview(theme_name)
        
        # Show preview dialog
        msg = f"Theme: {preview['name']}\n\n"
        msg += f"Description: {preview['description']}\n\n"
        msg += f"Background: {preview['background']}\n"
        msg += f"Active Key: {preview['active_key']}\n"
        msg += f"Inactive Key: {preview['inactive_key']}\n"
        msg += f"Text: {preview['text']}\n"
        msg += f"Border: {preview['border']}"
        
        messagebox.showinfo("Theme Preview", msg)
    
    def _apply_selected_theme(self):
        """Apply the selected theme."""
        selection = self.themes_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a theme to apply")
            return
        
        theme_name = self.themes_list.get(selection[0])
        self.config = self.theme_manager.apply_theme(theme_name, self.config)
        
        # Update UI widgets to reflect theme
        appearance = self.config['appearance']
        self.bg_color_btn.configure(bg=appearance['background_color'])
        self.active_color_btn.configure(bg=appearance['active_key_color'])
        self.inactive_color_btn.configure(bg=appearance['inactive_key_color'])
        self.text_color_btn.configure(bg=appearance['text_color'])
        self.border_color_btn.configure(bg=appearance['border_color'])
        self.font_family.set(appearance['font_family'])
        self.font_size.set(appearance['font_size'])
        
        self._update_live_preview()
        messagebox.showinfo("Theme Applied", f"Theme '{theme_name}' applied successfully!")
    
    def _import_theme(self):
        """Import a theme from file."""
        file_path = filedialog.askopenfilename(
            title="Import Theme",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            theme_name = self.theme_manager.import_theme(file_path)
            if theme_name:
                self.themes_list.insert('end', theme_name)
                messagebox.showinfo("Success", f"Theme '{theme_name}' imported!")
            else:
                messagebox.showerror("Error", "Failed to import theme")
    
    def _export_current_theme(self):
        """Export current configuration as theme."""
        theme_name = tk.simpledialog.askstring("Theme Name", "Enter name for theme:")
        
        if theme_name:
            self._extract_settings()
            
            file_path = filedialog.asksaveasfilename(
                title="Export Theme",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"{theme_name.lower().replace(' ', '_')}.json"
            )
            
            if file_path:
                # Create theme from current config
                theme_data = {
                    "theme_name": theme_name,
                    "description": "Custom theme",
                    "appearance": self.config['appearance']
                }
                
                import json
                with open(file_path, 'w') as f:
                    json.dump(theme_data, f, indent=4)
                
                messagebox.showinfo("Success", f"Theme exported to {file_path}")
    
    def _apply_settings(self):
        """Apply settings without saving."""
        try:
            self._extract_settings()
            
            if self.update_callback:
                self.update_callback(self.config)
            
            messagebox.showinfo("Settings Applied", "Settings applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
    
    def _save_settings(self):
        """Save settings to config file."""
        try:
            self._extract_settings()
            
            # Save using config manager
            self.config_manager.save_config(self.config)
            
            messagebox.showinfo("Settings Saved", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def _apply_and_save(self):
        """Apply and save settings."""
        try:
            self._extract_settings()
            
            # Apply to live overlay
            if self.update_callback:
                self.update_callback(self.config)
            
            # Save to file
            self.config_manager.save_config(self.config)
            
            messagebox.showinfo("Success", "Settings applied and saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply and save settings: {str(e)}")
    
    def _reset_defaults(self):
        """Reset to default settings."""
        if messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            self.config = self.config_manager.DEFAULT_CONFIG.copy()
            # Reload UI
            self.window.destroy()
            # Would need to reinitialize window here
    
    def _on_close(self):
        """Handle window close."""
        self.window.destroy()
    
    def show(self):
        """Show the settings window."""
        self.window.deiconify()
        self.window.focus()
