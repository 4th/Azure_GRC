from __future__ import annotations

from typing import Any, Dict

from .schema import PolicyProfile


class ProfileValidationError(Exception):
    """Raised when a profile fails validation."""


def validate_profile(data: Dict[str, Any]) -> None:
    """
    Lightweight structural validation for a profile dict before schema validation.

    This is where you can enforce:
    - required top-level keys
    - conventions on profile_id, version, etc.
    - cross-field checks

    For now, we keep it minimal and let Pydantic do most of the work.
    """
    if "profile_id" not in data:
        raise ProfileValidationError("Missing required field: profile_id")

    if "version" not in data:
        raise ProfileValidationError("Missing required field: version")

    # Example: ensure 'rules' is a list if present
    rules = data.get("rules", [])
    if rules is not None and not isinstance(rules, list):
        raise ProfileValidationError("Field 'rules' must be a list if present.")

    # After structural checks, Pydantic-based schema validation happens elsewhere
    PolicyProfile.model_validate(data)
