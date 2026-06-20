#!/usr/bin/env python
"""
Script to run the Outdoor Maintenance Activity Suggester Dashboard
"""
import sys
import os

# Get the root directory of the project
root_dir = os.path.dirname(os.path.abspath(__file__))
dash_app_dir = os.path.join(root_dir, 'dash_app')

# Add the dash_app directory to the Python path so imports work
sys.path.insert(0, dash_app_dir)

# Import the Dash app (keeps the project root as the working dir)
from app import app

if __name__ == '__main__':
    # Read run configuration from environment (falls back to sensible defaults)
    debug = os.getenv('DASH_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('DASH_PORT', 8050))
    host = os.getenv('DASH_HOST', '127.0.0.1')

    # Disable the Werkzeug reloader when launching from this runner to
    # avoid attempts to re-execute a non-existent script path
    # (the reloader can try to re-run the original script relative to cwd).
    if debug:
        app.run(debug=True, host=host, port=port, use_reloader=False)
    else:
        app.run(debug=False, host=host, port=port)
