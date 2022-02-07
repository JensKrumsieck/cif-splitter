import json
import os
import typing


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
