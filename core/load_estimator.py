# ============================================================
# Load estimation module
# Support rough estimation of P_core
# ============================================================

from core.defaults import DEFAULTS


def estimate_p_core_from_equipment(
    equipment_count,
    rated_power_per_unit,
    utilization_factor=0.7,
):
    """
    Estimate core load from equipment count.

    P_core = N * P_rated * utilization
    """

    if equipment_count <= 0 or rated_power_per_unit <= 0:
        return None

    return equipment_count * rated_power_per_unit * utilization_factor


def estimate_p_core_from_total_energy(
    total_energy_kwh,
    hours,
    assumed_pue=1.6,
):
    """
    Estimate core load from total energy consumption.

    P_total = energy / hours
    P_core = P_total / PUE
    """

    if total_energy_kwh <= 0 or hours <= 0:
        return None

    p_total = total_energy_kwh / hours
    p_core = p_total / assumed_pue

    return p_core


def estimate_p_core_from_total_cost(
    total_cost,
    price,
    hours,
    assumed_pue=1.6,
):
    """
    Estimate core load from total electricity cost.

    energy = cost / price
    then reuse energy-based estimation
    """

    if total_cost <= 0 or price <= 0:
        return None

    total_energy = total_cost / price

    return estimate_p_core_from_total_energy(
        total_energy_kwh=total_energy,
        hours=hours,
        assumed_pue=assumed_pue,
    )


def auto_estimate_p_core(
    mode,
    direct_input=None,
    equipment_count=None,
    rated_power=None,
    utilization_factor=0.7,
    total_energy=None,
    total_cost=None,
    price=None,
    hours=None,
    assumed_pue=1.6,
):
    """
    Unified interface:
    mode = "direct" | "equipment" | "energy" | "cost"
    """

    if mode == "direct":
        return direct_input

    if mode == "equipment":
        return estimate_p_core_from_equipment(
            equipment_count,
            rated_power,
            utilization_factor,
        )

    if mode == "energy":
        return estimate_p_core_from_total_energy(
            total_energy,
            hours,
            assumed_pue,
        )

    if mode == "cost":
        return estimate_p_core_from_total_cost(
            total_cost,
            price,
            hours,
            assumed_pue,
        )

    return None