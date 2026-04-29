# ============================================================
# Tariff model
# Support flat price, 3-level TOU compatibility, and 5-level TOU
# ============================================================


def calculate_flat_cost(power, hours, price):
    """
    Flat electricity price:
    cost = power * hours * price
    """

    energy = power * hours
    cost = energy * price

    return {
        "energy": energy,
        "cost": cost,
    }


def calculate_weighted_average_price(tou_structure):
    """
    Weighted average electricity price from TOU structure.

    tou_structure example:
    [
        {"name": "critical_peak", "price": 2.0, "hours": 2},
        {"name": "peak", "price": 1.5, "hours": 4},
        {"name": "flat", "price": 1.0, "hours": 8},
        {"name": "valley", "price": 0.5, "hours": 6},
        {"name": "super_valley", "price": 0.3, "hours": 4},
    ]
    """

    total_hours = sum(float(period["hours"]) for period in tou_structure)

    if total_hours <= 0:
        return 0

    weighted_sum = sum(
        float(period["price"]) * float(period["hours"])
        for period in tou_structure
    )

    return weighted_sum / total_hours


def calculate_tou_cost(power, tou_structure, scale_hours=None):
    """
    TOU pricing calculation using weighted average price.

    If scale_hours is provided, the result is scaled to that total operating period.
    If not provided, it uses the sum of TOU period hours directly.
    """

    avg_price = calculate_weighted_average_price(tou_structure)

    if scale_hours is None:
        hours = sum(float(period["hours"]) for period in tou_structure)
    else:
        hours = scale_hours

    energy = power * hours
    cost = energy * avg_price

    breakdown = []

    total_tou_hours = sum(float(period["hours"]) for period in tou_structure)

    for period in tou_structure:
        period_hours = float(period["hours"])
        period_price = float(period["price"])

        if total_tou_hours > 0:
            period_scaled_hours = hours * period_hours / total_tou_hours
        else:
            period_scaled_hours = 0

        period_energy = power * period_scaled_hours
        period_cost = period_energy * period_price

        breakdown.append(
            {
                "name": period["name"],
                "price": period_price,
                "hours": period_hours,
                "scaled_hours": period_scaled_hours,
                "energy": period_energy,
                "cost": period_cost,
            }
        )

    return {
        "energy": energy,
        "cost": cost,
        "avg_price": avg_price,
        "breakdown": breakdown,
    }


def build_5level_tou_structure(
    critical_peak_price,
    critical_peak_hours,
    peak_price,
    peak_hours,
    flat_price,
    flat_hours,
    valley_price,
    valley_hours,
    super_valley_price,
    super_valley_hours,
):
    """
    Build 5-level TOU tariff structure.

    Levels:
    - critical_peak
    - peak
    - flat
    - valley
    - super_valley
    """

    return [
        {
            "name": "critical_peak",
            "price": critical_peak_price,
            "hours": critical_peak_hours,
        },
        {
            "name": "peak",
            "price": peak_price,
            "hours": peak_hours,
        },
        {
            "name": "flat",
            "price": flat_price,
            "hours": flat_hours,
        },
        {
            "name": "valley",
            "price": valley_price,
            "hours": valley_hours,
        },
        {
            "name": "super_valley",
            "price": super_valley_price,
            "hours": super_valley_hours,
        },
    ]


def generate_simple_tou_structure(peak_price, mid_price, off_price):
    """
    Compatibility function for old 3-level TOU version.
    """

    return [
        {"name": "peak", "price": peak_price, "hours": 6},
        {"name": "mid", "price": mid_price, "hours": 10},
        {"name": "off", "price": off_price, "hours": 8},
    ]