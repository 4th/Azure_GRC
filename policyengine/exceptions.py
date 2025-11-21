"""
Custom exception types for the PolicyEngine core library.
"""


class PolicyEngineError(Exception):
    """Base class for all PolicyEngine-related errors."""


class ProfileNotFoundError(PolicyEngineError):
    """Raised when a requested profile_ref cannot be resolved."""

    def __init__(self, profile_ref: str):
        super().__init__(f"Profile not found: {profile_ref}")
        self.profile_ref = profile_ref


class ProfileValidationError(PolicyEngineError):
    """Raised when a profile fails structural or schema validation."""

    def __init__(self, message: str, profile_id: str | None = None):
        if profile_id:
            super().__init__(f"Profile validation failed [{profile_id}]: {message}")
        else:
            super().__init__(f"Profile validation failed: {message}")
        self.profile_id = profile_id
        self.details = message


class EvaluationError(PolicyEngineError):
    """
    Generic evaluation-level error.

    Kept for backward compatibility with older code that imports
    `EvaluationError` from policyengine.exceptions and/or raises it
    from core evaluation logic.
    """

    def __init__(self, message: str):
        super().__init__(f"Evaluation error: {message}")
        self.details = message


class RuleEvaluationError(PolicyEngineError):
    """Raised when a rule fails to evaluate."""

    def __init__(self, rule_id: str, message: str):
        super().__init__(f"Rule '{rule_id}' evaluation error: {message}")
        self.rule_id = rule_id
        self.details = message
