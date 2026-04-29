from __future__ import annotations

import streamlit as st

from core.defaults import DEFAULTS
from core.thermal_model import (
    compare_current_and_target,
    generate_temperature_curve,
)
from core.cost_model import (
    compare_costs,
    annualize_savings,
    calculate_marginal_savings_per_degree,
)
from core.load_estimator import auto_estimate_p_core
from core.tariff_model import (
    build_5level_tou_structure,
    calculate_weighted_average_price,
)
from core.report import build_report
from utils.i18n import get_text
from utils.validators import validate_inputs
from utils.formatters import (
    fmt_percent,
    fmt_pue,
    fmt_temp,
)
from visualization.plots import (
    create_temperature_pue_curve,
    create_temperature_cost_curve,
    create_power_breakdown_chart,
    create_savings_chart,
)


# ============================================================
# Language state
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "en"


def toggle_language() -> None:
    st.session_state.language = "en" if st.session_state.language == "zh" else "zh"


language = st.session_state.language
T = get_text(language)
is_zh = language == "zh"

st.set_page_config(
    page_title=T["page_title"],
    page_icon="🌡️",
    layout="wide",
)


# ============================================================
# UI style
# ============================================================

st.markdown(
    """
    <style>
    /* ============================================================
       Global color tokens
    ============================================================ */
    :root {
        --bg-main: #0E1117;
        --bg-sidebar: #0E1117;
        --bg-panel: rgba(255,255,255,0.045);
        --bg-panel-soft: rgba(255,255,255,0.030);
        --bg-input: #1A1D24;
        --bg-input-hover: #20242D;
        --bg-input-focus: #222936;
        --bg-popover: #151922;
        --bg-tooltip: #151922;
        --text-main: #F7FBFF;
        --text-soft: #EAF8FF;
        --text-muted: rgba(234,248,255,0.72);
        --text-faint: rgba(234,248,255,0.56);
        --border-soft: rgba(255,255,255,0.12);
        --border-faint: rgba(255,255,255,0.08);
        --border-blue: rgba(0,194,255,0.30);
        --border-blue-strong: rgba(0,194,255,0.62);
        --blue-soft: rgba(0,174,239,0.16);
        --blue-mid: rgba(0,174,239,0.26);
        --shadow-soft: rgba(0,0,0,0.20);
    }

    /* ============================================================
       Main layout
    ============================================================ */
    .block-container {
        padding-top: 2.4rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

        /* ============================================================
       Sidebar
    ============================================================ */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255,255,255,0.10);
        overflow-y: auto;
    }

    [data-testid="stSidebarContent"] {
        overflow-y: auto;
        max-height: 100vh;
        padding-bottom: 2rem;
    }

    /* ============================================================
       General text
    ============================================================ */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-main) !important;
    }

    /* ============================================================
       Number input / text input base
    ============================================================ */
    [data-testid="stNumberInput"],
    [data-testid="stTextInput"] {
        color: var(--text-soft) !important;
    }

    [data-testid="stNumberInput"] label,
    [data-testid="stTextInput"] label {
        color: var(--text-soft) !important;
        font-weight: 600 !important;
    }

    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input {
        background-color: var(--bg-input) !important;
        color: var(--text-main) !important;
        caret-color: var(--text-main) !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stNumberInput"] input::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: var(--text-faint) !important;
    }

    [data-baseweb="input"],
    [data-baseweb="base-input"] {
        background-color: var(--bg-input) !important;
        color: var(--text-main) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    [data-baseweb="input"]:hover,
    [data-baseweb="base-input"]:hover {
        background-color: var(--bg-input-hover) !important;
        border-color: rgba(0,194,255,0.18) !important;
    }

    [data-baseweb="input"]:focus-within,
    [data-baseweb="base-input"]:focus-within {
        background-color: var(--bg-input-focus) !important;
        border-color: rgba(0,194,255,0.28) !important;
        box-shadow: 0 0 0 1px rgba(0,194,255,0.10) !important;
    }

    /* ============================================================
       Number input +/- buttons
    ============================================================ */
    [data-testid="stNumberInput"] button {
        background: #151922 !important;
        color: var(--text-soft) !important;
        border-color: rgba(255,255,255,0.08) !important;
        box-shadow: none !important;
    }

    [data-testid="stNumberInput"] button:hover {
        background: rgba(0,174,239,0.16) !important;
        color: #FFFFFF !important;
        border-color: rgba(0,194,255,0.22) !important;
    }

    [data-testid="stNumberInput"] button:disabled {
        background: rgba(255,255,255,0.035) !important;
        color: rgba(234,248,255,0.30) !important;
        border-color: rgba(255,255,255,0.05) !important;
    }

    [data-testid="stNumberInput"] button svg {
        color: var(--text-soft) !important;
        fill: var(--text-soft) !important;
    }

    [data-testid="stNumberInput"] button:hover svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* ============================================================
       Selectbox
    ============================================================ */
    [data-testid="stSelectbox"] label {
        color: var(--text-soft) !important;
        font-weight: 600 !important;
    }

    [data-baseweb="select"] > div {
        background-color: var(--bg-input) !important;
        color: var(--text-main) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    [data-baseweb="select"] > div:hover {
        background-color: var(--bg-input-hover) !important;
        border-color: rgba(0,194,255,0.18) !important;
    }

    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: var(--text-main) !important;
    }

    [data-baseweb="select"] svg {
        color: var(--text-soft) !important;
        fill: var(--text-soft) !important;
    }

    /* ============================================================
       Popover / dropdown / menu
    ============================================================ */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {
        background: var(--bg-popover) !important;
        color: var(--text-main) !important;
        border: 1px solid rgba(0,194,255,0.22) !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35) !important;
    }

    [role="option"],
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] ul {
        background: var(--bg-popover) !important;
        color: var(--text-main) !important;
    }

    [role="option"] div,
    [role="option"] span {
        color: var(--text-main) !important;
    }

    [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: rgba(0,174,239,0.20) !important;
        color: #FFFFFF !important;
    }

    /* ============================================================
       Help icon
       Keep the question-mark icon visible without overriding tooltip popup.
    ============================================================ */
    [data-testid="stTooltipHoverTarget"] svg,
    [data-testid="stTooltipIcon"] svg {
        color: #00AEEF !important;
        fill: #00AEEF !important;
        opacity: 1 !important;
    }

    [data-testid="stTooltipHoverTarget"] svg path,
    [data-testid="stTooltipIcon"] svg path {
        fill: #00AEEF !important;
        stroke: #00AEEF !important;
    }

    [data-testid="stTooltipHoverTarget"]:hover svg,
    [data-testid="stTooltipIcon"]:hover svg,
    [data-testid="stTooltipHoverTarget"]:hover svg path,
    [data-testid="stTooltipIcon"]:hover svg path {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* ============================================================
       Slider
    ============================================================ */
    [data-testid="stSlider"] label,
    [data-testid="stSlider"] p,
    [data-testid="stSlider"] span,
    [data-testid="stSlider"] div {
        color: var(--text-soft) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background-color: #00C2FF !important;
        border-color: #00C2FF !important;
    }

    /* ============================================================
       Buttons
    ============================================================ */
    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid rgba(0,194,255,0.30) !important;
        background: rgba(0,174,239,0.16) !important;
        color: #F7FBFF !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        border-color: rgba(0,194,255,0.65) !important;
        background: rgba(0,174,239,0.26) !important;
        color: #FFFFFF !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, rgba(0,174,239,0.85), rgba(0,115,180,0.85)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(0,194,255,0.65) !important;
        box-shadow: 0 8px 18px rgba(0,174,239,0.18) !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(135deg, rgba(0,194,255,0.95), rgba(0,130,205,0.95)) !important;
        color: #FFFFFF !important;
    }

    /* ============================================================
       Metric cards
    ============================================================ */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.035) !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 16px !important;
        padding: 14px 14px 10px 14px !important;
        min-height: 104px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.08) !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] span {
        color: rgba(234,248,255,0.78) !important;
        font-size: 14px !important;
        line-height: 1.25 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div,
    [data-testid="stMetricValue"] span {
        color: #F7FBFF !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] div,
    [data-testid="stMetricDelta"] span {
        color: #8BE9FD !important;
    }

    /* ============================================================
       Tabs
    ============================================================ */
    [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent !important;
        border-bottom: none !important;
    }

    [data-baseweb="tab-border"],
    [data-baseweb="tab-highlight"] {
        display: none !important;
        height: 0px !important;
        background: transparent !important;
        border: none !important;
    }

    [data-baseweb="tab"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: var(--text-soft) !important;
        padding: 10px 14px !important;
        min-height: 46px !important;
        box-shadow: none !important;
    }

    [data-baseweb="tab"]::before,
    [data-baseweb="tab"]::after {
        display: none !important;
        background: transparent !important;
        border: none !important;
        height: 0px !important;
    }

    [data-baseweb="tab"] p,
    [data-baseweb="tab"] span,
    [data-baseweb="tab"] div {
        color: var(--text-soft) !important;
        font-weight: 750 !important;
        font-size: 17px !important;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(0,174,239,0.20) !important;
        border-color: rgba(0,194,255,0.35) !important;
        box-shadow: none !important;
    }

    [data-baseweb="tab"][aria-selected="true"] p,
    [data-baseweb="tab"][aria-selected="true"] span,
    [data-baseweb="tab"][aria-selected="true"] div {
        color: #FFFFFF !important;
    }

    [data-baseweb="tab-panel"] {
        background: transparent !important;
        color: var(--text-main) !important;
        padding-top: 12px !important;
    }

    [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"] p,
    [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"] li,
    [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"] span {
        font-size: 17px !important;
        line-height: 1.72 !important;
    }

    [data-baseweb="tab-panel"] h3 {
        font-size: 24px !important;
        margin-bottom: 14px !important;
    }

    /* ============================================================
       Expander
    ============================================================ */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.035) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 16px !important;
        color: var(--text-main) !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {
        background: transparent !important;
        color: var(--text-main) !important;
    }

    [data-testid="stExpander"] summary:hover {
        background: rgba(0,174,239,0.08) !important;
    }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] div,
    [data-testid="stExpander"] span,
    [data-testid="stExpander"] label {
        color: var(--text-main) !important;
    }

    [data-testid="stExpander"] svg {
        color: var(--text-soft) !important;
        fill: var(--text-soft) !important;
    }

    /* ============================================================
       Plotly chart outer containers
    ============================================================ */
    [data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.025) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 6px !important;
    }

    /* ============================================================
       Custom cards from previous EOE demo style
    ============================================================ */
    .hero-card {
        background: linear-gradient(135deg, rgba(0,174,239,0.18), rgba(14,17,23,0.96));
        border: 1px solid rgba(0,194,255,0.28);
        border-radius: 20px;
        padding: 24px 24px 18px 24px;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 6px;
        letter-spacing: 0.2px;
        color: #F7FBFF !important;
    }

    .hero-subtitle {
        font-size: 15px;
        opacity: 0.86;
        line-height: 1.5;
        margin-bottom: 14px;
        color: #EAF8FF !important;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 6px;
    }

    .chip {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        color: #EAF8FF !important;
        background: rgba(0,174,239,0.16);
        border: 1px solid rgba(0,174,239,0.30);
    }

    .section-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 14px 14px 10px 14px;
        margin-top: 10px;
        margin-bottom: 10px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.08);
    }

    .section-title {
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 2px;
        color: #F5FBFF !important;
    }

    .section-desc {
        font-size: 12px;
        opacity: 0.76;
        margin-bottom: 0px;
        color: #EAF8FF !important;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 2px;
        color: #F7FBFF !important;
    }

    .sidebar-subtitle {
        font-size: 12px;
        opacity: 0.74;
        margin-bottom: 10px;
        color: #EAF8FF !important;
    }

    .panel-title {
        font-size: 22px;
        font-weight: 800;
        margin: 4px 0 12px 0;
        color: #F7FBFF !important;
    }

    .panel-subtitle {
        font-size: 13px;
        opacity: 0.74;
        margin-top: -6px;
        margin-bottom: 12px;
        color: #EAF8FF !important;
    }

    .scenario-bar {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 14px;
    }

    .scenario-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
    }

    .scenario-item {
        background: rgba(255,255,255,0.025);
        border-radius: 12px;
        padding: 12px 14px;
        border: 1px solid rgba(255,255,255,0.05);
        min-width: 0;
    }

    .scenario-label {
        font-size: 12.5px;
        opacity: 0.70;
        text-transform: uppercase;
        letter-spacing: 0.35px;
        margin-bottom: 5px;
        color: #EAF8FF !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .scenario-value {
        font-size: 16px;
        line-height: 1.25;
        font-weight: 780;
        color: #F7FBFF !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .summary-card {
        background: linear-gradient(135deg, rgba(0,174,239,0.12), rgba(255,255,255,0.02));
        border: 1px solid rgba(0,174,239,0.20);
        border-radius: 18px;
        padding: 16px 16px 4px 16px;
        margin-bottom: 14px;
    }

    .summary-title {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 10px;
        color: #F7FBFF !important;
    }

    .comparison-title {
        font-size: 18px;
        line-height: 1.25;
        font-weight: 800;
        margin: 4px 0 12px 0;
        color: #F7FBFF !important;
    }

    .small-note {
        font-size: 12px;
        opacity: 0.72;
        margin-top: 4px;
        margin-bottom: 0px;
        color: #EAF8FF !important;
    }

    .empty-state {
        background: rgba(255,255,255,0.02);
        border: 1px dashed rgba(0,194,255,0.25);
        border-radius: 18px;
        padding: 24px 20px;
        margin-top: 10px;
    }

    .empty-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
        color: #F7FBFF !important;
    }

    .empty-body {
        font-size: 14px;
        opacity: 0.80;
        line-height: 1.7;
        color: #EAF8FF !important;
    }

    @media (max-width: 1100px) {
        .scenario-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar helper
# ============================================================

def render_sidebar_section(title: str, desc: str) -> None:
    st.sidebar.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_number(value: float, digits: int = 0) -> str:
    return f"{value:,.{digits}f}"


# ============================================================
# Sidebar header
# ============================================================

top_left, top_right = st.sidebar.columns([4, 1])

with top_left:
    st.markdown(
        f"""
        <div class="sidebar-title">{T['sidebar_title']}</div>
        <div class="sidebar-subtitle">{T['sidebar_desc']}</div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.button(T["language_toggle"], on_click=toggle_language, use_container_width=True)


# ============================================================
# Sidebar - model
# ============================================================

render_sidebar_section(T["section_model"], T["section_model_desc"])

mode_label = st.sidebar.selectbox(
    T["calculation_mode"],
    [
        T["mode_basic"],
        T["mode_baseline_pue"],
        T["mode_cop"],
    ],
    key="calculation_mode_select",
)

if mode_label == T["mode_basic"]:
    mode = "basic"
    st.sidebar.info(T["mode_basic_help"])
elif mode_label == T["mode_baseline_pue"]:
    mode = "baseline_pue"
    st.sidebar.info(T["mode_baseline_pue_help"])
else:
    mode = "cop"
    st.sidebar.info(T["mode_cop_help"])


# ============================================================
# Sidebar - temperature and weather
# ============================================================

render_sidebar_section(T["section_temp_weather"], T["section_temp_weather_desc"])

t_current = st.sidebar.number_input(
    T["t_current"],
    min_value=0.0,
    max_value=50.0,
    value=20.0,
    step=1.0,
    key="t_current",
)

t_target = st.sidebar.number_input(
    T["t_target"],
    min_value=0.0,
    max_value=50.0,
    value=24.0,
    step=1.0,
    key="t_target",
)

t_outdoor = st.sidebar.number_input(
    T["outdoor_temp"],
    min_value=-30.0,
    max_value=60.0,
    value=30.0,
    step=1.0,
    key="outdoor_temp",
)

st.sidebar.info(T["temperature_hint"])


# ============================================================
# Sidebar - load input
# ============================================================

render_sidebar_section(T["section_load"], T["section_load_desc"])

load_mode_label = st.sidebar.selectbox(
    T["load_mode"],
    [
        T["load_direct"],
        T["load_equipment"],
        T["load_energy"],
        T["load_cost"],
    ],
    key="load_mode_select",
)

assumed_pue_for_estimation = st.sidebar.number_input(
    T["assumed_pue"],
    min_value=1.01,
    max_value=5.00,
    value=1.60,
    step=0.01,
    key="assumed_pue_for_estimation",
)

p_core = None

if load_mode_label == T["load_direct"]:
    p_core = st.sidebar.number_input(
        T["p_core"],
        min_value=1.0,
        value=500.0,
        step=10.0,
        help=T["p_core_help"],
        key="p_core_direct",
    )

elif load_mode_label == T["load_equipment"]:
    equipment_count = st.sidebar.number_input(
        T["equipment_count"],
        min_value=1,
        value=100,
        step=1,
        key="equipment_count",
    )
    rated_power = st.sidebar.number_input(
        T["rated_power"],
        min_value=0.1,
        value=5.0,
        step=0.1,
        key="rated_power",
    )
    utilization = st.sidebar.slider(
        T["utilization"],
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.05,
        key="utilization_factor",
    )

    p_core = auto_estimate_p_core(
        mode="equipment",
        equipment_count=equipment_count,
        rated_power=rated_power,
        utilization_factor=utilization,
    )

elif load_mode_label == T["load_energy"]:
    total_energy = st.sidebar.number_input(
        T["total_energy"],
        min_value=1.0,
        value=100000.0,
        step=1000.0,
        key="total_energy_for_estimation",
    )

    estimate_hours = st.sidebar.number_input(
        T["estimate_hours"],
        min_value=1,
        value=720,
        step=1,
        key="estimate_hours_energy",
    )

    p_core = auto_estimate_p_core(
        mode="energy",
        total_energy=total_energy,
        hours=estimate_hours,
        assumed_pue=assumed_pue_for_estimation,
    )

elif load_mode_label == T["load_cost"]:
    total_cost = st.sidebar.number_input(
        T["total_cost"],
        min_value=1.0,
        value=100000.0,
        step=1000.0,
        key="total_cost_for_estimation",
    )

    estimate_hours = st.sidebar.number_input(
        T["estimate_hours"],
        min_value=1,
        value=720,
        step=1,
        key="estimate_hours_cost",
    )

    estimate_price = st.sidebar.number_input(
        T["estimate_price"],
        min_value=0.01,
        value=1.00,
        step=0.01,
        key="estimate_price_cost",
    )

    p_core = auto_estimate_p_core(
        mode="cost",
        total_cost=total_cost,
        price=estimate_price,
        hours=estimate_hours,
        assumed_pue=assumed_pue_for_estimation,
    )


# ============================================================
# Sidebar - tariff and operating period
# ============================================================

render_sidebar_section(T["section_tariff"], T["section_tariff_desc"])

tariff_col1, tariff_col2 = st.sidebar.columns([1, 1])
with tariff_col1:
    critical_peak_price = st.number_input(
        T["critical_peak_price"],
        min_value=0.0,
        value=2.00,
        step=0.01,
        key="critical_peak_price",
    )
with tariff_col2:
    critical_peak_hours = st.number_input(
        T["critical_peak_hours"],
        min_value=0.0,
        value=2.0,
        step=0.5,
        key="critical_peak_hours",
    )

tariff_col3, tariff_col4 = st.sidebar.columns([1, 1])
with tariff_col3:
    peak_price = st.number_input(
        T["peak_price"],
        min_value=0.0,
        value=1.70,
        step=0.01,
        key="peak_price",
    )
with tariff_col4:
    peak_hours = st.number_input(
        T["peak_hours"],
        min_value=0.0,
        value=4.0,
        step=0.5,
        key="peak_hours",
    )

tariff_col5, tariff_col6 = st.sidebar.columns([1, 1])
with tariff_col5:
    flat_price = st.number_input(
        T["flat_price"],
        min_value=0.0,
        value=1.00,
        step=0.01,
        key="flat_price",
    )
with tariff_col6:
    flat_hours = st.number_input(
        T["flat_hours"],
        min_value=0.0,
        value=8.0,
        step=0.5,
        key="flat_hours",
    )

tariff_col7, tariff_col8 = st.sidebar.columns([1, 1])
with tariff_col7:
    valley_price = st.number_input(
        T["valley_price"],
        min_value=0.0,
        value=0.50,
        step=0.01,
        key="valley_price",
    )
with tariff_col8:
    valley_hours = st.number_input(
        T["valley_hours"],
        min_value=0.0,
        value=6.0,
        step=0.5,
        key="valley_hours",
    )

tariff_col9, tariff_col10 = st.sidebar.columns([1, 1])
with tariff_col9:
    super_valley_price = st.number_input(
        T["super_valley_price"],
        min_value=0.0,
        value=0.30,
        step=0.01,
        key="super_valley_price",
    )
with tariff_col10:
    super_valley_hours = st.number_input(
        T["super_valley_hours"],
        min_value=0.0,
        value=4.0,
        step=0.5,
        key="super_valley_hours",
    )

operating_hours = st.sidebar.number_input(
    T["operating_hours"],
    min_value=1,
    value=720,
    step=1,
    key="operating_hours_main",
)

currency = "¥"

tou_structure = build_5level_tou_structure(
    critical_peak_price=critical_peak_price,
    critical_peak_hours=critical_peak_hours,
    peak_price=peak_price,
    peak_hours=peak_hours,
    flat_price=flat_price,
    flat_hours=flat_hours,
    valley_price=valley_price,
    valley_hours=valley_hours,
    super_valley_price=super_valley_price,
    super_valley_hours=super_valley_hours,
)

weighted_avg_price = calculate_weighted_average_price(tou_structure)
tou_hours_sum = (
    critical_peak_hours
    + peak_hours
    + flat_hours
    + valley_hours
    + super_valley_hours
)


# ============================================================
# Sidebar - advanced parameters
# ============================================================

render_sidebar_section(T["section_advanced"], T["section_advanced_desc"])

with st.sidebar.expander(T["advanced_params"], expanded=False):
    aux_ratio = st.number_input(
        T["aux_ratio"],
        min_value=0.00,
        max_value=0.50,
        value=DEFAULTS["aux_ratio"],
        step=0.01,
        help=T["aux_ratio_help"],
        key="aux_ratio",
    )

    t_ref = st.number_input(
        T["t_ref"],
        min_value=10.0,
        max_value=40.0,
        value=DEFAULTS["t_ref"],
        step=1.0,
        key="t_ref",
    )

    k_ref = st.number_input(
        T["k_ref"],
        min_value=0.05,
        max_value=1.00,
        value=DEFAULTS["k_ref"],
        step=0.01,
        key="k_ref",
    )

    cooling_sensitivity = st.number_input(
        T["cooling_sensitivity"],
        min_value=0.00,
        max_value=0.20,
        value=DEFAULTS["cooling_sensitivity"],
        step=0.01,
        help=T["cooling_sensitivity_help"],
        key="cooling_sensitivity",
    )

    pue_base = st.number_input(
        T["pue_base"],
        min_value=1.01,
        max_value=5.00,
        value=1.60,
        step=0.01,
        key="pue_base",
    )

    cop_ref = st.number_input(
        T["cop_ref"],
        min_value=1.00,
        max_value=10.00,
        value=DEFAULTS["cop_ref"],
        step=0.10,
        key="cop_ref",
    )

    cop_sensitivity = st.number_input(
        T["cop_sensitivity"],
        min_value=0.00,
        max_value=1.00,
        value=DEFAULTS["cop_sensitivity"],
        step=0.01,
        key="cop_sensitivity",
    )

    heat_load_factor = st.number_input(
        T["heat_load_factor"],
        min_value=0.50,
        max_value=1.50,
        value=DEFAULTS["heat_load_factor"],
        step=0.05,
        key="heat_load_factor",
    )

    has_local_monitoring = st.checkbox(
        T["has_local_monitoring"],
        value=False,
        key="has_local_monitoring",
    )


# ============================================================
# Sidebar - run button
# ============================================================

st.sidebar.markdown("")
st.sidebar.markdown(
    f"""
    <div class="small-note">{T['run_hint']}</div>
    """,
    unsafe_allow_html=True,
)

run_button = st.sidebar.button(
    T["run_button_new"],
    type="primary",
    use_container_width=True,
    key="run_button",
)


# ============================================================
# Hero area
# ============================================================

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-title">{T['app_name']}</div>
        <div class="hero-subtitle">{T['page_subtitle']}</div>
        <div class="chip-row">
            {''.join([
                f"<span class='chip'>{chip}</span>"
                for chip in [
                    T["chip_thermal_optimization"],
                    T["chip_pue_analysis"],
                    T["chip_tou_tariff"],
                    T["chip_risk_assessment"],
                ]
            ])}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(T["app_caption"])


# ============================================================
# Scenario summary
# ============================================================

scenario_temp_change = f"{fmt_temp(t_current)} → {fmt_temp(t_target)}"

if mode == "basic":
    scenario_mode_label = "初级模式" if is_zh else "Basic mode"
elif mode == "baseline_pue":
    scenario_mode_label = "基线 PUE 模式" if is_zh else "Baseline PUE mode"
else:
    scenario_mode_label = "COP 模式" if is_zh else "COP mode"

st.markdown(
    f"""
    <div class="scenario-bar">
        <div class="section-title" style="margin-bottom:10px;">{T['scenario_summary']}</div>
        <div class="scenario-grid">
            <div class="scenario-item">
                <div class="scenario-label">{T['label_model']}</div>
                <div class="scenario-value">{scenario_mode_label}</div>
            </div>
            <div class="scenario-item">
                <div class="scenario-label">{T['label_load_mode']}</div>
                <div class="scenario-value">{load_mode_label}</div>
            </div>
            <div class="scenario-item">
                <div class="scenario-label">{T['label_avg_price']}</div>
                <div class="scenario-value">{weighted_avg_price:,.4f}</div>
            </div>
            <div class="scenario-item">
                <div class="scenario-label">{T['label_temp_change']}</div>
                <div class="scenario-value">{scenario_temp_change}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Main pipeline execution
# ============================================================

if run_button:
    try:
        if p_core is None or p_core <= 0:
            st.error(f"{T['input_error']}: invalid core load.")
            st.stop()

        ok, message = validate_inputs(
            p_core=p_core,
            t_current=t_current,
            t_target=t_target,
            price=weighted_avg_price,
            hours=operating_hours,
        )

        if not ok:
            st.error(f"{T['input_error']}: {message}")
            st.stop()

        comparison = compare_current_and_target(
            mode=mode,
            p_core=p_core,
            t_current=t_current,
            t_target=t_target,
            pue_base=pue_base,
            aux_ratio=aux_ratio,
            t_ref=t_ref,
            k_ref=k_ref,
            cooling_sensitivity=cooling_sensitivity,
            cop_ref=cop_ref,
            cop_sensitivity=cop_sensitivity,
            heat_load_factor=heat_load_factor,
            use_weather=True,
            weather_mode="outdoor",
            t_outdoor=t_outdoor,
        )

        cost_comparison = compare_costs(
            current=comparison["current"],
            target=comparison["target"],
            hours=operating_hours,
            price=weighted_avg_price,
            use_tou=True,
            tou_structure=tou_structure,
        )

        annual_savings = annualize_savings(
            hourly_power_saved=comparison["diff"]["total_power_saved"],
            price=weighted_avg_price,
            use_tou=True,
            tou_structure=tou_structure,
        )

        marginal_savings = calculate_marginal_savings_per_degree(
            cost_saved=cost_comparison["savings"]["cost_saved"],
            t_current=t_current,
            t_target=t_target,
        )

        report = build_report(
            comparison=comparison,
            cost_comparison=cost_comparison,
            annual_savings=annual_savings,
            t_current=t_current,
            t_target=t_target,
            has_local_monitoring=has_local_monitoring,
            lang=language,
            currency=currency,
        )

        curve_data = generate_temperature_curve(
            mode=mode,
            p_core=p_core,
            temp_min=18,
            temp_max=30,
            t_current=t_current,
            pue_base=pue_base,
            aux_ratio=aux_ratio,
            t_ref=t_ref,
            k_ref=k_ref,
            cooling_sensitivity=cooling_sensitivity,
            cop_ref=cop_ref,
            cop_sensitivity=cop_sensitivity,
            heat_load_factor=heat_load_factor,
            use_weather=True,
            weather_mode="outdoor",
            t_outdoor=t_outdoor,
        )

        st.success(T["analysis_done"])

        # ============================================================
        # Model notice
        # ============================================================

        with st.expander(T["model_notice_title"], expanded=False):
            if mode == "basic":
                st.write(T["basic_notice"])
            elif mode == "baseline_pue":
                st.write(T["baseline_notice"])
            else:
                st.write(T["cop_notice"])

        # ============================================================
        # Results
        # ============================================================

        st.markdown(f"<div class='panel-title'>{T['key_metrics']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='panel-subtitle'>{T['kpi_desc']}</div>", unsafe_allow_html=True)

        current = cost_comparison["current"]
        target = cost_comparison["target"]
        savings = cost_comparison["savings"]

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(T["power_saved"], format_number(comparison["diff"]["total_power_saved"], 2))
        kpi2.metric(T["energy_saved"], format_number(savings["energy_saved"], 0))
        kpi3.metric(T["cost_saved"], format_number(savings["cost_saved"], 0))
        kpi4.metric(T["annual_cost_saved"], format_number(annual_savings["annual_cost_saved"], 0))

        kpi5, kpi6, kpi7, kpi8 = st.columns(4)
        kpi5.metric(T["pue"], fmt_pue(target["pue"]))
        kpi6.metric(T["total_power"], format_number(target["p_total"], 2))
        kpi7.metric(T["cooling_power"], format_number(target["p_cooling"], 2))
        kpi8.metric(T["marginal_savings"], format_number(marginal_savings, 0))

        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-title">{T['results_title']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='comparison-title'>{T['current_scenario']}</div>", unsafe_allow_html=True)
            st.metric(T["pue"], fmt_pue(current["pue"]))
            st.metric(T["total_power"], format_number(current["p_total"], 2))
            st.metric(T["cooling_power"], format_number(current["p_cooling"], 2))
            st.metric(T["cost"], format_number(current["cost"], 0))

        with col2:
            st.markdown(f"<div class='comparison-title'>{T['target_scenario']}</div>", unsafe_allow_html=True)
            st.metric(T["pue"], fmt_pue(target["pue"]))
            st.metric(T["total_power"], format_number(target["p_total"], 2))
            st.metric(T["cooling_power"], format_number(target["p_cooling"], 2))
            st.metric(T["cost"], format_number(target["cost"], 0))

        with col3:
            st.markdown(f"<div class='comparison-title'>{T['difference']}</div>", unsafe_allow_html=True)
            st.metric(T["power_saved"], format_number(comparison["diff"]["total_power_saved"], 2))
            st.metric(T["energy_saved"], format_number(savings["energy_saved"], 0))
            st.metric(T["cost_saved"], format_number(savings["cost_saved"], 0))
            st.metric(T["cooling_ratio"], fmt_percent(target["cooling_ratio"]))

        # ============================================================
        # Charts
        # ============================================================

        st.markdown(f"<div class='panel-title'>{T['charts_title']}</div>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(
                create_temperature_pue_curve(curve_data, T),
                use_container_width=True,
            )

        with chart_col2:
            st.plotly_chart(
                create_temperature_cost_curve(
                    curve_data=curve_data,
                    hours=operating_hours,
                    text=T,
                    price=weighted_avg_price,
                    use_tou=True,
                    tou_structure=tou_structure,
                ),
                use_container_width=True,
            )

        st.plotly_chart(
            create_power_breakdown_chart(current, target, T, bar_thickness=0.34),
            use_container_width=True,
        )

        # ============================================================
        # Decision report
        # ============================================================

        st.markdown(f"<div class='panel-title'>{T['report_title']}</div>", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                T["summary_tab"],
                T["economic_tab"],
                T["decision_tab"],
                T["risk_tab"],
            ]
        )

        with tab1:
            st.subheader(report["summary_title"])
            st.write(report["summary"])
            st.write(report["savings_summary"])

            st.markdown(f"**{report['advanced_title']}**")
            for item in report["insights"]:
                st.write(f"- {item}")

        with tab2:
            st.subheader(report["economic_title"])
            for item in report["economic_items"]:
                st.write(f"- {item}")

        with tab3:
            st.subheader(report["decision_title"])
            for item in report["decision_items"]:
                st.write(f"- {item}")

        with tab4:
            st.subheader(report["risk_title"])
            st.warning(report["risk_text"])
            for item in report["risk_items"]:
                st.write(f"- {item}")

    except Exception as e:
        st.error(f"{T['simulation_failed']}: {e}")

else:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-title">{T['empty_title']}</div>
            <div class="empty-body">{T['empty_body']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )