"""Investment Results generator for technology investments"""

import pandas as pd
from tqdm import tqdm

from mppsteel.model_config import (
    MODEL_YEAR_START,
    PKL_DATA_INTERMEDIATE,
    PKL_DATA_FINAL
)

from mppsteel.utility.utils import (
    read_pickle_folder, get_logger, serialize_file,
    timer_func, add_results_metadata,
)

from mppsteel.data_loading.steel_plant_formatter import map_plant_id_to_df

# Create logger
logger = get_logger("Investment Results")

def create_capex_dict():
    """[summary]

    Returns:
        [type]: [description]
    """
    capex = read_pickle_folder(PKL_DATA_INTERMEDIATE, 'capex_switching_df', 'df')
    capex_c = capex.copy()
    capex_c.reset_index(inplace=True)
    capex_c.columns = [col.lower().replace(' ', '_') for col in capex_c.columns]
    return capex_c.set_index(['year', 'start_technology']).sort_index()

def get_capex_ref(capex_df: pd.DataFrame, year: int, start_tech: str, new_tech: str, switch_type: str):
    """[summary]

    Args:
        capex_df (pd.DataFrame): [description]
        year (int): [description]
        start_tech (str): [description]
        new_tech (str): [description]

    Returns:
        [type]: [description]
    """    
    capex_year = year
    if year > 2050:
        capex_year = 2050
    if new_tech == 'Close plant':
        return 0
    if switch_type == 'no switch':
        return 0
    capex_ref = capex_df.loc[capex_year, start_tech]
    return capex_ref.loc[capex_ref['new_technology'] == new_tech]['value'].values[0]

def investment_switch_getter(inv_df: pd.DataFrame, year: int, plant_name: str):
    """[summary]

    Args:
        inv_df (pd.DataFrame): [description]
        year (int): [description]
        plant_name (str): [description]

    Returns:
        [type]: [description]
    """    
    inv_df_ref = inv_df.reset_index().set_index(['year', 'plant_name']).sort_values(['year'])
    return inv_df_ref.loc[year, plant_name].values[0]

def get_tech_choice(tc_dict: dict, year: int, plant_name: str):
    """[summary]

    Args:
        tc_dict (dict): [description]
        year (int): [description]
        plant_name (str): [description]

    Returns:
        [type]: [description]
    """    
    return tc_dict[str(year)][plant_name]

def investment_row_calculator(inv_df: pd.DataFrame, capex_df: pd.DataFrame, tech_choices: dict, plant_name: str, country_code: str, year: int, capacity_value: float):
    """[summary]

    Args:
        inv_df (pd.DataFrame): [description]
        capex_df (pd.DataFrame): [description]
        tech_choices (dict): [description]
        plant_name (str): [description]
        country_code (str): [description]
        year (int): [description]
        production_value (float) [description]

    Returns:
        [type]: [description]
    """
    switch_type = investment_switch_getter(inv_df, year, plant_name)

    if year == 2020:
        start_tech = get_tech_choice(tech_choices, 2020, plant_name)
    else:
        start_tech = get_tech_choice(tech_choices, year-1, plant_name)

    new_tech = get_tech_choice(tech_choices, year, plant_name)
    capex_ref = get_capex_ref(capex_df, year, start_tech, new_tech, switch_type)
    actual_capex = capex_ref * (capacity_value * 1000 * 1000) # convert from Mt to T
    new_row = {
        'steel_plant' : plant_name,
        'country_code': country_code,
        'year': year,
        'start_tech': start_tech,
        'end_tech': new_tech,
        'switch_type': switch_type,
        'capital_cost': actual_capex,
    }
    return new_row

def production_stats_getter(df: pd.DataFrame, year: int, plant_name, value_col: str):
    df_c = df.copy()
    df_c.set_index(['year', 'steel_plant'], inplace=True)
    return df_c.xs((year, plant_name))[value_col]

@timer_func
def investment_results(scenario_dict: dict, serialize_only: bool = False):
    """[summary]

    Args:
        serialize_only (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """    
    logger.info(f'Generating Investment Results')
    tech_choice_dict = read_pickle_folder(PKL_DATA_INTERMEDIATE, 'tech_choice_dict', 'df')
    plant_investment_cycles = read_pickle_folder(PKL_DATA_INTERMEDIATE, 'plant_investment_cycles', 'df')
    steel_plant_df = read_pickle_folder(PKL_DATA_INTERMEDIATE, 'steel_plants_processed', 'df')
    plant_names_and_country_codes = zip(steel_plant_df['plant_name'].values, steel_plant_df['country_code'].values)
    production_stats_all = read_pickle_folder(PKL_DATA_FINAL, 'production_stats_all', 'df')
    capex_df = create_capex_dict()
    max_year = max([int(year) for year in tech_choice_dict.keys()])
    year_range = range(MODEL_YEAR_START, max_year+1)
    data_container = []
    for plant_name, country_code in tqdm(plant_names_and_country_codes, total=len(steel_plant_df), desc='Steel Plant Investments'):
        for year in year_range:
            capacity_value = production_stats_getter(production_stats_all, year, plant_name, 'capacity')
            data_container.append(
                investment_row_calculator(
                    plant_investment_cycles, capex_df, tech_choice_dict, plant_name, country_code, year, capacity_value))

    investment_results = pd.DataFrame(data_container).set_index(['year']).sort_values('year')
    investment_results.reset_index(inplace=True)
    investment_results = map_plant_id_to_df(investment_results, 'plant_name')
    investment_results = add_results_metadata(investment_results, scenario_dict, single_line=True)

    if serialize_only:
        logger.info(f'-- Serializing dataframes')
        serialize_file(investment_results, PKL_DATA_FINAL, "investment_results")
    return investment_results
