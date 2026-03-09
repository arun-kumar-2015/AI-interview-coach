"""
This file exists to allow running the backend from the repo root.
It adds the backend directory to the Python path and imports the FastAPI app.
"""
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, backend_dir)

# Now import the app from backend/main.py
from main import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("backend_start:app", host="0.0.0.0", port=port, reload=False)
