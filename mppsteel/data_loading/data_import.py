"""Manages data imports"""
# For Data Manipulation
import pandas as pd

# For logger and units dict
from mppsteel.utility.utils import get_logger, extract_data, serialize_df_dict, timer_func

# Get model parameters
from mppsteel.model_config import IMPORT_DATA_PATH, PKL_DATA_IMPORTS, PE_MODEL_FILENAME_DICT, PE_MODEL_SHEETNAME_DICT

# Create logger
logger = get_logger("Data Import")


def replace_rows(df: pd.DataFrame, header_row: int) -> pd.DataFrame:
    """For WSA trade data, this function replaces the column names with the appropriate row.

    Args:
        df (DataFrame): The unformatted DataFrame
        header_row (int): The row that the DataFrame should start from.

    Returns:
        DataFrame: A reformatted DataFrame
    """
    df_c = df.copy()
    new_header = df_c.iloc[header_row]  # grab the first row for the header
    df_c = df[header_row + 1 :]  # take the data less the header row
    df_c.columns = new_header  # set the header row as the df header
    return df_c


def get_pe_model_data(model_name: str):
    def get_path(model_name: str, filenames_dict: dict):
        return f'{IMPORT_DATA_PATH}/{filenames_dict[model_name]}'
    datapath = get_path(model_name, PE_MODEL_FILENAME_DICT)
    return pd.read_excel(datapath, sheet_name=PE_MODEL_SHEETNAME_DICT[model_name])

@timer_func
def load_data(serialize_only: bool = False) -> dict:
    """Loads all the data you specify when the function is called.

    Args:
        serialize_only (bool, optional): Flag to only serialize the dict to a pickle file and not return a dict. Defaults to False.

    Returns:
        dict: A dictionary with all the data
    """
    # Import capex numbers
    greenfield_capex = extract_data(
        IMPORT_DATA_PATH, "CAPEX OPEX Per Technology", "xlsx", 0
    )
    brownfield_capex = extract_data(
        IMPORT_DATA_PATH, "CAPEX OPEX Per Technology", "xlsx", 1
    )
    other_opex = extract_data(IMPORT_DATA_PATH, "CAPEX OPEX Per Technology", "xlsx", 2)

    # Import ccs co2 capacity numbers
    ccs_co2 = extract_data(IMPORT_DATA_PATH, "CO2 CCS Capacity", "csv")

    # Import country reference
    country_ref = extract_data(IMPORT_DATA_PATH, "Country Reference", "xlsx").fillna("")

    # Import emissions factors
    s1_emissions_factors = extract_data(
        IMPORT_DATA_PATH, "Scope 1 Emissions Factors", "xlsx"
    )

    # Import scope 3 EF data
    s3_emissions_factors_1 = extract_data(
        IMPORT_DATA_PATH, "Scope 3 Emissions Factors", "xlsx", 0
    )
    s3_emissions_factors_2 = pd.read_excel(
        f"{IMPORT_DATA_PATH}/Scope 3 Emissions Factors.xlsx", sheet_name=1, skiprows=1
    )

    # Import grid emissivity
    grid_emissivity = extract_data(IMPORT_DATA_PATH, "Grid Emissivity", "xlsx")

    # Import static energy prices
    static_energy_prices = extract_data(
        IMPORT_DATA_PATH, "Energy Prices - Static", "xlsx"
    )

    # Import feedstock prices
    feedstock_prices = extract_data(IMPORT_DATA_PATH, "Feedstock Prices", "xlsx")

    # Import steel demand
    steel_demand = extract_data(IMPORT_DATA_PATH, "Steel Demand", "csv")

    # Import steel plant data
    steel_plants = extract_data(IMPORT_DATA_PATH, "Steel Plant Data Full", "xlsx")

    # Import technology availability
    tech_availability = extract_data(IMPORT_DATA_PATH, "Technology Availability", "csv")

    # Import power grid assumptions
    power_grid_assumptions = extract_data(
        IMPORT_DATA_PATH, "Power Grid Assumptions", "xlsx"
    )

    # Import technology availability
    carbon_tax_assumptions = extract_data(
        IMPORT_DATA_PATH, "Carbon Tax Assumptions", "csv"
    )

    # Import WSA data
    crude_regional_shares = extract_data(
        IMPORT_DATA_PATH, "WSA World Steel In Figures 2021", "xlsx", 0
    )
    crude_regional_real = extract_data(
        IMPORT_DATA_PATH, "WSA World Steel In Figures 2021", "xlsx", 1
    )
    iron_ore_pig_iron = extract_data(
        IMPORT_DATA_PATH, "WSA World Steel In Figures 2021", "xlsx", 2
    )

    crude_trade = replace_rows(
        extract_data(IMPORT_DATA_PATH, "WSA World Steel In Figures 2021", "xlsx", 3), 1
    ).fillna(0)
    iron_ore_trade = replace_rows(
        extract_data(IMPORT_DATA_PATH, "WSA World Steel In Figures 2021", "xlsx", 4), 1
    ).fillna(0)
    scrap_trade = replace_rows(
        extract_data(IMPORT_DATA_PATH, "WSA World Steel In Figures 2021", "xlsx", 5), 1
    ).fillna(0)

    # Import Technology Business Cases
    business_cases = replace_rows(
        extract_data(IMPORT_DATA_PATH, "Business Cases One Table", "xlsx"), 0
    ).fillna(0)

    # Import Hydrogen Electrolyzer Capex Data
    hydrogen_electrolyzer_capex = extract_data(
        IMPORT_DATA_PATH, "Hydrogen Electrolyzer Capex", "xlsx"
    )

    # Import Commodities Data
    ethanol_plastic_charcoal = extract_data(
        IMPORT_DATA_PATH, "Ethanol Plastic Charcoal", "csv"
    )

    # Import Regional Steel Demand Data
    regional_steel_demand = extract_data(
        IMPORT_DATA_PATH, "Regional Steel Demand", "csv"
    )

    # Import Price and Emissions Models
    power_model = get_pe_model_data('power')
    hydrogen_model = get_pe_model_data('hydrogen')
    ccus_model = get_pe_model_data('ccus')

    # Define a data dictionary
    df_dict = {
        "greenfield_capex": greenfield_capex,
        "brownfield_capex": brownfield_capex,
        "other_opex": other_opex,
        "ccs_co2": ccs_co2,
        "country_ref": country_ref,
        "s1_emissions_factors": s1_emissions_factors,
        "static_energy_prices": static_energy_prices,
        "feedstock_prices": feedstock_prices,
        "grid_emissivity": grid_emissivity,
        "steel_demand": steel_demand,
        "regional_steel_demand": regional_steel_demand,
        "steel_plants": steel_plants,
        "tech_availability": tech_availability,
        "crude_regional_real": crude_regional_real,
        "crude_regional_shares": crude_regional_shares,
        "iron_ore_pig_iron": iron_ore_pig_iron,
        "crude_trade": crude_trade,
        "iron_ore_trade": iron_ore_trade,
        "scrap_trade": scrap_trade,
        "s3_emissions_factors_1": s3_emissions_factors_1,
        "s3_emissions_factors_2": s3_emissions_factors_2,
        "business_cases": business_cases,
        "power_grid_assumptions": power_grid_assumptions,
        "hydrogen_electrolyzer_capex": hydrogen_electrolyzer_capex,
        "carbon_tax_assumptions": carbon_tax_assumptions,
        "ethanol_plastic_charcoal": ethanol_plastic_charcoal,
        "power_model": power_model,
        "hydrogen_model": hydrogen_model,
        "ccus_model": ccus_model,
    }

    if serialize_only:
        # Turn dataframes into pickle files
        serialize_df_dict(PKL_DATA_IMPORTS, df_dict)
        return
    return df_dict
