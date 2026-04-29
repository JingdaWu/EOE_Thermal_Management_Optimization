# ============================================================
# Plotly charts for Thermal Management Demo
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.cost_model import calculate_energy_and_cost


# ============================================================
# Shared Plotly style
# ============================================================

def apply_dark_plot_style(fig):
    """
    Apply visual style consistent with the Streamlit app.
    This version avoids deprecated/incompatible axis properties.
    """

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(14,17,23,0)",
        plot_bgcolor="rgba(255,255,255,0.025)",
        font=dict(
            color="#EAF8FF",
            size=13,
        ),
        title=dict(
            font=dict(
                color="#F7FBFF",
                size=18,
            )
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.10)",
            borderwidth=0,
            font=dict(color="#EAF8FF"),
        ),
        margin=dict(l=30, r=30, t=60, b=30),
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.10)",
        zerolinecolor="rgba(255,255,255,0.16)",
        linecolor="rgba(255,255,255,0.22)",
        tickfont=dict(color="#EAF8FF"),
        title_font=dict(color="#EAF8FF"),
        showline=True,
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.10)",
        zerolinecolor="rgba(255,255,255,0.16)",
        linecolor="rgba(255,255,255,0.22)",
        tickfont=dict(color="#EAF8FF"),
        title_font=dict(color="#EAF8FF"),
        showline=True,
    )

    return fig


# ============================================================
# Temperature - PUE curve
# ============================================================

def create_temperature_pue_curve(curve_data, text):
    """
    Temperature - PUE curve.
    """

    df = pd.DataFrame(curve_data)

    fig = px.line(
        df,
        x="t_set",
        y="pue",
        markers=True,
        labels={
            "t_set": text["temperature"],
            "pue": text["estimated_pue"],
        },
        title=text["chart_temp_pue"],
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
    )

    fig.update_layout(
        height=420,
        legend_title_text="",
    )

    return apply_dark_plot_style(fig)


# ============================================================
# Temperature - cost curve
# ============================================================

def create_temperature_cost_curve(
    curve_data,
    hours,
    text,
    price=None,
    use_tou=False,
    tou_structure=None,
):
    """
    Temperature - cost curve.
    """

    rows = []

    for item in curve_data:
        cost_item = calculate_energy_and_cost(
            scenario=item,
            hours=hours,
            price=price,
            use_tou=use_tou,
            tou_structure=tou_structure,
        )
        rows.append(
            {
                "t_set": item["t_set"],
                "cost": cost_item["cost"],
            }
        )

    df = pd.DataFrame(rows)

    fig = px.line(
        df,
        x="t_set",
        y="cost",
        markers=True,
        labels={
            "t_set": text["temperature"],
            "cost": text["estimated_cost"],
        },
        title=text["chart_temp_cost"],
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
    )

    fig.update_layout(
        height=420,
        legend_title_text="",
    )

    return apply_dark_plot_style(fig)


# ============================================================
# Current vs target power breakdown
# ============================================================

def create_power_breakdown_chart(current, target, text):
    """
    Current vs target power breakdown.
    """

    df = pd.DataFrame(
        {
            "Scenario": [
                text["current_scenario"],
                text["current_scenario"],
                text["current_scenario"],
                text["target_scenario"],
                text["target_scenario"],
                text["target_scenario"],
            ],
            "Type": [
                text["core_load"],
                text["cooling_load"],
                text["aux_load"],
                text["core_load"],
                text["cooling_load"],
                text["aux_load"],
            ],
            "Power": [
                current["p_core"],
                current["p_cooling"],
                current["p_aux"],
                target["p_core"],
                target["p_cooling"],
                target["p_aux"],
            ],
        }
    )

    fig = px.bar(
        df,
        x="Scenario",
        y="Power",
        color="Type",
        barmode="stack",
        labels={
            "Scenario": "",
            "Power": text["power_kw"],
            "Type": "",
        },
        title=text["chart_power_compare"],
    )

    fig.update_layout(
        height=420,
        legend_title_text="",
    )

    return apply_dark_plot_style(fig)


# ============================================================
# Savings comparison chart
# ============================================================

def create_savings_chart(savings, annual_savings, text):
    """
    Savings comparison chart.
    """

    df = pd.DataFrame(
        {
            "Metric": [
                text["energy_saved"],
                text["annual_energy_saved"],
                text["cost_saved"],
                text["annual_cost_saved"],
            ],
            "Value": [
                savings["energy_saved"],
                annual_savings["annual_energy_saved"],
                savings["cost_saved"],
                annual_savings["annual_cost_saved"],
            ],
        }
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Metric"],
            y=df["Value"],
            text=[f"{v:,.0f}" for v in df["Value"]],
            textposition="auto",
        )
    )

    fig.update_layout(
        title=text["chart_savings"],
        height=420,
        xaxis_title="",
        yaxis_title="",
    )

    return apply_dark_plot_style(fig)