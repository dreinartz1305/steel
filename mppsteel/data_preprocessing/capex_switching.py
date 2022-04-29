"""Script for establishing capex switching values"""

# For Data Manipulation
import pandas as pd
from tqdm import tqdm

# For logger
from mppsteel.utility.function_timer_utility import timer_func
from mppsteel.utility.file_handling_utility import (
    read_pickle_folder, serialize_file
)
from mppsteel.utility.log_utility import get_logger

from mppsteel.config.model_config import (
    MODEL_YEAR_RANGE,
    PKL_DATA_FORMATTED,
    SWITCH_CAPEX_DATA_POINTS,
    MODEL_YEAR_START,
)

from mppsteel.config.reference_lists import (
    FURNACE_GROUP_DICT,
    TECH_REFERENCE_LIST,
    SWITCH_DICT,
)
from mppsteel.data_load_and_format.data_interface import capex_generator

# Create logger
logger = get_logger(__name__)


def create_switching_dfs(technology_list: list) -> dict:
    """Creates a dictionary that hold a DataFrame with three columns fo each tehnology passed to it in a list.

    Args:
        technology_list (list): A list of technologies that will be the dictionary keys.

    Returns:
        dict: A dictionary with each key as the technologies.
    """
    logger.info("Creating the base switching dict")
    df_dict = {}
    for technology in technology_list:
        df_temp = pd.DataFrame(
            data={
                "Start Technology": technology,
                "New Technology": technology_list,
                "value": "",
            }
        )
        df_dict[technology] = df_temp
    return df_dict


def get_capex_values(
    df_switching_dict: dict,
    capex_dict_ref: dict,
    single_year: int = None,
    year_end: int = 2021,
) -> pd.DataFrame:
    """Assign values to the a DataFrame based on start and potential switching technology.

    Args:
        df_switching_dict (dict): A dictionary with each technology as the key.
        capex_dict_ref (dict): A dictionary with greenfield, brownfield and other_opex values for each technology.

    Returns:
        pd.DataFrame: A dictionary with capex values for each technology.
    """
    logger.info("Generating the capex values for each technology")
    df_dict_c = df_switching_dict.copy()

    # Create a year range
    year_range = range(MODEL_YEAR_START, tuple({year_end + 1 or 2021})[0])
    if single_year:
        year_range = [single_year]

    year_list = []
    for year in tqdm(year_range, total=len(year_range), desc="Get Capex Values"):
        tech_list = []
        for technology in SWITCH_DICT:
            df_temp = df_dict_c[technology].copy()
            for new_technology in SWITCH_DICT[technology]:
                capex_difference = (
                    capex_generator(capex_dict_ref, new_technology, year)["greenfield"]
                    - capex_generator(capex_dict_ref, technology, year)["greenfield"]
                )
                if technology == new_technology:
                    brownfield_capex_value = capex_generator(
                        capex_dict_ref, technology, year
                    )["brownfield"]
                    df_temp.loc[
                        (df_temp["Start Technology"] == technology)
                        & (df_temp["New Technology"] == technology),
                        "value",
                    ] = brownfield_capex_value

                elif new_technology == "Close plant":
                    switch_capex_value = (
                        capex_generator(capex_dict_ref, technology, year)["greenfield"]
                        * 0.05
                    )
                    df_temp.loc[
                        (df_temp["Start Technology"] == technology)
                        & (df_temp["New Technology"] == new_technology),
                        "value",
                    ] = switch_capex_value

                else:
                    if (
                        technology in FURNACE_GROUP_DICT["blast_furnace"]
                        and new_technology in FURNACE_GROUP_DICT["blast_furnace"]
                    ):
                        if new_technology == "BAT BF-BOF":
                            switch_capex_value = capex_generator(
                                capex_dict_ref, new_technology, year
                            )["brownfield"]
                            df_temp.loc[
                                (df_temp["Start Technology"] == technology)
                                & (df_temp["New Technology"] == new_technology),
                                "value",
                            ] = switch_capex_value

                        elif (
                            new_technology == "BAT BF-BOF+CCUS"
                            or new_technology == "BAT BF-BOF+CCU"
                            or new_technology == "BAT BF-BOF+BECCUS"
                        ):
                        
                            switch_capex_value = (
                                capex_generator(capex_dict_ref, "BAT BF-BOF", year)[
                                "brownfield"
                                ]
                                + capex_difference
                                )
                            df_temp.loc[
                                (df_temp["Start Technology"] == technology)
                                & (df_temp["New Technology"] == new_technology),
                                "value",
                            ] = switch_capex_value

                        else:  # bio PCI or H2PCI
                            if technology == "Avg BF-BOF":
                                switch_capex_value = (
                                    capex_generator(capex_dict_ref, "BAT BF-BOF", year)[
                                    'brownfield'
                                    ]
                                )
                                df_temp.loc[
                                    (df_temp["Start Technology"] == technology)
                                    & (df_temp["New Technology"] == new_technology),
                                    "value",
                                ] = switch_capex_value

                            else:  # technology is BAT BF BOF
                                switch_capex_value = capex_generator(
                                    capex_dict_ref, technology, year
                                )["brownfield"]
                                df_temp.loc[
                                    (df_temp["Start Technology"] == technology)
                                    & (df_temp["New Technology"] == new_technology),
                                    "value",
                                ] = switch_capex_value

                    elif (
                        technology in FURNACE_GROUP_DICT["dri-bof"]
                        and new_technology in FURNACE_GROUP_DICT["dri-bof"]
                    ):
                        if new_technology == "DRI-Melt-BOF_100% zero-C H2":
                            switch_capex_value = capex_generator(
                                capex_dict_ref, technology, year
                            )["brownfield"]
                            df_temp.loc[
                                (df_temp["Start Technology"] == technology)
                                & (df_temp["New Technology"] == new_technology),
                                "value",
                            ] = switch_capex_value

                        else:  # 'DRI-Melt-BOF + CCUS'
                            switch_capex_value = (
                                capex_generator(capex_dict_ref, technology, year)[
                                    "brownfield"
                                ]
                                + capex_difference
                            )
                            df_temp.loc[
                                (df_temp["Start Technology"] == technology)
                                & (df_temp["New Technology"] == new_technology),
                                "value",
                            ] = switch_capex_value

                    elif (
                        technology in FURNACE_GROUP_DICT["dri-eaf"]
                        and new_technology in FURNACE_GROUP_DICT["dri-eaf"]
                    ):
                        if (
                            new_technology == "DRI-EAF_50% bio-CH4"
                            or new_technology == "DRI-EAF_50% green H2"
                            or new_technology == "DRI-EAF_100% green H2"
                        ):
                            switch_capex_value = capex_generator(
                                capex_dict_ref, technology, year
                            )["brownfield"]
                            df_temp.loc[
                                (df_temp["Start Technology"] == technology)
                                & (df_temp["New Technology"] == new_technology),
                                "value",
                            ] = switch_capex_value

                        else:  # new_technology='DRI-EAF+CCUS':
                            switch_capex_value = (
                                capex_generator(capex_dict_ref, technology, year)[
                                    "brownfield"
                                ]
                                + capex_difference
                            )
                            df_temp.loc[
                                (df_temp["Start Technology"] == technology)
                                & (df_temp["New Technology"] == new_technology),
                                "value",
                            ] = switch_capex_value

                    elif (
                        technology in FURNACE_GROUP_DICT["smelting_reduction"]
                        and new_technology in FURNACE_GROUP_DICT["smelting_reduction"]
                    ):
                        switch_capex_value = (
                            capex_generator(capex_dict_ref, technology, year)[
                                "brownfield"
                            ]
                            + capex_difference
                        )
                        df_temp.loc[
                            (df_temp["Start Technology"] == technology)
                            & (df_temp["New Technology"] == new_technology),
                            "value",
                        ] = switch_capex_value

                    elif (
                        technology in FURNACE_GROUP_DICT["blast_furnace"]
                        and new_technology in FURNACE_GROUP_DICT["dri-bof"]
                    ):
                        if new_technology== "DRI-Melt-BOF+CCUS":
                            switch_capex_value=(
                                capex_generator(capex_dict_ref, new_technology, year)[
                                    'greenfield'
                                ]
                                -460/4
                            )
                            df_temp.loc[
                            (df_temp["Start Technology"] == technology)
                            & (df_temp["New Technology"] == new_technology),
                            "value",
                        ] = switch_capex_value

                        elif new_technology == 'DRI-Melt-BOF' or new_technology =='DRI-Melt-BOF_100% zero-C H2':
                            switch_capex_value=(
                                capex_generator(capex_dict_ref, 'DRI-EAF', year)[
                                    'greenfield'
                                ]-
                                capex_generator(capex_dict_ref, 'EAF', year)[
                                    'greenfield'
                                ]
                            )
                            df_temp.loc[
                            (df_temp["Start Technology"] == technology)
                            & (df_temp["New Technology"] == new_technology),
                            "value",
                        ] = switch_capex_value
                    elif (
                        technology in FURNACE_GROUP_DICT['dri-eaf']
                        and new_technology in FURNACE_GROUP_DICT['eaf-advanced']
                    ):
                        switch_capex_value=(
                            capex_generator(capex_dict_ref, new_technology, year)[
                                'greenfield'
                            ]-
                            (
                            capex_generator(capex_dict_ref, 'EAF', year)[
                                'greenfield'
                            ]-
                            capex_generator(capex_dict_ref, 'EAF', year)[
                                'brownfield'
                            ]
                            )
                        )
                        df_temp.loc[
                            (df_temp["Start Technology"] == technology)
                            & (df_temp["New Technology"] == new_technology),
                            "value",
                        ] = switch_capex_value

                    else:
                        switch_capex_value = capex_generator(
                            capex_dict_ref, new_technology, year
                        )["greenfield"]
                        df_temp.loc[
                            (df_temp["Start Technology"] == technology)
                            & (df_temp["New Technology"] == new_technology),
                            "value",
                        ] = switch_capex_value
            df_temp = df_temp.loc[df_temp["value"] != ""]
            df_temp["Year"] = year
            tech_list.append(df_temp)
        combined_tech_df = pd.concat(tech_list)
        year_list.append(combined_tech_df)
    combined_year_df = pd.concat(year_list)

    return (
        combined_year_df.reset_index(drop=True)
        .set_index(["Year"])
        .sort_index(ascending=True)
    )

def greenfield_preprocessing(greenfield_df: pd.DataFrame):
    df_c = greenfield_df.copy()
    df_c.reset_index(inplace=True)
    df_c.columns = [col.lower().replace(' ', '_') for col in df_c.columns]
    df_c.rename({'technology': 'base_tech'}, axis=1, inplace=True)
    df_c = df_c[~df_c['base_tech'].isin(['Charcoal mini furnace', 'Close plant'])].copy()
    return df_c.set_index('year')

def create_greenfield_switching_df(gf_df: pd.DataFrame, year_range: range):
    def switch_mapper(row, ref_dict: dict):
        return ref_dict[row.switch_tech] - ref_dict[row.base_tech]
    df_container = []
    for year in tqdm(year_range, total=len(year_range), desc='Greenfield Switch Dict'):
        df = gf_df.loc[year].copy()
        ref_dict = dict(zip(df['base_tech'], df['value']))
        technology_df_ref = {tech: pd.DataFrame({'year': year, 'base_tech': tech, 'switch_tech': SWITCH_DICT[tech]}) for tech in TECH_REFERENCE_LIST}
        technology_df_ref = pd.concat(technology_df_ref.values())
        technology_df_ref['switch_value'] = technology_df_ref.apply(switch_mapper, ref_dict=ref_dict, axis=1)
        technology_df_ref.set_index(['year', 'base_tech', 'switch_tech'], inplace=True)
        df_container.append(technology_df_ref)
    return pd.concat(df_container)

@timer_func
def create_capex_timeseries(serialize: bool = False) -> pd.DataFrame:
    """Complete flow to create a capex dictionary.

    Args:
        serialize (bool, optional): Flag to only serialize the dict to a pickle file and not return a dict. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame with all of the potential technology capex switches.
    """
    logger.info("Creating the base switching dict")
    switching_dict = create_switching_dfs(TECH_REFERENCE_LIST)
    capex_dict = read_pickle_folder(PKL_DATA_FORMATTED, "capex_dict")
    max_model_year = max([int(year) for year in SWITCH_CAPEX_DATA_POINTS.keys()])
    switching_df_with_capex = get_capex_values(
        df_switching_dict=switching_dict,
        capex_dict_ref=capex_dict,
        year_end=max_model_year,
    )
    greenfield_df_f = greenfield_preprocessing(capex_dict['greenfield'])
    greenfield_switch_df = create_greenfield_switching_df(greenfield_df_f, MODEL_YEAR_RANGE)
    if serialize:
        serialize_file(
            switching_df_with_capex, PKL_DATA_FORMATTED, "capex_switching_df"
        )
        serialize_file(
            greenfield_switch_df, PKL_DATA_FORMATTED, "greenfield_switching_df"
        )
    return {
        'capex_switching_df': switching_df_with_capex,
        'greenfield_switching_df': greenfield_switch_df
    }