from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException as FastAPIHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException


from app.core.exceptions import AppException
from app.schemas.error import ErrorResponse
from app.core.logging import get_logger

logger = get_logger(__name__)

async def app_exception_handler(request: Request, exc: AppException):
    logger.error("Application exception occurred", exc_info=exc, status_code=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            status_code=exc.status_code,
            error_code=exc.error_code,
            type=exc.type,
        ).dict(exclude_none=True),
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"Field '{field}': {message}")
    detail = "Validation error: " + "; ".join(error_messages)
    logger.error("Request validation error", detail=detail, errors=exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            type="RequestValidationError",
        ).dict(exclude_none=True),
    )

async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    logger.error("HTTP exception occurred", exc_info=exc, status_code=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            status_code=exc.status_code,
            type="HTTPException",
        ).dict(exclude_none=True),
    )

async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error("Starlette HTTP exception occurred", exc_info=exc, status_code=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail, # StarletteHTTPException might not have all custom attributes
            status_code=exc.status_code,
            type="StarletteHTTPException",
        ).dict(exclude_none=True),
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("An unexpected error occurred", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            detail="An unexpected internal server error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            type="UnhandledException",
        ).dict(exclude_none=True),
    )

def register_error_handlers(app: FastAPI) -> None:
    """Register custom exception handlers with the FastAPI app."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(FastAPIHTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
    # It's generally a good practice to have a catch-all for unexpected errors.
    # However, be cautious as this can sometimes mask issues.
    # Ensure this is the last handler registered if you choose to use it.
    app.add_exception_handler(Exception, generic_exception_handler)