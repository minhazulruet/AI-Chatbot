"""
ASGI entry point for Render deployment
This wrapper properly handles module imports from the project root
"""
import sys
from pathlib import Path

# Add backend directory to Python path BEFORE any imports
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Now import the app
from app.main import app

# This makes the app available for uvicorn
__all__ = ["app"]
