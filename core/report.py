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


REPORT_TEXT = {'zh': {'summary_title': '热管理调优与经济性分析摘要',
        'economic_title': '经济性分析结论',
        'decision_title': '进一步能源调优相关决策建议',
        'risk_title': '风险提示',
        'advanced_title': '使用模型相关内容洞察',
        'summary_basic': '当前评估模式采用初级经验比例模型。将热管理系统设定温度由 {t_current} 调整至 {t_target} 后，设施内总功率消耗将由 {current_power} 优化至 '
                         '{target_power}，PUE（总能耗系数）将由 {current_pue} 优化至 {target_pue}。该结果适合设施详细数据未知或仅需快速评估调温节能潜力场景。',
        'summary_baseline_pue': '当前评估模式采用中级基线PUE模型，并以当前基线PUE（总能耗系数）= {pue_base} 作为能效基准。将热管理系统设定温度由 {t_current} 调整至 '
                                '{t_target} 后，设施内总功率消耗将由 {current_power} 优化至 {target_power}，PUE（总能耗系数）将由 {current_pue} '
                                '优化至 {target_pue}。该结果更适合冷却系统COP已知场景，可开展高精度、高专业性温控收益评估与分析',
        'summary_cop': '当前采用高级COP模型，并考虑室外温度 {t_outdoor} 对冷却效率的影响。将热管理系统设定温度由 {t_current} 调整至 {t_target} 后，设施内总功率消耗将由 '
                       '{current_power} 优化至 {target_power}，PUE（总能耗系数）将由 {current_pue} 优化至 {target_pue}。冷却系统COP由 '
                       '{current_cop} 变化至 {target_cop}。',
        'savings_positive': '按用户输入总功率消耗估算，热管理系统优化前年化电量消耗 {current_energy}，优化前年化电量消耗为 '
                            '{target_energy}，按加权平均电价估算，热管理系统优化前后年化电量节省为 {annual_energy_saved}，年化能源经济性节省为 '
                            '{annual_cost_saved}。热管理系统每1°C调整所对应的年化边际节省电费为 {marginal_savings}。',
        'savings_negative': '在当前输入数据与参数下，热管理系统调优方案未体现出明确节能收益。建议检查目标温度、当前PUE、冷却参数、室外温度或电价输入是否合理。',
        'economic_positive_savings': '热管理系统调优可以降低基础运行负荷，通常属于低成本支出、高经济收益的能效优化措施。',
        'economic_no_positive_savings': '当前热管理系统调优方案未产生正向节能收益，不建议直接作为经济性优化方案采用。',
        'economic_high_savings': '在当前输入数据与参数下年化经济性收益较高，建议优先开展小规模试运行和现场验证。',
        'economic_medium_savings': '在当前输入数据与参数下存在正向年化经济性收益，热管理系统调优适合作为运维优化或能效改造的候选方案。',
        'economic_low_savings': '在当前输入数据与参数下年化经济性收益较低，建议结合设备风险、管理成本和现场改造难度综合判断。',
        'economic_annual_view': '分析结果已以年化收益进行标准化，更适合判断设施长期运行的经济性收益',
        'economic_cooling_cost': '仅从冷却系统收益角度分析，预计年化冷却系统电费节约 {cooling_cost_saved}，可作为评估优化冷却系统经济性收益的重要参考。',
        'decision_raise_temperature': '建议采用分阶段逐渐升温策略，不建议一次性大幅调整温度。',
        'decision_lower_temperature': '热管理系统调优目标温度低于当前设定温度，通常会提高冷却能耗；若无明确安全性或运维需求，不建议主动降温。',
        'decision_keep_temperature': '当前温度与热管理系统调优目标温度相同，温控策略不会带来能源和经济性收益。',
        'decision_target_in_recommended_range': '热管理系统调优目标温度处于相对合理区间，适合在具备安全性监测的前提下进行试运行。',
        'decision_target_too_conservative': '热管理系统调优目标温度设定较为保守，能源及经济性优化空间可能没有充分释放。',
        'decision_target_aggressive': '热管理系统调优目标温度设定较为激进，虽然能源及经济性优化潜力更高，但需要进一步确认进风温度、热点和设备预警情况。',
        'decision_target_high_risk': '目标温度较高，风险可能明显增加，不建议在缺少现场监测的情况下直接采用。',
        'decision_basic': '初级模式分析结果适合用于早期快速评估，不建议直接作为热管理系统调优的决策依据。',
        'decision_baseline': '开展中级模式应优先确认基线PUE的数据来源，若基线PUE来自于长期监测数据，结论可信度会明显提高。',
        'decision_cop': '高级模式适合用于更接近工程现场的预评估，但仍建议结合现场温度、气流组织和设备预警记录进行交叉验证。',
        'risk_lack_local_monitoring': '当前未启用局部热点及温度监测假设，分析结果不能替代现场热管理系统运行实际测试。',
        'risk_hotspot_risk': '较高的设定设定可能增加局部热点、设备预警可能性，可能导致设备长期运行稳定性风险。',
        'risk_large_temperature_step': '本次热管理系统温度调整幅度较大，建议分阶段逐步调整，并实际观察至少一个完整运行周期。',
        'risk_pue_worse': '热管理系统调优后PUE高于当前方案，说明当前输入数据及参数条件下调优效果变差，请重新检查输入数据是否有误。',
        'risk_general': '本程序为基于平均负荷、简化冷却模型和分时电价假设的能耗评估和决策辅助工具，不替代专业热仿真、CFD分析或现场测试。',
        'risk_basic_model': '初级分析模式忽略了部分冷却系统细节，仅适合优化前期快速估算，不适合直接评价复杂冷却系统的真实性能和调优收益。',
        'risk_baseline_model': '中级分析模式对基线PUE精度较敏感，若输入的PUE偏离设施真实运行水平，能耗与经济性分析结论也可能有所偏离。',
        'risk_cop_model': '高级分析模式虽然已经充分考虑COP和室外温度等参数，但仍未覆盖机柜级热点、气流短路、湿度、冗余策略等现场实际因素。',
        'insight_temp_sensitive': '系统设施能耗对温度变化较敏感，优化热管理系统可带来较明显的能源与经济性收益。',
        'insight_temp_insensitive': '系统设施能耗对温度变化不够敏感，单纯优化热管理系统带来的能源与经济性空间可能有限。',
        'insight_cooling_dominant': '系统设施冷却功率占比较高，对冷却设施功耗的优化应优先于热管理策略、气流组织或冷却系统效率上。',
        'insight_low_cooling': '系统设施冷却功率占比较低，对冷却设施功耗的优化对系统整体能耗和经济性的影响有限。',
        'insight_high_pue': '当前PUE偏高，除热管理系统调优外，还存在进一步系统性优化的空间。',
        'insight_good_pue': '当前PUE已处于相对较好区间，后续优化应关注风险控制和边际收益。',
        'insight_pue_reduction': '本次热管理系统调优带来的PUE降低比例为 {pue_reduction_rate}。',
        'insight_power_reduction': '本次热管理系统调优带来的总功率下降比例为 {power_reduction_rate}。',
        'insight_cop_improved': '热管理系统调优方案下COP有所提高，说明在当前数据和参数下，热管理系统调优有助于明显改善冷却效率。',
        'insight_cop_not_improved': '当前热管理系统调优方案下COP改善不明显，说明能源与经济性收益主要来自冷却负荷比例变化或经验参数假设。',
        'insight_outdoor': '系统设施所处环境室外温度越高，冷却系统效率越容易承受负向影响，因此高级分析模式的结果应结合当地气候和季节开展进一步复核。',
        'risk_low': '整体系统风险较低，建议进一步推进热管理系统调优。',
        'risk_normal': '整体系统风险可控，建议在推进热管理系统调优过程中逐步验证分析结果的准确性。',
        'risk_elevated': '整体系统存在一定风险，建议谨慎开展热管理系统调优并加强实际监测与核实。',
        'risk_high': '整体系统风险较高，不建议直接大范围开展热管理系统调优。'},
 'en': {'summary_title': 'Thermal Optimization and Economic Assessment Summary',
        'economic_title': 'Economic Assessment Conclusions',
        'decision_title': 'Operational Recommendations',
        'risk_title': 'Risk Notes',
        'advanced_title': 'Model-Based Insights',
        'summary_basic': 'The assessment uses the Basic empirical ratio model. After adjusting the thermal setpoint '
                         'from {t_current} to {t_target}, the estimated facility total power decreases from '
                         '{current_power} to {target_power}, and PUE changes from {current_pue} to {target_pue}. This '
                         'mode is intended for early-stage screening when detailed facility data are limited.',
        'summary_baseline_pue': 'The assessment uses the Standard baseline PUE model, with the current baseline PUE of '
                                '{pue_base} as the energy-efficiency reference. After adjusting the thermal setpoint '
                                'from {t_current} to {t_target}, the estimated facility total power decreases from '
                                '{current_power} to {target_power}, and PUE changes from {current_pue} to '
                                '{target_pue}. This mode is more suitable when measured PUE or reliable '
                                'energy-performance records are available.',
        'summary_cop': 'The assessment uses the Advanced COP model and accounts for the impact of outdoor temperature '
                       '({t_outdoor}) on cooling efficiency. After adjusting the thermal setpoint from {t_current} to '
                       '{t_target}, the estimated facility total power decreases from {current_power} to '
                       '{target_power}, PUE changes from {current_pue} to {target_pue}, and the estimated '
                       'cooling-system COP changes from {current_cop} to {target_cop}.',
        'savings_positive': 'Based on the input load assumptions and 24×365 operation, annual energy consumption is '
                            'estimated at {current_energy} before adjustment and {target_energy} after adjustment. The '
                            'annual energy saving is {annual_energy_saved}, corresponding to an estimated annual '
                            'electricity cost saving of {annual_cost_saved}. The annualized marginal electricity-cost '
                            'saving per 1°C of setpoint adjustment is {marginal_savings}.',
        'savings_negative': 'Under the current inputs and assumptions, the target scenario does not show a clear '
                            'energy-saving benefit. Review the target setpoint, baseline PUE, cooling parameters, '
                            'outdoor temperature, and tariff inputs before using the result for decision-making.',
        'economic_positive_savings': 'Thermal setpoint optimization can reduce base operating load and is typically a '
                                     'low-CAPEX energy-efficiency measure.',
        'economic_no_positive_savings': 'The target scenario does not generate positive savings under the current '
                                        'assumptions and should not be adopted as an energy-cost optimization measure '
                                        'without further review.',
        'economic_high_savings': 'The estimated annual savings are material. A staged pilot and on-site validation are '
                                 'recommended before broader implementation.',
        'economic_medium_savings': 'The scenario shows positive annual savings and can be considered as a candidate '
                                   'for operational optimization or energy-efficiency improvement.',
        'economic_low_savings': 'The estimated annual savings are limited. Equipment risk, operational effort, and '
                                'implementation difficulty should be considered together.',
        'economic_annual_view': 'The results are normalized on an annual basis to better support long-term '
                                'operating-cost evaluation.',
        'economic_cooling_cost': 'Considering the cooling system alone, the estimated annualized cooling electricity '
                                 'cost saving is {cooling_cost_saved}, which can be used as a reference for '
                                 'cooling-system optimization value.',
        'decision_raise_temperature': 'Use a staged setpoint increase rather than a one-step large adjustment.',
        'decision_lower_temperature': 'The target setpoint is lower than the current setpoint and will usually '
                                      'increase cooling energy use. This is not recommended unless required for '
                                      'safety, reliability, or operational constraints.',
        'decision_keep_temperature': 'The current and target setpoints are the same, so the setpoint strategy itself '
                                     'will not produce meaningful energy or cost savings.',
        'decision_target_in_recommended_range': 'The target setpoint is within a generally reasonable range and may be '
                                                'suitable for pilot operation with adequate monitoring.',
        'decision_target_too_conservative': 'The target setpoint is relatively conservative, so some energy-saving '
                                            'potential may remain unused.',
        'decision_target_aggressive': 'The target setpoint is relatively aggressive. It may provide higher savings, '
                                      'but inlet temperature, hotspots, and equipment alarms should be verified first.',
        'decision_target_high_risk': 'The target setpoint is high enough to raise operational risk. Broad '
                                     'implementation is not recommended without sufficient on-site monitoring.',
        'decision_basic': 'Basic mode is suitable for early screening. It should not be used as the sole basis for '
                          'final implementation decisions.',
        'decision_baseline': 'For Standard mode, first confirm the source and reliability of the baseline PUE. '
                             'Conclusions are more credible when PUE comes from long-term monitoring or reliable '
                             'energy records.',
        'decision_cop': 'Advanced mode is better suited for engineering-oriented pre-assessment, but results should '
                        'still be cross-checked with site temperature data, airflow conditions, and equipment alarm '
                        'history.',
        'risk_lack_local_monitoring': 'Local hotspot and temperature monitoring are not assumed, so the result cannot '
                                      'replace on-site thermal validation.',
        'risk_hotspot_risk': 'A higher setpoint may increase the probability of localized hotspots, equipment alarms, '
                             'or long-term reliability issues.',
        'risk_large_temperature_step': 'The setpoint change is large. Use staged adjustment and observe at least one '
                                       'full operating cycle before further changes.',
        'risk_pue_worse': 'PUE is higher after optimization, indicating worse energy performance under the current '
                          'inputs. Recheck the input data and model assumptions.',
        'risk_general': 'This tool is an energy and decision-support estimator based on average load, simplified '
                        'cooling models, and TOU tariff assumptions. It does not replace professional thermal '
                        'simulation, CFD analysis, or field testing.',
        'risk_basic_model': 'Basic mode omits many cooling-system details and is intended only for early screening, '
                            'not for evaluating complex cooling-system performance or final optimization benefits.',
        'risk_baseline_model': 'Standard mode is sensitive to the accuracy of baseline PUE. If the PUE input differs '
                               'from actual facility operation, the energy and economic conclusions may also deviate.',
        'risk_cop_model': 'Advanced mode considers COP and outdoor temperature, but it still does not capture '
                          'rack-level hotspots, airflow recirculation or bypass, humidity, redundancy strategy, or '
                          'other site-specific factors.',
        'insight_temp_sensitive': 'Facility energy use is sensitive to setpoint changes, so thermal optimization may '
                                  'provide meaningful energy and cost benefits.',
        'insight_temp_insensitive': 'Facility energy use is not highly sensitive to setpoint changes, so thermal '
                                    'optimization alone may provide limited energy and cost benefits.',
        'insight_cooling_dominant': 'Cooling power represents a high share of total power. Optimization should '
                                    'prioritize cooling-system operation, airflow management, and thermal-control '
                                    'strategy.',
        'insight_low_cooling': 'Cooling power represents a relatively low share of total power, so cooling-side '
                               'optimization may have a limited impact on overall energy cost.',
        'insight_high_pue': 'The current PUE is relatively high, indicating potential for broader system-level '
                            'efficiency improvement beyond setpoint optimization.',
        'insight_good_pue': 'The current PUE is already in a relatively efficient range. Further optimization should '
                            'focus on risk control and marginal benefit.',
        'insight_pue_reduction': 'The PUE reduction achieved by this setpoint adjustment is {pue_reduction_rate}.',
        'insight_power_reduction': 'The total power reduction achieved by this setpoint adjustment is '
                                   '{power_reduction_rate}.',
        'insight_cop_improved': 'The target scenario shows improved COP, indicating that the setpoint adjustment '
                                'improves cooling efficiency under the current assumptions.',
        'insight_cop_not_improved': 'The target scenario does not show a clear COP improvement; the savings are mainly '
                                    'driven by cooling-load changes or empirical model assumptions.',
        'insight_outdoor': 'Higher outdoor temperature can reduce cooling efficiency, so Advanced-mode results should '
                           'be reviewed alongside local climate and seasonal operating conditions.',
        'risk_low': 'Overall risk is low; the scenario can be considered for staged validation.',
        'risk_normal': 'Overall risk is manageable; gradual validation is recommended.',
        'risk_elevated': 'Some operational risk exists; proceed cautiously and strengthen monitoring.',
        'risk_high': 'Overall risk is high; broad setpoint optimization is not recommended without further '
                     'validation.'}}

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
