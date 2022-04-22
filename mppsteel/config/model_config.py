"""Config file for model parameters"""

# PATH NAMES
CORE_DATA_PATH = "mppsteel/data"
LOG_PATH = "logs/"
TEST_FOLDER = "tests/"
IMPORT_DATA_PATH = f"{CORE_DATA_PATH}/import_data"
OUTPUT_FOLDER = f"{CORE_DATA_PATH}/output_data"
PKL_FOLDER = f"{CORE_DATA_PATH}/pkl_data"
PKL_DATA_IMPORTS = f"{PKL_FOLDER}/imported_data"
PKL_DATA_FORMATTED = f"{PKL_FOLDER}/formatted_import_data"
PKL_DATA_INTERMEDIATE = f"{PKL_FOLDER}/intermediate_data"
PKL_DATA_FINAL = f"{PKL_FOLDER}/final_data"

FOLDERS_TO_CHECK_IN_ORDER = [
    # Top level folders
    CORE_DATA_PATH,
    LOG_PATH,
    TEST_FOLDER,
    # Second level folders
    IMPORT_DATA_PATH,
    PKL_FOLDER,
    OUTPUT_FOLDER,
    # Third level folders
    PKL_DATA_IMPORTS,
    PKL_DATA_FORMATTED,
    PKL_DATA_INTERMEDIATE,
    PKL_DATA_FINAL,
]

# MODEL YEAR PARAMETERS
MODEL_YEAR_START = 2020
MODEL_YEAR_END = 2050
MODEL_YEAR_RANGE = range(MODEL_YEAR_START, MODEL_YEAR_END + 1)
CARBON_TAX_START_YEAR = 2023
GREEN_PREMIUM_START_YEAR = 2023
TECH_MORATORIUM_DATE = 2030
NET_ZERO_TARGET = 2050

# FINANCIAL PARAMETERS
DISCOUNT_RATE = 0.07
USD_TO_EUR_CONVERSION_DEFAULT = 0.877
SWITCH_CAPEX_DATA_POINTS = {
    "2020": 319.249187119815,
    "2030": 319.249187119815,
    "2050": 286.218839300307,
}

# INVESTMENT PARAMETERS
STEEL_PLANT_LIFETIME_YEARS = 40
INVESTMENT_CYCLE_DURATION_YEARS = 20
INVESTMENT_CYCLE_VARIANCE_YEARS = 3
INVESTMENT_OFFCYCLE_BUFFER_TOP = 3
INVESTMENT_OFFCYCLE_BUFFER_TAIL = 8
NET_ZERO_VARIANCE_YEARS = 3

# CONVERSION FACTORS: WEIGHT
GIGATON_TO_MEGATON_FACTOR = 1000
MEGATON_TO_KILOTON_FACTOR = 1000
KILOTON_TO_TON_FACTOR = 1000
TON_TO_KILOGRAM_FACTOR = 1000
MEGATON_TO_TON = MEGATON_TO_KILOTON_FACTOR * KILOTON_TO_TON_FACTOR
BILLION_NUMBER = 1000000000

# CONVERSION FACTORS: ENERGY
EXAJOULE_TO_PETAJOULE = 1000
PETAJOULE_TO_TERAJOULE = 1000
TERAJOULE_TO_GIGAJOULE = 1000
GIGAJOULE_TO_MEGAJOULE_FACTOR = 1000
PETAJOULE_TO_GIGAJOULE = PETAJOULE_TO_TERAJOULE * TERAJOULE_TO_GIGAJOULE
EXAJOULE_TO_GIGAJOULE = EXAJOULE_TO_PETAJOULE * PETAJOULE_TO_TERAJOULE * TERAJOULE_TO_GIGAJOULE

# ENERGY DENSITY FACTORS
BIOMASS_ENERGY_DENSITY_GJ_PER_TON = 18
EMISSIONS_FACTOR_SLAG = 0.55
MEGAWATT_HOURS_TO_GIGAJOULES = 3.6
TERAWATT_TO_PETAJOULE_FACTOR = 3.6
MET_COAL_ENERGY_DENSITY_MJ_PER_KG = 28
HYDROGEN_ENERGY_DENSITY_MJ_PER_KG = 120
PLASTIC_WASTE_ENERGY_DENSITY_MJ_PER_KG = 45

# CAPACITY UTILIZATION PARAMETERS
CAPACITY_UTILIZATION_CUTOFF_FOR_NEW_PLANT_DECISION = 0.95
CAPACITY_UTILIZATION_CUTOFF_FOR_CLOSING_PLANT_DECISION = 0.6
SCRAP_OVERSUPPLY_CUTOFF_FOR_NEW_EAF_PLANT_DECISION = 0.15
RELATIVE_REGIONAL_COST_BOUNDARY_FROM_MEAN_PCT = 0.1

# TECHNOLOGY RANKING FACTORS
TCO_RANK_2_SCALER = 1.3
TCO_RANK_1_SCALER = 1.1
ABATEMENT_RANK_2 = 2.37656461606311  # Switching from Avg BF-BOF to BAT BF-BOF+CCUS
ABATEMENT_RANK_3 = 0.932690243851946  # Switching from Avg BF-BOF to BAT BF-BOF_bio PCI

# REGIONAL PARAMETERS
MAIN_REGIONAL_SCHEMA = 'rmi_region'
RESULTS_REGIONS_TO_MAP = ["continent", "wsa", "rmi"]

# OUTPUT FILE NAMES
INTERMEDIATE_RESULT_PKL_FILES = [
    "plant_result_df",
    "calculated_emissivity_combined",
    "levelized_cost",
    "emissivity_abatement_switches",
    "tco_summary_data",
    "trade_summary_results"
]

FINAL_RESULT_PKL_FILES = [
    "production_resource_usage",
    "production_emissions",
    "global_metaresults",
    "investment_results",
    'green_capacity_ratio'
]
