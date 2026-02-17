# Statistics Module Documentation

## Overview

The KeyKeeper statistics module provides real-time tracking and analysis of keyboard input, including Keys Per Second (KPS), key press counts, and historical data.

## Features

### 1. Keys Per Second (KPS) Tracking
- **Current KPS**: Real-time calculation of keys pressed per second
- **Peak KPS**: Tracks the highest KPS achieved during the session
- **Average KPS**: Running average of KPS over the session
- **Configurable Window**: Adjustable time window for KPS calculation (default: 1.0 seconds)

### 2. Key Press Counters
- **Total Press Count**: Total number of key presses in the session
- **Per-Key Counters**: Individual counters for each monitored key
- **Top Keys**: Ranking of most frequently pressed keys

### 3. Session Statistics
- **Session Duration**: Total time the application has been running
- **Last Press Time**: Timestamp of the most recent key press
- **Historical Data**: Time-series data of KPS and press counts

## Configuration

### Enabling Statistics

Edit `src/config/default_config.json`:

```json
{
    "statistics": {
        "enabled": true,
        "show_kps": true,
        "show_press_count": true,
        "kps_update_interval": 0.1
    }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable statistics tracking |
| `show_kps` | boolean | `true` | Display KPS in overlay window |
| `show_press_count` | boolean | `true` | Display total press count |
| `kps_update_interval` | float | `0.1` | Update interval in seconds (0.1 = 100ms) |

## Usage

### Basic Usage

Statistics are automatically tracked when enabled in the configuration. The overlay window displays:

1. **KPS**: Current keys per second
2. **Total**: Total key presses
3. **Peak**: Highest KPS achieved

### Display Example

```
[D] [F] [J] [K]
─────────────────
KPS: 8.50  Total: 142  Peak: 12.30
```

## API Reference

### StatisticsTracker Class

#### Initialization

```python
from core.statistics import StatisticsTracker

tracker = StatisticsTracker(
    kps_window=1.0,      # Time window for KPS calculation
    history_size=100     # Number of historical data points to keep
)
```

#### Recording Key Presses

```python
# Record a key press
tracker.record_press('d')
tracker.record_press('f')
```

#### Getting Statistics

```python
# Get current KPS
kps = tracker.get_kps()  # Returns: 8.50

# Get total presses
total = tracker.get_total_presses()  # Returns: 142

# Get count for specific key
count = tracker.get_key_count('d')  # Returns: 35

# Get complete statistics
stats = tracker.get_statistics()
# Returns: {
#   'current_kps': 8.50,
#   'peak_kps': 12.30,
#   'average_kps': 7.20,
#   'total_presses': 142,
#   'key_press_counts': {'d': 35, 'f': 40, 'j': 38, 'k': 29},
#   'session_duration': 45.2,
#   'last_press_time': 1234567890.123
# }
```

#### Advanced Features

```python
# Get top N pressed keys
top_keys = tracker.get_top_keys(5)
# Returns: [('f', 40), ('j', 38), ('d', 35), ('k', 29)]

# Get KPS history
history = tracker.get_kps_history()
# Returns: [
#   {'timestamp': 1234567890.1, 'kps': 8.2, 'total_presses': 100},
#   {'timestamp': 1234567890.2, 'kps': 8.5, 'total_presses': 101},
#   ...
# ]

# Export all statistics
exported = tracker.export_statistics()

# Reset statistics
tracker.reset_statistics()
```

## Implementation Details

### KPS Calculation Algorithm

The KPS calculation uses a sliding time window approach:

1. **Timestamp Recording**: Each key press timestamp is stored in a deque
2. **Window Filtering**: Only presses within the last `kps_window` seconds are counted
3. **Calculation**: `KPS = presses_in_window / kps_window`
4. **Real-time Updates**: Recalculated on every key press

### Thread Safety

The statistics tracker is thread-safe using Python's `threading.Lock`:
- All data modifications are protected by locks
- Safe for concurrent access from multiple threads
- No race conditions in multi-threaded environments

### Performance Considerations

- **Memory**: Uses `deque` with `maxlen` to limit memory usage
- **Efficiency**: O(n) complexity for KPS calculation where n = presses in window
- **Update Frequency**: Configurable update interval balances accuracy vs. performance

## Examples

### Example 1: Basic KPS Tracking

```python
from core.statistics import StatisticsTracker

# Create tracker with 1-second window
tracker = StatisticsTracker(kps_window=1.0)

# Simulate key presses
for i in range(10):
    tracker.record_press('d')
    time.sleep(0.05)  # 50ms between presses

# Get results
print(f"Current KPS: {tracker.get_kps()}")
print(f"Total presses: {tracker.get_total_presses()}")
```

### Example 2: Per-Key Statistics

```python
tracker = StatisticsTracker()

# Press different keys
for i in range(20):
    tracker.record_press('d')
for i in range(15):
    tracker.record_press('f')

# Get per-key counts
stats = tracker.get_statistics()
for key, count in stats['key_press_counts'].items():
    print(f"{key.upper()}: {count} presses")

# Get top keys
top_3 = tracker.get_top_keys(3)
print(f"Top 3 keys: {top_3}")
```

### Example 3: Session Summary

```python
tracker = StatisticsTracker()

# ... after some usage ...

# Print session summary
stats = tracker.get_statistics()
print(f"Session Duration: {stats['session_duration']:.1f}s")
print(f"Total Presses: {stats['total_presses']}")
print(f"Average KPS: {stats['average_kps']:.2f}")
print(f"Peak KPS: {stats['peak_kps']:.2f}")
```

## Customization

### Custom Update Callback

Set a callback function to be notified of statistics updates:

```python
def on_stats_update(stats):
    print(f"KPS: {stats['current_kps']}")

tracker.set_update_callback(on_stats_update)
```

### Adjusting KPS Window

For faster response to changes (rhythm games):
```json
{
    "statistics": {
        "kps_update_interval": 0.05
    }
}
```

For smoother averaging (general use):
```json
{
    "statistics": {
        "kps_update_interval": 0.5
    }
}
```

## Troubleshooting

### KPS shows 0.00

**Causes:**
- Statistics not enabled in config
- No keys have been pressed yet
- Update interval too large

**Solutions:**
1. Check `statistics.enabled` is `true`
2. Press some keys
3. Reduce `kps_update_interval`

### Inaccurate KPS

**Causes:**
- Window size too large or too small
- Update interval doesn't match window

**Solutions:**
1. Adjust `kps_window` in tracker initialization
2. Set appropriate `kps_update_interval`
3. For rhythm games: 0.1-0.5s windows
4. For general use: 1.0s windows

### High Memory Usage

**Causes:**
- Large `history_size` setting
- Long-running sessions

**Solutions:**
1. Reduce `history_size` in tracker initialization
2. Periodically call `reset_statistics()` for long sessions

## Testing

Run the statistics tests:

```bash
pytest tests/test_statistics.py -v
```

Expected output:
```
test_statistics.py::TestStatisticsTracker::test_initialization PASSED
test_statistics.py::TestStatisticsTracker::test_record_single_press PASSED
test_statistics.py::TestStatisticsTracker::test_kps_calculation PASSED
...
```

## Future Enhancements

- [ ] Configurable KPS calculation algorithms
- [ ] Export statistics to CSV/JSON files
- [ ] Historical graphs and visualizations
- [ ] Per-session statistics comparison
- [ ] Auto-save statistics on exit
- [ ] Statistics profiles for different applications

## Related Documentation

- [Configuration Guide](../docs/QUICKSTART.md)
- [Development Guide](../docs/DEVELOPMENT.md)
- [API Reference](../docs/PROJECT_STRUCTURE.md)
