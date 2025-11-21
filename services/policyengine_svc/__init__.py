"""
PolicyEngine Service Package

This package hosts the FastAPI microservice that exposes the 4th.GRC
PolicyEngine evaluation API (e.g., /v1/evaluate, /healthz).

Public API surface:

- app:        FastAPI instance (imported from .main)
- get_app():  Helper to retrieve the FastAPI app (for ASGI servers / tests)
- get_settings(): Optional helper to access typed service settings
- get_router():   Optional helper to access the main API router
- __version__:    Service version string

Typical usage:

    from services.policyengine_svc import app

    # or, for more explicit wiring:
    from services.policyengine_svc import get_app, get_settings
    app = get_app()
    settings = get_settings()
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Optional, TYPE_CHECKING

from .main import app as app  # FastAPI app is defined in main.py

__all__ = [
    "app",
    "get_app",
    "get_settings",
    "get_router",
    "__version__",
]

# Bump this as you evolve the service
__version__ = "0.1.0"

if TYPE_CHECKING:  # for editors / type checkers only
    try:
        from fastapi import FastAPI
    except Exception:  # pragma: no cover
        FastAPI = Any  # type: ignore[assignment]

    try:
        # If you define a Settings model in config.py
        from .config import Settings  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover
        Settings = Any  # type: ignore[assignment]

    try:
        from fastapi import APIRouter
    except Exception:  # pragma: no cover
        APIRouter = Any  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Core accessors
# ---------------------------------------------------------------------------

def get_app() -> "FastAPI":
    """
    Return the FastAPI application instance.

    This is a small indirection helper useful for:
    - ASGI servers that prefer a callable (e.g. `get_app`)
    - Tests that want a stable import location

    Example:

        from services.policyengine_svc import get_app
        app = get_app()
    """
    # `app` is imported at module import time from .main
    return app  # type: ignore[return-value]


def get_settings() -> Optional["Settings"]:
    """
    Attempt to fetch typed service settings, if available.

    This assumes you have a config.py file with a `get_settings()` function
    and a `Settings` model, e.g.:

        # config.py
        from pydantic_settings import BaseSettings

        class Settings(BaseSettings):
            policyengine_url: str = "http://127.0.0.1:8080"

        def get_settings() -> Settings:
            return Settings()

    If config.py or get_settings() are not present, this returns None.
    """
    try:
        config_mod = import_module("services.policyengine_svc.config")
    except ModuleNotFoundError:
        return None

    get_settings_fn = getattr(config_mod, "get_settings", None)
    if get_settings_fn is None:
        return None

    return get_settings_fn()


def get_router() -> Optional["APIRouter"]:
    """
    Attempt to fetch the main API router, if your service uses one.

    This assumes an optional structure like:

        services/policyengine_svc/api/__init__.py
        services/policyengine_svc/api/routes_eval.py

    And in api/__init__.py:

        from fastapi import APIRouter
        from .routes_eval import router as eval_router

        router = APIRouter()
        router.include_router(eval_router, prefix="/v1", tags=["evaluation"])

    If the api module or router is not present, this returns None.
    """
    try:
        api_mod = import_module("services.policyengine_svc.api")
    except ModuleNotFoundError:
        return None

    router = getattr(api_mod, "router", None)
    return router
