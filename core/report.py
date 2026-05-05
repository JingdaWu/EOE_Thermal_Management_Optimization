# ============================================================
# Front-end report text generation
# Mode-aware report for Thermal Management Demo
# ============================================================

from core.recommendations import generate_recommendation_keys
from core.risk_model import evaluate_overall_risk
from utils.formatters import (
    fmt_kw,
    fmt_kwh,
    fmt_money,
    fmt_pue,
    fmt_temp,
    fmt_percent,
)


REPORT_TEXT = {
    "zh": {
        "summary_title": "分析摘要",
        "economic_title": "经济性结论",
        "decision_title": "决策建议",
        "risk_title": "风险提示",
        "advanced_title": "模型洞察",

        "summary_basic": (
            "当前采用初级经验比例模型。将设定温度由 {t_current} 调整至 {t_target} 后，"
            "预计设施总功率由 {current_power} 变化至 {target_power}，"
            "PUE / 总能耗系数由 {current_pue} 变化至 {target_pue}。"
            "该结果适合作为缺少现场详细参数时的快速节能潜力判断。"
        ),
        "summary_baseline_pue": (
            "当前采用中级基线 PUE 模型，并以当前基线 PUE = {pue_base} 作为能效基准。"
            "将设定温度由 {t_current} 调整至 {t_target} 后，预计设施总功率由 {current_power} 变化至 {target_power}，"
            "PUE / 总能耗系数由 {current_pue} 变化至 {target_pue}。"
            "该结果更适合已有 PUE 监测或能耗台账的场景。"
        ),
        "summary_cop": (
            "当前采用高级 COP 模型，并纳入室外温度 {t_outdoor} 对冷却效率的影响。"
            "将设定温度由 {t_current} 调整至 {t_target} 后，预计设施总功率由 {current_power} 变化至 {target_power}，"
            "PUE / 总能耗系数由 {current_pue} 变化至 {target_pue}，"
            "冷却系统 COP 由 {current_cop} 变化至 {target_cop}。"
        ),

        "savings_positive": (
            "按全年 24×365 小时运行估算，调温前年电量约 {current_energy}，调温后年电量约 {target_energy}，"
            "年节省电量约 {annual_energy_saved}，年化节省电费约 {annual_cost_saved}。"
            "折算到每 1°C 调整，年化边际节省电费约 {marginal_savings}。"
        ),
        "savings_negative": (
            "在当前参数下，目标方案未体现出明确节能收益。建议检查目标温度、当前 PUE、冷却参数、室外温度或电价输入是否合理。"
        ),

        "economic_positive_savings": "温控优化可以降低基础运行负荷，通常属于低 CAPEX、见效较快的能效优化措施。",
        "economic_no_positive_savings": "当前目标方案未产生正向节能收益，不建议直接作为节能方案采用。",
        "economic_high_savings": "本场景的年化节省电费较高，建议优先开展小规模试运行和现场验证。",
        "economic_medium_savings": "本场景存在一定节能价值，适合作为运维优化或能效改造的候选方案。",
        "economic_low_savings": "本场景节省金额较低，建议结合设备风险、管理成本和现场改造难度综合判断。",
        "economic_annual_view": "右侧结果已优先采用年化口径，更适合判断长期运行成本与节能价值。",
        "economic_cooling_cost": "仅从冷却侧看，预计年化冷却电费节省约 {cooling_cost_saved}，可作为评估冷却系统优化收益的重要参考。",

        "decision_raise_temperature": "建议采用分阶段升温策略，不建议一次性大幅调整温度。",
        "decision_lower_temperature": "目标温度低于当前温度，通常会提高冷却能耗；若无明确安全或工艺需求，不建议主动降温。",
        "decision_keep_temperature": "当前温度与目标温度相同，温控策略本身不会带来明显节能变化。",
        "decision_target_in_recommended_range": "目标温度处于相对合理区间，适合在加强监测的前提下进行试运行。",
        "decision_target_too_conservative": "目标温度偏保守，节能空间可能没有充分释放。",
        "decision_target_aggressive": "目标温度偏激进，虽然节能潜力更高，但需要确认进风温度、热点和设备告警情况。",
        "decision_target_high_risk": "目标温度较高，风险可能明显增加，不建议在缺少现场监测的情况下直接采用。",
        "decision_basic": "初级模式结果适合用于早期筛选，不建议直接作为最终改造依据。",
        "decision_baseline": "中级模式应优先确认基线 PUE 的来源，若 PUE 来自长期监测数据，结论可信度会明显提高。",
        "decision_cop": "高级模式适合用于更接近工程现场的预评估，但仍建议结合现场温度、气流组织和设备告警记录进行验证。",

        "risk_lack_local_monitoring": "当前未启用局部热点/温度监测假设，结果不能替代现场热环境测试。",
        "risk_hotspot_risk": "较高温度设定可能增加局部热点、设备告警或稳定性风险。",
        "risk_large_temperature_step": "本次温度调整幅度较大，建议分阶段调整，并观察至少一个完整运行周期。",
        "risk_pue_worse": "目标方案 PUE 高于当前方案，说明参数下能效表现变差，需要重新检查输入。",
        "risk_general": "本模块为基于平均负荷、简化冷却模型和分时电价假设的估算工具，不替代专业热仿真、CFD 分析或现场测试。",
        "risk_basic_model": "初级模式隐藏了冷却系统细节，适合快速估算，但不适合直接评价复杂冷却系统的真实性能。",
        "risk_baseline_model": "中级模式对当前基线 PUE 较敏感，若输入的 PUE 偏离真实运行水平，经济性结论也会偏离。",
        "risk_cop_model": "高级模式已考虑 COP 和室外温度，但仍未覆盖机柜级热点、气流短路、湿度、冗余策略等现场因素。",

        "insight_temp_sensitive": "该系统对温度变化较敏感，调温可带来较明显的节能收益。",
        "insight_temp_insensitive": "该系统对温度变化不够敏感，单纯调温带来的节能空间可能有限。",
        "insight_cooling_dominant": "冷却功率占比较高，优化重点应优先放在温控策略、气流组织或冷却系统效率上。",
        "insight_low_cooling": "冷却功率占比较低，温控优化对整体电费的影响有限。",
        "insight_high_pue": "当前 PUE 偏高，除调温外，还存在进一步系统性优化空间。",
        "insight_good_pue": "当前 PUE 已处于相对较好区间，后续优化应关注风险控制和边际收益。",
        "insight_pue_reduction": "本次调温带来的 PUE 降低比例约为 {pue_reduction_rate}。",
        "insight_power_reduction": "本次调温带来的总功率下降比例约为 {power_reduction_rate}。",
        "insight_cop_improved": "目标方案下 COP 有所提高，说明在当前参数下，温度调整有助于改善冷却效率。",
        "insight_cop_not_improved": "目标方案下 COP 改善不明显，节能收益主要来自冷却负荷比例变化或经验参数假设。",
        "insight_outdoor": "室外温度越高，冷却系统效率通常越容易受压制，因此高级模式结果应结合当地气候和季节复核。",
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
        "advanced_title": "Model Insights",

        "summary_basic": (
            "The basic empirical ratio model is used. After adjusting the temperature setpoint from {t_current} to {t_target}, "
            "the estimated facility total power changes from {current_power} to {target_power}, "
            "and the PUE / total energy factor changes from {current_pue} to {target_pue}. "
            "This result is suitable for quick screening when detailed site parameters are not available."
        ),
        "summary_baseline_pue": (
            "The standard baseline PUE model is used, with current baseline PUE = {pue_base} as the efficiency baseline. "
            "After adjusting the temperature setpoint from {t_current} to {t_target}, the estimated facility total power changes from {current_power} to {target_power}, "
            "and the PUE / total energy factor changes from {current_pue} to {target_pue}. "
            "This result is more suitable when PUE monitoring or energy records are available."
        ),
        "summary_cop": (
            "The advanced COP model is used, including the impact of outdoor temperature {t_outdoor} on cooling efficiency. "
            "After adjusting the temperature setpoint from {t_current} to {t_target}, the estimated facility total power changes from {current_power} to {target_power}, "
            "the PUE / total energy factor changes from {current_pue} to {target_pue}, "
            "and the cooling system COP changes from {current_cop} to {target_cop}."
        ),

        "savings_positive": (
            "Assuming 24×365 operation, annual energy use before adjustment is about {current_energy}, and annual energy use after adjustment is about {target_energy}. "
            "The annual energy saving is about {annual_energy_saved}, with annualized electricity cost savings of about {annual_cost_saved}. "
            "Converted per 1°C adjustment, the annualized marginal cost saving is about {marginal_savings}."
        ),
        "savings_negative": (
            "Under the current assumptions, the target scenario does not show clear energy-saving benefits. "
            "Please check the target temperature, current PUE, cooling parameters, outdoor temperature, or tariff inputs."
        ),

        "economic_positive_savings": "Thermal optimization can reduce base operating load and is usually a low-CAPEX, fast-impact efficiency measure.",
        "economic_no_positive_savings": "The target scenario does not generate positive savings, so it should not be directly adopted as an energy-saving measure.",
        "economic_high_savings": "The estimated annual cost saving is significant. A small-scale pilot and on-site validation are recommended.",
        "economic_medium_savings": "The scenario shows moderate energy-saving value and can be considered as an operational optimization option.",
        "economic_low_savings": "The estimated saving is limited. Please consider equipment risk, management cost, and implementation difficulty together.",
        "economic_annual_view": "The displayed results use an annualized view, which is more suitable for long-term operating cost evaluation.",
        "economic_cooling_cost": "From the cooling side alone, annualized cooling electricity cost saving is estimated at about {cooling_cost_saved}, which can help evaluate cooling-system optimization value.",

        "decision_raise_temperature": "A phased temperature increase is recommended. Avoid a one-step large temperature adjustment.",
        "decision_lower_temperature": "The target temperature is lower than the current temperature, which usually increases cooling energy use. This is not recommended unless required by safety or process needs.",
        "decision_keep_temperature": "The current and target temperatures are the same, so the temperature strategy itself will not create meaningful energy savings.",
        "decision_target_in_recommended_range": "The target temperature is within a relatively reasonable range and can be tested with stronger monitoring.",
        "decision_target_too_conservative": "The target temperature is conservative, so the energy-saving potential may not be fully released.",
        "decision_target_aggressive": "The target temperature is aggressive. It may offer higher savings, but inlet temperature, hotspots, and alarms must be checked.",
        "decision_target_high_risk": "The target temperature is relatively high. Direct adoption is not recommended without sufficient on-site monitoring.",
        "decision_basic": "Basic mode is suitable for early screening and should not be used as the final basis for implementation.",
        "decision_baseline": "Standard mode should first verify the source of the baseline PUE. If it comes from long-term monitoring, the conclusion becomes more reliable.",
        "decision_cop": "Advanced mode is better for engineering-oriented pre-evaluation, but it should still be validated with site temperature, airflow, and equipment alarm records.",

        "risk_lack_local_monitoring": "Local hotspot or temperature monitoring is not assumed, so the result cannot replace on-site thermal testing.",
        "risk_hotspot_risk": "A higher temperature setpoint may increase hotspot, alarm, or stability risks.",
        "risk_large_temperature_step": "The temperature adjustment is large. A phased approach and observation over at least one full operating cycle are recommended.",
        "risk_pue_worse": "The target PUE is higher than the current PUE, meaning the energy efficiency becomes worse under the current assumptions.",
        "risk_general": "This module is an estimation tool based on average load, simplified cooling models, and TOU tariff assumptions. It does not replace professional thermal simulation, CFD analysis, or field testing.",
        "risk_basic_model": "Basic mode hides cooling-system details. It is useful for quick estimation but not for evaluating complex cooling-system performance.",
        "risk_baseline_model": "Standard mode is sensitive to the current baseline PUE. If the PUE input deviates from actual operation, the economic conclusion will also deviate.",
        "risk_cop_model": "Advanced mode considers COP and outdoor temperature, but it still does not cover rack-level hotspots, airflow short circuiting, humidity, or redundancy strategies.",

        "insight_temp_sensitive": "The system is sensitive to temperature changes, and setpoint optimization may deliver meaningful savings.",
        "insight_temp_insensitive": "The system is not very sensitive to temperature changes, so the savings from setpoint adjustment may be limited.",
        "insight_cooling_dominant": "Cooling power accounts for a high share of total power. Optimization should focus on thermal control, airflow management, or cooling efficiency.",
        "insight_low_cooling": "Cooling power accounts for a relatively low share, so temperature optimization may have limited impact on total cost.",
        "insight_high_pue": "The current PUE is relatively high, indicating additional system-level optimization potential.",
        "insight_good_pue": "The current PUE is already in a relatively efficient range. Further optimization should focus on risk control and marginal benefit.",
        "insight_pue_reduction": "The PUE reduction from this temperature adjustment is about {pue_reduction_rate}.",
        "insight_power_reduction": "The total power reduction from this temperature adjustment is about {power_reduction_rate}.",
        "insight_cop_improved": "The target scenario shows improved COP, meaning the temperature adjustment helps improve cooling efficiency under the current assumptions.",
        "insight_cop_not_improved": "The target scenario does not show clear COP improvement; savings mainly come from cooling-load ratio changes or empirical assumptions.",
        "insight_outdoor": "Higher outdoor temperature can suppress cooling efficiency, so advanced-mode results should be reviewed together with local climate and seasonality.",
        "risk_low": "Overall risk is low; optimization can proceed.",
        "risk_normal": "Risk is manageable; gradual validation is recommended.",
        "risk_elevated": "Some risk exists; proceed cautiously with monitoring.",
        "risk_high": "Risk is high; large adjustments are not recommended.",
    },
}


def _safe_ratio(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator / denominator


def _mode_summary_key(mode):
    if mode == "baseline_pue":
        return "summary_baseline_pue"
    if mode == "cop":
        return "summary_cop"
    return "summary_basic"


def build_report(
    comparison,
    cost_comparison,
    annual_savings,
    t_current,
    t_target,
    has_local_monitoring,
    lang="zh",
    currency="¥",
    mode="basic",
    annual_cost_comparison=None,
    pue_base=None,
    t_outdoor=None,
    weighted_avg_price=None,
    marginal_savings=None,
):
    """
    Build mode-aware front-end report sections.
    """

    text = REPORT_TEXT.get(lang, REPORT_TEXT["zh"])

    if annual_cost_comparison is None:
        annual_cost_comparison = cost_comparison

    current_period = cost_comparison["current"]
    target_period = cost_comparison["target"]
    current = annual_cost_comparison["current"]
    target = annual_cost_comparison["target"]
    savings = annual_cost_comparison["savings"]

    current_power = current["p_total"]
    target_power = target["p_total"]
    current_pue = current["pue"]
    target_pue = target["pue"]

    current_energy = current["energy"]
    target_energy = target["energy"]
    annual_energy_saved = savings["energy_saved"]
    annual_cost_saved = savings["cost_saved"]
    cooling_cost_saved = savings.get("cooling_cost_saved", 0)

    power_reduction_rate = _safe_ratio(current_power - target_power, current_power)
    pue_reduction_rate = _safe_ratio(current_pue - target_pue, current_pue)

    if marginal_savings is None:
        temp_delta = abs(t_target - t_current)
        marginal_savings = annual_cost_saved / temp_delta if temp_delta else 0

    recommendation_keys = generate_recommendation_keys(
        t_current=t_current,
        t_target=t_target,
        current_pue=current_pue,
        target_pue=target_pue,
        annual_cost_saved=annual_cost_saved,
        has_local_monitoring=has_local_monitoring,
    )

    risk = evaluate_overall_risk(
        t_current=t_current,
        t_target=t_target,
        current_pue=current_pue,
        target_pue=target_pue,
        has_local_monitoring=has_local_monitoring,
    )

    current_cop = comparison["current"].get("cop")
    target_cop = comparison["target"].get("cop")

    summary = text[_mode_summary_key(mode)].format(
        t_current=fmt_temp(t_current),
        t_target=fmt_temp(t_target),
        current_power=fmt_kw(current_power),
        target_power=fmt_kw(target_power),
        current_pue=fmt_pue(current_pue),
        target_pue=fmt_pue(target_pue),
        pue_base=fmt_pue(pue_base) if pue_base is not None else fmt_pue(current_pue),
        t_outdoor=fmt_temp(t_outdoor) if t_outdoor is not None else "N/A",
        current_cop=f"{current_cop:.2f}" if current_cop is not None else "N/A",
        target_cop=f"{target_cop:.2f}" if target_cop is not None else "N/A",
    )

    if annual_cost_saved > 0:
        savings_summary = text["savings_positive"].format(
            current_energy=fmt_kwh(current_energy),
            target_energy=fmt_kwh(target_energy),
            annual_energy_saved=fmt_kwh(annual_energy_saved),
            annual_cost_saved=fmt_money(annual_cost_saved, currency),
            marginal_savings=fmt_money(marginal_savings, currency),
        )
    else:
        savings_summary = text["savings_negative"]

    economic_items = []
    for key in recommendation_keys["economic_keys"]:
        text_key = f"economic_{key}"
        if text_key in text:
            economic_items.append(text[text_key])

    economic_items.append(text["economic_annual_view"])
    economic_items.append(text["economic_cooling_cost"].format(
        cooling_cost_saved=fmt_money(cooling_cost_saved, currency)
    ))

    decision_items = []
    for key in recommendation_keys["decision_keys"]:
        text_key = f"decision_{key}"
        if text_key in text:
            decision_items.append(text[text_key])

    if mode == "baseline_pue":
        decision_items.append(text["decision_baseline"])
    elif mode == "cop":
        decision_items.append(text["decision_cop"])
    else:
        decision_items.append(text["decision_basic"])

    risk_items = []
    for key in recommendation_keys["risk_keys"]:
        text_key = f"risk_{key}"
        if text_key in text:
            risk_items.append(text[text_key])

    if mode == "baseline_pue":
        risk_items.append(text["risk_baseline_model"])
    elif mode == "cop":
        risk_items.append(text["risk_cop_model"])
    else:
        risk_items.append(text["risk_basic_model"])

    risk_items.append(text["risk_general"])

    insights = []

    if annual_cost_saved > 5000:
        insights.append(text["insight_temp_sensitive"])
    else:
        insights.append(text["insight_temp_insensitive"])

    cooling_share = current_period["p_cooling"] / current_period["p_total"] if current_period["p_total"] > 0 else 0
    if cooling_share > 0.35:
        insights.append(text["insight_cooling_dominant"])
    else:
        insights.append(text["insight_low_cooling"])

    if current_pue > 1.8:
        insights.append(text["insight_high_pue"])
    else:
        insights.append(text["insight_good_pue"])

    insights.append(text["insight_power_reduction"].format(
        power_reduction_rate=fmt_percent(power_reduction_rate)
    ))
    insights.append(text["insight_pue_reduction"].format(
        pue_reduction_rate=fmt_percent(pue_reduction_rate)
    ))

    if mode == "cop":
        if current_cop is not None and target_cop is not None and target_cop > current_cop:
            insights.append(text["insight_cop_improved"])
        else:
            insights.append(text["insight_cop_not_improved"])
        insights.append(text["insight_outdoor"])

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
