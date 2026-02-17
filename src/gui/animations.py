"""
Animation Module
Provides animation effects for key presses and visual feedback.
"""

import time
import threading
from typing import Callable, Dict, Any


class AnimationController:
    """
    Controls animations for keyboard overlay.
    Supports various animation types: fade, pulse, scale, glow.
    """
    
    # Animation types
    FADE = "fade"
    PULSE = "pulse"
    SCALE = "scale"
    GLOW = "glow"
    SLIDE = "slide"
    
    def __init__(self):
        """Initialize the animation controller."""
        self.active_animations = {}
        self.animation_threads = {}
        self.lock = threading.Lock()
        
    def animate_key_press(self, key: str, widget_info: Dict, 
                          animation_type: str = PULSE,
                          duration: float = 0.3,
                          callback: Callable = None):
        """
        Animate a key press event.
        
        Args:
            key: The key being pressed
            widget_info: Dictionary containing widget references
            animation_type: Type of animation to perform
            duration: Animation duration in seconds
            callback: Optional callback when animation completes
        """
        with self.lock:
            # Cancel existing animation for this key
            if key in self.active_animations:
                self.active_animations[key]['cancel'] = True
        
        # Start new animation based on type
        if animation_type == self.PULSE:
            self._animate_pulse(key, widget_info, duration, callback)
        elif animation_type == self.FADE:
            self._animate_fade(key, widget_info, duration, callback)
        elif animation_type == self.SCALE:
            self._animate_scale(key, widget_info, duration, callback)
        elif animation_type == self.GLOW:
            self._animate_glow(key, widget_info, duration, callback)
    
    def _animate_pulse(self, key: str, widget_info: Dict, 
                       duration: float, callback: Callable):
        """
        Create a pulsing animation effect.
        
        Args:
            key: The key being animated
            widget_info: Widget information
            duration: Animation duration
            callback: Completion callback
        """
        def pulse():
            frame = widget_info['frame']
            label = widget_info['label']
            steps = 10
            step_duration = duration / (steps * 2)  # Up and down
            
            animation_info = {'cancel': False}
            with self.lock:
                self.active_animations[key] = animation_info
            
            try:
                # Pulse up
                for i in range(steps):
                    if animation_info.get('cancel'):
                        return
                    
                    scale = 1.0 + (i / steps) * 0.2  # Scale up to 1.2x
                    frame.configure(highlightthickness=int(2 * scale))
                    time.sleep(step_duration)
                
                # Pulse down
                for i in range(steps, 0, -1):
                    if animation_info.get('cancel'):
                        return
                    
                    scale = 1.0 + (i / steps) * 0.2
                    frame.configure(highlightthickness=int(2 * scale))
                    time.sleep(step_duration)
                
                # Reset to normal
                frame.configure(highlightthickness=2)
                
            finally:
                with self.lock:
                    if key in self.active_animations:
                        del self.active_animations[key]
                if callback:
                    callback()
        
        thread = threading.Thread(target=pulse, daemon=True)
        thread.start()
    
    def _animate_fade(self, key: str, widget_info: Dict, 
                      duration: float, callback: Callable):
        """
        Create a fade animation effect.
        
        Args:
            key: The key being animated
            widget_info: Widget information
            duration: Animation duration
            callback: Completion callback
        """
        def fade():
            label = widget_info['label']
            original_fg = label.cget('fg')
            steps = 20
            step_duration = duration / steps
            
            animation_info = {'cancel': False}
            with self.lock:
                self.active_animations[key] = animation_info
            
            try:
                # Fade out (make text more transparent-looking by blending with bg)
                for i in range(steps):
                    if animation_info.get('cancel'):
                        return
                    time.sleep(step_duration)
                
                # Reset
                label.configure(fg=original_fg)
                
            finally:
                with self.lock:
                    if key in self.active_animations:
                        del self.active_animations[key]
                if callback:
                    callback()
        
        thread = threading.Thread(target=fade, daemon=True)
        thread.start()
    
    def _animate_scale(self, key: str, widget_info: Dict, 
                       duration: float, callback: Callable):
        """
        Create a scaling animation effect.
        
        Args:
            key: The key being animated
            widget_info: Widget information
            duration: Animation duration
            callback: Completion callback
        """
        def scale():
            label = widget_info['label']
            current_font = label.cget('font')
            
            # Parse font
            if isinstance(current_font, tuple):
                font_family, font_size = current_font[0], current_font[1]
            else:
                font_family, font_size = 'Arial', 24
            
            original_size = font_size
            steps = 8
            step_duration = duration / (steps * 2)
            
            animation_info = {'cancel': False}
            with self.lock:
                self.active_animations[key] = animation_info
            
            try:
                # Scale up
                for i in range(steps):
                    if animation_info.get('cancel'):
                        return
                    
                    scale_factor = 1.0 + (i / steps) * 0.3  # Scale up to 1.3x
                    new_size = int(original_size * scale_factor)
                    label.configure(font=(font_family, new_size, 'bold'))
                    time.sleep(step_duration)
                
                # Scale down
                for i in range(steps, 0, -1):
                    if animation_info.get('cancel'):
                        return
                    
                    scale_factor = 1.0 + (i / steps) * 0.3
                    new_size = int(original_size * scale_factor)
                    label.configure(font=(font_family, new_size, 'bold'))
                    time.sleep(step_duration)
                
                # Reset to original
                label.configure(font=(font_family, original_size, 'bold'))
                
            finally:
                with self.lock:
                    if key in self.active_animations:
                        del self.active_animations[key]
                if callback:
                    callback()
        
        thread = threading.Thread(target=scale, daemon=True)
        thread.start()
    
    def _animate_glow(self, key: str, widget_info: Dict, 
                      duration: float, callback: Callable):
        """
        Create a glowing animation effect.
        
        Args:
            key: The key being animated
            widget_info: Widget information
            duration: Animation duration
            callback: Completion callback
        """
        def glow():
            frame = widget_info['frame']
            steps = 12
            step_duration = duration / (steps * 2)
            
            animation_info = {'cancel': False}
            with self.lock:
                self.active_animations[key] = animation_info
            
            try:
                # Increase border thickness for glow effect
                for i in range(steps):
                    if animation_info.get('cancel'):
                        return
                    
                    thickness = 2 + int((i / steps) * 4)  # 2 to 6
                    frame.configure(highlightthickness=thickness)
                    time.sleep(step_duration)
                
                # Decrease border thickness
                for i in range(steps, 0, -1):
                    if animation_info.get('cancel'):
                        return
                    
                    thickness = 2 + int((i / steps) * 4)
                    frame.configure(highlightthickness=thickness)
                    time.sleep(step_duration)
                
                # Reset
                frame.configure(highlightthickness=2)
                
            finally:
                with self.lock:
                    if key in self.active_animations:
                        del self.active_animations[key]
                if callback:
                    callback()
        
        thread = threading.Thread(target=glow, daemon=True)
        thread.start()
    
    def cancel_animation(self, key: str):
        """
        Cancel an active animation for a key.
        
        Args:
            key: The key whose animation should be cancelled
        """
        with self.lock:
            if key in self.active_animations:
                self.active_animations[key]['cancel'] = True
    
    def cancel_all_animations(self):
        """Cancel all active animations."""
        with self.lock:
            for animation_info in self.active_animations.values():
                animation_info['cancel'] = True
            self.active_animations.clear()
