# ============================================================
# Weather & ambient temperature model
# Used to adjust cooling efficiency (COP)
# ============================================================


def adjust_cop_with_outdoor_temp(
    base_cop,
    t_set,
    t_outdoor,
    t_ref=24.0,
    outdoor_ref=30.0,
    indoor_sensitivity=0.1,
    outdoor_sensitivity=0.05,
):
    """
    COP adjustment considering indoor setpoint and outdoor temperature.
    """

    cop = (
        base_cop
        + indoor_sensitivity * (t_set - t_ref)
        - outdoor_sensitivity * (t_outdoor - outdoor_ref)
    )

    return max(cop, 1.0)


def seasonal_outdoor_temp(season):
    """
    Rough seasonal outdoor temperature (for demo use)
    """

    season_map = {
        "winter": 5.0,
        "spring": 18.0,
        "summer": 32.0,
        "autumn": 20.0,
    }

    return season_map.get(season, 30.0)


def adjust_cop_with_season(
    base_cop,
    t_set,
    season,
    t_ref=24.0,
    indoor_sensitivity=0.1,
    outdoor_sensitivity=0.05,
):
    """
    COP adjustment using seasonal approximation
    """

    t_outdoor = seasonal_outdoor_temp(season)

    return adjust_cop_with_outdoor_temp(
        base_cop=base_cop,
        t_set=t_set,
        t_outdoor=t_outdoor,
        t_ref=t_ref,
        indoor_sensitivity=indoor_sensitivity,
        outdoor_sensitivity=outdoor_sensitivity,
    )


def generate_monthly_outdoor_profile():
    """
    Simplified monthly outdoor temperature profile
    """

    return {
        1: 5,
        2: 6,
        3: 10,
        4: 16,
        5: 22,
        6: 27,
        7: 32,
        8: 33,
        9: 28,
        10: 20,
        11: 12,
        12: 6,
    }


def adjust_cop_with_month(
    base_cop,
    t_set,
    month,
    t_ref=24.0,
    indoor_sensitivity=0.1,
    outdoor_sensitivity=0.05,
):
    """
    COP adjustment using monthly temperature
    """

    monthly_profile = generate_monthly_outdoor_profile()
    t_outdoor = monthly_profile.get(month, 30)

    return adjust_cop_with_outdoor_temp(
        base_cop=base_cop,
        t_set=t_set,
        t_outdoor=t_outdoor,
        t_ref=t_ref,
        indoor_sensitivity=indoor_sensitivity,
        outdoor_sensitivity=outdoor_sensitivity,
    )