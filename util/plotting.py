from matplotlib import pyplot as plt
import pandas as pd

from util.analysis import CoordNo_Grouper, cavityAnalysis, doopAnalysis, groupAnalysis, plot_selector, perc_selector
from util.stackedbar import stackedbar, stackedbar_doop

x_axis_labels = {
    "Coord_No": "Koordinationszahl",
    "Group": "Gruppe",
    "M": "",
    "Ligand": "Ligand",
    "No_Subs": "Anzahl Substituenten",
    "title": "",
    "Axial": "",
    "category": "",
    "10_Pos": "Heteroatom",
    "Cavity": "N4 Cavity"
}


def save_plot(filenameWithoutExtension: str):
    # plt.savefig(f"out/{filenameWithoutExtension}.svg")
    plt.savefig(f"out/{filenameWithoutExtension}.png")
    plt.close('all')
    print(f"exported {filenameWithoutExtension}")


def cm_to_inch(value):
    return value/2.54


def export_with_stackedbar_doop(df: pd.DataFrame, ranges: list[float],  filenameWithoutExtension: str, selector: list[str] = perc_selector, start: float = 0):
    current = doopAnalysis(df, ranges, "range", selector)
    stackedbar_doop(current, ranges, selector, start)
    export(current, filenameWithoutExtension)


def export_with_stackedbar_cavity(df: pd.DataFrame, ranges: list[float],  filenameWithoutExtension: str, selector: list[str] = perc_selector, start: float = 0):
    current = cavityAnalysis(df, ranges, "range", selector)
    stackedbar_doop(current, ranges, selector, start)
    export(current, filenameWithoutExtension)


def export_with_stackedbars(df: pd.DataFrame, by: str, filenameWithoutExtension: str, print_no: bool = True, print_legend: bool = False):
    current = groupAnalysis(df, by)

    if by == "Coord_No":
        stackedbar(CoordNo_Grouper(df),
                   x_axis_labels[by], print_no, print_legend)
    else:
        rot = 0
        if by == "category":
            current = current.sort_values(by="structures", ascending=True)
            rot = 90
        stackedbar(current, x_axis_labels[by],
                   print_no, print_legend, plot_selector, rot)
    export(current, filenameWithoutExtension)


def export(df: pd.DataFrame, filenameWithoutExtension: str):
    save_plot(filenameWithoutExtension)
    # df.to_excel(f"out/{filenameWithoutExtension}.xlsx")
