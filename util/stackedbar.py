from typing import Tuple, Union
import matplotlib
from matplotlib.axes import Axes
from matplotlib.container import Container
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from util.analysis import plot_selector, perc_ext_rev, perc_min
from util.settings import colors_ext, colors_min, doop_axis_label
from matplotlib.ticker import AutoMinorLocator


def __prepare_plot(y_selector: list[str]) -> Tuple[Figure, Axes, list[str], list[str]]:
    selector = y_selector[::-1]
    le_colors = colors_min[::-1] + colors_ext[::-1]
    fig, ax = plt.subplots()
    ax.tick_params(direction="out", top=False, right=False)
    ax.tick_params(which="minor", axis="y", right=False, direction="out")
    ax.tick_params(which="minor", axis="x", top=False, direction="out")
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    return fig, ax, selector, le_colors


def __prepare_width(ranges: list[float] = None) -> Union[float, list[float]]:
    if ranges is not None:
        width = []
        cur = 0
        for val in ranges:
            width.append(round(val-cur, 2))
            cur = val
        return width
    else:
        return .95


def __print_structures(ax: Axes, df: pd.DataFrame, c: Container):
    ax.bar_label(c, labels=[df["structures"].iloc[idv]
                            for idv, v in enumerate(c)], label_type="edge", fontsize=9, fontstyle="italic")


def __print_labels(idx: int, ax: Axes, df: pd.DataFrame, max_y: float, selector: str, c: Container):
    labels = ["{:.0%}".format(df[selector].iloc[idv]) if v.get_height() > 0.03 *
              max_y else '' for idv, v in enumerate(c)]
    ax.bar_label(c, labels=labels, label_type='center',
                 color="white", fontsize=8, fontweight=700)


def __print_modes(idx: int, ax: Axes, df: pd.DataFrame, max_y: float, width: float, selector: str, c: Container):
    offset = -.02
    mode = " ".join(selector[idx].split(" ")[:-1])
    if len(selector) > 6 or "comp" not in selector[3]:
        mode = selector[idx]
    legend = [mode if v.get_height() > 0.03 *
              max_y and idv == len(c)-1 else '' for idv, v in enumerate(c)]
    for text, bar in zip(legend, c):
        ax.text(bar.get_x() + bar.get_width() + offset * width, bar.get_height() + bar.get_y() + offset / 5,
                text, color="white",
                ha='right', va='top', fontsize=8, weight="bold")


def stackedbar_doop(df: pd.DataFrame, ranges: list[float], y_selector: list[str] = plot_selector, start=0) -> Tuple[Figure, Axes]:
    if len(y_selector) > 8:
        y_selector = perc_ext_rev
    elif "comp" not in y_selector[3]:
        y_selector = perc_min
    fig, ax, selector, le_colors = __prepare_plot(y_selector)

    ranges = ranges[:-1]
    width = __prepare_width(ranges)
    sel = [c for c in selector if "Doop" not in c]
    data = df.drop(df.tail(1).index)[sel].copy(deep=True)
    last = [0 for c in data.index]
    x_pos = [0]+ranges
    for c in data.columns:
        idx = data.columns.get_loc(c)
        ax.bar(x_pos[:-1], data[c], align='edge', edgecolor="black", linewidth=.3,
               width=width, color=le_colors[idx], bottom=last)
        last += data[c]
    plt.xticks(x_pos, x_pos)
    ax.set_xlabel(doop_axis_label)
    ax.set(ylim=(0, 1))
    if start == 0:  # auto set
        no0 = df.index.get_loc(df["structures"].ne(0).idxmax())
        start = x_pos[no0]

    ax.set(xlim=(start, ranges[-1]))
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter('{x:.0%}'))
    ax.set_title("$\it{Anzahl}$ $\it{Strukturen}$", pad=12)
    for idx, c in enumerate(ax.containers):
        __print_labels(idx, ax, data, 1.0, sel[idx], c)
        if idx == len(ax.containers)-1:
            __print_structures(ax, df.drop(df.tail(1).index), c)
        __print_modes(idx, ax, data, 1.0, width[0], [
                      " ".join(mode.split(" ")[:-1]) for mode in sel], c)
    return fig, ax


def stackedbar(df: pd.DataFrame, x_label: str, print_no: bool = True, print_legend: bool = False, y_selector: list[str] = plot_selector, tickRotation: int = 0) -> Tuple[Figure, Axes]:
    fig, ax, selector, le_colors = __prepare_plot(y_selector)
    width = __prepare_width()
    df.plot.bar(y=selector, stacked=True, color=le_colors,
                width=width, edgecolor="black", linewidth=.3, ax=ax, legend=print_legend)
    if print_legend:
        handles, labels = ax.get_legend_handles_labels()
        labels = [" ".join(i.split(" ")[:-1])
                  for i in selector]
        ax.legend(handles=handles[::-1], labels=labels[::-1],
                  loc=2, prop={'size': 8}, labelspacing=0.1)

    ax.tick_params(which="minor", axis="x", length=0)
    ax.set(xlim=(-0.5, len(df)-.5))
    ax.set_ylabel(doop_axis_label)
    ax.set_xlabel(x_label)
    max_doop = df["Doop (exp.)"].max()
    ax.set(ylim=(0, max_doop + max_doop * .1))
    if print_no:
        ax.set_title("$\it{Anzahl}$ $\it{Strukturen}$", y=1.0, pad=-10)
    for idx, c in enumerate(ax.containers):
        if print_no and idx == len(ax.containers)-1:
            __print_structures(ax, df, c)
        __print_labels(idx, ax, df, max_doop, selector[idx]+" %", c)
        if not print_legend:
            __print_modes(idx, ax, df, max_doop, width, selector, c)
    plt.xticks(rotation=tickRotation)
    return fig, ax
