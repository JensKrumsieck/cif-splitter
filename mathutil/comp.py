import pandas as pd
import numpy as np
from data import constants


def __compValue(mode1: pd.Series, mode2: pd.Series) -> pd.Series:
    res = (mode1*mode1)+(mode2*mode2)
    return np.sqrt(res)


def createCompData(df: pd.DataFrame) -> pd.DataFrame:
    for col in constants.modes:
        df[col + " comp"] = __compValue(df[col+"1"], df[col + "2"])
    return df

def createSumData(df: pd.DataFrame) -> pd.DataFrame:
    for col in constants.modes:
        df[col + " summed"] = df[col+"1"]+df[col+"2"]
    return df
