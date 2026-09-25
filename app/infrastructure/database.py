"""
Database Infrastructure Module.

Provides SQLAlchemy 2.0 AsyncEngine, session factory, base declarative model,
and FastAPI get_db dependency generator for async session management.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Async Engine (Connection Pool Manager)
engine = create_async_engine(
    settings.ASYNC_DATABASE_URI,
    echo=settings.DEBUG,
    future=True,
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy ORM models."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency generator for FastAPI routes.
    Provides an isolated AsyncSession per request and handles transaction cleanup.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
