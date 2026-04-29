# ============================================================
# UI text dictionary
# Most front-end text should be modified here.
# ============================================================

TEXT = {
    "zh": {
        # Page
        "page_title": "热管理与能效优化引擎",
        "page_subtitle": "面向数据中心与高能耗数字基础设施的温控、冷却能耗、PUE 与运行电费估算工具",
        "app_name": "热管理与能效优化引擎",
        "app_caption": "本工具用于快速评估温度设定、冷却功耗、室外温度与分时电价对设施总能耗和运行成本的影响。",

        # Sidebar
        "sidebar_title": "参数输入",
        "sidebar_desc": "配置温度、负载、电价、气温与计算模型。",
        "language_toggle": "EN",

        "section_model": "计算模型",
        "section_model_desc": "选择热管理估算方法。",

        "section_temp_weather": "温度与气温",
        "section_temp_weather_desc": "设置当前温度、目标温度与室外温度。",

        "section_load": "核心负载",
        "section_load_desc": "支持直接输入、设备估算、电量反推与电费反推。",

        "section_tariff": "分时电价",
        "section_tariff_desc": "默认使用五档峰谷电价，并按时段加权估算电费。",

        "section_advanced": "高级参数",
        "section_advanced_desc": "用于校准冷却模型、辅助功耗和风险判断。",

        # Mode
        "calculation_mode": "计算模式",
        "mode_basic": "初级模式：经验比例模型",
        "mode_baseline_pue": "中级模式：基线 PUE 模型",
        "mode_cop": "高级模式：COP 模型",
        "mode_basic_help": "适合缺少现场详细数据、只想快速估算温控节能潜力的场景。",
        "mode_baseline_pue_help": "适合已知当前 PUE，希望基于当前能效水平估算调温影响的场景。",
        "mode_cop_help": "适合已知冷却系统 COP，或希望使用更专业冷却效率逻辑的场景。",

        # Load estimation
        "load_mode": "核心负载获取方式",
        "load_direct": "直接输入",
        "load_equipment": "设备估算",
        "load_energy": "电量反推",
        "load_cost": "电费反推",
        "p_core": "核心负载功率（kW）",
        "p_core_help": "数据中心可理解为 IT 功率；其他数字基础设施可理解为主要发热设备或生产设备功率。",
        "equipment_count": "设备数量",
        "rated_power": "单台额定功率（kW）",
        "utilization": "平均利用率",
        "total_energy": "周期总电量（kWh）",
        "total_cost": "周期总电费（¥）",
        "assumed_pue": "反推用假设 PUE",
        "estimate_hours": "反推周期时长（h）",
        "estimate_price": "反推用电价（¥/kWh）",

        # Temperature
        "t_current": "当前设定温度（°C）",
        "t_target": "目标设定温度（°C）",
        "outdoor_temp": "室外温度（°C）",
        "temperature_hint": "节能优化场景下，目标温度通常高于当前温度。建议逐步升温并观察热点与设备告警。",

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
        "aux_ratio_help": "辅助功耗包括 UPS 损耗、照明、监控、配电损耗等。常见粗估范围约 5%–12%。",
        "t_ref": "参考温度 T_ref（°C）",
        "k_ref": "参考冷却比例 k_ref",
        "cooling_sensitivity": "温度敏感系数 c",
        "cooling_sensitivity_help": "表示温度每降低 1°C 时冷却功率比例增加多少。数值越大，温控节能越敏感。",
        "pue_base": "当前基线 PUE",
        "cop_ref": "参考 COP",
        "cop_sensitivity": "COP 温度敏感系数",
        "heat_load_factor": "热负荷系数 β",
        "has_local_monitoring": "现场具备局部热点/温度监测",

        # Buttons
        "run_hint": "点击运行后生成能耗、成本、图表和决策报告。",
        "run_button_new": "开始模拟运行",

        # Hero chips
        "chip_thermal_optimization": "温控优化",
        "chip_pue_analysis": "PUE分析",
        "chip_tou_tariff": "峰谷电价",
        "chip_risk_assessment": "风险提示",

        # Scenario summary
        "scenario_summary": "场景概览",
        "label_model": "计算模型",
        "label_load_mode": "负载方式",
        "label_avg_price": "加权电价（¥/kWh）",
        "label_outdoor_temp": "室外温度",
        "label_temp_change": "温度调整",

        # Results
        "results_title": "计算结果",
        "key_metrics": "关键指标",
        "kpi_desc": "核心节能、成本与温控影响指标。",
        "current_scenario": "当前方案",
        "target_scenario": "目标方案",
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
        "chart_temp_pue": "温度 - PUE 曲线",
        "chart_temp_cost": "温度 - 电费曲线",
        "chart_power_compare": "当前与目标方案功率构成对比",
        "chart_savings": "节能收益对比",
        "temperature": "设定温度（°C）",
        "estimated_pue": "预计 PUE",
        "estimated_cost": "预计电费（¥）",
        "power_kw": "功率（kW）",
        "core_load": "核心负载",
        "cooling_load": "冷却功耗",
        "aux_load": "辅助功耗",

        # Report
        "report_title": "决策报告",
        "summary_tab": "摘要",
        "economic_tab": "经济性",
        "decision_tab": "决策建议",
        "risk_tab": "风险提示",
        "advanced_insight": "高级洞察",
        "risk_level": "风险等级",
        "executive_summary": "执行摘要",
        "detailed_insights": "详细洞察",

        # Notices
        "input_error": "输入参数有误",
        "model_notice_title": "模型说明",
        "basic_notice": "当前使用初级经验模型，适合快速估算，不替代现场测试。",
        "baseline_notice": "当前使用基线 PUE 模型，结果依赖用户输入的当前 PUE 是否可靠。",
        "cop_notice": "当前使用 COP 模型，并默认考虑室外温度对冷却效率的影响。",
        "analysis_done": "模拟完成",
        "simulation_failed": "模拟失败",
        "empty_title": "等待模拟运行",
        "empty_body": "请在左侧输入参数，然后点击“开始模拟运行”。",
    },

    "en": {
        # Page
        "page_title": "Thermal Management & Energy Efficiency Engine",
        "page_subtitle": "A temperature control, cooling energy, PUE, and operating cost estimation tool for data centers and high-energy digital facilities.",
        "app_name": "Thermal Management & Energy Efficiency Engine",
        "app_caption": "This tool estimates how temperature setpoint, cooling power, outdoor temperature, and TOU tariff affect total energy use and operating cost.",

        # Sidebar
        "sidebar_title": "Input Parameters",
        "sidebar_desc": "Configure temperature, load, tariff, outdoor temperature, and model settings.",
        "language_toggle": "中",

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


def get_text(lang="zh"):
    return TEXT.get(lang, TEXT["zh"])