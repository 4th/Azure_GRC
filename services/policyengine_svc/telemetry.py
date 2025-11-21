"""Telemetry helpers for the 4th.GRC PolicyEngine service.

This module provides a small convenience wrapper for wiring the service
logger to Azure Application Insights using the ``opencensus-ext-azure``
integration. When configured, all log records emitted through the chosen
logger will be exported to Azure Monitor / Application Insights.

The connection string is read from the ``APPINSIGHTS_CONNECTION_STRING``
environment variable so that no secrets are hard-coded in the source.
"""

import logging
import os
from typing import Optional

from opencensus.ext.azure.log_exporter import AzureLogHandler


def configure_app_insights(logger_name: str = "policyengine_svc") -> Optional[AzureLogHandler]:
    """Configure Azure Application Insights logging for the given logger.

    This helper looks for the ``APPINSIGHTS_CONNECTION_STRING`` environment
    variable and, if present, attaches an :class:`AzureLogHandler` to the
    specified logger. If the environment variable is not set, the function
    becomes a no-op and returns ``None`` so callers can easily branch on
    whether telemetry is enabled.

    The function is safe to call multiple times; it will only attach a new
    handler if one is not already present for the target logger.

    Example:
        >>> from services.policyengine_svc.telemetry import configure_app_insights
        >>> handler = configure_app_insights()
        >>> logger = logging.getLogger("policyengine_svc")
        >>> logger.info("PolicyEngine service started")

    Args:
        logger_name: Name of the logger to configure. Defaults to the main
            service logger, ``"policyengine_svc"``.

    Returns:
        The AzureLogHandler instance that was attached to the logger, or
        ``None`` if the ``APPINSIGHTS_CONNECTION_STRING`` environment
        variable is not defined.
    """
    conn = os.getenv("APPINSIGHTS_CONNECTION_STRING")
    if not conn:
        return None

    logger = logging.getLogger(logger_name)

    # Avoid attaching duplicate handlers if this function is called more than once
    for handler in logger.handlers:
        if isinstance(handler, AzureLogHandler):
            return handler

    handler = AzureLogHandler(connection_string=conn)
    logger.addHandler(handler)
    return handler
