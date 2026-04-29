# ============================================================
# Recommendation logic
# ============================================================

from core.defaults import DEFAULTS


def get_temperature_level(t_target):
    """
    Classify target temperature level.
    """

    if t_target < DEFAULTS["recommended_low_temp"]:
        return "conservative"

    if DEFAULTS["recommended_low_temp"] <= t_target <= DEFAULTS["recommended_high_temp"]:
        return "recommended"

    if DEFAULTS["recommended_high_temp"] < t_target < DEFAULTS["high_risk_temp"]:
        return "aggressive"

    return "high_risk"


def get_savings_level(annual_cost_saved):
    """
    Classify annual savings level.
    """

    if annual_cost_saved <= 0:
        return "none"

    if annual_cost_saved < 10000:
        return "low"

    if annual_cost_saved < 100000:
        return "medium"

    return "high"


def get_pue_level(pue):
    """
    Simple PUE level classification.
    """

    if pue < 1.30:
        return "excellent"

    if pue < 1.60:
        return "good"

    if pue < 2.00:
        return "normal"

    return "high"


def generate_recommendation_keys(
    t_current,
    t_target,
    current_pue,
    target_pue,
    annual_cost_saved,
    has_local_monitoring,
):
    """
    Generate recommendation keys.
    Actual Chinese/English text should be handled in report.py or i18n.py.
    """

    temp_level = get_temperature_level(t_target)
    savings_level = get_savings_level(annual_cost_saved)
    current_pue_level = get_pue_level(current_pue)
    target_pue_level = get_pue_level(target_pue)

    keys = {
        "temperature_level": temp_level,
        "savings_level": savings_level,
        "current_pue_level": current_pue_level,
        "target_pue_level": target_pue_level,
        "economic_keys": [],
        "decision_keys": [],
        "risk_keys": [],
    }

    if annual_cost_saved > 0:
        keys["economic_keys"].append("positive_savings")
    else:
        keys["economic_keys"].append("no_positive_savings")

    if savings_level == "high":
        keys["economic_keys"].append("high_savings")
    elif savings_level == "medium":
        keys["economic_keys"].append("medium_savings")
    elif savings_level == "low":
        keys["economic_keys"].append("low_savings")

    if t_target > t_current:
        keys["decision_keys"].append("raise_temperature")
    elif t_target < t_current:
        keys["decision_keys"].append("lower_temperature")
    else:
        keys["decision_keys"].append("keep_temperature")

    if temp_level == "recommended":
        keys["decision_keys"].append("target_in_recommended_range")
    elif temp_level == "conservative":
        keys["decision_keys"].append("target_too_conservative")
    elif temp_level == "aggressive":
        keys["decision_keys"].append("target_aggressive")
    else:
        keys["decision_keys"].append("target_high_risk")

    if not has_local_monitoring:
        keys["risk_keys"].append("lack_local_monitoring")

    if temp_level in ["aggressive", "high_risk"]:
        keys["risk_keys"].append("hotspot_risk")

    if t_target - t_current >= 4:
        keys["risk_keys"].append("large_temperature_step")

    if target_pue > current_pue:
        keys["risk_keys"].append("pue_worse")

    return keys