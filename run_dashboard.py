#!/usr/bin/env python
"""
Script to run the Outdoor Maintenance Activity Suggester Dashboard
"""
import sys
import os

# Get the root directory of the project
root_dir = os.path.dirname(os.path.abspath(__file__))
dash_app_dir = os.path.join(root_dir, 'dash_app')

# Add the dash_app directory to the Python path
sys.path.insert(0, dash_app_dir)

# Change to the dash_app directory
os.chdir(dash_app_dir)

# Import and run the app
from app import app

if __name__ == '__main__':
    app.run(debug=True)
