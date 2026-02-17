"""
Test suite for statistics module.
"""

import pytest
import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.statistics import StatisticsTracker


class TestStatisticsTracker:
    """Test cases for StatisticsTracker class."""
    
    def test_initialization(self):
        """Test that tracker initializes correctly."""
        tracker = StatisticsTracker(kps_window=1.0)
        
        assert tracker.kps_window == 1.0
        assert tracker.total_presses == 0
        assert tracker.current_kps == 0.0
        assert tracker.peak_kps == 0.0
        
    def test_record_single_press(self):
        """Test recording a single key press."""
        tracker = StatisticsTracker()
        
        tracker.record_press('d')
        
        assert tracker.total_presses == 1
        assert tracker.get_key_count('d') == 1
        
    def test_record_multiple_presses(self):
        """Test recording multiple key presses."""
        tracker = StatisticsTracker()
        
        tracker.record_press('d')
        tracker.record_press('f')
        tracker.record_press('d')
        tracker.record_press('j')
        
        assert tracker.total_presses == 4
        assert tracker.get_key_count('d') == 2
        assert tracker.get_key_count('f') == 1
        assert tracker.get_key_count('j') == 1
        
    def test_kps_calculation(self):
        """Test KPS calculation."""
        tracker = StatisticsTracker(kps_window=1.0)
        
        # Record 5 presses quickly
        for i in range(5):
            tracker.record_press('d')
            time.sleep(0.05)  # Small delay to avoid exact same timestamp
        
        kps = tracker.get_kps()
        assert kps > 0  # Should have some KPS
        assert kps <= 5 / 0.25  # Can't exceed actual rate
        
    def test_peak_kps_tracking(self):
        """Test that peak KPS is tracked correctly."""
        tracker = StatisticsTracker(kps_window=0.5)
        
        # Create a burst of presses
        for i in range(10):
            tracker.record_press('d')
            time.sleep(0.01)
        
        peak_kps = tracker.get_statistics()['peak_kps']
        assert peak_kps > 0
        
        # Wait for window to pass
        time.sleep(0.6)
        
        # Current KPS should drop, but peak should remain
        tracker.record_press('d')
        stats = tracker.get_statistics()
        assert stats['current_kps'] < stats['peak_kps']
        
    def test_get_statistics(self):
        """Test getting complete statistics."""
        tracker = StatisticsTracker()
        
        tracker.record_press('d')
        tracker.record_press('f')
        
        stats = tracker.get_statistics()
        
        assert 'current_kps' in stats
        assert 'peak_kps' in stats
        assert 'average_kps' in stats
        assert 'total_presses' in stats
        assert 'key_press_counts' in stats
        assert 'session_duration' in stats
        
        assert stats['total_presses'] == 2
        assert 'd' in stats['key_press_counts']
        assert 'f' in stats['key_press_counts']
        
    def test_top_keys(self):
        """Test getting top pressed keys."""
        tracker = StatisticsTracker()
        
        # Press different keys different amounts
        for i in range(5):
            tracker.record_press('d')
        for i in range(3):
            tracker.record_press('f')
        for i in range(7):
            tracker.record_press('j')
        tracker.record_press('k')
        
        top_keys = tracker.get_top_keys(3)
        
        assert len(top_keys) == 3
        assert top_keys[0][0] == 'j'  # Most pressed
        assert top_keys[0][1] == 7
        assert top_keys[1][0] == 'd'
        assert top_keys[1][1] == 5
        
    def test_reset_statistics(self):
        """Test resetting statistics."""
        tracker = StatisticsTracker()
        
        # Record some presses
        for i in range(10):
            tracker.record_press('d')
        
        assert tracker.total_presses == 10
        
        # Reset
        tracker.reset_statistics()
        
        assert tracker.total_presses == 0
        assert tracker.current_kps == 0.0
        assert tracker.peak_kps == 0.0
        assert len(tracker.key_press_counts) == 0
        
    def test_session_duration(self):
        """Test session duration tracking."""
        tracker = StatisticsTracker()
        
        time.sleep(0.1)
        
        duration = tracker.get_session_duration()
        assert duration >= 0.1
        assert duration < 0.3  # Should be close to 0.1
        
    def test_key_press_counts(self):
        """Test individual key press counting."""
        tracker = StatisticsTracker()
        
        tracker.record_press('d')
        tracker.record_press('d')
        tracker.record_press('f')
        
        assert tracker.get_key_count('d') == 2
        assert tracker.get_key_count('f') == 1
        assert tracker.get_key_count('j') == 0  # Never pressed
        
    def test_thread_safety(self):
        """Test that tracker is thread-safe."""
        import threading
        
        tracker = StatisticsTracker()
        
        def press_keys():
            for i in range(100):
                tracker.record_press('d')
        
        # Create multiple threads
        threads = [threading.Thread(target=press_keys) for _ in range(5)]
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Should have exactly 500 presses
        assert tracker.total_presses == 500
        
    def test_export_statistics(self):
        """Test exporting statistics."""
        tracker = StatisticsTracker()
        
        tracker.record_press('d')
        tracker.record_press('f')
        
        exported = tracker.export_statistics()
        
        assert 'current_kps' in exported
        assert 'total_presses' in exported
        assert 'kps_history' in exported
        assert 'top_keys' in exported
        
    def test_kps_history(self):
        """Test KPS history tracking."""
        tracker = StatisticsTracker()
        
        # Record some presses with delays
        for i in range(3):
            tracker.record_press('d')
            time.sleep(0.1)
        
        history = tracker.get_kps_history()
        
        assert len(history) == 3
        assert all('timestamp' in entry for entry in history)
        assert all('kps' in entry for entry in history)
        assert all('total_presses' in entry for entry in history)
        

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
