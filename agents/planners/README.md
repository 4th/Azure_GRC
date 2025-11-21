# 4th.GRC – Planners Layer

**Directory:** `agents/planners/`  
**Purpose:** Orchestration logic for all Agentic AI governance workflows.

Planners coordinate the *flow* of an evaluation, remediation, or monitoring cycle.  
They decide **what happens, when it happens, and which configurations or tools to use**.

Planners **do not** directly perform I/O, database calls, API requests, or UI rendering.

---

## 📁 Directory Structure

```text
agents/planners/
├── README.md
├── __init__.py
├── evaluate_flow.py          # Main end-to-end governance evaluation planner
├── remediation_flow.py       # Builds remediation tasks from evaluation results
├── continuous_monitoring.py  # Decides when to re-run evaluations
└── utils.py                  # Shared helpers across planners
🔑 Responsibilities of Planners
Planners are the orchestration layer of 4th.GRC. They:

✔ Load configuration
From agents.configs:

settings.yaml

agent_profiles.yaml

policy_mappings.yaml

✔ Resolve the correct profile
Selects the policy profile for the given:

System

Use case

System type

Business domain

✔ Sequence governance operations
Common steps include:

Determine the correct profile

Discover or load evidence

Run the PolicyEngine evaluation

Parse findings

Produce structured results

Pass results to remediation or monitoring workflows

✔ Produce standardized output
Including:

Verdict

Findings

Evaluation summary

Required remediation

Monitoring recommendations

Timestamps & metadata

✔ Trigger secondary workflows
Such as:

Remediation execution

Human-in-the-loop escalation

Monitoring schedule updates

📄 Files
evaluate_flow.py
The main orchestrator for a governance run.

Coordinates:

Config loading

Profile resolution

Evidence discovery

PolicyEngine execution

Return a cohesive evaluation object

Example:

python
Copy code
from agents.planners.evaluate_flow import plan_and_run

result = plan_and_run(
    system_id="my-llm-agent",
    use_case="llm_agent_general",
    system_type="realtime_api",
)
remediation_flow.py
Builds a structured remediation plan based on evaluation findings.

Groups findings by severity

Applies HITL policies

Prioritizes critical issues

Outputs clear remediation steps

Example:

python
Copy code
from agents.planners.remediation_flow import plan_remediation
plan = plan_remediation(evaluation_result)
continuous_monitoring.py
Determines when systems should be re-evaluated.

Uses thresholds in settings.yaml, e.g.:

yaml
Copy code
monitoring:
  max_age_days: 7
  rerun_on_verdict:
    - fail
  rerun_on_warn: true
Example:

python
Copy code
from agents.planners.continuous_monitoring import plan_monitoring

plan = plan_monitoring(
    systems=my_list,
    get_last_evaluation=my_cosmos_lookup_fn,
)
Outputs:

"run_evaluation"

"skip"

With full metadata and reasoning.

utils.py
Provides helper utilities such as:

Loading settings and policy mappings

Normalizing severities and verdicts

Profile resolution via SystemContext

ISO-8601 time utilities

Summarizing evaluation objects

These utilities keep planner code small and clear.

