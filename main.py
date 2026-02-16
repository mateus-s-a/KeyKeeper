"""
Keyboard Overlay Application
Main entry point for the application.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.app import KeyboardOverlayApp


def main():
    """
    Main entry point for the Keyboard Overlay application.
    """
    try:
        app = KeyboardOverlayApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
