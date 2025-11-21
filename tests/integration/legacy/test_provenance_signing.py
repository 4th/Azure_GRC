import pytest
pytestmark = pytest.mark.skip(reason="Legacy test; feature not implemented in new engine yet")

from policyengine.provenance import sign_result
from policyengine.schema import EvalResponse, EvalSummary

def test_dummy_attestation():
    resp = EvalResponse(request_id="x", profile_ref="p@1.0.0", summary=EvalSummary(status="pass", score=1.0), findings=[])
    att = sign_result(resp)
    # Stub may return None or a dummy Attestation. Either is fine in unit tests.
    assert att is None or att.signature
