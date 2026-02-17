"""
Tests for Phase 3 Features
Tests profile manager, per-key KPS tracking, and related functionality.
"""

import unittest
import time
import tempfile
import os
import json
from collections import defaultdict
from core.profile_manager import ProfileManager, Profile
from core.statistics import StatisticsTracker


class TestProfileManager(unittest.TestCase):
    """Test the ProfileManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(profiles_dir=self.temp_dir)
        self.test_config = {
            'keys_to_monitor': ['a', 'b', 'c'],
            'overlay': {'width': 300, 'height': 100}
        }
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_profile(self):
        """Test profile creation."""
        profile = self.profile_manager.create_profile("Test Profile", self.test_config)
        
        self.assertIsNotNone(profile)
        self.assertEqual(profile.name, "Test Profile")
        self.assertEqual(profile.config, self.test_config)
        self.assertIn(profile.id, self.profile_manager.profiles)
    
    def test_get_profile(self):
        """Test getting a profile by ID."""
        profile = self.profile_manager.create_profile("Test", self.test_config)
        
        retrieved = self.profile_manager.get_profile(profile.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, profile.id)
        self.assertEqual(retrieved.name, profile.name)
    
    def test_get_profile_by_name(self):
        """Test getting a profile by name."""
        profile = self.profile_manager.create_profile("My Profile", self.test_config)
        
        retrieved = self.profile_manager.get_profile_by_name("My Profile")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, profile.id)
    
    def test_update_profile(self):
        """Test updating a profile."""
        profile = self.profile_manager.create_profile("Test", self.test_config)
        
        new_config = {'keys_to_monitor': ['x', 'y', 'z']}
        self.profile_manager.update_profile(profile.id, new_config)
        
        updated = self.profile_manager.get_profile(profile.id)
        self.assertEqual(updated.config, new_config)
    
    def test_delete_profile(self):
        """Test deleting a profile."""
        profile = self.profile_manager.create_profile("Test", self.test_config)
        profile_id = profile.id
        
        success = self.profile_manager.delete_profile(profile_id)
        self.assertTrue(success)
        self.assertIsNone(self.profile_manager.get_profile(profile_id))
    
    def test_list_profiles(self):
        """Test listing all profiles."""
        self.profile_manager.create_profile("Profile 1", self.test_config)
        self.profile_manager.create_profile("Profile 2", self.test_config)
        
        profiles = self.profile_manager.list_profiles()
        self.assertEqual(len(profiles), 2)
    
    def test_active_profile(self):
        """Test setting and getting active profile."""
        profile = self.profile_manager.create_profile("Test", self.test_config)
        
        success = self.profile_manager.set_active_profile(profile.id)
        self.assertTrue(success)
        
        active = self.profile_manager.get_active_profile()
        self.assertIsNotNone(active)
        self.assertEqual(active.id, profile.id)
    
    def test_duplicate_profile(self):
        """Test duplicating a profile."""
        original = self.profile_manager.create_profile("Original", self.test_config)
        
        duplicate = self.profile_manager.duplicate_profile(original.id, "Copy")
        self.assertIsNotNone(duplicate)
        self.assertEqual(duplicate.name, "Copy")
        self.assertEqual(duplicate.config, original.config)
        self.assertNotEqual(duplicate.id, original.id)
    
    def test_import_export_profile(self):
        """Test importing and exporting profiles."""
        profile = self.profile_manager.create_profile("Export Test", self.test_config)
        
        # Export
        export_path = os.path.join(self.temp_dir, "exported.json")
        success = self.profile_manager.export_profile(profile.id, export_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(export_path))
        
        # Import
        imported = self.profile_manager.import_profile(export_path)
        self.assertIsNotNone(imported)
        self.assertEqual(imported.config, profile.config)
    
    def test_profile_persistence(self):
        """Test that profiles persist across manager instances."""
        # Create profile
        profile = self.profile_manager.create_profile("Persistent", self.test_config)
        profile_id = profile.id
        
        # Create new manager instance
        new_manager = ProfileManager(profiles_dir=self.temp_dir)
        
        # Check profile exists
        retrieved = new_manager.get_profile(profile_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Persistent")


class TestPerKeyKPS(unittest.TestCase):
    """Test per-key KPS tracking."""
    
    def setUp(self):
        """Set up test environment."""
        self.tracker = StatisticsTracker(kps_window=1.0)
    
    def test_per_key_kps_tracking(self):
        """Test that per-key KPS is tracked correctly."""
        # Press key 'd' 10 times
        for _ in range(10):
            self.tracker.record_press('d')
            time.sleep(0.01)  # Small delay
        
        # Check per-key KPS
        d_kps = self.tracker.get_key_kps('d')
        self.assertGreater(d_kps, 0)
        
        stats = self.tracker.get_statistics()
        self.assertIn('per_key_kps', stats)
        self.assertIn('d', stats['per_key_kps'])
    
    def test_multiple_keys_independent_kps(self):
        """Test that different keys have independent KPS."""
        # Press 'd' 10 times
        for _ in range(10):
            self.tracker.record_press('d')
            time.sleep(0.01)
        
        # Press 'f' 5 times
        for _ in range(5):
            self.tracker.record_press('f')
            time.sleep(0.01)
        
        d_kps = self.tracker.get_key_kps('d')
        f_kps = self.tracker.get_key_kps('f')
        
        # 'd' should have higher KPS than 'f'
        self.assertGreater(d_kps, f_kps)
    
    def test_per_key_peak_kps(self):
        """Test per-key peak KPS tracking."""
        # Press key rapidly
        for _ in range(20):
            self.tracker.record_press('d')
            time.sleep(0.01)
        
        # Wait a bit
        time.sleep(0.5)
        
        # Press slower
        for _ in range(5):
            self.tracker.record_press('d')
            time.sleep(0.1)
        
        peak_kps = self.tracker.get_key_peak_kps('d')
        current_kps = self.tracker.get_key_kps('d')
        
        # Peak should be higher than current
        self.assertGreater(peak_kps, current_kps)
    
    def test_per_key_kps_in_statistics(self):
        """Test that per-key KPS appears in statistics export."""
        self.tracker.record_press('d')
        self.tracker.record_press('f')
        
        stats = self.tracker.get_statistics()
        
        self.assertIn('per_key_kps', stats)
        self.assertIn('per_key_peak_kps', stats)
        self.assertIn('d', stats['per_key_kps'])
        self.assertIn('f', stats['per_key_kps'])
    
    def test_per_key_kps_reset(self):
        """Test that per-key KPS is reset with statistics."""
        # Record some presses
        for _ in range(10):
            self.tracker.record_press('d')
        
        # Reset
        self.tracker.reset_statistics()
        
        # Check that per-key data is cleared
        d_kps = self.tracker.get_key_kps('d')
        peak_kps = self.tracker.get_key_peak_kps('d')
        
        self.assertEqual(d_kps, 0.0)
        self.assertEqual(peak_kps, 0.0)
    
    def test_per_key_kps_sliding_window(self):
        """Test that per-key KPS uses sliding window correctly."""
        # Press key rapidly
        for _ in range(10):
            self.tracker.record_press('d')
            time.sleep(0.05)  # 50ms between presses
        
        kps_immediately = self.tracker.get_key_kps('d')
        
        # Wait for window to slide
        time.sleep(1.2)
        
        kps_after_wait = self.tracker.get_key_kps('d')
        
        # KPS should drop after window slides past the presses
        self.assertLess(kps_after_wait, kps_immediately)
    
    def test_per_key_kps_history(self):
        """Test that per-key KPS is included in history."""
        self.tracker.record_press('d')
        self.tracker.record_press('f')
        
        history = self.tracker.get_kps_history()
        
        # History entries should contain per_key_kps
        for entry in history:
            self.assertIn('per_key_kps', entry)


class TestProfile(unittest.TestCase):
    """Test the Profile class."""
    
    def test_profile_creation(self):
        """Test creating a profile."""
        config = {'test': 'value'}
        profile = Profile("Test", config)
        
        self.assertEqual(profile.name, "Test")
        self.assertEqual(profile.config, config)
        self.assertIsNotNone(profile.id)
        self.assertIsNotNone(profile.created_at)
    
    def test_profile_to_dict(self):
        """Test converting profile to dictionary."""
        config = {'test': 'value'}
        profile = Profile("Test", config)
        
        data = profile.to_dict()
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('config', data)
        self.assertIn('created_at', data)
        self.assertIn('modified_at', data)
    
    def test_profile_from_dict(self):
        """Test creating profile from dictionary."""
        data = {
            'id': 'test_id',
            'name': 'Test Profile',
            'config': {'test': 'value'},
            'created_at': '2026-01-01',
            'modified_at': '2026-01-02'
        }
        
        profile = Profile.from_dict(data)
        
        self.assertEqual(profile.id, 'test_id')
        self.assertEqual(profile.name, 'Test Profile')
        self.assertEqual(profile.config, {'test': 'value'})
    
    def test_profile_update_config(self):
        """Test updating profile configuration."""
        profile = Profile("Test", {'old': 'value'})
        
        new_config = {'new': 'value'}
        profile.update_config(new_config)
        
        self.assertEqual(profile.config, new_config)
        self.assertNotEqual(profile.created_at, profile.modified_at)


if __name__ == '__main__':
    unittest.main()
