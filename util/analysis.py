import pandas as pd

# region CONSTANTS
modes = ["dom", "sad", "ruf", "wav x", "wav y", "pro"]
ext_modes = ["dom 1", "sad 1", "ruf 1", "wav x 1", "wav y 1", "pro 1",
             "dom 2", "sad 2", "ruf 2", "wav x 2", "wav y 2", "pro 2"]
ext_modes_rev = ["dom 2", "sad 2", "ruf 2", "wav x 2", "wav y 2", "pro 2",
                 "dom 1", "sad 1", "ruf 1", "wav x 1", "wav y 1", "pro 1"]
perc_min = []
for mode in modes:
    perc_min.append(mode + " %")
perc_min_selector = perc_min + list(["Doop (exp.)"])

perc_comp = []
for mode in modes:
    perc_comp.append(mode + " comp %")
perc_comp = list(perc_comp)
perc_selector = perc_comp + list(["Doop (exp.)"])

perc_ext = []
for mode in ext_modes:
    perc_ext.append(mode + " %")
perc_ext_selector = perc_ext + list(["Doop (exp.)"])

perc_ext_rev = []
for mode in ext_modes_rev:
    perc_ext_rev.append(mode + " %")

plot_selector = []
for mode in modes:
    plot_selector.append(mode + " comp")
# endregion


# region functions


def doopRanger(dataFrame: pd.DataFrame, ranges: list, selector: list = perc_selector) -> pd.DataFrame:
    return FieldRanger(dataFrame, ranges, selector)


def cavityRanger(dataFrame: pd.DataFrame, ranges: list, selector: list = perc_selector) -> pd.DataFrame:
    return FieldRanger(dataFrame, ranges, selector, "Cavity")


def FieldRanger(dataFrame: pd.DataFrame, ranges: list, selector: list = perc_selector, field: str = "Doop (exp.)") -> pd.DataFrame:
    start = 0
    newDF = pd.DataFrame()
    for range in ranges:
        bin = dataFrame.query(
            f"`{field}` >= {start} and `{field}` < {range}")[selector]
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


def FieldAnalysis(dataFrame: pd.DataFrame, ranges: list, by: str = "range", selector: list = perc_selector, field: str = "Doop (exp.)") -> pd.DataFrame:
    dataFrame = dataFrame.query(f"`{field}` > 0.0001")
    bins = FieldRanger(dataFrame, ranges, selector, field)
    bins.fillna(0, inplace=True)
    res = groupAnalysis(bins, by, selector, False)
    res["structures"] = pd.Series(bins["structures"]).tolist()
    return res


def doopAnalysis(dataFrame: pd.DataFrame, doopRanges: list, by: str = "range", selector: list = perc_selector) -> pd.DataFrame:
    return FieldAnalysis(dataFrame, doopRanges, by, selector)


def cavityAnalysis(dataFrame: pd.DataFrame, ranges: list, by: str = "range", selector: list = perc_selector) -> pd.DataFrame:
    return FieldAnalysis(dataFrame, ranges, by, selector, "Cavity")
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
