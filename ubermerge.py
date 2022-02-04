import fnmatch
import json
import os
import string


path = r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\Übergangsmetalle"

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


class Row:
    ccdc: str
    metal: str
    group: int
    ligand: str
    substituents: int
    axial: str
    coord_no: int
    co_solv: str
    doop_exp: float
    min_analysis: MinAnalysis
    ext_analysis: ExtAnalysis

    def __repr__(self) -> str:
        return f"Row: {self.ccdc} {self.min_analysis} {self.ext_analysis}"


analysis = []
for root, dir, files in os.walk(path):
    for file in fnmatch.filter(files, "*_analysis.json"):
        analysis.append(os.path.join(root, file))

rows = {}
for data in analysis:
    base: str = os.path.basename(data)
    parts = base.split("_")
    ccdc = parts[0]

    doop_exp = 0.0
    row = Row()
    row.ccdc = ccdc
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
                        setattr(rows[suffixed], "min_analysis",
                                row.min_analysis)
                    elif hasattr(rows[suffixed], 'min_analysis'):  # has extended basis
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
