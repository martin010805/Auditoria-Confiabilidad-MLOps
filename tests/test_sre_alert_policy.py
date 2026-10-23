from monitoring.sre_alert_policy import classify_psi


def test_no_drift_is_record():
    result = classify_psi({"V1": 0.03, "V2": 0.08})
    assert result.level == "record"


def test_moderate_drift_is_ticket():
    result = classify_psi({"V1": 0.12, "V2": 0.04})
    assert result.level == "ticket"
    assert result.variables == ("V1",)


def test_one_severe_variable_is_ticket_not_page():
    result = classify_psi({"V1": 0.30, "V2": 0.04})
    assert result.level == "ticket"


def test_two_severe_variables_escalate():
    result = classify_psi({"V1": 0.30, "V2": 0.41, "V3": 0.02})
    assert result.level == "alert"
    assert result.variables == ("V1", "V2")


def test_empty_input_is_record():
    assert classify_psi({}).level == "record"


def test_invalid_negative_psi_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        classify_psi({"V1": -0.1})


def test_invalid_nan_psi_is_rejected():
    import math
    import pytest
    with pytest.raises(ValueError):
        classify_psi({"V1": math.nan})
