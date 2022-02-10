from pickle import BINUNICODE
import numpy as np
import pandas as pd

### THE AWESOME MOMENT WHEN SCRIPTS WRITE YOUR THESIS 😎 ###

# region CONSTANTS
modes = ["dom", "sad", "ruf", "wav x", "wav y", "pro"]
ext_modes = ["dom 1", "sad 1", "ruf 1", "wav x 1", "wav y 1", "pro 1",
             "dom 2", "sad 2", "ruf 2", "wav x 2", "wav y 2", "pro 2"]
perc_comp = []
for mode in modes:
    perc_comp.append(mode + " comp %")
perc_comp = list(perc_comp)
perc_selector = perc_comp + list(["Doop (exp.)"])

perc_ext = []
for mode in ext_modes:
    perc_ext.append(mode + " %")
perc_ext_selector = perc_ext + list(["Doop (exp.)"])
# endregion

# region functions


def doopRanger(dataFrame: pd.DataFrame, ranges: list, selector: list = perc_selector) -> pd.DataFrame:
    start = 0
    newDF = pd.DataFrame()
    for range in ranges:
        bin = dataFrame.query(
            f"`Doop (exp.)` >= {start} and `Doop (exp.)` < {range}")[selector]
        bin_analysis = pd.DataFrame(bin.mean()).T
        bin_analysis["range"] = f"[{start, {range}}]"
        newDF = pd.concat([newDF, bin_analysis])
        start = range  # set end to start
    return newDF


def groupAnalysis(dataFrame: pd.DataFrame, by: str, selector: list = perc_selector) -> pd.DataFrame:
    grouped = dataFrame.groupby(by)[selector]
    mean_grouped = grouped.mean()
    mean_grouped["structures"] = grouped.size().values
    return mean_grouped


def doopAnalysis(dataFrame: pd.DataFrame, doopRanges: list, by: str, selector: list = perc_selector) -> pd.DataFrame:
    bins = doopRanger(dataFrame, doopRanges, selector)
    return groupAnalysis(bins, by, selector)
# endregion


### ENTER PATHS OF UBERMERGED XLSX FILES HERE! ####
paths = [r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\TransitionMetals.xlsx",
         r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\MainGroup.xlsx",
         r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\fBlock.xlsx"]

df = pd.DataFrame()
for path in paths:
    df = pd.concat([df, pd.read_excel(path)], ignore_index=True)

# DataFrame contains all data now!, add percentage cols
sum = df["dom comp"] + df["sad comp"] + df["ruf comp"] + \
    df["wav x comp"] + df["wav y comp"] + df["pro comp"]
for mode in modes:
    df[mode + " comp %"] = df[mode + " comp"] / sum

sum_ext = df["dom 1"].abs() + df["dom 2"].abs() + \
    df["sad 1"].abs() + df["sad 2"].abs() + \
    df["ruf 1"].abs() + df["ruf 2"].abs() + \
    df["wav x 1"].abs() + df["wav x 2"].abs() + \
    df["wav y 1"].abs() + df["wav y 2"].abs() + \
    df["pro 1"].abs() + df["pro 2"].abs()
for mode in ext_modes:
    df[mode + " %"] = df[mode].abs()/sum

### MAINGROUP ###
nonLa = df.query("Group != 'Ln'")
mainGroup = nonLa.query("Group < 3 or Group > 12")
### LANTHANOIDS ###
lanthanoids = df.query("Group == 'Ln'")
### TRANSITION METALS ###
transition = nonLa.query("Group > 3 and Group < 13")

# sanity check
assert len(transition) + len(mainGroup) + \
    len(lanthanoids) == len(df), "Oh no something is missing!"

# groupwise all
groupAnalysis(df, "Group").to_excel("out/all_overview.xlsx")
# ligands all
groupAnalysis(df, "Ligand").to_excel("out/all_ligands.xlsx")
# maingroup by CN
groupAnalysis(mainGroup, "Coord_No").to_excel("out/maingroup_coordNo.xlsx")
# groupwise transition
groupAnalysis(pd.concat([transition, lanthanoids]),
              "Group").to_excel("out/transition_overview.xlsx")
# transition by CN
groupAnalysis(mainGroup, "Coord_No").to_excel("out/transition_coordNo.xlsx")
# group 4-5 by Metal
groupAnalysis(transition.query("Group == 4 or Group == 5"),
              "M").to_excel("out/transition_g4g5_metals.xlsx")
# group 6 by metal
groupAnalysis(transition.query("Group == 6"), "M").to_excel(
    "out/transition_g6_metals.xlsx")
# group 7 by metal
groupAnalysis(transition.query("Group == 7"), "M").to_excel(
    "out/transition_g7_metals.xlsx")
# group 8 by metal
groupAnalysis(transition.query("Group == 8"), "M").to_excel(
    "out/transition_g8_metals.xlsx")
# group 9 by metal
groupAnalysis(transition.query("Group == 9"), "M").to_excel(
    "out/transition_g9_metals.xlsx")
# group 10 by metal
groupAnalysis(transition.query("Group == 10"), "M").to_excel(
    "out/transition_g10_metals.xlsx")
# group 11 by metal
groupAnalysis(transition.query("Group == 11"), "M").to_excel(
    "out/transition_g11_metals.xlsx")
# group 12 by metal
groupAnalysis(transition.query("Group == 12"), "M").to_excel(
    "out/transition_g12_metals.xlsx")

# region SELECTED MAINGROUP COMPLEXES
mgcn4 = mainGroup.query("Coord_No == 4")
mgcn5 = mainGroup.query("Coord_No == 5")
mgcn6 = mainGroup.query("Coord_No == 6")
phos_6c = mgcn6.query("M == 'P'")[perc_selector].mean()
gall_6c = mgcn6.query("M == 'Ga'")[perc_selector].mean()
germ_5c = mgcn5.query("M == 'Ge'")[perc_selector].mean()
tin_5c = mgcn5.query("M == 'Sn'")[perc_selector].mean()
metals = ["P", "Ga", "Ge", "Sn"]
lens = [len(mgcn6.query("M == 'P'")), len(mgcn6.query("M == 'Ga'")),
        len(mgcn5.query("M == 'Ge'")), len(mgcn5.query("M == 'Sn'"))]
sel_comp = pd.DataFrame([phos_6c, gall_6c, germ_5c, tin_5c])
sel_comp["M"] = metals
sel_comp["structures"] = lens
sel_comp.to_excel("out/maingroup_selectedMetals.xlsx")
# endregion

# region pFTPCMn by Ligand
MnpFTPC = transition.query("M == 'Mn' and Ligand == 'pFTPC'")
groupAnalysis(MnpFTPC, "Axial").to_excel(
    "out/transition_mnpftpc_axial.xlsx")
# endregion

# region FeTPC vs FepFTPC and CN
IronCorroles = transition.query("M == 'Fe'")
groupAnalysis(IronCorroles, "Ligand").to_excel(
    "out/transition_iron_ligands.xlsx")
groupAnalysis(IronCorroles, "Coord_No").to_excel(
    "out/transition_iron_coordNo.xlsx")
# endregion

# region copper corroles extended basis
CopperCorroles = transition.query("M == 'Cu'")
ranges = [.4, .5, 1, 1000]
doopAnalysis(CopperCorroles, ranges, "range", perc_ext_selector).to_excel(
    "out/transition_copper_doop.xlsx")
# endregion
