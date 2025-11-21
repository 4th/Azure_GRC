import logging
import azure.functions as func

from functions.shared.clients import (
    get_systems_to_monitor,
    plan_monitoring_for_systems,
    run_governance_for_system,
)


def main(mytimer: func.TimerRequest) -> None:
    logging.info("monitoring_timer: trigger fired")

    systems = get_systems_to_monitor()
    if not systems:
        logging.info("monitoring_timer: no systems registered for monitoring")
        return

    plan = plan_monitoring_for_systems(systems)

    for item in plan.get("systems", []):
        if item.get("action") != "run_evaluation":
            continue

        system_id = item["system_id"]
        logging.info("monitoring_timer: running evaluation for %s", system_id)

        run_governance_for_system(
            system_id=system_id,
            use_case=item.get("use_case"),
            system_type=item.get("system_type"),
        )

    logging.info("monitoring_timer: completed")
