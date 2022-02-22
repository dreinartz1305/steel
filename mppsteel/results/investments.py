"""Investment Results generator for technology investments"""
from typing import Union

import pandas as pd
from tqdm import tqdm

from mppsteel.config.model_config import (
    MODEL_YEAR_START,
    MODEL_YEAR_END,
    PKL_DATA_INTERMEDIATE,
    PKL_DATA_FINAL,
)

from mppsteel.utility.function_timer_utility import timer_func
from mppsteel.utility.dataframe_utility import add_results_metadata
from mppsteel.utility.file_handling_utility import read_pickle_folder, serialize_file
from mppsteel.utility.log_utility import get_logger
from mppsteel.data_loading.steel_plant_formatter import map_plant_id_to_df
from mppsteel.results.production import get_tech_choice

# Create logger
logger = get_logger("Investment Results")


def create_capex_dict() -> pd.DataFrame:
    """Creates a reformatted and reindexed Capex Switching DataFrame.

    Returns:
        pd.DataFrame: A reformatted and reindexed Capex Switching DataFrame.
    """
    capex = read_pickle_folder(PKL_DATA_INTERMEDIATE, "capex_switching_df", "df")
    capex_c = capex.copy()
    capex_c.reset_index(inplace=True)
    capex_c.columns = [col.lower().replace(" ", "_") for col in capex_c.columns]
    return capex_c.set_index(["year", "start_technology"]).sort_index()


def capex_getter_f(
    capex_df: pd.DataFrame, year: int, start_tech: str, new_tech: str, switch_type: str
) -> float:
    """Returns a capex value from a reference DataFrame taking into consideration edge cases.

    Args:
        capex_df (pd.DataFrame): The capex reference DataFrame.
        year (int): The year you want to retrieve values for.
        start_tech (str): The initial technology used.
        new_tech (str): The desired switch technology.
        switch_type (str): The type of technology switch [`no switch`, `trans switch`, `main cycle`].

    Returns:
        float: A value containing the capex value based on the function arguments.
    """
    capex_year = min(MODEL_YEAR_END, year)
    if new_tech == "Close plant":
        return 0
    if switch_type == "no switch":
        return 0
    capex_ref = capex_df.loc[capex_year, start_tech]
    return capex_ref.loc[capex_ref["new_technology"] == new_tech]["value"].values[0]


def investment_switch_getter(
    inv_df: pd.DataFrame, year: int, plant_name: str
) -> str:
    """Returns the switch type of an investment made in a particular year for a particular plant.

    Args:
        inv_df (pd.DataFrame): The Investment cycle reference DataFrame.
        year (int): The year that you want to reference.
        plant_name (str): The name of the reference plant.

    Returns:
        str: The switch type [`no switch`, `trans switch`, `main cycle`].
    """
    inv_df_ref = (
        inv_df.reset_index().set_index(["year", "plant_name"]).sort_values(["year"])
    )
    return inv_df_ref.loc[year, plant_name].values[0]


def investment_row_calculator(
    inv_df: pd.DataFrame,
    capex_df: pd.DataFrame,
    tech_choices: dict,
    plant_name: str,
    country_code: str,
    year: int,
    capacity_value: float,
) -> dict:
    """_summary_

    Args:
        inv_df (pd.DataFrame): The Investment cycle reference DataFrame.
        capex_df (pd.DataFrame): A switch capex reference. 
        tech_choices (dict): Dictionary containing all technology choices for every plant across every year.
        plant_name (str): The name of the reference plant.
        country_code (str): Country code of the plant.
        year (int): The year that you want to reference.
        capacity_value (float): The value of the plant capacity.

    Returns:
        dict: A dictionary containing the column-value pairs to be inserted in a DataFrame.
    """
    switch_type = investment_switch_getter(inv_df, year, plant_name)

    if year == 2020:
        start_tech = get_tech_choice(tech_choices, 2020, plant_name)
    else:
        start_tech = get_tech_choice(tech_choices, year - 1, plant_name)

    new_tech = get_tech_choice(tech_choices, year, plant_name)
    capex_ref = capex_getter_f(capex_df, year, start_tech, new_tech, switch_type)
    actual_capex = capex_ref * (capacity_value * 1000 * 1000)  # convert from Mt to T
    return {
        "plant_name": plant_name,
        "country_code": country_code,
        "year": year,
        "start_tech": start_tech,
        "end_tech": new_tech,
        "switch_type": switch_type,
        "capital_cost": actual_capex,
    }


def production_stats_getter(
    df: pd.DataFrame, year: int, plant_name, value_col: str
) -> float:
    """Returns a specified stat from the Production DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame of the Production Statistics containing resource usage.
        year (int): The year that you want to reference.
        plant_name (_type_): The name of the reference plant.
        value_col (str): The column containing the value you want to reference.

    Returns:
        float: The value of the value_col passed as a function argument.
    """
    df_c = df.copy()
    df_c.set_index(["year", "plant_name"], inplace=True)
    return df_c.xs((year, plant_name))[value_col]


def create_inv_stats(
    df: pd.DataFrame, results: str = "global", agg: bool = False, operation: str = "sum"
) -> Union[pd.DataFrame, dict]:
    """Generates an statistics column for an Investment DataFrame according to parameters set in the function arguments.

    Args:
        df (pd.DataFrame): The initial Investments DataFrame.
        results (str, optional): Specifies the desired regional results [`regional` or `global`]. Defaults to "global".
        agg (bool, optional): Determines whether to aggregate regional results as a DataFrame. Defaults to False.
        operation (str, optional): Determines the type of operation to be conducted for the new stats column [`sum` or `cumsum` for cumulative sum]. Defaults to "sum".

    Returns:
        Union[pd.DataFrame, dict]: Returns a DataFrame if `results` is set to `global`. Returns a dict of regional results if `results` is set to `regional` and `agg` is set to False.
    """

    df_c = df[
        [
            "year",
            "plant_name",
            "country_code",
            "start_tech",
            "end_tech",
            "switch_type",
            "capital_cost",
            "region_wsa_region",
        ]
    ].copy()

    def create_global_stats(df, operation: str = "sum"):
        calc = df_c.groupby(["year"]).sum()
        if operation == "sum":
            return calc
        if operation == "cumsum":
            return calc.cumsum()

    if results == "global":
        return create_global_stats(df_c, operation).reset_index()

    if results == "regional":
        regions = df_c["region_wsa_region"].unique()
        region_dict = {}
        for region in regions:
            calc = df_c[df_c["region_wsa_region"] == region].groupby(["year"]).sum()
            if operation == "sum":
                pass
            if operation == "cumsum":
                calc = calc.cumsum()
            region_dict[region] = calc
        if agg:
            df_list = []
            for region_key in region_dict:
                df_r = region_dict[region_key]
                df_r["region"] = region_key
                df_list.append(df_r[["region", "capital_cost"]])
            return pd.concat(df_list).reset_index()
        return region_dict


@timer_func
def investment_results(scenario_dict: dict, serialize: bool = False) -> pd.DataFrame:
    """Complete Investment Results Flow to generate the Investment Results References DataFrame.

    Args:
        scenario_dict (dict): A dictionary with scenarios key value mappings from the current model execution.
        serialize (bool, optional): Flag to only serialize the dict to a pickle file and not return a dict. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the investment results.
    """
    logger.info("Generating Investment Results")
    tech_choice_dict = read_pickle_folder(
        PKL_DATA_INTERMEDIATE, "tech_choice_dict", "df"
    )
    plant_investment_cycles = read_pickle_folder(
        PKL_DATA_INTERMEDIATE, "plant_investment_cycles", "df"
    )
    steel_plant_df = read_pickle_folder(
        PKL_DATA_INTERMEDIATE, "steel_plants_processed", "df"
    )
    plant_names_and_country_codes = zip(
        steel_plant_df["plant_name"].values, steel_plant_df["country_code"].values
    )
    production_resource_usage = read_pickle_folder(
        PKL_DATA_FINAL, "production_resource_usage", "df"
    )
    capex_df = create_capex_dict()
    max_year = max([int(year) for year in tech_choice_dict])
    year_range = range(MODEL_YEAR_START, max_year + 1)
    data_container = []
    for plant_name, country_code in tqdm(
        plant_names_and_country_codes,
        total=len(steel_plant_df),
        desc="Steel Plant Investments",
    ):
        for year in year_range:
            capacity_value = production_stats_getter(
                production_resource_usage, year, plant_name, "capacity"
            )
            data_container.append(
                investment_row_calculator(
                    plant_investment_cycles,
                    capex_df,
                    tech_choice_dict,
                    plant_name,
                    country_code,
                    year,
                    capacity_value,
                )
            )

    investment_results = (
        pd.DataFrame(data_container).set_index(["year"]).sort_values("year")
    )
    investment_results.reset_index(inplace=True)
    investment_results = map_plant_id_to_df(investment_results, "plant_name")
    investment_results = add_results_metadata(
        investment_results, scenario_dict, single_line=True
    )
    cumulative_investment_results = create_inv_stats(
        investment_results, results="regional", agg=True, operation="cumsum"
    )

    if serialize:
        logger.info(f"-- Serializing dataframes")
        serialize_file(investment_results, PKL_DATA_FINAL, "investment_results")
        serialize_file(
            cumulative_investment_results,
            PKL_DATA_FINAL,
            "cumulative_investment_results",
        )
    return investment_results
