from typing import Any, Dict

from agents.planners.utils import SystemContext, resolve_profile_for_system, get_settings
from agents.planners.evaluate_flow import plan_and_run  # once you add it


def run_governance_for_event(
    system_id: str,
    use_case: str | None = None,
    system_type: str | None = None,
    profile_ref: str | None = None,
    extra_context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Shared helper used by multiple functions (model deploy, schema change, webhook).
    """

    # You can either call into evaluate_flow.plan_and_run directly…
    result = plan_and_run(
        system_id=system_id,
        use_case=use_case,
        system_type=system_type,
        profile_ref=profile_ref,
        extra_context=extra_context or {},
    )
    return result
