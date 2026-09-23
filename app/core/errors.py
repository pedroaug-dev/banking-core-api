"""
Global Exception Handlers Module.

Converts domain business exceptions into RFC 7807 compliant JSON responses
and handles unhandled 500 server errors securely.
"""

from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    BusinessRuleException,
    ConflictException,
    DomainException,
    EntityNotFoundException,
    ForbiddenException,
    UnauthorizedException,
)


def create_error_response(
    status_code: int, title: str, detail: str, request: Request
) -> JSONResponse:
    """Helper function to build RFC 7807 compliant error responses."""
    return JSONResponse(
        status_code=status_code,
        content={
            "title": title,
            "status": status_code,
            "detail": detail,
            "path": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers into the FastAPI application instance."""

    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundException):
        """Handles HTTP 404 NOT FOUND when a domain entity does not exist."""
        return create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Entity Not Found",
            detail=exc.message,
            request=request,
        )

    @app.exception_handler(BusinessRuleException)
    async def business_rule_handler(request: Request, exc: BusinessRuleException):
        """Handles HTTP 400 BAD REQUEST when a financial business rule is violated."""
        return create_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            title="Business Rule Violation",
            detail=exc.message,
            request=request,
        )

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):
        """Handles HTTP 409 CONFLICT when resource collisions occur (e.g. duplicate CPF)."""
        return create_error_response(
            status_code=status.HTTP_409_CONFLICT,
            title="Resource Conflict",
            detail=exc.message,
            request=request,
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        """Handles HTTP 401 UNAUTHORIZED when authentication fails or token is invalid."""
        return create_error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            title="Unauthorized Access",
            detail=exc.message,
            request=request,
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        """Handles HTTP 403 FORBIDDEN when user lacks permission for a resource."""
        return create_error_response(
            status_code=status.HTTP_403_FORBIDDEN,
            title="Access Forbidden",
            detail=exc.message,
            request=request,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handles HTTP 500 INTERNAL SERVER ERROR safely without leaking tracebacks."""
        return create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Internal Server Error",
            detail="An unexpected error occurred. Please contact system support.",
            request=request,
        )
