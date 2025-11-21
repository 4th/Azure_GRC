from policyengine.rules_engine import evaluate_rule


def test_fairness_rule_passes_for_demo_system():
    context = {"system_name": "Demo LLM System"}
    evidence = {}
    params = {"severity": "low", "title": "Fairness demo rule"}

    finding = evaluate_rule(
        rule_id="fairness_demo_rule",
        params=params,
        context=context,
        evidence=evidence,
    )

    assert finding is not None
    assert finding.id == "fairness_demo_rule"
    assert finding.status == "pass"
    assert finding.severity == "low"


def test_fairness_rule_warns_for_non_demo_system():
    context = {"system_name": "Prod LLM System"}
    evidence = {}
    params = {"severity": "medium", "title": "Fairness demo rule"}

    finding = evaluate_rule(
        rule_id="fairness_demo_rule",
        params=params,
        context=context,
        evidence=evidence,
    )

    assert finding is not None
    assert finding.status == "warn"
    assert finding.severity == "medium"
