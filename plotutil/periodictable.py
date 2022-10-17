import json
import numpy as np
from typing import Tuple
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from mathutil.analyze import groupBy
from plotutil.misc import cm_to_inch
import matplotlib.pyplot as plt
from data.constants import colors_min, percCompColumns
import pandas as pd
import os

def draw_pie(pos_x: int, pos_y: int, ratios: list, size: float, colors: list, ax):
    markers = []
    previous = 0

    for color, ratio in zip(colors, ratios):
        cur = 2*np.pi*ratio+previous
        angles = np.linspace(previous, cur, 30)
        x = [0] + np.cos(angles).tolist() + [0]
        y = [0] + np.sin(angles).tolist() + [0]
        xy = np.column_stack([x, y])
        previous = cur
        markers.append({'marker': xy, 's': np.abs(
            xy).max()**2*size, 'facecolor': color})

    for marker in markers:
        ax.scatter(pos_x, pos_y, **marker)

def make_scatter_pie(df: pd.DataFrame) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots(1, figsize=(cm_to_inch(16), cm_to_inch(8)))
    plt.box(False)
    ax.set(xlim=(0.25, 18.75), ylim=(9.75, .25))
    plt.xticks(range(1, 19))
    plt.yticks(range(1, 8))
    ax.minorticks_off()
    ax.xaxis.tick_top()
    ax.tick_params(axis='both', which='both', length=0)
    anal = groupBy(df, percCompColumns, "Metal")
    custom_lines = [Line2D([0], [0], color=colors_min[0], lw=4),
                    Line2D([0], [0], color=colors_min[1], lw=4),
                    Line2D([0], [0], color=colors_min[2], lw=4),
                    Line2D([0], [0], color=colors_min[3], lw=4),
                    Line2D([0], [0], color=colors_min[4], lw=4),
                    Line2D([0], [0], color=colors_min[5], lw=4)]
    legend = plt.legend(
        custom_lines, ['dom', 'sad', 'ruf', 'wav x', 'wav y', 'pro'], frameon=1, loc=9, ncol=3)
    frame = legend.get_frame()
    frame.set_color('white')

    plt.text(1, 8, "Lanthanoide", fontsize=8, verticalalignment='center')
    plt.text(1, 9, "Actinoide", fontsize=8, verticalalignment='center')
    plt.text(3, 6, "*", horizontalalignment='center',
             verticalalignment='center')
    plt.text(3, 7, "**", horizontalalignment='center',
             verticalalignment='center')
    for idx, row in df_periodic_table().iterrows():
        sym = row["Symbol"]
        res = anal.query("Metal==@sym")
        if(res.size == 0):
            plt.text(row["Group"], row["Period"], row["Symbol"], fontsize=8,
                     horizontalalignment='center',
                     verticalalignment='center')
            continue
        list = []
        for m in percCompColumns:
            if "Doop" in m:
                continue
            list.append(res[m].values[0])
        draw_pie(row["Group"], row["Period"], list,
                 res["DoopExp"]*400, colors_min, ax)
    return fig, ax


def df_periodic_table() -> pd.DataFrame:
    df = pd.DataFrame()
    dir = os.path.dirname(__file__)

    with open(dir+"/elements.json", "r") as elements:
        elements = json.load(elements)
        for element in elements:
            if element["Block"] == "f-block" or 57 <= element["AtomicNumber"] <= 71 or 89 <= element["AtomicNumber"] <= 103:
                if element["AtomicNumber"] >= 57 and element["AtomicNumber"] <= 71:  # lanthanoids
                    element["Period"] = 8
                    element["Group"] = element["AtomicNumber"] - 57 + 4
                else:  # actinoids
                    element["Period"] = 9
                    element["Group"] = element["AtomicNumber"] - 89 + 4
            data = {
                "Number": [int(element["AtomicNumber"])],
                "Symbol": [element["Symbol"]],
                "Name": [element["Name"]],
                "Group": [int(element["Group"])],
                "Period": [int(element["Period"])],
                "Weight": [float(element["AtomicWeight"])]
            }
            df = pd.concat([df, pd.DataFrame(data)])
        df.set_index("Number", inplace=True)
    return df