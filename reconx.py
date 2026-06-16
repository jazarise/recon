import sys
import os

# Inject the src/reconx directory into the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'reconx')))

# Import and execute the main application
try:
    import reconx
except ImportError as e:
    print(f"Failed to load application: {e}")
    sys.exit(1)