# ============================================================
# Thermal model (UPGRADED)
# Integrated with weather model (COP correction)
# ============================================================

from core.defaults import DEFAULTS
from core.weather_model import (
    adjust_cop_with_outdoor_temp,
    adjust_cop_with_season,
    adjust_cop_with_month,
)


# ============================================================
# Basic model（保持原逻辑）
# ============================================================

def calculate_basic_model(
    p_core,
    t_set,
    aux_ratio=None,
    t_ref=None,
    k_ref=None,
    cooling_sensitivity=None,
):
    if aux_ratio is None:
        aux_ratio = DEFAULTS["aux_ratio"]

    if t_ref is None:
        t_ref = DEFAULTS["t_ref"]

    if k_ref is None:
        k_ref = DEFAULTS["k_ref"]

    if cooling_sensitivity is None:
        cooling_sensitivity = DEFAULTS["cooling_sensitivity"]

    cooling_ratio = k_ref + cooling_sensitivity * (t_ref - t_set)
    cooling_ratio = max(cooling_ratio, 0.05)

    p_cooling = p_core * cooling_ratio
    p_aux = p_core * aux_ratio
    p_total = p_core + p_cooling + p_aux
    pue = p_total / p_core

    return {
        "p_core": p_core,
        "t_set": t_set,
        "p_cooling": p_cooling,
        "p_aux": p_aux,
        "p_total": p_total,
        "pue": pue,
        "cooling_ratio": cooling_ratio,
    }


# ============================================================
# Baseline PUE model（保持原逻辑）
# ============================================================

def calculate_baseline_pue_model(
    p_core,
    t_current,
    t_target,
    pue_base,
    aux_ratio=None,
    cooling_sensitivity=None,
):
    if aux_ratio is None:
        aux_ratio = DEFAULTS["aux_ratio"]

    if cooling_sensitivity is None:
        cooling_sensitivity = DEFAULTS["cooling_sensitivity"]

    p_total_base = pue_base * p_core
    p_noncore_base = p_total_base - p_core
    p_aux = p_core * aux_ratio
    p_cooling_base = max(p_noncore_base - p_aux, 0)

    delta = t_target - t_current
    factor = 1 - cooling_sensitivity * delta
    factor = max(factor, 0.2)

    p_cooling = p_cooling_base * factor
    p_total = p_core + p_aux + p_cooling
    pue = p_total / p_core

    return {
        "p_core": p_core,
        "t_set": t_target,
        "p_cooling": p_cooling,
        "p_aux": p_aux,
        "p_total": p_total,
        "pue": pue,
        "cooling_ratio": p_cooling / p_core,
    }


# ============================================================
# COP model（🔥升级：支持气温修正）
# ============================================================

def calculate_cop_model(
    p_core,
    t_set,
    aux_ratio=None,
    t_ref=None,
    cop_ref=None,
    cop_sensitivity=None,
    heat_load_factor=None,

    # NEW ↓↓↓
    use_weather=False,
    weather_mode="none",   # none / outdoor / season / month
    t_outdoor=None,
    season=None,
    month=None,
):
    if aux_ratio is None:
        aux_ratio = DEFAULTS["aux_ratio"]

    if t_ref is None:
        t_ref = DEFAULTS["t_ref"]

    if cop_ref is None:
        cop_ref = DEFAULTS["cop_ref"]

    if cop_sensitivity is None:
        cop_sensitivity = DEFAULTS["cop_sensitivity"]

    if heat_load_factor is None:
        heat_load_factor = DEFAULTS["heat_load_factor"]

    # ===============================
    # Base COP
    # ===============================
    cop = cop_ref + cop_sensitivity * (t_set - t_ref)

    # ===============================
    # Weather correction
    # ===============================
    if use_weather:

        if weather_mode == "outdoor" and t_outdoor is not None:
            cop = adjust_cop_with_outdoor_temp(
                base_cop=cop,
                t_set=t_set,
                t_outdoor=t_outdoor,
            )

        elif weather_mode == "season" and season is not None:
            cop = adjust_cop_with_season(
                base_cop=cop,
                t_set=t_set,
                season=season,
            )

        elif weather_mode == "month" and month is not None:
            cop = adjust_cop_with_month(
                base_cop=cop,
                t_set=t_set,
                month=month,
            )

    cop = max(cop, 1.0)

    # ===============================
    # Cooling calculation
    # ===============================
    q_cooling = heat_load_factor * p_core
    p_cooling = q_cooling / cop
    p_aux = p_core * aux_ratio
    p_total = p_core + p_cooling + p_aux
    pue = p_total / p_core

    return {
        "p_core": p_core,
        "t_set": t_set,
        "cop": cop,
        "p_cooling": p_cooling,
        "p_aux": p_aux,
        "p_total": p_total,
        "pue": pue,
        "cooling_ratio": p_cooling / p_core,
    }


# ============================================================
# Unified interface（升级）
# ============================================================

def calculate_scenario(
    mode,
    p_core,
    t_set,
    t_current=None,
    pue_base=None,
    aux_ratio=None,
    t_ref=None,
    k_ref=None,
    cooling_sensitivity=None,
    cop_ref=None,
    cop_sensitivity=None,
    heat_load_factor=None,

    # NEW ↓↓↓
    use_weather=False,
    weather_mode="none",
    t_outdoor=None,
    season=None,
    month=None,
):
    if mode == "basic":
        return calculate_basic_model(
            p_core,
            t_set,
            aux_ratio,
            t_ref,
            k_ref,
            cooling_sensitivity,
        )

    if mode == "baseline_pue":
        return calculate_baseline_pue_model(
            p_core,
            t_current,
            t_set,
            pue_base,
            aux_ratio,
            cooling_sensitivity,
        )

    if mode == "cop":
        return calculate_cop_model(
            p_core,
            t_set,
            aux_ratio,
            t_ref,
            cop_ref,
            cop_sensitivity,
            heat_load_factor,

            # NEW
            use_weather,
            weather_mode,
            t_outdoor,
            season,
            month,
        )

    raise ValueError("Unknown mode")


# ============================================================
# Compare（升级支持天气）
# ============================================================

def compare_current_and_target(
    mode,
    p_core,
    t_current,
    t_target,
    **kwargs
):
    current = calculate_scenario(
        mode=mode,
        p_core=p_core,
        t_set=t_current,
        t_current=t_current,
        **kwargs
    )

    target = calculate_scenario(
        mode=mode,
        p_core=p_core,
        t_set=t_target,
        t_current=t_current,
        **kwargs
    )

    return {
        "current": current,
        "target": target,
        "diff": {
            "total_power_saved": current["p_total"] - target["p_total"],
        },
    }


# ============================================================
# Curve（升级支持天气）
# ============================================================

def generate_temperature_curve(
    mode,
    p_core,
    temp_min,
    temp_max,
    **kwargs
):
    results = []

    for t in range(int(temp_min), int(temp_max) + 1):
        r = calculate_scenario(
            mode=mode,
            p_core=p_core,
            t_set=t,
            **kwargs
        )
        results.append(r)

    return results