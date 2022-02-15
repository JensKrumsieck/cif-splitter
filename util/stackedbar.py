from typing import Tuple
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from util.analysis import plot_selector
from util.settings import colors_ext, colors_min, doop_axis_label
from matplotlib.ticker import AutoMinorLocator


def stackedbar(df: pd.DataFrame, x_label: str, print_no: bool = True, print_legend: bool = False, y_selector: list[str] = plot_selector) -> Tuple[Figure, Axes]:
    selector = y_selector[::-1]
    le_colors = colors_min[::-1] + colors_ext[::-1]
    fig, ax = plt.subplots(1, figsize=(4, 3))
    width = .95
    df.plot.bar(y=selector, stacked=True, color=le_colors,
                width=width, edgecolor="black", linewidth=.3, ax=ax, legend=print_legend)
    if print_legend:
        handles, labels = ax.get_legend_handles_labels()
        labels = [" ".join(i.split(" ")[:-1])
                  for i in selector]
        ax.legend(handles=handles[::-1], labels=labels[::-1],
                  loc=2, prop={'size': 5}, labelspacing=0.1)

    ax.set(xlim=(-0.5, len(df)-.5))
    ax.tick_params(direction="out", top=False, right=False)
    ax.tick_params(which="minor", axis="x", length=0)
    ax.tick_params(which="minor", axis="y", right=False, direction="out")
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_ylabel(doop_axis_label)
    ax.set_xlabel(x_label)
    max_doop = df["Doop (exp.)"].max()
    offset = -.02
    for idx, c in enumerate(ax.containers):
        if print_no and idx == len(ax.containers)-1:
            ax.bar_label(c, labels=[df["structures"].iloc[idv]
                         for idv, v in enumerate(c)], label_type="edge", fontsize=5, fontstyle="italic")
        labels = ["{:.0%}".format(df[selector[idx]+" %"].iloc[idv]) if v.get_height() > 0.03 *
                  max_doop else '' for idv, v in enumerate(c)]
        if not print_legend:
            legend = [" ".join(selector[idx].split(" ")[:-1]) if v.get_height() > 0.03 *
                      max_doop and idv == len(c)-1 else '' for idv, v in enumerate(c)]
            for text, bar in zip(legend, c):
                ax.text(bar.get_x() + bar.get_width() + offset * width, bar.get_height() + bar.get_y() + offset / 5,
                        text, color="white",
                        ha='right', va='top', fontsize=5, weight="bold")
        ax.bar_label(c, labels=labels, label_type='center',
                     color="white", fontsize=5, fontweight="bold")
    plt.xticks(rotation=0)
    return fig, ax
