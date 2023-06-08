from cProfile import label
import pandas as pd
import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

def plot(df: pd.DataFrame, x: str, y: str,
         categories: list[str], column: str,
         colors: list[str],
         x_label = "", y_label="",
         size: str = "DoopExp", sizeMult=10) -> Tuple[Figure, list[Axes]]:
    fig,ax = plt.subplots()
    i = 0
    for cat in categories:
        values = df[df[column] == cat]
        data_x=values[x]
        if len(data_x) != 0:
            data_y=values[y]
            ax.scatter(x=data_x, y=data_y, c=colors[i], s=values[size]*sizeMult, label=cat)
            i+=1

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.legend()
    return fig,ax

