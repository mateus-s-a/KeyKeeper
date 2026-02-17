"""
Heatmap Visualization Module
Displays a visual heatmap of key press frequency and distribution.
"""

import tkinter as tk
from tkinter import ttk
import math
from typing import Dict, List, Optional
from collections import defaultdict


class HeatmapWindow:
    """
    A window that displays a heatmap visualization of key press frequency.
    """
    
    def __init__(self, parent=None, statistics_tracker=None):
        """
        Initialize the heatmap window.
        
        Args:
            parent: Parent window
            statistics_tracker: StatisticsTracker instance
        """
        self.statistics_tracker = statistics_tracker
        
        # Create window
        if parent:
            self.window = tk.Toplevel(parent)
        else:
            self.window = tk.Tk()
        
        self.window.title("Key Press Heatmap")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Style configuration
        self.max_intensity = 1.0
        self.color_scheme = "fire"  # fire, cool, ocean, monochrome
        
        # Create UI
        self._create_ui()
        
        # Update timer
        self.update_interval = 100  # ms
        self._schedule_update()
    
    def _create_ui(self):
        """Create the UI components."""
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title and controls
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(title_frame, text="Key Press Heatmap", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # Color scheme selector
        ttk.Label(title_frame, text="Color Scheme:").pack(side=tk.LEFT, padx=(20, 5))
        self.color_scheme_var = tk.StringVar(value=self.color_scheme)
        color_selector = ttk.Combobox(title_frame, textvariable=self.color_scheme_var,
                                     values=["fire", "cool", "ocean", "monochrome"],
                                     state="readonly", width=12)
        color_selector.pack(side=tk.LEFT)
        color_selector.bind('<<ComboboxSelected>>', self._on_color_scheme_changed)
        
        # Reset button
        ttk.Button(title_frame, text="Reset Heatmap", 
                  command=self._reset_heatmap).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Canvas for heatmap
        canvas_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2)
        canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#1a1a1a', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, 
                                   command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL,
                                   command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="No data yet", 
                                     font=('Arial', 10))
        self.stats_label.pack()
        
        # Legend
        legend_frame = ttk.LabelFrame(main_frame, text="Legend", padding="10")
        legend_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.legend_canvas = tk.Canvas(legend_frame, height=40, bg='white')
        self.legend_canvas.pack(fill=tk.X)
        self._draw_legend()
        
        # Key data storage
        self.key_data = {}
        self.key_widgets = {}
    
    def _get_color_for_intensity(self, intensity: float) -> str:
        """
        Get a color based on intensity and color scheme.
        
        Args:
            intensity: Value between 0 and 1
            
        Returns:
            Hex color string
        """
        # Normalize intensity
        intensity = max(0.0, min(1.0, intensity))
        
        if self.color_scheme == "fire":
            # Fire: black -> red -> orange -> yellow -> white
            if intensity < 0.25:
                r = int(intensity * 4 * 255)
                return f'#{r:02x}0000'
            elif intensity < 0.5:
                r = 255
                g = int((intensity - 0.25) * 4 * 255)
                return f'#{r:02x}{g:02x}00'
            elif intensity < 0.75:
                r = 255
                g = 255
                b = int((intensity - 0.5) * 4 * 255)
                return f'#{r:02x}{g:02x}{b:02x}'
            else:
                v = int(255)
                return f'#{v:02x}{v:02x}{v:02x}'
        
        elif self.color_scheme == "cool":
            # Cool: black -> blue -> cyan -> white
            if intensity < 0.5:
                b = int(intensity * 2 * 255)
                return f'#0000{b:02x}'
            else:
                b = 255
                g = int((intensity - 0.5) * 2 * 255)
                return f'#00{g:02x}{b:02x}'
        
        elif self.color_scheme == "ocean":
            # Ocean: dark blue -> green -> light blue
            if intensity < 0.5:
                g = int(intensity * 2 * 255)
                b = int(128 + intensity * 127)
                return f'#00{g:02x}{b:02x}'
            else:
                g = int(255 - (intensity - 0.5) * 2 * 127)
                b = 255
                return f'#00{g:02x}{b:02x}'
        
        else:  # monochrome
            # Monochrome: black -> white
            v = int(intensity * 255)
            return f'#{v:02x}{v:02x}{v:02x}'
    
    def _draw_legend(self):
        """Draw the color legend."""
        self.legend_canvas.delete("all")
        width = self.legend_canvas.winfo_width()
        if width <= 1:
            width = 400
        
        height = 40
        steps = 100
        step_width = width / steps
        
        for i in range(steps):
            intensity = i / steps
            color = self._get_color_for_intensity(intensity)
            x1 = i * step_width
            x2 = (i + 1) * step_width
            self.legend_canvas.create_rectangle(x1, 10, x2, 30, 
                                               fill=color, outline="")
        
        # Labels
        self.legend_canvas.create_text(10, 35, text="Low", anchor=tk.W)
        self.legend_canvas.create_text(width - 10, 35, text="High", anchor=tk.E)
    
    def _on_color_scheme_changed(self, event=None):
        """Handle color scheme change."""
        self.color_scheme = self.color_scheme_var.get()
        self._draw_legend()
        self._update_heatmap()
    
    def _reset_heatmap(self):
        """Reset the heatmap data."""
        self.key_data.clear()
        self.max_intensity = 1.0
        self._update_heatmap()
    
    def update(self):
        """Update the heatmap with current statistics."""
        if not self.statistics_tracker:
            return
        
        stats = self.statistics_tracker.get_statistics()
        key_counts = stats.get('key_press_counts', {})
        per_key_kps = stats.get('per_key_kps', {})
        
        # Update key data
        for key, count in key_counts.items():
            kps = per_key_kps.get(key, 0.0)
            self.key_data[key] = {
                'count': count,
                'kps': kps,
                'intensity': count  # Use count as intensity measure
            }
        
        # Update max intensity for normalization
        if self.key_data:
            self.max_intensity = max(data['count'] for data in self.key_data.values())
            if self.max_intensity == 0:
                self.max_intensity = 1.0
        
        self._update_heatmap()
        self._update_statistics_panel(stats)
    
    def _update_heatmap(self):
        """Redraw the heatmap."""
        self.canvas.delete("all")
        
        if not self.key_data:
            self.canvas.create_text(400, 300, text="No key press data yet",
                                   fill='white', font=('Arial', 14))
            return
        
        # Sort keys for consistent display
        sorted_keys = sorted(self.key_data.keys())
        
        # Calculate grid layout
        keys_per_row = 10
        cell_size = 70
        padding = 10
        
        row = 0
        col = 0
        
        for key in sorted_keys:
            data = self.key_data[key]
            
            # Calculate position
            x = col * (cell_size + padding) + padding
            y = row * (cell_size + padding) + padding
            
            # Calculate intensity (normalized)
            intensity = data['intensity'] / self.max_intensity
            color = self._get_color_for_intensity(intensity)
            
            # Draw cell
            self.canvas.create_rectangle(x, y, x + cell_size, y + cell_size,
                                        fill=color, outline='white', width=2)
            
            # Draw key label
            self.canvas.create_text(x + cell_size/2, y + cell_size/3,
                                   text=key.upper(), fill='white',
                                   font=('Arial', 16, 'bold'))
            
            # Draw count
            self.canvas.create_text(x + cell_size/2, y + cell_size*2/3,
                                   text=f"{data['count']}", fill='white',
                                   font=('Arial', 12))
            
            # Draw KPS
            self.canvas.create_text(x + cell_size/2, y + cell_size - 10,
                                   text=f"{data['kps']:.1f} KPS", fill='white',
                                   font=('Arial', 9))
            
            # Move to next position
            col += 1
            if col >= keys_per_row:
                col = 0
                row += 1
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _update_statistics_panel(self, stats: Dict):
        """Update the statistics panel."""
        total = stats.get('total_presses', 0)
        kps = stats.get('current_kps', 0.0)
        peak_kps = stats.get('peak_kps', 0.0)
        
        top_keys = sorted(self.key_data.items(), 
                         key=lambda x: x[1]['count'], 
                         reverse=True)[:5]
        
        top_keys_str = ", ".join([f"{k.upper()}({v['count']})" 
                                  for k, v in top_keys])
        
        stats_text = (f"Total Presses: {total}  |  "
                     f"Current KPS: {kps:.2f}  |  "
                     f"Peak KPS: {peak_kps:.2f}  |  "
                     f"Top Keys: {top_keys_str}")
        
        self.stats_label.configure(text=stats_text)
    
    def _schedule_update(self):
        """Schedule the next update."""
        self.update()
        self.window.after(self.update_interval, self._schedule_update)
    
    def show(self):
        """Show the heatmap window."""
        self.window.deiconify()
    
    def hide(self):
        """Hide the heatmap window."""
        self.window.withdraw()
    
    def destroy(self):
        """Destroy the window."""
        self.window.destroy()


class HeatmapVisualizer:
    """
    Simplified heatmap visualizer that can be embedded in the overlay.
    """
    
    def __init__(self, canvas: tk.Canvas, x: int, y: int, 
                 width: int, height: int, statistics_tracker=None):
        """
        Initialize the heatmap visualizer.
        
        Args:
            canvas: Canvas to draw on
            x, y: Position
            width, height: Size
            statistics_tracker: StatisticsTracker instance
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.statistics_tracker = statistics_tracker
        
        self.color_scheme = "fire"
        self.max_intensity = 1.0
        self.key_data = {}
    
    def update(self):
        """Update the visualizer with current data."""
        if not self.statistics_tracker:
            return
        
        stats = self.statistics_tracker.get_statistics()
        key_counts = stats.get('key_press_counts', {})
        
        # Update key data
        for key, count in key_counts.items():
            self.key_data[key] = count
        
        # Update max intensity
        if self.key_data:
            self.max_intensity = max(self.key_data.values())
            if self.max_intensity == 0:
                self.max_intensity = 1.0
    
    def draw(self, keys: List[str]):
        """
        Draw a mini heatmap for specified keys.
        
        Args:
            keys: List of keys to display
        """
        if not keys:
            return
        
        cell_width = self.width / len(keys)
        
        for i, key in enumerate(keys):
            count = self.key_data.get(key, 0)
            intensity = count / self.max_intensity if self.max_intensity > 0 else 0
            
            # Simple fire color scheme
            if intensity < 0.5:
                r = int(intensity * 2 * 255)
                color = f'#{r:02x}0000'
            else:
                r = 255
                g = int((intensity - 0.5) * 2 * 255)
                color = f'#{r:02x}{g:02x}00'
            
            x1 = self.x + i * cell_width
            x2 = x1 + cell_width
            
            # Draw as a bar under the keys
            self.canvas.create_rectangle(x1, self.y, x2, self.y + self.height,
                                        fill=color, outline="")
