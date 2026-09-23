from fastapi import FastAPI
from app.core.config import settings
from app.core.errors import register_exception_handlers


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None
)

register_exception_handlers(app)


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    System health check
    Returns basic server status and version information
    """
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }
