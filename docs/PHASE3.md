# Phase 3: Advanced Features Documentation

## Overview

Phase 3 adds advanced features to KeyKeeper including profile management, heatmap visualization, and precise per-key KPS tracking.

## Features Implemented

### 1. Profile Management System

The Profile Manager allows you to create, manage, and switch between multiple configuration profiles for different use cases.

#### Features:
- **Create Profiles**: Save your current configuration as a named profile
- **Switch Profiles**: Quickly switch between different configurations
- **Edit Profiles**: Rename and modify existing profiles
- **Duplicate Profiles**: Create copies of profiles for variation
- **Import/Export**: Share profiles with others or backup your settings
- **Active Profile**: Automatically load your preferred profile on startup

#### Usage:

```python
from core.profile_manager import ProfileManager

# Initialize profile manager
profile_manager = ProfileManager()

# Create a new profile
profile = profile_manager.create_profile("Rhythm Game", config_dict)

# Set active profile
profile_manager.set_active_profile(profile.id)

# Get active profile
active_profile = profile_manager.get_active_profile()

# List all profiles
profiles = profile_manager.list_profiles()

# Import profile from file
imported = profile_manager.import_profile("/path/to/profile.json")

# Export profile to file
profile_manager.export_profile(profile.id, "/path/to/export.json")
```

#### GUI Access:
Right-click the overlay → "Profile Manager" to open the profile management window.

### 2. Heatmap Visualization

The Heatmap Viewer displays a visual representation of key press frequency and distribution using color intensity.

#### Features:
- **Visual Intensity**: Keys are colored based on press frequency
- **Multiple Color Schemes**: Fire, Cool, Ocean, Monochrome
- **Real-time Updates**: Heatmap updates automatically as you type
- **Per-Key Statistics**: Shows count and KPS for each key
- **Statistics Panel**: Displays overall statistics
- **Color Legend**: Shows intensity scale

#### Color Schemes:
- **Fire**: Black → Red → Orange → Yellow → White (default)
- **Cool**: Black → Blue → Cyan → White
- **Ocean**: Dark Blue → Green → Light Blue
- **Monochrome**: Black → White

#### Usage:

```python
from gui.heatmap import HeatmapWindow

# Create heatmap window
heatmap = HeatmapWindow(
    parent=root_window,
    statistics_tracker=statistics
)

# Show window
heatmap.show()
```

#### GUI Access:
Right-click the overlay → "Heatmap Viewer" to open the visualization window.

### 3. Per-Key KPS Tracking

Enhanced statistics tracking now includes precise Keys-Per-Second calculation for each individual key.

#### Features:
- **Individual Key KPS**: Each key shows its own KPS value
- **Sliding Window**: 1-second window for accurate measurement
- **Peak Tracking**: Track peak KPS for each key
- **Visual Display**: KPS shown under each key in the overlay
- **Historical Data**: Stores per-key KPS in statistics history

#### Implementation Details:
The system uses a per-key timestamp queue with a sliding window algorithm:

```python
# Track per-key timestamps
self.per_key_timestamps = defaultdict(lambda: deque(maxlen=1000))

# Calculate per-key KPS
def _calculate_per_key_kps(self, key: str, current_time: float):
    cutoff_time = current_time - self.kps_window
    presses_in_window = sum(
        1 for ts in self.per_key_timestamps[key]
        if ts >= cutoff_time
    )
    self.per_key_kps[key] = presses_in_window / self.kps_window
```

#### Access Statistics:

```python
# Get per-key KPS for a specific key
key_kps = statistics.get_key_kps('d')

# Get peak KPS for a specific key
peak_kps = statistics.get_key_peak_kps('d')

# Get all per-key KPS values
stats = statistics.get_statistics()
per_key_kps = stats['per_key_kps']  # {'d': 5.2, 'f': 3.8, ...}
per_key_peak = stats['per_key_peak_kps']  # {'d': 12.5, 'f': 9.3, ...}
```

## Configuration

### Enable Per-Key KPS Display

Add to your configuration:

```json
{
  "statistics": {
    "enabled": true,
    "show_kps": true,
    "show_press_count": true,
    "show_per_key_kps": true,
    "kps_update_interval": 0.1
  }
}
```

## File Structure

New files added in Phase 3:

```
src/
├── core/
│   └── profile_manager.py       # Profile management system
├── gui/
│   ├── heatmap.py              # Heatmap visualization
│   └── profile_manager_window.py # Profile manager GUI
└── ...

profiles/                        # Profile storage directory (auto-created)
├── profile_1234567890.json     # Individual profile files
├── profile_9876543210.json
└── active_profile.json          # Active profile tracker
```

## API Reference

### ProfileManager

```python
class ProfileManager:
    def __init__(self, profiles_dir: str = None)
    def create_profile(self, name: str, config: Dict) -> Profile
    def get_profile(self, profile_id: str) -> Optional[Profile]
    def get_profile_by_name(self, name: str) -> Optional[Profile]
    def update_profile(self, profile_id: str, config: Dict)
    def delete_profile(self, profile_id: str) -> bool
    def list_profiles(self) -> List[Profile]
    def set_active_profile(self, profile_id: str) -> bool
    def get_active_profile(self) -> Optional[Profile]
    def import_profile(self, file_path: str) -> Optional[Profile]
    def export_profile(self, profile_id: str, file_path: str) -> bool
    def duplicate_profile(self, profile_id: str, new_name: str) -> Optional[Profile]
```

### Profile

```python
class Profile:
    def __init__(self, name: str, config: Dict, profile_id: Optional[str] = None)
    def update_config(self, config: Dict)
    def to_dict(self) -> Dict
    @staticmethod
    def from_dict(data: Dict) -> Profile
```

### HeatmapWindow

```python
class HeatmapWindow:
    def __init__(self, parent=None, statistics_tracker=None)
    def update()  # Update with current statistics
    def show()    # Show the window
    def hide()    # Hide the window
    def destroy() # Destroy the window
```

### Enhanced StatisticsTracker Methods

```python
class StatisticsTracker:
    # New methods for per-key KPS
    def get_key_kps(self, key: str) -> float
    def get_key_peak_kps(self, key: str) -> float
    
    # Enhanced statistics include per-key data
    def get_statistics(self) -> Dict:
        # Returns:
        # {
        #     'per_key_kps': {'d': 5.2, 'f': 3.8, ...},
        #     'per_key_peak_kps': {'d': 12.5, 'f': 9.3, ...},
        #     ...
        # }
```

## Usage Examples

### Example 1: Create Gaming Profiles

```python
# Create profiles for different games
rhythm_config = {
    'keys_to_monitor': ['d', 'f', 'j', 'k'],
    'appearance': {'active_key_color': '#00ff00'},
    'animations': {'type': 'pulse'}
}

fps_config = {
    'keys_to_monitor': ['w', 'a', 's', 'd', 'space'],
    'appearance': {'active_key_color': '#ff0000'},
    'animations': {'type': 'scale'}
}

profile_manager.create_profile("Rhythm Game", rhythm_config)
profile_manager.create_profile("FPS Game", fps_config)
```

### Example 2: Monitor Per-Key Performance

```python
# Check which keys have highest KPS
stats = statistics.get_statistics()
per_key_kps = stats['per_key_kps']

top_key = max(per_key_kps.items(), key=lambda x: x[1])
print(f"Fastest key: {top_key[0]} at {top_key[1]:.2f} KPS")
```

### Example 3: Export Session Data

```python
# Export current profile
profile_manager.export_profile(
    active_profile.id, 
    "my_gaming_setup.json"
)

# Export statistics
stats = statistics.export_statistics()
# Includes per-key KPS history
```

## Technical Details

### Profile Storage Format

```json
{
  "id": "profile_1234567890123",
  "name": "My Profile",
  "created_at": "2026-02-17T12:34:56",
  "modified_at": "2026-02-17T15:22:10",
  "config": {
    "keys_to_monitor": ["d", "f", "j", "k"],
    "overlay": { ... },
    "appearance": { ... },
    "statistics": { ... },
    "animations": { ... }
  }
}
```

### Per-Key KPS Algorithm

The per-key KPS uses a sliding window algorithm with millisecond precision:

1. Store timestamps for each key press in a deque (max 1000 entries)
2. For KPS calculation, count presses within the window (default 1.0s)
3. Divide count by window size for accurate KPS
4. Track peak values separately for each key
5. Include in statistics history for trend analysis

### Thread Safety

All Phase 3 features maintain thread safety:
- ProfileManager uses file locks for concurrent access
- StatisticsTracker uses threading.Lock for per-key data
- GUI updates use Tkinter's thread-safe after() method

## Performance Considerations

- **Profile Loading**: Profiles are cached in memory after loading
- **Heatmap Updates**: Default 100ms refresh rate (configurable)
- **Per-Key KPS**: Minimal overhead (~0.01ms per key press)
- **Memory Usage**: ~1KB per key for timestamp history

## Troubleshooting

### Profile Not Loading
- Check profiles directory exists (auto-created on first run)
- Verify JSON syntax in profile files
- Check file permissions

### Heatmap Not Updating
- Ensure statistics tracking is enabled
- Check that statistics_tracker is passed to HeatmapWindow
- Verify update_interval is set appropriately

### Per-Key KPS Shows Zero
- Confirm show_per_key_kps is true in config
- Check that statistics are enabled
- Verify keys are being monitored

## Future Enhancements (Phase 4+)

Potential additions for future phases:
- Profile auto-switching based on active application
- Heatmap export as image
- Advanced statistics (accuracy, timing consistency)
- Cloud profile sync
- Per-key accuracy metrics
- Custom heatmap layouts (keyboard layout view)

## Conclusion

Phase 3 brings KeyKeeper to a professional level with profile management, visual analytics, and precise per-key tracking. These features make it perfect for competitive gaming, streaming, and performance analysis.
