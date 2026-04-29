# ============================================================
# Formatting helpers
# ============================================================

def fmt_kw(value):
    return f"{value:,.2f} kW"


def fmt_kwh(value):
    return f"{value:,.0f} kWh"


def fmt_money(value, currency="¥"):
    return f"{currency}{value:,.0f}"


def fmt_percent(value):
    return f"{value * 100:.1f}%"


def fmt_pue(value):
    return f"{value:.3f}"


def fmt_temp(value):
    return f"{value:.1f} °C"