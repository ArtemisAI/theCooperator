from typing import Optional
from .base import BaseSchema

class ErrorResponse(BaseSchema):
    detail: str
    status_code: int
    error_code: Optional[str] = None
    type: Optional[str] = None
