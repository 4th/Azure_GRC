from policyengine.rules_engine import evaluate_rule


def test_bias_rule_basic_behavior():
    context = {"system_name": "Some System"}
    evidence = {}
    params = {"severity": "critical", "title": "Bias risk check"}

    finding = evaluate_rule(
        rule_id="bias_risk_check",
        params=params,
        context=context,
        evidence=evidence,
    )

    assert finding is not None
    assert finding.id == "bias_risk_check"
    assert finding.severity == "critical"
    # For non-demo systems, our placeholder logic returns 'warn'
    assert finding.status in ("warn", "pass")
