import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # Import the Flask app from app.py

# Vercel will look for the variable named 'app'
