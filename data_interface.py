"""Functions to access data sources"""

from collections import namedtuple

# For Data Manipulation
import pandas as pd

# For logger and units dict
from utils import get_logger, read_pickle_folder

# Get model parameters
from model_config import PKL_FOLDER

# Create logger
logger = get_logger('Data Interface')

def melt_and_index(df: pd.DataFrame, id_vars: list, var_name: str, index: list) -> pd.DataFrame:
    """Make the dataframes tabular and create a multiindex

    Args:
        df (pd.DataFrame): The data import of the capex tables

    Returns:
        pd.DataFrame: A datframe of the tabular dataframe
    """
    df_c = df.copy()
    df_c = pd.melt(frame=df_c, id_vars=id_vars, var_name=var_name)
    df_c.set_index(index, inplace=True)
    return df_c

def capex_generator(
    capex_dict: dict, technology: str, year: int, output_type: str = 'all'):
    """Creates an interface to the tabular capex data.

    Args:
        capex_dict (dict): A capex dictionary with each capex type as a DataFrame
        technology (str): The technology that you want to access
        year (int): The year that you want to access
        output_type (str, optional): Flag whether to access all the the capex values or whichever you specify. Defaults to 'all'.

    Returns:
        A (dict) if output_type is set to 'all'.
        Otherwise returns the specific output_type specified (as float).
    """

    greenfield = capex_dictionary['greenfield'].loc[technology, year].value
    brownfield = capex_dictionary['brownfield'].loc[technology, year].value
    other_opex = capex_dictionary['other_opex'].loc[technology, year].value

    capex_dict = {
        'greenfield': greenfield,
        'brownfield': brownfield,
        'other_opex': other_opex
    }

    if output_type == 'all':
        logger.info(f'Creating capex values dictionary')
        return capex_dict
    logger.info(f'Creating capex value')
    return capex_dict[output_type]

def create_data_tuples(df: pd.DataFrame, namedtuple_name: str):
    """Generic function that dynamically create namedtuples from a dataframe.
    *** WARNING *** You won't see these namedtuples defined prior to creation so you have to be careful.

    Args:
        df (pd.DataFrame): DataFrame containing the data to translate into the namedtuples
        namedtuple_name (str): The name of the namedtuple that you want to create
    """
    df_c = df.copy()
    df_c.columns = [colname.lower() for colname in df_c.columns]
    class_names = [metric.upper().replace(' ', '_') for metric in df_c['metric'].to_list()]
    globals()[namedtuple_name] = namedtuple('namedtuple_name', ['metric', 'unit', 'year', 'value'])
    ticker = 0
    logger.info(f'Creating new namtedtuples with the following names: {class_names}')
    for row in df_c.itertuples():
        globals()[class_names[ticker]] = globals()[namedtuple_name](row.metric, row.unit, row.year, row.value)
        ticker+=1


greenfield_capex_df = read_pickle_folder(PKL_FOLDER, 'greenfield_capex')
brownfield_capex_df = read_pickle_folder(PKL_FOLDER, 'brownfield_capex')
other_opex_df = read_pickle_folder(PKL_FOLDER, 'other_opex')

brownfield_capex_df.drop(
    ['Available from', 'Available until', 'Technology type'], axis=1, inplace=True)

capex_dictionary = {
    'greenfield': melt_and_index(greenfield_capex_df, ['Technology'], 'Year', ['Technology', 'Year']),
    'brownfield': melt_and_index(brownfield_capex_df, ['Technology'], 'Year', ['Technology', 'Year']),
    'other_opex': melt_and_index(other_opex_df, ['Technology'], 'Year', ['Technology', 'Year'])
}

feedstock_prices = read_pickle_folder(PKL_FOLDER, 'feedstock_prices')

steel_demand = read_pickle_folder(PKL_FOLDER, 'steel_demand')[['Steel Type', 'Scenario', 'Year', 'Value']]

def steel_demand_getter(df: pd.DataFrame, steel_type: str, scenario: str, year: str):
    df_c = df.copy()
    df_c.set_index(['Steel Type', 'Scenario', 'Year'], inplace=True)
    logger.info(f'Getting Steel Demand value for: {steel_type} - {scenario} - {year}')
    value = df_c.loc[steel_type, scenario, year]['Value']
    return value

steel_demand_exmaple = steel_demand_getter(steel_demand, 'Crude', 'BAU', 2030)

carbon_tax_assumptions = read_pickle_folder(PKL_FOLDER, 'carbon_tax_assumptions')[['Year', 'Value']]

def carbon_tax_getter(df: pd.DataFrame, year: str):
    df_c = df.copy()
    df_c.set_index(['Year'], inplace=True)
    logger.info(f'Getting Carbon Tax value for: {year}')
    value = df_c.loc[year]['Value']
    return value

print(carbon_tax_getter(carbon_tax_assumptions, 2040))

steel_demand_example = steel_demand_getter(steel_demand, 'Crude', 'BAU', 2030)

create_data_tuples(feedstock_prices, 'FeedstockPrices')
