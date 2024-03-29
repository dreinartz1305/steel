"""Investment Graph"""

from itertools import zip_longest

import pandas as pd
import plotly.express as px

from mppsteel.config.reference_lists import MPP_COLOR_LIST, TECH_REFERENCE_LIST
from mppsteel.model_results.investments import create_inv_stats

from mppsteel.utility.log_utility import get_logger
from mppsteel.model_graphs.plotly_graphs import line_chart, bar_chart

logger = get_logger(__name__)


def investment_line_chart(
    investment_df: pd.DataFrame,
    global_results: bool = True,
    operation: str = "cumsum",
    save_filepath: str = None,
    ext: str = "png",
) -> px.line:
    """Creates a line graph showing the level of investment across all technologies.

    Args:
        investment_df (pd.DataFrame): The investment DataFrame.
        global_results (bool, optional): Specifies if the results should be global -> float value if set to True. Else results will be regional. Defaults to True.
        operation (str, optional): The operation you want to perform on the DataFrame 'sum' or 'cumsum'. Defaults to "cumsum".
        save_filepath (str, optional): The filepath that you save the graph to. Defaults to None.
        ext (str, optional): The extension of the image you are creating. Defaults to "png".

    Returns:
        px.line: A plotly express line graph.
    """
    data = create_inv_stats(
        investment_df, global_results=global_results, operation=operation, agg=False
    )

    fig_ = line_chart(
        data=data,
        x="year",
        y="capital_cost",
        color=None,
        name="Investment Over Time",
        x_axis="Year",
        y_axis="Capital Cost",
    )

    if save_filepath:
        fig_.write_image(f"{save_filepath}.{ext}")


def investment_per_tech(
    investment_df: pd.DataFrame, save_filepath: str = None, ext: str = "png"
) -> px.bar:
    """Creates a bar graph showing the level of investment per technology.

    Args:
        investment_df: The investment DataFrame.
        save_filepath (str, optional): The filepath that you save the graph to. Defaults to None.
        ext (str, optional): The extension of the image you are creating. Defaults to "png".

    Returns:
        px.bar: A Plotly express bar chart.
    """
    tech_investment = (
        investment_df.groupby(["end_tech", "region_rmi"])
        .agg({"capital_cost": "sum"})
        .reset_index()
        .copy()
    )
    tech_inv_color_map = dict(
        zip_longest(tech_investment["end_tech"].unique(), MPP_COLOR_LIST)
    )

    fig_ = bar_chart(
        data=tech_investment,
        x="end_tech",
        y="capital_cost",
        color="region_rmi",
        color_discrete_map=tech_inv_color_map,
        array_order=TECH_REFERENCE_LIST,
        xaxis_title="End Technology",
        yaxis_title="Capital Cost",
        title_text="Capital Investment Per Technology (Regional Split)",
    )

    if save_filepath:
        fig_.write_image(f"{save_filepath}.{ext}")

    return fig_
