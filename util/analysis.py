import pandas as pd

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

plot_selector = []
for mode in modes:
    plot_selector.append(mode + " comp")
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
        bin_analysis["structures"] = bin.shape[0]
        newDF = pd.concat([newDF, bin_analysis])
        start = range  # set end to start
    return newDF


def groupAnalysis(dataFrame: pd.DataFrame, by: str, selector: list = perc_selector, create_sizes: bool = True) -> pd.DataFrame:
    grouped = dataFrame.groupby(by)[selector]
    mean_grouped = grouped.mean()
    for sel in selector:
        sel: str = sel
        if "Doop" in sel:
            continue
        mean_grouped[sel.replace('%', ' ').strip(
        )] = mean_grouped[sel] * mean_grouped["Doop (exp.)"]
    if create_sizes:
        mean_grouped["structures"] = grouped.size().values
    return mean_grouped


def doopAnalysis(dataFrame: pd.DataFrame, doopRanges: list, by: str = "range", selector: list = perc_selector) -> pd.DataFrame:
    dataFrame = dataFrame.query("`Doop (exp.)` > 0.0001")
    bins = doopRanger(dataFrame, doopRanges, selector)
    bins.fillna(0, inplace=True)
    res = groupAnalysis(bins, by, selector, False)
    res["structures"] = pd.Series(bins["structures"]).tolist()
    return res
# endregion


def CoordNo_Grouper(df: pd.DataFrame) -> pd.DataFrame:
    pd.options.mode.chained_assignment = None
    part01 = df.query("Coord_No < 7")
    result01 = groupAnalysis(part01, "Coord_No")
    part02 = df.query("Coord_No >= 7")
    part02.groupby("Group")
    part02["CoordNo"] = "sonstige"
    result02 = groupAnalysis(part02, "CoordNo")
    pd.options.mode.chained_assignment = "warn"
    return pd.concat([result01, result02])
