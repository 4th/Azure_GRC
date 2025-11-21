# 4th.GRC – Tools Layer

**Directory:** `agents/tools/`  
**Purpose:** External integration layer for all Agentic AI workflows.

The tools layer handles all external I/O—HTTP calls, storage access, LLM clients, logs, Cosmos queries, etc.  
Planners orchestrate logic; tools perform the work.

## Directory Structure
agents/tools/
├── README.md
├── __init__.py
├── policyengine_tool.py
├── evidence_tool.py
├── scoring_tool.py
├── hitl_tool.py
└── utils.py

## Responsibilities
- Execute external operations
- Provide runtime-safe APIs
- Hide complexity from planners
- Support config-driven behavior

## Modules
### policyengine_tool.py
Wrapper for PolicyEngine API.

### evidence_tool.py
Loads evidence from local/cloud/APIs.

### scoring_tool.py
Applies scoring + post-processing.

### hitl_tool.py
Human-in-the-loop (Teams/Jira/etc.).

### utils.py
HTTP helpers, retry logic, secrets, logging, key vault helpers.

