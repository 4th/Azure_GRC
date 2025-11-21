from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EvalRequest(BaseModel):
    """
    Request model for PolicyEngine evaluation.

    - profile_ref: e.g. "iso_42001-global@1.2.0"
    - context: system-level context (system_id, owner, environment, etc.)
    - evidence: evidence bundle (model cards, logs, configs, etc.)
    """

    profile_ref: str = Field(..., description="Profile reference, e.g. iso_42001-global@1.2.0")
    context: Dict[str, Any] = Field(default_factory=dict)
    evidence: Dict[str, Any] = Field(default_factory=dict)


class Finding(BaseModel):
    """
    Individual governance finding produced by PolicyEngine.
    """

    id: str
    title: str
    severity: str = Field(..., description="e.g. low, medium, high, critical")
    status: str = Field(..., description="e.g. pass, warn, fail")
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)


class Summary(BaseModel):
    """
    Summary block for an evaluation run.
    """

    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score in [0,1]")
    verdict: str = Field(..., description="Overall verdict, e.g. pass, warn, fail")
    finding_count: int
    profile_ref: str
    profile_id: Optional[str] = None


class EvalResponse(BaseModel):
    """
    Response model for PolicyEngine evaluation.

    Shape designed to work with:
    - services/policyengine_svc/main.py
    - scripts/run_agentic_demo.py
    - scripts/generate_scorecard_report.py
    """

    profile_ref: str
    profile_id: Optional[str] = None
    summary: Summary
    findings: List[Finding] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
