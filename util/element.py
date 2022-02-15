import json
import os
import typing
import pandas as pd


class Element:
    """Small Element Type"""

    def __init__(self, symbol: str, group: int, weight: float, number: int, name: str):
        self.symbol = symbol
        self.group = group
        self.weight = weight
        self.number = number
        self.name = name

    def __repr__(self) -> str:
        return f"Element {self.symbol}"


def get_element(symbol: str) -> Element:
    """Returns Element with given Symbol"""
    with open("elements.json", "r") as elements:
        elements = json.load(elements)
        element = list(filter(lambda el: symbol in el["Symbol"], elements))[0]
        return Element(element["Symbol"], int(element["Group"]), float(element["AtomicWeight"]), int(element["AtomicNumber"]), element["Name"])


def periodic_table() -> typing.Dict[str, Element]:
    """returns complete periodic table as dictionary indexed by symbol"""
    dir = os.path.dirname(__file__)

    with open(dir+"/elements.json", "r") as elements:
        elements = json.load(elements)
        list = {}
        for element in elements:
            if("Group" not in element):
                element["Group"] = 0
            list[element["Symbol"]] = Element(element["Symbol"], int(element["Group"]), float(
                element["AtomicWeight"]), int(element["AtomicNumber"]), element["Name"])
        return list


def df_periodic_table() -> pd.DataFrame:
    """returns complete periodic table as dictionary indexed by symbol"""
    df = pd.DataFrame()
    dir = os.path.dirname(__file__)

    with open(dir+"/elements.json", "r") as elements:
        elements = json.load(elements)
        for element in elements:
            if element["Block"] == "f-block" or 57 <= element["AtomicNumber"] <= 71 or 89 <= element["AtomicNumber"] <= 103:
                if element["AtomicNumber"] >= 57 and element["AtomicNumber"] <= 71:  # lanthanoids
                    element["Period"] = 8
                    element["Group"] = element["AtomicNumber"] - 57 + 4
                else:  # actinoids
                    element["Period"] = 9
                    element["Group"] = element["AtomicNumber"] - 89 + 4
            data = {
                "Number": [int(element["AtomicNumber"])],
                "Symbol": [element["Symbol"]],
                "Name": [element["Name"]],
                "Group": [int(element["Group"])],
                "Period": [int(element["Period"])],
                "Weight": [float(element["AtomicWeight"])]
            }
            df = pd.concat([df, pd.DataFrame(data)])
        df.set_index("Number", inplace=True)
    return df
