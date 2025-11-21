"""OpenAPI customization helpers for the 4th.GRC PolicyEngine service.

FastAPI automatically generates an OpenAPI schema for the application, but
for production use—especially behind Azure API Management (APIM) and other
gateway layers—we often need to:

* Apply consistent branding (title, description, contact, license).
* Group operations into logical tags (e.g., "Health", "Evaluation").
* Add vendor extensions (such as `x-logo` or `x-ms-visibility` for APIM).
* Hide or de-emphasize internal or experimental endpoints.

This module centralizes those concerns so the main FastAPI application
(`main.py`) can remain focused on routing and behavior while all schema
customization lives in one place.
"""

from typing import Any, Dict

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def generate_custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """Generate a customized OpenAPI schema for the given FastAPI app.

    This function is intended to be assigned to ``app.openapi`` during
    application startup, replacing FastAPI's default OpenAPI generator.
    It first calls :func:`fastapi.openapi.utils.get_openapi` to build the
    base schema and then applies 4th.GRC-specific overrides, such as:

    * Title, version, and description suitable for external consumers.
    * Tag metadata for logical grouping of operations.
    * Vendor extensions (e.g., logos, links, Azure/APIM metadata).

    Args:
        app: The FastAPI application instance for which to generate the
            OpenAPI schema. The app must have its routes already registered
            before this function is called.

    Returns:
        A dictionary representing the OpenAPI schema. This will be used by
        FastAPI to serve ``/openapi.json`` and drive the interactive docs
        at ``/docs`` and ``/redoc``.

    Note:
        This function is pure with respect to the application state; it
        should not modify routes or middleware. It only reads the existing
        app configuration and returns a schema.
    """
    openapi_schema = get_openapi(
        title="4th.GRC PolicyEngine Service",
        version="0.1.0",
        description=(
            "HTTP API for evaluating AI/ML systems, workflows, and "
            "infrastructure configurations against 4th.GRC profiles "
            "and rule sets. This schema is suitable for use in Azure "
            "API Management, client SDK generation, and interactive "
            "documentation."
        ),
        routes=app.routes,
    )

    # Example: tag metadata to group endpoints in the UI
    openapi_schema.setdefault("tags", [])
    openapi_schema["tags"].extend(
        [
            {
                "name": "health",
                "description": "Endpoints used for liveness and readiness checks.",
            },
            {
                "name": "evaluation",
                "description": "Endpoints that perform policy evaluations.",
            },
        ]
    )

    # Example: vendor extension for logo/branding in external UIs
    openapi_schema.setdefault("info", {})
    openapi_schema["info"].setdefault("x-logo", {})
    openapi_schema["info"]["x-logo"].update(
        {
            # This should be a publicly accessible logo URL when deployed
            "url": "https://4th.is/assets/4th_logo.png",
            "altText": "Fourth Industrial Systems",
        }
    )

    # Example: Azure API Management-specific hints (optional)
    # These `x-ms-` extensions can be used by APIM to control visibility,
    # grouping, or SDK generation behavior.
    openapi_schema.setdefault("x-ms-visibility", "public")

    return openapi_schema


def apply_openapi_overrides(app: FastAPI) -> None:
    """Attach the custom OpenAPI generator to the FastAPI app.

    This is a convenience function that wires :func:`generate_custom_openapi`
    into the application instance by overriding ``app.openapi``. Call this
    once during application setup (typically in ``main.py``) after all
    routes have been registered.

    Example:
        >>> from fastapi import FastAPI
        >>> from services.policyengine_svc.openapi_overrides import apply_openapi_overrides
        >>>
        >>> app = FastAPI()
        >>> # register routes here...
        >>> apply_openapi_overrides(app)

    Args:
        app: The FastAPI application instance whose OpenAPI generator should
            be overridden.

    Side Effects:
        Replaces ``app.openapi`` with a function that returns the customized
        OpenAPI schema. Subsequent calls to ``/openapi.json`` and the
        interactive docs will serve the overridden schema.
    """

    def custom_openapi() -> Dict[str, Any]:
        # FastAPI caches the schema on the app, so we reuse it if present.
        if getattr(app, "openapi_schema", None) is not None:
            return app.openapi_schema  # type: ignore[return-value]
        app.openapi_schema = generate_custom_openapi(app)  # type: ignore[attr-defined]
        return app.openapi_schema  # type: ignore[return-value]

    app.openapi = custom_openapi  # type: ignore[assignment]
