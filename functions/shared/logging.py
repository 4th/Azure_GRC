import logging
import json
from typing import Any, Dict

_logger = logging.getLogger("functions.shared")
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)


def get_logger() -> logging.Logger:
    return _logger


def log_event(event_type: str, message: str, extra: Dict[str, Any] | None = None) -> None:
    payload = {
        "event_type": event_type,
        "message": message,
        "extra": extra or {},
    }
    _logger.info(json.dumps(payload))
