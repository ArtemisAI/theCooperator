from typing import Optional

class AppException(Exception):
    """Base class for application-specific exceptions."""
    def __init__(
        self,
        detail: str,
        status_code: int,
        error_code: Optional[str] = None,
        type: Optional[str] = None,
    ):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        self.type = type

class NotFoundException(AppException):
    """Exception raised when a resource is not found."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail, status_code=404, type="NotFoundError")

class BadRequestException(AppException):
    """Exception raised for bad requests."""
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail, status_code=400, type="BadRequestError")

class UnauthorizedException(AppException):
    """Exception raised for unauthorized access."""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail, status_code=401, type="UnauthorizedError")

class ForbiddenException(AppException):
    """Exception raised when access is forbidden."""
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail, status_code=403, type="ForbiddenError")

class UnprocessableEntityException(AppException):
    """Exception raised for unprocessable entities."""
    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(detail, status_code=422, type="UnprocessableEntityError")

class InternalServerErrorException(AppException):
    """Exception raised for internal server errors."""
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail, status_code=500, type="InternalServerError")

class AssignmentLimitExceededException(BadRequestException): # Inherits from BadRequest (400)
    """Exception raised when a user cannot be assigned more tasks."""
    def __init__(self, detail: str = "Task assignment limit exceeded for user"):
        super().__init__(detail, type="AssignmentLimitExceededError")

class ProposalNotFoundException(NotFoundException):
    """Exception raised when a proposal is not found."""
    def __init__(self, detail: str = "Proposal not found"):
        super().__init__(detail, type="ProposalNotFoundError")
