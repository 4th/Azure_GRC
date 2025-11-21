import logging
import json
import azure.functions as func
import requests
import os

POLICYENGINE_URL = os.getenv("POLICYENGINE_URL")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("policy_eval_webhook triggered.")

    try:
        body = req.get_json()
    except:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON payload"}),
            status_code=400
        )

    # Validate required fields
    required = ["system_id", "profile_ref", "input"]
    missing = [r for r in required if r not in body]

    if missing:
        return func.HttpResponse(
            json.dumps({"error": f"Missing fields: {missing}"}),
            status_code=400
        )

    # Forward to PolicyEngine
    resp = requests.post(
        f"{POLICYENGINE_URL}/evaluate",
        json=body,
        timeout=30
    )

    return func.HttpResponse(resp.text, status_code=resp.status_code)
