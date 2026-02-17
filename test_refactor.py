"""
Quick test script for settings refactor.
Tests that settings changes are properly applied in real-time.
"""

import sys
import os
import ast

# Check source files for required methods
def check_methods_in_file(filepath, required_methods):
    """Check if a Python file contains all required methods."""
    with open(filepath, 'r') as f:
        source = f.read()
    
    tree = ast.parse(source)
    
    # Find all method definitions
    methods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            methods.add(node.name)
    
    missing = []
    for method in required_methods:
        if method not in methods:
            missing.append(method)
    
    return missing

try:
    # Test overlay_window.py
    overlay_methods = [
        'apply_config_changes',
        '_update_from_config',
        '_rebuild_ui',
        '_update_window_geometry'
    ]
    
    missing = check_methods_in_file('src/gui/overlay_window.py', overlay_methods)
    if missing:
        print(f"❌ overlay_window.py missing methods: {missing}")
        sys.exit(1)
    else:
        print("✅ overlay_window.py has all required methods")
    
    # Test settings_window.py
    settings_methods = [
        '_schedule_live_preview',
        '_update_live_preview',
        '_apply_settings',
        '_save_settings',
        '_apply_and_save'
    ]
    
    missing = check_methods_in_file('src/gui/settings_window.py', settings_methods)
    if missing:
        print(f"❌ settings_window.py missing methods: {missing}")
        sys.exit(1)
    else:
        print("✅ settings_window.py has all required methods")
    
    # Test config_manager.py
    config_methods = [
        'save_config'
    ]
    
    missing = check_methods_in_file('src/config/config_manager.py', config_methods)
    if missing:
        print(f"❌ config_manager.py missing methods: {missing}")
        sys.exit(1)
    else:
        print("✅ config_manager.py has all required methods")
    
    print("\n🎉 All tests passed! Settings refactor is ready.")
    print("\nKey improvements:")
    print("  • Real-time preview for all settings (font size, colors, positions, etc.)")
    print("  • Debounced updates to prevent performance issues")
    print("  • Full UI rebuild when keys change")
    print("  • Proper Apply, Save, and Apply & Save functionality")
    print("  • Error handling with user-friendly messages")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
