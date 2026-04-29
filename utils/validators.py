# ============================================================
# Input validation helpers
# ============================================================

def validate_positive(value, name):
    if value <= 0:
        return False, f"{name} must be greater than 0."
    return True, ""


def validate_temperature(t_current, t_target):
    if t_current < 0 or t_target < 0:
        return False, "Temperature should not be below 0 °C."

    if t_current > 50 or t_target > 50:
        return False, "Temperature seems too high. Please check the input."

    return True, ""


def validate_inputs(p_core, t_current, t_target, price, hours):
    checks = [
        validate_positive(p_core, "Core load power"),
        validate_positive(price, "Electricity price"),
        validate_positive(hours, "Operating hours"),
        validate_temperature(t_current, t_target),
    ]

    for ok, message in checks:
        if not ok:
            return False, message

    return True, ""