"""Reference Lists for the Application"""

# RESOURCE GROUPINGS
from mppsteel.config.mypy_config_settings import MYPY_DICT_STR_LIST, MYPY_STR_DICT


RESOURCE_CATEGORY_MAPPER: MYPY_STR_DICT = {
    "Iron ore": "Feedstock",
    "Scrap": "Feedstock",
    "DRI": "Feedstock",
    "Met coal": "Fossil Fuels",
    "Thermal coal": "Fossil Fuels",
    "Coke": "Fossil Fuels",
    "COG": "Fossil Fuels",
    "BF gas": "Fossil Fuels",
    "BOF gas": "Fossil Fuels",
    "Natural gas": "Fossil Fuels",
    "Plastic waste": "Fossil Fuels",
    "Biomass": "Bio Fuels",
    "Biomethane": "Bio Fuels",
    "Hydrogen": "Hydrogen",
    "Electricity": "Electricity",
    "Steam": "Other Opex",
    "BF slag": "Other Opex",
    "Other slag": "Other Opex",
    "Captured CO2": "CCS",
    "Used CO2": "CCS",
    "Process emissions": "Emissivity",
    "Emissivity wout CCS": "Emissivity",
    "Emissivity": "Carbon Cost",
}

RESOURCE_CONTAINER_REF: MYPY_DICT_STR_LIST = {
    "scrap": ["Scrap"],
    "biomass": ["Biomass", "Biomethane"],
    "ccs": ["Captured CO2"],
    "co2": ["Used CO2"],
}

# TECHNOLOGY GROUPINGS
FURNACE_GROUP_DICT: MYPY_DICT_STR_LIST = {
    "blast_furnace": [
        "Avg BF-BOF",
        "BAT BF-BOF",
        "BAT BF-BOF_bio PCI",
        "BAT BF-BOF_H2 PCI",
        "BAT BF-BOF+CCUS",
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCU",
    ],
    "dri-bof": ["DRI-Melt-BOF", "DRI-Melt-BOF_100% zero-C H2", "DRI-Melt-BOF+CCUS"],
    "dri-eaf": [
        "DRI-EAF",
        "DRI-EAF_50% bio-CH4",
        "DRI-EAF_50% green H2",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
    ],
    "smelting_reduction": ["Smelting Reduction", "Smelting Reduction+CCUS"],
    "eaf-basic": ["EAF"],
    "eaf-advanced": ["Electrolyzer-EAF", "Electrowinning-EAF"],
    "ccs": [
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCUS",
        "DRI-Melt-BOF+CCUS",
        "DRI-EAF+CCUS",
        "Smelting Reduction+CCUS",
    ],
    "ccu": ["BAT BF-BOF+CCU"],
}
FURNACE_GROUP_DICT["dri"] = (
    FURNACE_GROUP_DICT["dri-bof"] + FURNACE_GROUP_DICT["dri-eaf"]
)
FURNACE_GROUP_DICT["eaf-all"] = (
    FURNACE_GROUP_DICT["eaf-basic"] + FURNACE_GROUP_DICT["eaf-advanced"]
)

SWITCH_DICT: MYPY_DICT_STR_LIST = {
    "Avg BF-BOF": [
        "Avg BF-BOF",
        "BAT BF-BOF",
        "BAT BF-BOF_bio PCI",
        "BAT BF-BOF_H2 PCI",
        "BAT BF-BOF+CCUS",
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCU",
        "DRI-Melt-BOF",
        "DRI-Melt-BOF_100% zero-C H2",
        "DRI-Melt-BOF+CCUS",
        "DRI-EAF",
        "DRI-EAF_50% bio-CH4",
        "DRI-EAF_50% green H2",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
        "Smelting Reduction",
        "Smelting Reduction+CCUS",
        "EAF",
        "Electrolyzer-EAF",
        "Electrowinning-EAF",
    ],
    "BAT BF-BOF": [
        "BAT BF-BOF",
        "BAT BF-BOF_bio PCI",
        "BAT BF-BOF_H2 PCI",
        "BAT BF-BOF+CCUS",
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCU",
        "DRI-Melt-BOF",
        "DRI-Melt-BOF_100% zero-C H2",
        "DRI-Melt-BOF+CCUS",
        "DRI-EAF",
        "DRI-EAF_50% bio-CH4",
        "DRI-EAF_50% green H2",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
        "Smelting Reduction",
        "Smelting Reduction+CCUS",
        "EAF",
        "Electrolyzer-EAF",
        "Electrowinning-EAF",
    ],
    "BAT BF-BOF_bio PCI": [
        "BAT BF-BOF_bio PCI",
        "BAT BF-BOF+CCUS",
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCU",
        "DRI-Melt-BOF_100% zero-C H2",
        "DRI-Melt-BOF+CCUS",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
        "Smelting Reduction+CCUS",
        "EAF",
        "Electrolyzer-EAF",
        "Electrowinning-EAF",
    ],
    "BAT BF-BOF_H2 PCI": [
        "BAT BF-BOF_H2 PCI",
        "BAT BF-BOF+CCUS",
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCU",
        "DRI-Melt-BOF_100% zero-C H2",
        "DRI-Melt-BOF+CCUS",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
        "Smelting Reduction+CCUS",
        "EAF",
        "Electrolyzer-EAF",
        "Electrowinning-EAF",
    ],
    "DRI-Melt-BOF": [
        "DRI-Melt-BOF",
        "DRI-Melt-BOF_100% zero-C H2",
        "DRI-Melt-BOF+CCUS",
    ],
    "DRI-EAF": [
        "DRI-EAF",
        "DRI-EAF_50% bio-CH4",
        "DRI-EAF_50% green H2",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
        "Smelting Reduction",
        "Smelting Reduction+CCUS",
        "Electrolyzer-EAF",
        "Electrowinning-EAF",
    ],
    "DRI-EAF_50% bio-CH4": [
        "DRI-EAF_50% bio-CH4",
        "Smelting Reduction+CCUS",
        "Electrolyzer-EAF",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
    ],
    "DRI-EAF_50% green H2": [
        "DRI-EAF_50% green H2",
        "Smelting Reduction+CCUS",
        "Electrolyzer-EAF",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
    ],
    "Smelting Reduction": [
        "Smelting Reduction",
        "Smelting Reduction+CCUS",
    ],
    "BAT BF-BOF+CCUS": ["BAT BF-BOF+CCUS"],
    "BAT BF-BOF+BECCUS": ["BAT BF-BOF+BECCUS"],
    "BAT BF-BOF+CCU": ["BAT BF-BOF+CCU"],
    "DRI-Melt-BOF_100% zero-C H2": ["DRI-Melt-BOF_100% zero-C H2"],
    "DRI-Melt-BOF+CCUS": ["DRI-Melt-BOF+CCUS"],
    "DRI-EAF+CCUS": ["DRI-EAF+CCUS"],
    "DRI-EAF_100% green H2": ["DRI-EAF_100% green H2"],
    "Smelting Reduction+CCUS": ["Smelting Reduction+CCUS"],
    "EAF": ["EAF"],
    "Electrolyzer-EAF": ["Electrolyzer-EAF"],
    "Electrowinning-EAF": ["Electrowinning-EAF"],
}

TECH_REFERENCE_LIST = list(SWITCH_DICT.keys())

TECHNOLOGY_PHASES: MYPY_DICT_STR_LIST = {
    "initial": ["Avg BF-BOF"],
    "transitional": [
        "BAT BF-BOF",
        "BAT BF-BOF_bio PCI",
        "BAT BF-BOF_H2 PCI",
        "DRI-EAF",
        "DRI-EAF_50% bio-CH4",
        "DRI-EAF_50% green H2",
        "Smelting Reduction",
        "DRI-Melt-BOF",
    ],
    "end_state": [
        "BAT BF-BOF+CCUS",
        "DRI-EAF_100% green H2",
        "DRI-EAF+CCUS",
        "EAF",
        "BAT BF-BOF+CCU",
        "BAT BF-BOF+BECCUS",
        "Electrolyzer-EAF",
        "Smelting Reduction+CCUS",
        "DRI-Melt-BOF+CCUS",
        "DRI-Melt-BOF_100% zero-C H2",
        "Electrowinning-EAF",
    ],
}

TECHNOLOGIES_TO_DROP = ["Charcoal mini furnace", "Close plant"]

# GRAPH REFRENCE LISTS

MPP_COLOR_LIST = [
    "#A0522D",
    "#7F6000",
    "#1E3B63",
    "#9DB1CF",
    "#FFC000",
    "#59A270",
    "#BCDAC6",
    "#E76B67",
    "#A5A5A5",
    "#F2F2F2",
]

GRAPH_CAPEX_OPEX_DICT_SPLIT: MYPY_DICT_STR_LIST = {
    "Feedstock": ["Iron Ore", "Scrap", "DRI"],
    "Fossil Fuels": [
        "Met coal",
        "Coke",
        "Thermal coal",
        "BF gas",
        "BOF gas",
        "Natural gas",
        "Plastic waste",
    ],
    "Bio Fuels": ["Biomass", "Biomethane"],
    "Hydrogen": ["Hydrogen"],
    "Electricity": ["Electricity"],
    "CCS": ["CCS"],
    "Other OPEX": [
        ["Other OPEX"],
        ["Steam", "BF slag"],
    ],  # attention! BF slag is a co product that is sold of to other industry sectors and produces revenue (so its negative costs added to the OPEX sum which reduces the actual result of other OPEX)
    "BF Capex": ["BF Capex"],  # with WACC over 20 years
    "GF Capex": ["GF Capex"],  # with WACC over 20 years
}

GRAPH_COL_ORDER = [
    "Avg BF-BOF",
    "BAT BF-BOF",
    "DRI-EAF",
    "BAT BF-BOF_H2 PCI",
    "BAT BF-BOF_bio PCI",
    "DRI-EAF_50% bio-CH4",
    "DRI-EAF_50% green H2",
    "DRI-Melt-BOF",
    "Smelting Reduction",
    "BAT BF-BOF+CCUS",
    "BAT BF-BOF+CCU",
    "BAT BF-BOF+BECCUS",
    "DRI-EAF+CCUS",
    "DRI-EAF_100% green H2",
    "DRI-Melt-BOF+CCUS",
    "DRI-Melt-BOF_100% zero-C H2",
    "Electrolyzer-EAF",
    "Electrowinning-EAF",
    "Smelting Reduction+CCUS",
    "EAF",
]

# BUSINESS CASE UNITS
GJ_RESOURCES = [
    "BF gas",
    "COG",
    "BOF gas",
    "Natural gas",
    "Plastic waste",
    "Biomass",
    "Biomethane",
    "Hydrogen",
    "Electricity",
    "Steam",
    "Coke",
    "Thermal coal",
]

KG_RESOURCES = ["BF slag", "Other slag"]

TON_RESOURCES = [
    "Iron ore",
    "Scrap",
    "DRI",
    "Met coal",
    "Process emissions",
    "Emissivity wout CCS",
    "Captured CO2",
    "Used CO2",
    "Emissivity",
]

WESTERN_EUROPE_COUNTRIES = [
    "ITA",
    "AND",
    "SMR",
    "PRT",
    "AUT",
    "BEL",
    "DNK",
    "FRO",
    "FRA",
    "DEU",
    "ISL",
    "IRL",
    "IMN",
    "LIE",
    "LUX",
    "MCO",
    "NLD",
    "NOR",
    "SWE",
    "CHE",
    "ESP",
    "GBR",
]

EASTERN_EUROPE_COUNTRIES = [
    "GEO",
    "ALB",
    "BLR",
    "BIH",
    "BGR",
    "HRV",
    "CZE",
    "EST",
    "FIN",
    "GIB",
    "GRC",
    "VAT",
    "HUN",
    "LVA",
    "LTU",
    "MKD",
    "MLT",
    "MNE",
    "POL",
    "MDA",
    "ROU",
    "SRB",
    "SVK",
    "SVN",
    "UKR",
]

EU_COUNTRIES = [
    "AUT",
    "BEL",
    "BGR",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "HUN",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "ESP",
    "SWE",
]

CIS_COUNTRIES = [
    "ARM",
    "AZE",
    "BLR",
    "KAZ",
    "KGZ",
    "MDA",
    "TJK",
    "TKM",
    "UKR",
    "UZB",
    "RUS",
]

NAFTA_COUNTRIES = ["BMU", "CAN", "GRL", "MEX", "SPM", "USA"]

MIDDLE_EAST_COUNTRIES = [
    "BHR",
    "CYP",
    "EGY",
    "IRN",
    "IRQ",
    "ISR",
    "JOR",
    "KWT",
    "LBN",
    "OMN",
    "PSE",
    "QAT",
    "SAU",
    "SYR",
    "TUR",
    "ARE",
    "YEM",
]

SOUTHEAST_ASIA_COUNTRIES = [
    "BRN",
    "KHM",
    "TLS",
    "IDN",
    "LAO",
    "MYS",
    "MMR",
    "PHL",
    "SGP",
    "THA",
    "VNM",
]

CENTRAL_ASIA_COUNTRIES = ["KAZ", "KGZ", "TJK", "TKM", "UZB"]

SOUTH_ASIA_COUNTRIES = ["AFG", "BGD", "BTN", "IND", "IRN", "MDV", "NPL", "PAK", "LKA"]

NORTH_ASIA_COUNTRIES = ["CHN", "HKG", "MAC", "MNG", "KOR", "TWN"]

JAPAN_SOUTHKOREA_TAIWAN = ["JPN", "PRK", "TWN"]

ALL_ASIA_COUNTRIES = (
    CENTRAL_ASIA_COUNTRIES
    + SOUTH_ASIA_COUNTRIES
    + NORTH_ASIA_COUNTRIES
    + JAPAN_SOUTHKOREA_TAIWAN
)

ALL_EUROPE_COUNTRIES = WESTERN_EUROPE_COUNTRIES + EASTERN_EUROPE_COUNTRIES

REGION_LIST = [
    "Africa",
    "China",
    "CIS",
    "Europe",
    "India",
    "Japan, South Korea, and Taiwan",
    "Middle East",
    "NAFTA",
    "RoW",
    "South and Central America",
    "Southeast Asia",
]

PKL_FILE_RESULTS_REFERENCE = {
    "intermediate_data": [
        "tco_summary_data",
        "emissivity_abatement_switches",
        "variable_costs_regional",
        "calculated_emissivity_combined",
    ],
    "final_data": [
        "cost_of_steelmaking",
        "cumulative_investment_results",
        "global_metaresults",
        "green_capacity_ratio",
        "investment_results",
        "levelized_cost_results",
        "production_emissions",
        "production_resource_usage",
    ],
}

MULTI_RUN_MULTI_SCENARIO_SUMMARY_FILENAMES = [
    "production_emissions_summary",
    "production_resource_usage_summary",
    "plant_capacity_summary",
    "plant_capacity_summary_country_breakdown",
    "cost_of_steelmaking_summary",
    "investment_results_summary",
    "levelized_cost_standardized_summary",
    "calculated_emissivity_combined_summary",
    "full_trade_summary",
    "plant_result_df",
]

# FORMATTED DATA
FORMATTED_PKL_FILES = ["capex_switching_df"]

# OUTPUT FILE NAMES
INTERMEDIATE_RESULT_PKL_FILES = [
    "plant_result_df",
    "calculated_emissivity_combined",
    "levelized_cost_standardized",
    "emissivity_abatement_switches",
    "tco_summary_data",
    "full_trade_summary",
    "tech_choice_records",
    "tech_rank_records",
]

FINAL_RESULT_PKL_FILES = [
    "production_resource_usage",
    "production_emissions",
    "global_metaresults",
    "investment_results",
    "green_capacity_ratio",
    "cost_of_steelmaking",
    "levelized_cost_results",
]

ITERATION_FILES_TO_AGGREGATE = [
    "production_resource_usage",
    "production_emissions",
    "investment_results",
    "cost_of_steelmaking",
    "calculated_emissivity_combined",
    "tco_summary_data",
]

SCENARIO_SETTINGS_TO_ITERATE = [
    "carbon_tax_scenario",
    "hydrogen_cost_scenario",
    "electricity_cost_scenario",
    "steel_demand_scenario",
    "grid_scenario",
]
