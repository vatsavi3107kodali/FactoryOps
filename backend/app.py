"""
backend.app
Entry point for Uvicorn server: uvicorn backend.app:app --reload
"""

from backend.api.main import app

__all__ = ["app"]
