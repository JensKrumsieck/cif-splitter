import re
from typing import Tuple, Union
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.container import Container
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, StrMethodFormatter
from data import constants


def __prepare(selectedFields: list[str]) -> Tuple[Figure, Axes, list[str], list[str]]:
    selector = selectedFields[::1]
    if len(selectedFields) > 8:
        selector = [m + "2%" for m in constants.modes] + [m + "1%" for m in constants.modes]
    selector = selector[::-1]
    colors = constants.colors_min[::-1] + constants.colors_ext[::-1]
    fix, ax = plt.subplots()
    ax.tick_params(direction="out", top=False, right=False)
    ax.tick_params(which="minor", axis="y", right=False, direction="out")
    ax.tick_params(which="minor", axis="x", top=False, direction="out")
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    return fix, ax, selector, colors


def __width(ranges: list[float] = None) -> Union[float, list[float]]:
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


def __print_labels(ax: Axes, df: pd.DataFrame, max_y: float, selector: str, c: Container):
    labels = ["{:.0%}".format(df[selector].iloc[idv]) if v.get_height() > 0.03 *
              max_y else '' for idv, v in enumerate(c)]
    ax.bar_label(c, labels=labels, label_type='center',
                 color="white", fontsize=8, fontweight=700)


def __print_modes(idx: int, ax: Axes, max_y: float, width: float, selector: str, c: Container):
    offset = -.02
    mode = ""
    pattern = r"^([a-zA-Z]{3})(?:[a-z]*)?(X|Y)?(\d)?"
    match = re.match(pattern, selector[idx])
    for g in match.groups():
        if(g != None):
            mode += " "+g.lower()
    legend = [mode if v.get_height() > 0.03 *
              max_y and idv == len(c)-1 else '' for idv, v in enumerate(c)]
    for text, bar in zip(legend, c):
        ax.text(bar.get_x() + bar.get_width() + offset * width, bar.get_height() + bar.get_y() + offset / 5,
                text, color="white",
                ha='right', va='top', fontsize=8, weight="bold")


def plot_doop(df: pd.DataFrame, ranges: list[float], selectedFields: list[str], start=0, x_title="") -> Tuple[Figure, Axes]:
    fig, ax, selector, colors = __prepare(selectedFields)
    ranges = ranges[:-1]
    width = __width(ranges)
    sel = [c for c in selector if "Doop" not in c]
    data = df.drop(df.tail(1).index)[sel].copy(deep=True)
    last = [0 for c in data.index]
    x_pos = [0]+ranges
    for c in data.columns:
        idx = data.columns.get_loc(c)
        ax.bar(x_pos[:-1], data[c], align="edge", edgecolor="black", linewidth=.3,
               width=width, color=colors[idx], bottom=last)
        last += data[c]
    plt.xticks(x_pos, x_pos)
    if x_title == "":
        ax.set_xlabel(constants.doop_axis_label)
    else:
        ax.set_xlabel(x_title)
    ax.set(ylim=(0, 1))
    if(start == 0):  # auto set
        no0 = df.index.get_loc(df["structures"].ne(0).idxmax())
        start = x_pos[no0]
    no1 = df["structures"].to_numpy().nonzero()[0][-1] + 1
    end = x_pos[-1]
    if no1 < len(x_pos):
        end = x_pos[no1]
    ax.set(xlim=(start, end))
    ax.yaxis.set_major_formatter(
        StrMethodFormatter('{x:.0%}'))
    ax.set_title("$\it{Anzahl}$ $\it{Strukturen}$", pad=12)
    for idx, c in enumerate(ax.containers):
        __print_labels(ax, data, 1.0, sel[idx], c)
        if idx == len(ax.containers)-1:
            __print_structures(ax, df.drop(df.tail(1).index), c)
        __print_modes(idx, ax, 1.0, width[-1], sel, c)
    return fig, ax


def plot(df: pd.DataFrame, x_label: str, y_selector: list[str], print_no: bool = True, print_legend: bool = False, tickRotation: int = 0, ncol:int=1) -> Tuple[Figure, Axes]:
    fig, ax, selector, colors = __prepare(y_selector)
    width = __width()
    df.plot.bar(y=selector, stacked=True, color=colors,
                width=width, edgecolor='black', linewidth=.3, ax=ax, legend=print_legend)
    if print_legend:
        handles, labels = ax.get_legend_handles_labels()
        labels = [" ".join(i.split(" ")[:-1])
                  for i in selector]
        ax.legend(handles=handles[::-1], labels=labels[::-1],
                  loc=2, prop={'size': 8}, labelspacing=0.1, ncol=ncol)

    ax.tick_params(which="minor", axis="x", length=0)
    ax.set(xlim=(-0.5, len(df)-.5))
    ax.set_ylabel(constants.doop_axis_label)
    ax.set_xlabel(x_label)
    max_doop = df["DoopExp"].max()
    ax.set(ylim=(0, max_doop + max_doop * .1))
    if print_no:
        ax.set_title("$\it{Anzahl}$ $\it{Strukturen}$", y=1.0, pad=-10)
    for idx, c in enumerate(ax.containers):
        if print_no and idx == len(ax.containers)-1:
            __print_structures(ax, df, c)
        __print_labels(ax, df, max_doop, selector[idx], c)
        if not print_legend:
            __print_modes(idx, ax, max_doop, width, selector, c)
    plt.xticks(rotation=tickRotation)
    return fig,ax
