# ============================================================
# Energy and cost calculations
# Support flat price + weighted TOU pricing
# ============================================================

from core.defaults import DEFAULTS
from core.tariff_model import (
    calculate_flat_cost,
    calculate_tou_cost,
    calculate_weighted_average_price,
)


def calculate_energy_and_cost(
    scenario,
    hours,
    price=None,
    use_tou=False,
    tou_structure=None,
):
    """
    Calculate electricity consumption and cost for one scenario.

    Supports:
    - flat price
    - weighted TOU price
    """

    p_total = scenario["p_total"]
    p_cooling = scenario["p_cooling"]

    if use_tou and tou_structure is not None:
        total_result = calculate_tou_cost(
            power=p_total,
            tou_structure=tou_structure,
            scale_hours=hours,
        )

        cooling_result = calculate_tou_cost(
            power=p_cooling,
            tou_structure=tou_structure,
            scale_hours=hours,
        )

        avg_price = total_result["avg_price"]

        result = scenario.copy()
        result.update(
            {
                "hours": hours,
                "price": avg_price,
                "avg_price": avg_price,
                "energy": total_result["energy"],
                "cost": total_result["cost"],
                "cooling_energy": cooling_result["energy"],
                "cooling_cost": cooling_result["cost"],
                "tou_breakdown": total_result["breakdown"],
            }
        )

        return result

    if price is None:
        price = 0

    total_result = calculate_flat_cost(
        power=p_total,
        hours=hours,
        price=price,
    )

    cooling_result = calculate_flat_cost(
        power=p_cooling,
        hours=hours,
        price=price,
    )

    result = scenario.copy()
    result.update(
        {
            "hours": hours,
            "price": price,
            "avg_price": price,
            "energy": total_result["energy"],
            "cost": total_result["cost"],
            "cooling_energy": cooling_result["energy"],
            "cooling_cost": cooling_result["cost"],
            "tou_breakdown": [],
        }
    )

    return result


def compare_costs(
    current,
    target,
    hours,
    price=None,
    use_tou=False,
    tou_structure=None,
):
    """
    Compare energy and cost between current and target scenarios.
    """

    current_cost = calculate_energy_and_cost(
        scenario=current,
        hours=hours,
        price=price,
        use_tou=use_tou,
        tou_structure=tou_structure,
    )

    target_cost = calculate_energy_and_cost(
        scenario=target,
        hours=hours,
        price=price,
        use_tou=use_tou,
        tou_structure=tou_structure,
    )

    energy_saved = current_cost["energy"] - target_cost["energy"]
    cooling_energy_saved = current_cost["cooling_energy"] - target_cost["cooling_energy"]
    cost_saved = current_cost["cost"] - target_cost["cost"]
    cooling_cost_saved = current_cost["cooling_cost"] - target_cost["cooling_cost"]

    return {
        "current": current_cost,
        "target": target_cost,
        "savings": {
            "energy_saved": energy_saved,
            "cooling_energy_saved": cooling_energy_saved,
            "cost_saved": cost_saved,
            "cooling_cost_saved": cooling_cost_saved,
        },
    }


def annualize_savings(
    hourly_power_saved,
    price=None,
    use_tou=False,
    tou_structure=None,
):
    """
    Estimate annual savings based on 24/7 operation.
    """

    annual_hours = DEFAULTS["hours_per_day"] * DEFAULTS["days_per_year"]

    if use_tou and tou_structure is not None:
        avg_price = calculate_weighted_average_price(tou_structure)
    else:
        avg_price = price if price is not None else 0

    annual_energy_saved = hourly_power_saved * annual_hours
    annual_cost_saved = annual_energy_saved * avg_price

    return {
        "annual_hours": annual_hours,
        "annual_energy_saved": annual_energy_saved,
        "annual_cost_saved": annual_cost_saved,
        "avg_price": avg_price,
    }


def calculate_marginal_savings_per_degree(
    cost_saved,
    t_current,
    t_target,
):
    """
    Calculate cost savings per °C.
    """

    temp_delta = abs(t_target - t_current)

    if temp_delta == 0:
        return 0

    return cost_saved / temp_delta