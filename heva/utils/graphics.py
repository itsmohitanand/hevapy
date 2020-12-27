from typing import List
import matplotlib.pylab as plt
from matplotlib.lines import Line2D
import numpy as np


def record_length_plot(dict_max_val: dict, save_path: str) -> bool:
    """Horizontal bar plot for list of station

    Args:
        dict_max_val (dict): max_val as the value with station name as key
        save_path (str): The path to save plots

    Returns:
        bool: Returns True if plotted successfully
    """

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    y = 1
    key_list = []
    for key, val in dict_max_val.items():
        key_list.append(key)
        strt_year = val[0, 0]
        for i in range(1, val.shape[0] - 1):
            if val[i + 1, 0] != 1 + val[i, 0]:
                width = val[i, 0] - strt_year
                col, color_dict = _color(width)
                ax.barh(y, width=width, left=strt_year, height=0.8, color=col)
                strt_year = val[i + 1, 0]

        width = val[-1, 0] - strt_year
        col, color_dict = _color(width)
        ax.barh(y, width=width, left=strt_year, height=0.8, color=col)
        y += 1

    legend_elements = [
        Line2D([0], [0], color=color_dict["1"], lw=4, label="year>75"),
        Line2D([0], [0], color=color_dict["2"], lw=4, label=" 5<year<75"),
        Line2D([0], [0], color=color_dict["3"], lw=4, label="year<5"),
    ]

    ax.legend(
        handles=legend_elements,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        fancybox=True,
        ncol=3,
        shadow=True,
    )
    y_pos = np.arange(1, len(key_list) + 1)
    ax.set_yticklabels(key_list)

    ax.set_yticks(y_pos)
    ax.grid(axis="x", linestyle="--")
    plt.tight_layout()
    plt.savefig(save_path)


def _color(width: int) -> str:
    """Gives color based on width

    Args:
        width (int): The value for which color is to be determined

    Returns:
        str: Matplotlib valid color string
    """
    color_dict = {"1": "rebeccapurple", "2": "mediumpurple", "3": "firebrick"}

    if width > 75:
        return color_dict["1"], color_dict
    elif width < 5:
        return color_dict["3"], color_dict
    else:
        return color_dict["2"], color_dict
