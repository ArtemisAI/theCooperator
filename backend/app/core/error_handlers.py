"""
Global error handler registration for theCooperator backend.

This module will define and register custom exception handlers to standardize
error responses (e.g., JSON API error format).
"""

from fastapi import FastAPI

def register_error_handlers(app: FastAPI) -> None:
    """Register custom exception handlers with the FastAPI app."""
    from fastapi import HTTPException, Request
    from fastapi.exceptions import RequestValidationError
    from fastapi.responses import JSONResponse
    from starlette.exceptions import HTTPException as StarletteHTTPException

    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {"type": "http_error", "status_code": exc.status_code, "message": exc.detail}
            },
        )

    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {"type": "validation_error", "errors": exc.errors()}
            },
        )

    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": {"type": "internal_error", "message": str(exc)}},
        )

    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)