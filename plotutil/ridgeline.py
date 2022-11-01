import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import matplotlib.gridspec as gsp
import pandas as pd
import numpy as np
from typing import Tuple
from matplotlib.figure import Figure
from matplotlib.axes import Axes


def plot(dataset: pd.DataFrame, categories: list[str], column: str,
         y_axis: str, y_axis_title: str,
         xlim: Tuple[int, int],
         ylim: Tuple[int, int],
         colors: list[str]) -> Tuple[Figure, list[Axes]]:
    gs = (gsp.GridSpec(len(categories), 1))
    fig = plt.figure()
    i = 0
    aos: list[Axes] = []
    xstart, xend = xlim
    ystart, yend = ylim
    for cat in categories:
        x = np.array(dataset[dataset[column] == cat][y_axis])
        if len(x) != 0:
            x_d = np.linspace(xstart, xend, 1000)
            kde = KernelDensity(kernel="gaussian", bandwidth=.1)
            kde.fit(x[:, None])
            logprob = kde.score_samples(x_d[:, None])
            aos.append(fig.add_subplot(gs[i:i+1, 0:]))
            aos[-1].plot(x_d, np.exp(logprob), color=colors[i], lw=1)
            aos[-1].fill_between(x_d, np.exp(logprob), color=colors[i], alpha=.5)

            aos[-1].set_xlim(xstart, xend)
            aos[-1].set_ylim(ystart, yend)

            rect = aos[-1].patch
            rect.set_alpha(0)

            aos[-1].set_yticklabels([])
            aos[-1].set_yticks([])

            spines = ["top", "right", "left", "bottom"]
            for s in spines:
                aos[-1].spines[s].set_visible(False)
                aos[-1].text(xstart -0.02, 0, r"$\bf{" + cat + "}$" + f"\n(n = {len(dataset[dataset[column] == cat])})", 
                fontsize=8, ha="right", color=colors[i])

            if(cat == categories[-1]):
                aos[-1].xaxis.set_ticks_position("bottom")
                aos[-1].spines["bottom"].set_visible(True)
                aos[-1].set_xlabel(y_axis_title)
            else:
                aos[-1].set_xticklabels([])
                aos[-1].set_xticks([])

            i += 1
    gs.update(hspace=-0.7)
    plt.tight_layout()
    return fig, aos
