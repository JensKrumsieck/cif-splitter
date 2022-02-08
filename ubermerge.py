import argparse
import fnmatch
import json
import os
from re import M
import string
import pandas as pd
from data.element import periodic_table

### ARGPARSE ###
parser = argparse.ArgumentParser(prog='PorphyStruct UBERMERGE!')
parser.add_argument("folder", help="Input folder path")
args = parser.parse_args()
####

path = args.folder
#path = r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\Übergangsmetalle"

# WARNING: Special Folder Structure needed : Metal Center -> min / ext -> FILES!
# Metal info is extracted from folder name!

# region constants
json_Simulation = "Simulation"
json_Result = "SimulationResult"
json_Doop = "OutOfPlaneParameter"
# endregion


class MinAnalysis:
    """Analysis result with minimal basis"""
    dom: float
    sad: float
    ruf: float
    wavx: float
    wavy: float
    pro: float
    doop_min: float

    def __repr__(self) -> str:
        return f"MIN: dom: {self.dom:.3f}, sad {self.sad:.3f}, ruf: {self.ruf:.3f}, wavx: {self.wavx:.3f}, wavy: {self.wavy:.3f}, pro: {self.pro:.3f}, Doop: {self.doop_min:.3f}"


class ExtAnalysis:
    """Analysis result with extended basis"""
    dom1: float
    dom2: float
    sad1: float
    sad2: float
    ruf1: float
    ruf2: float
    wavx1: float
    wavx2: float
    wavy1: float
    wavy2: float
    pro1: float
    pro2: float
    doop_ext: float

    def __repr__(self) -> str:
        return f"EXT: dom1: {self.dom1:.3f}, dom2: {self.dom2:.3f}, sad1: {self.sad1:.3f}, sad2: {self.sad2:.3f}, ruf1: {self.ruf1:.3f}, ruf2: {self.ruf2:.3f}, wavx1: {self.wavx1:.3f}, wavx2: {self.wavx2:.3f}, wavy1: {self.wavy1:.3f}, wavy2: {self.wavy2:.3f}, pro1: {self.pro1:.3f}, pro2: {self.pro2:.3f}  Doop: {self.doop_ext:.3f}"


class Row:
    ccdc: str
    metal: str = None
    group: int = 0
    ligand: str = None
    substituents: int = 0
    axial: str = None
    coord_no: int = 0
    co_solv: str = None
    doop_exp: float
    min_analysis: MinAnalysis
    ext_analysis: ExtAnalysis

    def __repr__(self) -> str:
        return f"Row: {self.ccdc}\n\t{self.min_analysis}\n\t{self.ext_analysis}\n\n"


analysis = []
for root, dir, files in os.walk(path):
    for file in fnmatch.filter(files, "*_analysis.json"):
        analysis.append(os.path.join(root, file))

rows = {}
pse = periodic_table()
for data in analysis:
    base: str = os.path.basename(data)
    parts = base.split("_")
    ccdc = parts[0]
    group = 0
    metal = ""

    try:
        metal = os.path.basename(os.path.abspath(
            os.path.join(os.path.dirname(data), os.pardir)))
        group = pse[metal].group
    except:
        pass

    doop_exp = 0.0
    row = Row()
    row.ccdc = ccdc
    row.metal = metal
    row.group = group
    with open(data, "r") as file:
        analysis = json.load(file)
        doop_exp = float(analysis[json_Doop]["Value"])
        row.doop_exp = doop_exp
        sim = analysis[json_Simulation][json_Result]
        if len(sim) > 6:  # having extended basis
            obj = ExtAnalysis()
            obj.dom1 = sim[0]["Value"]
            obj.dom2 = sim[6]["Value"]
            obj.sad1 = sim[1]["Value"]
            obj.sad2 = sim[7]["Value"]
            obj.ruf1 = sim[2]["Value"]
            obj.ruf2 = sim[8]["Value"]
            obj.wavx1 = sim[3]["Value"]
            obj.wavx2 = sim[9]["Value"]
            obj.wavy1 = sim[4]["Value"]
            obj.wavy2 = sim[10]["Value"]
            obj.pro1 = sim[5]["Value"]
            obj.pro2 = sim[11]["Value"]
            obj.doop_ext = analysis[json_Simulation][json_Doop]["Value"]
            row.ext_analysis = obj
        else:  # min basis
            obj = MinAnalysis()
            obj.dom = sim[0]["Value"]
            obj.sad = sim[1]["Value"]
            obj.ruf = sim[2]["Value"]
            obj.wavx = sim[3]["Value"]
            obj.wavy = sim[4]["Value"]
            obj.pro = sim[5]["Value"]
            obj.doop_min = analysis[json_Simulation][json_Doop]["Value"]
            row.min_analysis = obj

    if("#" in base):  # has multi analysis change suffix to letter
        for letter in string.ascii_uppercase:
            suffixed = parts[0] + " " + letter
            if suffixed in rows:  # if suffixed form is in list
                if abs(rows[suffixed].doop_exp-doop_exp) < 1e-6:  # equal doop -> same analysis
                    if hasattr(rows[suffixed], 'ext_analysis'):  # has extended basis
                        if hasattr(row, "ext_analysis"):
                            print("something weird happened")
                        setattr(rows[suffixed], "min_analysis",
                                row.min_analysis)
                    elif hasattr(rows[suffixed], 'min_analysis'):  # has extended basis
                        if hasattr(row, "min_analysis"):
                            print("something weird happened")
                        setattr(rows[suffixed], "ext_analysis",
                                row.ext_analysis)
                    break
                else:
                    continue
            else:
                row.ccdc = suffixed
                rows[suffixed] = row
                break
    else:
        if ccdc in rows:  # existing analysis, add other
            if hasattr(rows[ccdc], 'ext_analysis'):  # has extended basis
                setattr(rows[ccdc], "min_analysis",
                        row.min_analysis)
            elif hasattr(rows[ccdc], 'min_analysis'):  # has extended basis
                setattr(rows[ccdc], "ext_analysis",
                        row.ext_analysis)
        else:  # add new row
            rows[ccdc] = row

df = pd.DataFrame(columns=["CCDC", "M", "Group", "Ligand", "No_Subs", "Axial", "coord_no", "CoSolv", "Doop (exp.)",
                           "dom", "sad", "ruf", "wav x", "wav y", "pro", "Doop (min)", "δoop (min) %",
                           "dom 1", "dom 2", "sad 1", "sad 2", "ruf 1", "ruf 2", "wav x 1", "wav x 2",
                           "wav y 1", "wav y 2", "pro 1", "pro 2", "Doop (ext)", "δoop (ext) %"])
for row in rows:
    row: Row = rows[row]
    le_doop_min = 0
    le_doop_ext = 0
    if row.doop_exp != 0:  # THIS CASE DOES EXIST!
        le_doop_min = abs(row.min_analysis.doop_min -
                          row.doop_exp) / row.doop_exp
        le_doop_ext = abs(row.ext_analysis.doop_ext -
                          row.doop_exp)/row.doop_exp
    new = pd.DataFrame([(row.ccdc, row.metal, row.group, row.ligand, row.substituents, row.axial, row.coord_no, row.co_solv, row.doop_exp,
                         row.min_analysis.dom, row.min_analysis.sad, row.min_analysis.ruf, row.min_analysis.wavx, row.min_analysis.wavy,
                         row.min_analysis.pro, row.min_analysis.doop_min, le_doop_min, row.ext_analysis.dom1,
                         row.ext_analysis.dom2, row.ext_analysis.sad1, row.ext_analysis.sad2, row.ext_analysis.ruf1, row.ext_analysis.ruf2,
                         row.ext_analysis.wavx1, row.ext_analysis.wavx2, row.ext_analysis.wavy1, row.ext_analysis.wavy2,
                         row.ext_analysis.pro1, row.ext_analysis.pro2, row.ext_analysis.doop_ext,
                         le_doop_ext)],
                       columns=["CCDC", "M", "Group", "Ligand", "No_Subs", "Axial", "Coord_No", "CoSolv", "Doop (exp.)",
                                "dom", "sad", "ruf", "wav x", "wav y", "pro", "Doop (min)", "δoop (min) %",
                                "dom 1", "dom 2", "sad 1", "sad 2", "ruf 1", "ruf 2", "wav x 1", "wav x 2",
                                "wav y 1", "wav y 2", "pro 1", "pro 2", "Doop (ext)", "δoop (ext) %"])
    df = pd.concat([df, new], ignore_index=True)
df.to_excel("out/ubermerged.xlsx")
