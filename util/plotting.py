from matplotlib import pyplot as plt
import pandas as pd

from util.analysis import CoordNo_Grouper, groupAnalysis
from util.stackedbar import stackedbar
from util.analysis import perc_selector

x_axis_labels = {
    "Coord_No": "Koordinationszahl",
    "Group": "Gruppe",
    "M": "",
    "Ligand": "Ligand",
    "No_Subs": "Anzahl Substituenten",
    "title": "",
    "Axial": ""
}


def save_plot(filenameWithoutExtension: str):
    plt.savefig(f"out/{filenameWithoutExtension}.svg")
    plt.savefig(f"out/{filenameWithoutExtension}.png")


def cm_to_inch(value):
    return value/2.54


def export_with_stackedbars(df: pd.DataFrame, by: str, filenameWithoutExtension: str, print_no: bool = True, print_legend: bool = False):
    current = groupAnalysis(df, by)
    
    if by == "Coord_No":
        stackedbar(CoordNo_Grouper(df),
                   x_axis_labels[by], print_no, print_legend)
    else:
        stackedbar(current, x_axis_labels[by],  print_no, print_legend)
    export(current, filenameWithoutExtension)


def export(df: pd.DataFrame, filenameWithoutExtension: str):
    save_plot(filenameWithoutExtension)
    df.to_excel(f"out/{filenameWithoutExtension}.xlsx")
    print(f"exported {filenameWithoutExtension}")
    plt.close()
