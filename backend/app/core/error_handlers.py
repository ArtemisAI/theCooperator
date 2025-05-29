"""
Global error handler registration for theCooperator backend.

This module will define and register custom exception handlers to standardize
error responses (e.g., JSON API error format).
"""

from fastapi import FastAPI

def register_error_handlers(app: FastAPI) -> None:
    """Register custom exception handlers with the FastAPI app."""
    # TODO: implement handlers for HTTPException, ValidationError, etc.
    pass