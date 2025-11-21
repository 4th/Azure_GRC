from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RuleRef(BaseModel):
    """Reference to a rule, by id and optional params/weights."""
    id: str
    weight: float = Field(default=1.0, ge=0.0, description="Relative weight for scoring")
    params: Dict[str, Any] = Field(default_factory=dict)


class ProfileMetadata(BaseModel):
    """Metadata block for a profile."""
    title: Optional[str] = None
    description: Optional[str] = None
    standards: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    owners: List[str] = Field(default_factory=list)


class PolicyProfile(BaseModel):
    """
    Profile schema for YAML files under profiles/.

    Minimal, but structured enough for:
    - validation
    - docs/profile index
    - mapping in scripts
    """

    profile_id: str = Field(..., description="Unique profile identifier")
    version: str = Field(..., description="Profile version string")
    name: Optional[str] = None
    metadata: ProfileMetadata = Field(default_factory=ProfileMetadata)
    rules: List[RuleRef] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)
