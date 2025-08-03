import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as app

# Vercel will use the `app` variable as the WSGI entry point.
