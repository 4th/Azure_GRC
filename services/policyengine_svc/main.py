# C:\4th\4th.GRC\services\policyengine_svc\main.py

from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from policyengine import evaluate
from policyengine.models import EvalRequest, EvalResponse
from policyengine.exceptions import ProfileNotFoundError, ProfileValidationError

SERVICE_NAME = "4th.GRC PolicyEngine Service"
SERVICE_VERSION = "0.1.0"

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description="FastAPI microservice exposing the PolicyEngine evaluation API.",
)

# CORS – you can tighten this later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict[str, Any]:
    """Root metadata endpoint."""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
    }


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    """Simple health check endpoint used by tests and infra."""
    return {"status": "ok"}


@app.post("/v1/evaluate", response_model=EvalResponse)
def evaluate_endpoint(request: EvalRequest) -> EvalResponse:
    """
    Main evaluation endpoint.

    It delegates to policyengine.evaluate(profile_ref, context, evidence)
    and returns the standardized EvalResponse model.
    """
    try:
        result = evaluate(
            profile_ref=request.profile_ref,
            context=request.context,
            evidence=request.evidence,
        )
    except ProfileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ProfileValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        # You can log the exception here with your logging helper
        raise HTTPException(status_code=500, detail="Internal evaluation error") from exc

    # If `evaluate` already returns an EvalResponse-compatible dict/model,
    # we can just return it directly.
    if isinstance(result, EvalResponse):
        return result

    # Otherwise assume it's a dict compatible with EvalResponse
    return EvalResponse.model_validate(result)
