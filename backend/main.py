"""
backend.main
Alias entry point for Uvicorn server: uvicorn backend.main:app --reload
"""

from backend.api.main import app

__all__ = ["app"]
