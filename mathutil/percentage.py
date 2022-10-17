import pandas as pd
from data import constants


def createPercData(df: pd.DataFrame) -> pd.DataFrame:
    sum = 0
    for col in constants.analysisColumns:
        sum += df[col].abs()
    for col in constants.analysisColumns:
        df[col + "%"] = df[col].abs()/sum
    return df

def createCompPercData(df: pd.DataFrame) -> pd.DataFrame:
    sum = 0
    for col in constants.compColumns:
        sum += df[col].abs()
    for col in constants.compColumns:
        df[col + "%"] = df[col].abs()/sum
    return df