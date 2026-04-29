# ============================================================
# Risk evaluation model
# ============================================================

from core.defaults import DEFAULTS


def evaluate_temperature_risk(t_set):
    """
    Evaluate risk level based on temperature setpoint.
    """

    if t_set < DEFAULTS["recommended_low_temp"]:
        return "low"

    if DEFAULTS["recommended_low_temp"] <= t_set <= DEFAULTS["recommended_high_temp"]:
        return "normal"

    if t_set < DEFAULTS["high_risk_temp"]:
        return "elevated"

    return "high"


def evaluate_temperature_step_risk(t_current, t_target):
    """
    Risk due to large temperature adjustment.
    """

    delta = abs(t_target - t_current)

    if delta < 2:
        return "low"

    if delta < 4:
        return "medium"

    return "high"


def evaluate_monitoring_risk(has_local_monitoring):
    """
    Risk due to lack of monitoring.
    """

    return "low" if has_local_monitoring else "high"


def evaluate_pue_risk(current_pue, target_pue):
    """
    Risk if PUE becomes worse.
    """

    if target_pue <= current_pue:
        return "low"

    return "high"


def aggregate_risk_levels(
    temp_risk,
    step_risk,
    monitoring_risk,
    pue_risk,
):
    """
    Aggregate multiple risk dimensions.
    """

    risk_map = {
        "low": 1,
        "normal": 2,
        "medium": 2,
        "elevated": 3,
        "high": 4,
    }

    scores = [
        risk_map.get(temp_risk, 2),
        risk_map.get(step_risk, 2),
        risk_map.get(monitoring_risk, 2),
        risk_map.get(pue_risk, 2),
    ]

    max_score = max(scores)

    if max_score <= 1:
        return "low"

    if max_score == 2:
        return "normal"

    if max_score == 3:
        return "elevated"

    return "high"


def evaluate_overall_risk(
    t_current,
    t_target,
    current_pue,
    target_pue,
    has_local_monitoring,
):
    """
    Full risk evaluation.
    """

    temp_risk = evaluate_temperature_risk(t_target)
    step_risk = evaluate_temperature_step_risk(t_current, t_target)
    monitoring_risk = evaluate_monitoring_risk(has_local_monitoring)
    pue_risk = evaluate_pue_risk(current_pue, target_pue)

    overall = aggregate_risk_levels(
        temp_risk,
        step_risk,
        monitoring_risk,
        pue_risk,
    )

    return {
        "temperature_risk": temp_risk,
        "step_risk": step_risk,
        "monitoring_risk": monitoring_risk,
        "pue_risk": pue_risk,
        "overall_risk": overall,
    }