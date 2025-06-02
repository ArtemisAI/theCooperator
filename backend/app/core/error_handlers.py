from fastapi import Request # JSONResponse removed from here
from starlette.responses import JSONResponse # Added import from starlette
# import logging # Standard logging replaced by structlog
import structlog

logger = structlog.get_logger(__name__)

class APIException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class NotFoundException(APIException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)

class BadRequestException(APIException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)

class UnauthorizedException(APIException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(APIException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)

async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=exc, request_url=str(request.url))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )