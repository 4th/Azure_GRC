# monitoring_timer Function

**Trigger:** Timer (CRON)  
**Purpose:** Periodically run governance evaluations for systems that require re-checks.

## Behavior

1. Load list of systems to monitor (from config or Cosmos).
2. Call `continuous_monitoring.plan_monitoring(...)`.
3. For each system with `action = "run_evaluation"`, call the main evaluation planner.
4. Store or log results for Scorecard / reporting.

## Configuration

- Schedule is defined in `function.json`.
- Uses shared helpers from `functions/shared/clients.py`.
- Reads monitoring thresholds from `agents/configs/settings.yaml` (e.g. `monitoring.max_age_days`).
