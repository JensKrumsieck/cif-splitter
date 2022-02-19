import numpy as np
import pandas as pd
from .analysis import ext_modes, modes


def merge(paths: list[str]) -> pd.DataFrame:
    df = pd.DataFrame()
    for path in paths:
        df = pd.concat([df, pd.read_excel(path)], ignore_index=True)
    return __doCalculations(df)


def __doCalculations(df: pd.DataFrame) -> pd.DataFrame:
    if "domp comp" not in df.columns:
        df = __createComps(df)
    # DataFrame contains all data now!, add percentage cols
    sum = df["dom comp"] + df["sad comp"] + df["ruf comp"] + \
        df["wav x comp"] + df["wav y comp"] + df["pro comp"]
    for mode in modes:
        df[mode + " comp %"] = df[mode + " comp"] / sum

    sum_min = df["dom"].abs() + df["sad"].abs() + df["ruf"].abs() + \
        df["wav x"].abs() + df["wav y"].abs() + df["pro"].abs()
    for mode in modes:
        df[mode + " %"] = df[mode].abs()/sum_min

    sum_ext = df["dom 1"].abs() + df["dom 2"].abs() + \
        df["sad 1"].abs() + df["sad 2"].abs() + \
        df["ruf 1"].abs() + df["ruf 2"].abs() + \
        df["wav x 1"].abs() + df["wav x 2"].abs() + \
        df["wav y 1"].abs() + df["wav y 2"].abs() + \
        df["pro 1"].abs() + df["pro 2"].abs()
    for mode in ext_modes:
        df[mode + " %"] = df[mode].abs()/sum_ext
    return df


def __compValue(mode1: pd.Series, mode2: pd.Series) -> pd.Series:
    res = (mode1*mode1)+(mode2*mode2)
    return np.sqrt(res)


def __createComps(df: pd.DataFrame) -> pd.DataFrame:
    for mode in modes:
        df[mode + " comp"] = __compValue(df[mode + " 1"], df[mode + " 2"])
    return df
