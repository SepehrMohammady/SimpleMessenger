import sys
import os

# Add the parent directory to sys.path so we can import from the api directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vercel_app import app

# This is the entry point for Vercel
# Import the Vercel-optimized app that uses polling instead of WebSockets
