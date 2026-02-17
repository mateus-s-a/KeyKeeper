"""
Statistics Module
Tracks keyboard statistics including KPS, key press counts, and more.
"""

import time
import threading
from collections import deque, defaultdict
from typing import Dict, List, Optional


class StatisticsTracker:
    """
    Tracks keyboard statistics in real-time.
    
    Features:
    - Keys per second (KPS) calculation
    - Total key press counter
    - Per-key press counters
    - Historical data tracking
    - Peak KPS tracking
    """
    
    def __init__(self, kps_window: float = 1.0, history_size: int = 100):
        """
        Initialize the statistics tracker.
        
        Args:
            kps_window: Time window in seconds for KPS calculation (default: 1.0)
            history_size: Number of historical data points to keep (default: 100)
        """
        self.kps_window = kps_window
        self.history_size = history_size
        
        # Press tracking
        self.press_timestamps = deque(maxlen=1000)  # Timestamps of all presses
        self.key_press_counts = defaultdict(int)    # Count per key
        self.total_presses = 0                      # Total press count
        
        # KPS tracking
        self.current_kps = 0.0
        self.peak_kps = 0.0
        self.average_kps = 0.0
        self.kps_history = deque(maxlen=history_size)
        
        # Session tracking
        self.session_start_time = time.time()
        self.last_press_time = None
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Statistics update callback
        self.update_callback = None
        
    def record_press(self, key: str):
        """
        Record a key press event.
        
        Args:
            key: The key that was pressed
        """
        current_time = time.time()
        
        with self.lock:
            # Record timestamp
            self.press_timestamps.append(current_time)
            
            # Update counters
            self.key_press_counts[key] += 1
            self.total_presses += 1
            self.last_press_time = current_time
            
            # Calculate current KPS
            self._calculate_kps(current_time)
            
            # Update peak KPS
            if self.current_kps > self.peak_kps:
                self.peak_kps = self.current_kps
            
            # Add to history
            self.kps_history.append({
                'timestamp': current_time,
                'kps': self.current_kps,
                'total_presses': self.total_presses
            })
            
            # Trigger callback if set
            if self.update_callback:
                self.update_callback(self.get_statistics())
    
    def _calculate_kps(self, current_time: float):
        """
        Calculate the current keys per second.
        
        Args:
            current_time: Current timestamp
        """
        # Remove old timestamps outside the window
        cutoff_time = current_time - self.kps_window
        
        # Count presses within the window
        presses_in_window = sum(
            1 for ts in self.press_timestamps 
            if ts >= cutoff_time
        )
        
        # Calculate KPS
        self.current_kps = presses_in_window / self.kps_window
        
        # Calculate average KPS
        if self.kps_history:
            total_kps = sum(entry['kps'] for entry in self.kps_history)
            self.average_kps = total_kps / len(self.kps_history)
    
    def get_statistics(self) -> Dict:
        """
        Get current statistics snapshot.
        
        Returns:
            Dictionary containing all statistics
        """
        with self.lock:
            session_duration = time.time() - self.session_start_time
            
            return {
                'current_kps': round(self.current_kps, 2),
                'peak_kps': round(self.peak_kps, 2),
                'average_kps': round(self.average_kps, 2),
                'total_presses': self.total_presses,
                'key_press_counts': dict(self.key_press_counts),
                'session_duration': round(session_duration, 1),
                'last_press_time': self.last_press_time
            }
    
    def get_kps(self) -> float:
        """
        Get the current keys per second value.
        
        Returns:
            Current KPS value
        """
        with self.lock:
            return round(self.current_kps, 2)
    
    def get_total_presses(self) -> int:
        """
        Get the total number of key presses.
        
        Returns:
            Total press count
        """
        with self.lock:
            return self.total_presses
    
    def get_key_count(self, key: str) -> int:
        """
        Get the press count for a specific key.
        
        Args:
            key: The key to check
            
        Returns:
            Press count for the key
        """
        with self.lock:
            return self.key_press_counts.get(key, 0)
    
    def get_top_keys(self, n: int = 5) -> List[tuple]:
        """
        Get the top N most pressed keys.
        
        Args:
            n: Number of top keys to return
            
        Returns:
            List of (key, count) tuples
        """
        with self.lock:
            sorted_keys = sorted(
                self.key_press_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
            return sorted_keys[:n]
    
    def get_session_duration(self) -> float:
        """
        Get the session duration in seconds.
        
        Returns:
            Session duration in seconds
        """
        return time.time() - self.session_start_time
    
    def reset_statistics(self):
        """Reset all statistics to initial state."""
        with self.lock:
            self.press_timestamps.clear()
            self.key_press_counts.clear()
            self.total_presses = 0
            self.current_kps = 0.0
            self.peak_kps = 0.0
            self.average_kps = 0.0
            self.kps_history.clear()
            self.session_start_time = time.time()
            self.last_press_time = None
    
    def set_update_callback(self, callback):
        """
        Set a callback function to be called when statistics update.
        
        Args:
            callback: Function to call with statistics dictionary
        """
        self.update_callback = callback
    
    def get_kps_history(self) -> List[Dict]:
        """
        Get the historical KPS data.
        
        Returns:
            List of historical data points
        """
        with self.lock:
            return list(self.kps_history)
    
    def export_statistics(self) -> Dict:
        """
        Export all statistics for saving or analysis.
        
        Returns:
            Complete statistics dictionary
        """
        stats = self.get_statistics()
        stats['kps_history'] = self.get_kps_history()
        stats['top_keys'] = self.get_top_keys(10)
        return stats
