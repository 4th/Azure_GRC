from policyengine.rules_engine import evaluate_rule


def test_transparency_rule_uses_title_and_params():
    context = {"system_name": "Demo LLM System"}
    evidence = {}
    params = {"severity": "high", "title": "Transparency docs present"}

    finding = evaluate_rule(
        rule_id="transparency_docs",
        params=params,
        context=context,
        evidence=evidence,
    )

    assert finding is not None
    assert finding.title == "Transparency docs present"
    assert finding.severity == "high"
    assert "system" in finding.data
    assert finding.data["params"]["severity"] == "high"
