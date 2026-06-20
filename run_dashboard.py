#!/usr/bin/env python
"""
Script to run the Outdoor Maintenance Activity Suggester Dashboard
"""
import sys
import os

# Add the dash_app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Change to the dash_app directory
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dash_app'))

# Import and run the app
from app import app

if __name__ == '__main__':
    app.run_server(debug=True)
