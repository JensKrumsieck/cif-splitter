import pandas as pd


def createRanges(df: pd.DataFrame, ranges: list[float], selectedFields: list[str],  byField: str) -> pd.DataFrame:
    start = 0.0
    result = pd.DataFrame()
    for range in ranges:
        bin = df.query(
            f"`{byField}` >= {start} and `{byField}` < {range}"
        )[selectedFields + ["DoopExp"]]
        analysis = pd.DataFrame(bin.mean()).T
        analysis["range"] = f"[{start}, {range}]"
        analysis["structures"] = bin.shape[0]
        result = pd.concat([result, analysis])
        start = range
    return result


def groupBy(df: pd.DataFrame, selectedFields: list[str], by: str):
    grouped = df.groupby(by)[selectedFields + ["DoopExp"]]
    mean = grouped.mean()
    for sel in selectedFields:
        mean[sel.replace('%', ' ').strip()] = mean[sel]*mean["DoopExp"]
    mean["structures"] = grouped.size().values
    return mean

def fieldAnalysis(df: pd.DataFrame, ranges: list[float], selectedFields: list[str],  byField: str):
    df = df.query(f"`{byField}` > 0.00001")
    bins = createRanges(df, ranges, selectedFields, byField)
    bins.fillna(0, inplace=True)
    res = groupBy(bins, selectedFields, "range")
    res["structures"] = pd.Series(bins["structures"]).tolist()
    return res