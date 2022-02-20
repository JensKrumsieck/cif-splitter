from typing import Callable, Dict, Tuple
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

from util.plotting import save_plot


def scatter(df: pd.DataFrame, categories: Dict, analysis: str,
            lambda_x: Callable[[pd.DataFrame], pd.Series], title_x: str,
            lambda_y: Callable[[pd.DataFrame], pd.Series], title_y: str, filename: str) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots()
    for c in categories:
        data = df.query("{0} == @c".format(analysis))
        if data.shape[0] > 0:
            ax.scatter(x=lambda_x(data), y=lambda_y(data), c=categories[c],  alpha=.75, label=c)
    ax.legend()
    ax.set_xlabel(title_x)
    ax.set_ylabel(title_y)
    save_plot(filename)
    return fig, ax


def signed_mode(df: pd.DataFrame, mode: str) -> pd.Series:
    return df[mode + " 2"] * np.sign(df[mode + " 1"])
