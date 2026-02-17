"""
Profile Manager Module
Manages multiple configuration profiles for different use cases.
"""

import os
import json
import copy
from typing import Dict, List, Optional
from datetime import datetime


class Profile:
    """
    Represents a single configuration profile.
    """
    
    def __init__(self, name: str, config: Dict, profile_id: Optional[str] = None):
        """
        Initialize a profile.
        
        Args:
            name: Profile name
            config: Configuration dictionary
            profile_id: Unique profile ID (auto-generated if None)
        """
        self.name = name
        self.config = copy.deepcopy(config)
        self.id = profile_id or self._generate_id()
        self.created_at = datetime.now().isoformat()
        self.modified_at = self.created_at
        
    def _generate_id(self) -> str:
        """Generate a unique profile ID."""
        return f"profile_{int(datetime.now().timestamp() * 1000)}"
    
    def update_config(self, config: Dict):
        """
        Update the profile configuration.
        
        Args:
            config: New configuration dictionary
        """
        self.config = copy.deepcopy(config)
        self.modified_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'config': self.config,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Profile':
        """
        Create a profile from dictionary.
        
        Args:
            data: Profile dictionary
            
        Returns:
            Profile instance
        """
        profile = Profile(
            name=data['name'],
            config=data['config'],
            profile_id=data.get('id')
        )
        profile.created_at = data.get('created_at', profile.created_at)
        profile.modified_at = data.get('modified_at', profile.modified_at)
        return profile


class ProfileManager:
    """
    Manages multiple configuration profiles.
    
    Features:
    - Create, update, delete profiles
    - Load and save profiles to disk
    - Switch between profiles
    - Import/export profiles
    """
    
    def __init__(self, profiles_dir: str = None):
        """
        Initialize the profile manager.
        
        Args:
            profiles_dir: Directory to store profiles (default: ./profiles)
        """
        if profiles_dir is None:
            # Get the project root directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            profiles_dir = os.path.join(project_root, 'profiles')
        
        self.profiles_dir = profiles_dir
        self.profiles: Dict[str, Profile] = {}
        self.active_profile_id: Optional[str] = None
        
        # Create profiles directory if it doesn't exist
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Load existing profiles
        self.load_profiles()
    
    def create_profile(self, name: str, config: Dict) -> Profile:
        """
        Create a new profile.
        
        Args:
            name: Profile name
            config: Configuration dictionary
            
        Returns:
            Created profile
        """
        profile = Profile(name, config)
        self.profiles[profile.id] = profile
        self.save_profile(profile)
        return profile
    
    def get_profile(self, profile_id: str) -> Optional[Profile]:
        """
        Get a profile by ID.
        
        Args:
            profile_id: Profile ID
            
        Returns:
            Profile instance or None if not found
        """
        return self.profiles.get(profile_id)
    
    def get_profile_by_name(self, name: str) -> Optional[Profile]:
        """
        Get a profile by name.
        
        Args:
            name: Profile name
            
        Returns:
            Profile instance or None if not found
        """
        for profile in self.profiles.values():
            if profile.name == name:
                return profile
        return None
    
    def update_profile(self, profile_id: str, config: Dict):
        """
        Update a profile's configuration.
        
        Args:
            profile_id: Profile ID
            config: New configuration
        """
        profile = self.get_profile(profile_id)
        if profile:
            profile.update_config(config)
            self.save_profile(profile)
    
    def delete_profile(self, profile_id: str) -> bool:
        """
        Delete a profile.
        
        Args:
            profile_id: Profile ID
            
        Returns:
            True if deleted, False if not found
        """
        if profile_id in self.profiles:
            # Delete file
            profile_file = self._get_profile_file_path(profile_id)
            if os.path.exists(profile_file):
                os.remove(profile_file)
            
            # Remove from memory
            del self.profiles[profile_id]
            
            # Clear active profile if it was deleted
            if self.active_profile_id == profile_id:
                self.active_profile_id = None
            
            return True
        return False
    
    def list_profiles(self) -> List[Profile]:
        """
        Get a list of all profiles.
        
        Returns:
            List of profiles
        """
        return list(self.profiles.values())
    
    def set_active_profile(self, profile_id: str) -> bool:
        """
        Set the active profile.
        
        Args:
            profile_id: Profile ID
            
        Returns:
            True if set successfully, False if profile not found
        """
        if profile_id in self.profiles:
            self.active_profile_id = profile_id
            self._save_active_profile_id()
            return True
        return False
    
    def get_active_profile(self) -> Optional[Profile]:
        """
        Get the active profile.
        
        Returns:
            Active profile or None
        """
        if self.active_profile_id:
            return self.get_profile(self.active_profile_id)
        return None
    
    def save_profile(self, profile: Profile):
        """
        Save a profile to disk.
        
        Args:
            profile: Profile to save
        """
        profile_file = self._get_profile_file_path(profile.id)
        with open(profile_file, 'w') as f:
            json.dump(profile.to_dict(), f, indent=4)
    
    def load_profiles(self):
        """Load all profiles from disk."""
        if not os.path.exists(self.profiles_dir):
            return
        
        # Load profiles
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json') and filename != 'active_profile.json':
                profile_file = os.path.join(self.profiles_dir, filename)
                try:
                    with open(profile_file, 'r') as f:
                        data = json.load(f)
                        profile = Profile.from_dict(data)
                        self.profiles[profile.id] = profile
                except Exception as e:
                    print(f"Error loading profile {filename}: {e}")
        
        # Load active profile ID
        self._load_active_profile_id()
    
    def _get_profile_file_path(self, profile_id: str) -> str:
        """Get the file path for a profile."""
        return os.path.join(self.profiles_dir, f"{profile_id}.json")
    
    def _save_active_profile_id(self):
        """Save the active profile ID to disk."""
        active_file = os.path.join(self.profiles_dir, 'active_profile.json')
        with open(active_file, 'w') as f:
            json.dump({'active_profile_id': self.active_profile_id}, f)
    
    def _load_active_profile_id(self):
        """Load the active profile ID from disk."""
        active_file = os.path.join(self.profiles_dir, 'active_profile.json')
        if os.path.exists(active_file):
            try:
                with open(active_file, 'r') as f:
                    data = json.load(f)
                    self.active_profile_id = data.get('active_profile_id')
            except Exception as e:
                print(f"Error loading active profile ID: {e}")
    
    def import_profile(self, file_path: str) -> Optional[Profile]:
        """
        Import a profile from a JSON file.
        
        Args:
            file_path: Path to profile JSON file
            
        Returns:
            Imported profile or None on error
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Create new profile with imported config
                profile = Profile(
                    name=data.get('name', 'Imported Profile'),
                    config=data.get('config', data)  # Support both profile and config format
                )
                
                self.profiles[profile.id] = profile
                self.save_profile(profile)
                return profile
        except Exception as e:
            print(f"Error importing profile: {e}")
            return None
    
    def export_profile(self, profile_id: str, file_path: str) -> bool:
        """
        Export a profile to a JSON file.
        
        Args:
            profile_id: Profile ID
            file_path: Destination file path
            
        Returns:
            True if exported successfully
        """
        profile = self.get_profile(profile_id)
        if profile:
            try:
                with open(file_path, 'w') as f:
                    json.dump(profile.to_dict(), f, indent=4)
                return True
            except Exception as e:
                print(f"Error exporting profile: {e}")
                return False
        return False
    
    def duplicate_profile(self, profile_id: str, new_name: str) -> Optional[Profile]:
        """
        Duplicate an existing profile.
        
        Args:
            profile_id: Profile ID to duplicate
            new_name: Name for the new profile
            
        Returns:
            New profile or None if source not found
        """
        source_profile = self.get_profile(profile_id)
        if source_profile:
            return self.create_profile(new_name, source_profile.config)
        return None
