from fastapi import FastAPI, HTTPException

from policyengine.models import EvalRequest, EvalResponse
from policyengine.core import evaluate

app = FastAPI(
    title="4th.GRC PolicyEngine Service",
    version="0.1.0",
    description="Runs policy-as-code evaluations for governance profiles.",
)


@app.post("/v1/evaluate", response_model=EvalResponse)
async def evaluate_endpoint(req: EvalRequest):
    try:
        result = evaluate(
            profile_ref=req.profile_ref,
            context=req.context,
            evidence=req.evidence,
        )
        return EvalResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
