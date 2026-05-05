# ============================================================
# UI text dictionary
# Most front-end text should be modified here.
# ============================================================

TEXT = {
    "zh": {
        # Page
        "page_title": "EOE - 热管理系统调优",
        "page_subtitle": "面向数据中心与高能耗数字基础设施的热管理系统调优与经济收益评估助手",
        "app_name": "EOE - 热管理系统调优",
        "app_caption": "请核对以下模块中的内容，确保计算模型选择及全部必要数据输入无误",

        # Sidebar
        "sidebar_title": "EOE - 热管理系统调优",
        "sidebar_desc": "面向数据中心与高能耗数字基础设施的热管理系统调优与经济收益评估助手",
        "language_toggle": "English",

        "section_model": "计算模型选择",
        "section_model_desc": "选择评估热管理系统各项指标的计算模型",

        "section_temp_weather": "温度与气温",
        "section_temp_weather_desc": "设置当前温度、目标温度与室外温度。",

        "section_load": "核心负载输入",
        "section_load_desc": "支持直接输入、设备估算、电量反推与电费反推多种模式输入核心负荷",

        "section_tariff": "分时电价输入",
        "section_tariff_desc": "最多可以使用五档分时电价评估加权平均电费。",

        "section_advanced": "高级参数",
        "section_advanced_desc": "用于校准冷却模型、辅助功耗和风险判断。",

        # Mode
        "calculation_mode": "支持使用不同精度模型进行仿真",
        "mode_basic": "初级模式（使用经验比例模型）",
        "mode_baseline_pue": "中级模式（使用基线PUE模型）",
        "mode_cop": "高级模式（使用COP模型）",
        "mode_basic_help": "初级模式适合设施详细数据未知或仅需快速评估调温节能潜力场景",
        "mode_baseline_pue_help": "中级模式适合设施PUE已知场景，有助于以较高精度评估温控节能收益",
        "mode_cop_help": "高级模式适合冷却系统COP已知场景，可开展高精度、高专业性温控收益评估与分析",

        # Load estimation
        "load_mode": "核心负载输入方式",
        "load_direct": "手动输入",
        "load_equipment": "根据设备估算",
        "load_energy": "根据耗电量反推",
        "load_cost": "根据电费反推",
        "p_core": "核心负载功率（kW）",
        "p_core_help": "数据中心可理解为IT功率；其他数字基础设施可理解为主要发热设备或生产设备功率",
        "equipment_count": "主要负荷设备数量",
        "rated_power": "单台设备额定功率（kW）",
        "utilization": "设备平均利用率",
        "total_energy": "周期内总电量消耗（kWh）",
        "total_cost": "周期内总电费支出（¥）",
        "assumed_pue": "反推预设PUE",
        "estimate_hours": "反推周期时长（h）",
        "estimate_price": "反推预设加权平均电价（¥/kWh）",

        # Temperature
        "t_current": "当前热管理系统设定温度（°C）",
        "t_target": "目标热管理系统设定温度（°C）",
        "outdoor_temp": "室外温度（°C）",
        "temperature_hint": "温控调优场景下，目标温度通常高于当前温度。建议逐步缓慢提高热管理系统设定温度并关注设备预警情况",

        # Tariff
        "critical_peak_price": "尖峰电价（¥/kWh）",
        "peak_price": "峰电价（¥/kWh）",
        "flat_price": "平电价（¥/kWh）",
        "valley_price": "谷电价（¥/kWh）",
        "super_valley_price": "深谷电价（¥/kWh）",
        "critical_peak_hours": "尖峰时长（h）",
        "peak_hours": "峰时长（h）",
        "flat_hours": "平时长（h）",
        "valley_hours": "谷时长（h）",
        "super_valley_hours": "深谷时长（h）",
        "weighted_avg_price": "加权平均电价（¥/kWh）",
        "tou_hours_sum": "分时时长合计（h）",
        "tou_detail": "分时电价详情",

        # Time / Currency
        "operating_hours": "分析周期运行时长（h）",
        "currency": "货币符号",

        # Advanced parameters
        "advanced_params": "高级参数",
        "aux_ratio": "辅助功耗比例",
        "aux_ratio_help": "辅助功耗包括UPS损耗、照明、监控、配电损耗等，常见预估范围约为5%–12%",
        "t_ref": "参考温度（°C）",
        "k_ref": "参考冷却比例系数（k_ref）",
        "cooling_sensitivity": "温度敏感系数（c）",
        "cooling_sensitivity_help": "该参数表示温度每降低1°C时冷却功率增加比例",
        "pue_base": "当前基线PUE",
        "cop_ref": "参考COP",
        "cop_sensitivity": "COP温度敏感系数",
        "heat_load_factor": "热负荷系数β",
        "has_local_monitoring": "现场具备局部热点/温度监测系统",

        # Buttons
        "run_hint": "请核对是否完成全部数据与参数输入",
        "run_button_new": "开始热管理系统调优分析评估",

        # Hero chips
        "chip_thermal_optimization": "热管理系统调优",
        "chip_pue_analysis": "PUE（电能使用效率）评估",
        "chip_tou_tariff": "温控系统调优前后经济性分析",
        "chip_risk_assessment": "温控系统调优风险性评估",

        # Scenario summary
        "scenario_summary": "计算模型及数据输入状态摘要",
        "label_model": "计算模型",
        "label_load_mode": "负荷输入方法",
        "label_avg_price": "加权平均电价（¥/kWh）",
        "label_outdoor_temp": "室外温度",
        "label_temp_change": "冷却系统温度调整",

        # Results
        "results_title": "计算结果",
        "key_metrics": "关键指标",
        "kpi_desc": "核心节能、成本与温控影响指标。",
        "current_scenario": "当前设定温度",
        "target_scenario": "目标设定温度",
        "difference": "变化量",
        "pue": "PUE / 总能耗系数",
        "total_power": "总功率（kW）",
        "cooling_power": "冷却功率（kW）",
        "aux_power": "辅助功率（kW）",
        "cooling_ratio": "冷却比例",
        "cooling_share": "冷却占总功率比例",
        "energy": "周期总电量（kWh）",
        "cost": "周期总电费（¥）",
        "energy_saved": "节省电量（kWh）",
        "cost_saved": "节省电费（¥）",
        "annual_energy_saved": "年化节省电量（kWh）",
        "annual_cost_saved": "年化节省电费（¥）",
        "power_saved": "节省功率（kW）",
        "marginal_savings": "每 °C 节省电费（¥/°C）",

        # Charts
        "charts_title": "图表分析",
        "chart_temp_pue": "热管理系统设定温度与PUE相关性分析",
        "chart_temp_cost": "热管理系统设定温度与能耗支出相关性分析",
        "chart_power_compare": "热管理系统调优前后经济性收益对比",
        "chart_savings": "经济性收益对比",
        "temperature": "热管理系统设定温度（°C）",
        "estimated_pue": "预估PUE（电能使用效率）",
        "estimated_cost": "预估能耗支出（¥）",
        "power_kw": "功率消耗（kW）",
        "core_load": "核心负载功率消耗",
        "cooling_load": "热管理系统功率消耗",
        "aux_load": "辅助功能功率消耗",

        # Report
        "report_title": "热管理系统调优和经济性分析报告",
        "summary_tab": "摘要",
        "economic_tab": "经济性分析",
        "decision_tab": "决策建议",
        "risk_tab": "风险评估",
        "advanced_insight": "高级洞察",
        "risk_level": "风险等级",
        "executive_summary": "执行摘要",
        "detailed_insights": "详细洞察",

        # Notices
        "input_error": "输入数据或参数有误",
        "model_notice_title": "模型说明",
        "basic_notice": "当前使用初级经验模型，适合设施详细数据未知或仅需快速评估调温节能潜力场景",
        "baseline_notice": "当前使用基线PUE模型，适合设施PUE已知场景，有助于以较高精度评估温控节能收益",
        "cop_notice": "当前使用COP模型，适合冷却系统COP已知场景，可开展高精度、高专业性温控收益评估与分析",
        "analysis_done": "热管理系统调优和经济性分析已完成",
        "simulation_failed": "热管理系统调优和经济性分析失败",
        "empty_title": "热管理系统调优和经济性分析流程指南",
        "empty_body": "请在左侧输入栏依次完成各项数据和参数上传后点击“开始热管理系统调优分析评估”。如果部分数据或参数缺失，可以使用系统默认或自带数据/参数。",
    },

    "en": {
        # Page
        "page_title": "EOE - Thermal Management System Optimization",
        "page_subtitle": "A temperature control, cooling energy, PUE, and operating cost estimation tool for data centers and high-energy digital facilities.",
        "app_name": "EOE - Thermal Management System Optimization",
        "app_caption": "This tool estimates how temperature setpoint, cooling power, outdoor temperature, and TOU tariff affect total energy use and operating cost.",

        # Sidebar
        "sidebar_title": "EOE - Thermal Management System Optimization",
        "sidebar_desc": "Configure temperature, load, tariff, outdoor temperature, and model settings.",
        "language_toggle": "中文",

        "section_model": "Calculation Model",
        "section_model_desc": "Select the thermal estimation method.",

        "section_temp_weather": "Temperature & Weather",
        "section_temp_weather_desc": "Set current temperature, target temperature, and outdoor temperature.",

        "section_load": "Core Load",
        "section_load_desc": "Support direct input, equipment estimate, energy-based estimate, and cost-based estimate.",

        "section_tariff": "TOU Tariff",
        "section_tariff_desc": "Use five-level TOU tariff and weighted average price by default.",

        "section_advanced": "Advanced Parameters",
        "section_advanced_desc": "Calibrate cooling model, auxiliary load, and risk evaluation.",

        # Mode
        "calculation_mode": "Calculation Mode",
        "mode_basic": "Basic Mode: Empirical Ratio Model",
        "mode_baseline_pue": "Standard Mode: Baseline PUE Model",
        "mode_cop": "Advanced Mode: COP Model",
        "mode_basic_help": "Suitable for quick estimation when detailed site data is not available.",
        "mode_baseline_pue_help": "Suitable when the current PUE is known and temperature adjustment needs to be evaluated.",
        "mode_cop_help": "Suitable when cooling COP is known or a more professional cooling-efficiency logic is preferred.",

        # Load estimation
        "load_mode": "Core Load Input Mode",
        "load_direct": "Direct Input",
        "load_equipment": "Equipment Estimate",
        "load_energy": "Energy-Based Estimate",
        "load_cost": "Cost-Based Estimate",
        "p_core": "Core Load Power (kW)",
        "p_core_help": "For data centers, this can be interpreted as IT power. For other digital facilities, it refers to the main heat-generating equipment load.",
        "equipment_count": "Equipment Count",
        "rated_power": "Rated Power per Unit (kW)",
        "utilization": "Average Utilization",
        "total_energy": "Total Energy in Period (kWh)",
        "total_cost": "Total Cost in Period (¥)",
        "assumed_pue": "Assumed PUE for Back-Calculation",
        "estimate_hours": "Estimation Period (h)",
        "estimate_price": "Estimation Price (¥/kWh)",

        # Temperature
        "t_current": "Current Temperature Setpoint (°C)",
        "t_target": "Target Temperature Setpoint (°C)",
        "outdoor_temp": "Outdoor Temperature (°C)",
        "temperature_hint": "For energy-saving scenarios, the target temperature is usually higher than the current temperature. Increase gradually and monitor hotspots or equipment alarms.",

        # Tariff
        "critical_peak_price": "Critical Peak Price (¥/kWh)",
        "peak_price": "Peak Price (¥/kWh)",
        "flat_price": "Flat Price (¥/kWh)",
        "valley_price": "Valley Price (¥/kWh)",
        "super_valley_price": "Super Valley Price (¥/kWh)",
        "critical_peak_hours": "Critical Peak Hours (h)",
        "peak_hours": "Peak Hours (h)",
        "flat_hours": "Flat Hours (h)",
        "valley_hours": "Valley Hours (h)",
        "super_valley_hours": "Super Valley Hours (h)",
        "weighted_avg_price": "Weighted Average Price (¥/kWh)",
        "tou_hours_sum": "TOU Hours Sum (h)",
        "tou_detail": "TOU Details",

        # Time / Currency
        "operating_hours": "Operating Hours in Analysis Period (h)",
        "currency": "Currency Symbol",

        # Advanced parameters
        "advanced_params": "Advanced Parameters",
        "aux_ratio": "Auxiliary Load Ratio",
        "aux_ratio_help": "Auxiliary load includes UPS losses, lighting, monitoring, and power distribution losses. A rough range is usually 5%–12%.",
        "t_ref": "Reference Temperature T_ref (°C)",
        "k_ref": "Reference Cooling Ratio k_ref",
        "cooling_sensitivity": "Cooling Temperature Sensitivity c",
        "cooling_sensitivity_help": "The increase in cooling power ratio when temperature decreases by 1°C. Higher value means stronger temperature sensitivity.",
        "pue_base": "Current Baseline PUE",
        "cop_ref": "Reference COP",
        "cop_sensitivity": "COP Temperature Sensitivity",
        "heat_load_factor": "Heat Load Factor β",
        "has_local_monitoring": "Local hotspot / temperature monitoring is available",

        # Buttons
        "run_hint": "Click run to generate energy, cost, charts, and decision report.",
        "run_button_new": "Run Simulation",

        # Hero chips
        "chip_thermal_optimization": "Thermal Optimization",
        "chip_pue_analysis": "PUE Analysis",
        "chip_tou_tariff": "TOU Tariff",
        "chip_risk_assessment": "Risk Notes",

        # Scenario summary
        "scenario_summary": "Scenario Summary",
        "label_model": "Model",
        "label_load_mode": "Load Mode",
        "label_avg_price": "Weighted Price (¥/kWh)",
        "label_outdoor_temp": "Outdoor Temp",
        "label_temp_change": "Temp Change",

        # Results
        "results_title": "Calculation Results",
        "key_metrics": "Key Metrics",
        "kpi_desc": "Core energy-saving, cost, and thermal impact metrics.",
        "current_scenario": "Current Scenario",
        "target_scenario": "Target Scenario",
        "difference": "Difference",
        "pue": "PUE / Total Energy Factor",
        "total_power": "Total Power (kW)",
        "cooling_power": "Cooling Power (kW)",
        "aux_power": "Auxiliary Power (kW)",
        "cooling_ratio": "Cooling Ratio",
        "cooling_share": "Cooling Share",
        "energy": "Total Energy (kWh)",
        "cost": "Total Cost (¥)",
        "energy_saved": "Energy Saved (kWh)",
        "cost_saved": "Cost Saved (¥)",
        "annual_energy_saved": "Annualized Energy Saved (kWh)",
        "annual_cost_saved": "Annualized Cost Saved (¥)",
        "power_saved": "Power Saved (kW)",
        "marginal_savings": "Cost Saving per °C (¥/°C)",

        # Charts
        "charts_title": "Chart Analysis",
        "chart_temp_pue": "Temperature - PUE Curve",
        "chart_temp_cost": "Temperature - Cost Curve",
        "chart_power_compare": "Power Breakdown: Current vs Target",
        "chart_savings": "Energy-Saving Benefits",
        "temperature": "Temperature Setpoint (°C)",
        "estimated_pue": "Estimated PUE",
        "estimated_cost": "Estimated Cost (¥)",
        "power_kw": "Power (kW)",
        "core_load": "Core Load",
        "cooling_load": "Cooling Load",
        "aux_load": "Auxiliary Load",

        # Report
        "report_title": "Decision Report",
        "summary_tab": "Summary",
        "economic_tab": "Economic Insights",
        "decision_tab": "Decision Recommendations",
        "risk_tab": "Risk Notes",
        "advanced_insight": "Advanced Insights",
        "risk_level": "Risk Level",
        "executive_summary": "Executive Summary",
        "detailed_insights": "Detailed Insights",

        # Notices
        "input_error": "Input Error",
        "model_notice_title": "Model Note",
        "basic_notice": "The basic empirical model is used for quick estimation and does not replace on-site testing.",
        "baseline_notice": "The baseline PUE model depends on the reliability of the user-provided current PUE.",
        "cop_notice": "The COP model is used, and outdoor temperature correction is enabled by default.",
        "analysis_done": "Simulation Completed",
        "simulation_failed": "Simulation Failed",
        "empty_title": "Waiting for Simulation",
        "empty_body": "Set parameters in the sidebar and click Run Simulation.",
    },
}



# ============================================================
# Mode-aware UI additions
# ============================================================

EXTRA_TEXT = {
    "zh": {
        "section_temp": "温度设定输入",
        "section_temp_desc": "设置温控系统当前的设定温度和目标设定温度",
        "section_weather": "室外温度",
        "section_weather_desc": "高级模式（使用COP模型）下将使用室外温度修正冷却效率",
        "section_baseline": "基线PUE（电能使用效率）",
        "section_baseline_desc": "中级模式（使用基线PUE模型）下使用下列输入数据评估当前设施的能效水平",
        "section_cop": "COP（制冷性能系数）输入",
        "section_cop_desc": "高级模式（使用COP模型）下将使用下列冷却系统效率、热负荷和辅助功耗参数",
        "annual_results_title": "分析结果",
        "annual_results_desc": "分析结果基于数据中心或数字基础设施全年遵循输入数据运行进行仿真，以下数据重点聚焦于调整冷却系统前后的能源与经济性收益",
        "optimization_effect": "能源或经济性收益",
        "current_annual_energy": "调温前年化电量消耗（kWh）",
        "target_annual_energy": "调温后年化电量消耗（kWh）",
        "energy_saving_rate": "年化电量节省收益率",
        "current_annual_cost": "调温前年化电费（¥）",
        "target_annual_cost": "调温后年化电费（¥）",
        "annual_cost_saved_short": "年化节省电费金额（¥）",
        "current_total_power": "调温前总功率（kW）",
        "target_total_power": "调温后总功率（kW）",
        "power_reduction_rate": "总功率下降收益率",
        "current_pue": "调温前PUE（总能耗系数）",
        "target_pue": "调温后PUE（总能耗系数）",
        "pue_reduction_rate": "PUE（总能耗系数） 下降收益率",
    },
    "en": {
        "section_temp": "Temperature Setpoints",
        "section_temp_desc": "Set the current and target temperature setpoints.",
        "section_weather": "Outdoor Temperature",
        "section_weather_desc": "Used in Advanced COP mode to correct cooling efficiency.",
        "section_baseline": "Baseline PUE",
        "section_baseline_desc": "Used in Standard mode to describe current facility efficiency.",
        "section_cop": "COP & Cooling Parameters",
        "section_cop_desc": "Used in Advanced mode to describe cooling efficiency, heat load, and auxiliary load.",
        "annual_results_title": "Calculation Results",
        "annual_results_desc": "Results are annualized based on 24×365 operation, highlighting long-term energy and cost changes before and after temperature adjustment.",
        "optimization_effect": "Optimization Effect",
        "current_annual_energy": "Annual Energy Before Adjustment (kWh)",
        "target_annual_energy": "Annual Energy After Adjustment (kWh)",
        "energy_saving_rate": "Annual Energy Saving Rate",
        "current_annual_cost": "Annualized Cost Before Adjustment (¥)",
        "target_annual_cost": "Annualized Cost After Adjustment (¥)",
        "annual_cost_saved_short": "Annual Cost Saving (¥)",
        "current_total_power": "Total Power Before Adjustment (kW)",
        "target_total_power": "Total Power After Adjustment (kW)",
        "power_reduction_rate": "Total Power Reduction Rate",
        "current_pue": "PUE / Total Energy Factor Before Adjustment",
        "target_pue": "PUE / Total Energy Factor After Adjustment",
        "pue_reduction_rate": "PUE Reduction",
    },
}


def get_text(lang="zh"):
    base = TEXT.get(lang, TEXT["zh"]).copy()
    base.update(EXTRA_TEXT.get(lang, EXTRA_TEXT["zh"]))
    return base
