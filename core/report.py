# ============================================================
# Front-end report text generation
# Integrated with recommendation logic and risk model
# ============================================================

from core.recommendations import generate_recommendation_keys
from core.risk_model import evaluate_overall_risk
from utils.formatters import (
    fmt_kw,
    fmt_kwh,
    fmt_money,
    fmt_pue,
    fmt_temp,
)


REPORT_TEXT = {
    "zh": {
        "summary_title": "分析摘要",
        "economic_title": "经济性结论",
        "decision_title": "决策建议",
        "risk_title": "风险提示",
        "advanced_title": "高级洞察",

        "summary": (
            "将设定温度由 {t_current} 调整至 {t_target} 后，"
            "预计总功率由 {current_power} 变化至 {target_power}，"
            "PUE / 总能耗系数由 {current_pue} 变化至 {target_pue}。"
        ),

        "savings_positive": (
            "在当前运行时长和加权电价条件下，预计可节省电量 {energy_saved}，"
            "对应节省电费 {cost_saved}。按全年 24×365 小时运行估算，"
            "年化节省电量约 {annual_energy_saved}，年化节省电费约 {annual_cost_saved}。"
        ),

        "savings_negative": (
            "在当前参数下，目标方案未体现出明确节能收益。建议检查目标温度、冷却参数、当前 PUE 或室外温度输入是否合理。"
        ),

        "economic_positive_savings": "温控优化可以降低基础运行负荷，属于低 CAPEX、见效较快的能效优化措施。",
        "economic_no_positive_savings": "当前目标方案未产生正向节能收益，不建议直接作为节能方案采用。",
        "economic_high_savings": "本场景的年化节省电费较高，建议优先开展小规模试运行和现场验证。",
        "economic_medium_savings": "本场景存在一定节能价值，适合作为运维优化或能效改造的候选方案。",
        "economic_low_savings": "本场景节省金额较低，建议结合设备风险、管理成本和现场改造难度综合判断。",

        "decision_raise_temperature": "建议采用分阶段升温策略，不建议一次性大幅调整温度。",
        "decision_lower_temperature": "目标温度低于当前温度，通常会提高冷却能耗；若无明确安全或工艺需求，不建议主动降温。",
        "decision_keep_temperature": "当前温度与目标温度相同，温控策略本身不会带来明显节能变化。",
        "decision_target_in_recommended_range": "目标温度处于相对合理区间，适合在加强监测的前提下进行试运行。",
        "decision_target_too_conservative": "目标温度偏保守，节能空间可能没有充分释放。",
        "decision_target_aggressive": "目标温度偏激进，虽然节能潜力更高，但需要确认进风温度、热点和设备告警情况。",
        "decision_target_high_risk": "目标温度较高，风险可能明显增加，不建议在缺少现场监测的情况下直接采用。",

        "risk_lack_local_monitoring": "当前未启用局部热点/温度监测假设，结果不能替代现场热环境测试。",
        "risk_hotspot_risk": "较高温度设定可能增加局部热点、设备告警或稳定性风险。",
        "risk_large_temperature_step": "本次温度调整幅度较大，建议分阶段调整，并观察至少一个完整运行周期。",
        "risk_pue_worse": "目标方案 PUE 高于当前方案，说明参数下能效表现变差，需要重新检查输入。",
        "risk_general": "本模块为基于平均负荷、经验冷却模型和加权电价的估算工具，不替代专业热仿真、CFD 分析或现场测试。",

        "insight_temp_sensitive": "该系统对温度变化较敏感，调温可带来较明显的节能收益。",
        "insight_temp_insensitive": "该系统对温度变化不够敏感，单纯调温带来的节能空间可能有限。",
        "insight_cooling_dominant": "冷却功率占比较高，优化重点应优先放在温控策略、气流组织或冷却系统效率上。",
        "insight_low_cooling": "冷却功率占比较低，温控优化对整体电费的影响有限。",
        "insight_high_pue": "当前 PUE 偏高，除调温外，还存在进一步系统性优化空间。",
        "insight_good_pue": "当前 PUE 已处于相对较好区间，后续优化应关注风险控制和边际收益。",
        "risk_low": "整体风险较低，可推进优化。",
        "risk_normal": "风险可控，建议逐步验证。",
        "risk_elevated": "存在一定风险，建议谨慎调整并加强监测。",
        "risk_high": "风险较高，不建议直接实施大幅调整。",
    },

    "en": {
        "summary_title": "Analysis Summary",
        "economic_title": "Economic Insights",
        "decision_title": "Decision Recommendations",
        "risk_title": "Risk Notes",
        "advanced_title": "Advanced Insights",

        "summary": (
            "After adjusting the temperature setpoint from {t_current} to {t_target}, "
            "the estimated total power changes from {current_power} to {target_power}, "
            "and the PUE / total energy factor changes from {current_pue} to {target_pue}."
        ),

        "savings_positive": (
            "Under the current operating hours and weighted electricity price, the estimated energy saving is {energy_saved}, "
            "with an electricity cost saving of {cost_saved}. Assuming 24×365 operation, "
            "the annualized energy saving is about {annual_energy_saved}, and the annualized cost saving is about {annual_cost_saved}."
        ),

        "savings_negative": (
            "Under the current assumptions, the target scenario does not show clear energy-saving benefits. "
            "Please check the target temperature, cooling parameters, baseline PUE, or outdoor temperature input."
        ),

        "economic_positive_savings": "Thermal optimization can reduce base operating load and is usually a low-CAPEX, fast-impact efficiency measure.",
        "economic_no_positive_savings": "The target scenario does not generate positive savings, so it should not be directly adopted as an energy-saving measure.",
        "economic_high_savings": "The estimated annual cost saving is significant. A small-scale pilot and on-site validation are recommended.",
        "economic_medium_savings": "The scenario shows moderate energy-saving value and can be considered as an operational optimization option.",
        "economic_low_savings": "The estimated saving is limited. Please consider equipment risk, management cost, and implementation difficulty together.",

        "decision_raise_temperature": "A phased temperature increase is recommended. Avoid a one-step large temperature adjustment.",
        "decision_lower_temperature": "The target temperature is lower than the current temperature, which usually increases cooling energy use. This is not recommended unless required by safety or process needs.",
        "decision_keep_temperature": "The current and target temperatures are the same, so the temperature strategy itself will not create meaningful energy savings.",
        "decision_target_in_recommended_range": "The target temperature is within a relatively reasonable range and can be tested with stronger monitoring.",
        "decision_target_too_conservative": "The target temperature is conservative, so the energy-saving potential may not be fully released.",
        "decision_target_aggressive": "The target temperature is aggressive. It may offer higher savings, but inlet temperature, hotspots, and alarms must be checked.",
        "decision_target_high_risk": "The target temperature is relatively high. Direct adoption is not recommended without sufficient on-site monitoring.",

        "risk_lack_local_monitoring": "Local hotspot or temperature monitoring is not assumed, so the result cannot replace on-site thermal testing.",
        "risk_hotspot_risk": "A higher temperature setpoint may increase hotspot, alarm, or stability risks.",
        "risk_large_temperature_step": "The temperature adjustment is large. A phased approach and observation over at least one full operating cycle are recommended.",
        "risk_pue_worse": "The target PUE is higher than the current PUE, meaning the energy efficiency becomes worse under the current assumptions.",
        "risk_general": "This module is an estimation tool based on average load, empirical cooling model, and weighted tariff assumptions. It does not replace professional thermal simulation, CFD analysis, or field testing.",

        "insight_temp_sensitive": "The system is sensitive to temperature changes, and setpoint optimization may deliver meaningful savings.",
        "insight_temp_insensitive": "The system is not very sensitive to temperature changes, so the savings from setpoint adjustment may be limited.",
        "insight_cooling_dominant": "Cooling power accounts for a high share of total power. Optimization should focus on thermal control, airflow management, or cooling efficiency.",
        "insight_low_cooling": "Cooling power accounts for a relatively low share, so temperature optimization may have limited impact on total cost.",
        "insight_high_pue": "The current PUE is relatively high, indicating additional system-level optimization potential.",
        "insight_good_pue": "The current PUE is already in a relatively efficient range. Further optimization should focus on risk control and marginal benefit.",
        "risk_low": "Overall risk is low; optimization can proceed.",
        "risk_normal": "Risk is manageable; gradual validation is recommended.",
        "risk_elevated": "Some risk exists; proceed cautiously with monitoring.",
        "risk_high": "Risk is high; large adjustments are not recommended.",
    },
}


def build_report(
    comparison,
    cost_comparison,
    annual_savings,
    t_current,
    t_target,
    has_local_monitoring,
    lang="zh",
    currency="¥",
):
    """
    Build front-end report sections.
    """

    text = REPORT_TEXT.get(lang, REPORT_TEXT["zh"])

    current = cost_comparison["current"]
    target = cost_comparison["target"]
    savings = cost_comparison["savings"]

    recommendation_keys = generate_recommendation_keys(
        t_current=t_current,
        t_target=t_target,
        current_pue=current["pue"],
        target_pue=target["pue"],
        annual_cost_saved=annual_savings["annual_cost_saved"],
        has_local_monitoring=has_local_monitoring,
    )

    risk = evaluate_overall_risk(
        t_current=t_current,
        t_target=t_target,
        current_pue=current["pue"],
        target_pue=target["pue"],
        has_local_monitoring=has_local_monitoring,
    )

    summary = text["summary"].format(
        t_current=fmt_temp(t_current),
        t_target=fmt_temp(t_target),
        current_power=fmt_kw(current["p_total"]),
        target_power=fmt_kw(target["p_total"]),
        current_pue=fmt_pue(current["pue"]),
        target_pue=fmt_pue(target["pue"]),
    )

    if savings["cost_saved"] > 0:
        savings_summary = text["savings_positive"].format(
            energy_saved=fmt_kwh(savings["energy_saved"]),
            cost_saved=fmt_money(savings["cost_saved"], currency),
            annual_energy_saved=fmt_kwh(annual_savings["annual_energy_saved"]),
            annual_cost_saved=fmt_money(annual_savings["annual_cost_saved"], currency),
        )
    else:
        savings_summary = text["savings_negative"]

    economic_items = []
    for key in recommendation_keys["economic_keys"]:
        text_key = f"economic_{key}"
        if text_key in text:
            economic_items.append(text[text_key])

    decision_items = []
    for key in recommendation_keys["decision_keys"]:
        text_key = f"decision_{key}"
        if text_key in text:
            decision_items.append(text[text_key])

    risk_items = []
    for key in recommendation_keys["risk_keys"]:
        text_key = f"risk_{key}"
        if text_key in text:
            risk_items.append(text[text_key])

    risk_items.append(text["risk_general"])

    insights = []

    if savings["cost_saved"] > 5000:
        insights.append(text["insight_temp_sensitive"])
    else:
        insights.append(text["insight_temp_insensitive"])

    cooling_share = current["p_cooling"] / current["p_total"] if current["p_total"] > 0 else 0
    if cooling_share > 0.35:
        insights.append(text["insight_cooling_dominant"])
    else:
        insights.append(text["insight_low_cooling"])

    if current["pue"] > 1.8:
        insights.append(text["insight_high_pue"])
    else:
        insights.append(text["insight_good_pue"])

    risk_level = risk["overall_risk"]
    risk_text = text.get(f"risk_{risk_level}", text["risk_general"])

    return {
        "summary_title": text["summary_title"],
        "economic_title": text["economic_title"],
        "decision_title": text["decision_title"],
        "risk_title": text["risk_title"],
        "advanced_title": text["advanced_title"],
        "summary": summary,
        "savings_summary": savings_summary,
        "economic_items": economic_items,
        "decision_items": decision_items,
        "risk_items": risk_items,
        "insights": insights,
        "risk": risk,
        "risk_text": risk_text,
    }