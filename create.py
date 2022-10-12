# Creates a master xlsx file

# Prerequisites
# 1. You need to have your structures as .mol2 files (Can be done by ConQuest)
# 2. You need to classify each file with the File Classifier https://github.com/JensKrumsieck/FileClassification (.meta.json files present)
# 3. You need to run a batch analysis with PorphyStruct v2.0.x using the extended basis (analysis.json files present)

import argparse
import fnmatch
import json
import os
import pandas as pd
from data import Crystal, Analysis

parser = argparse.ArgumentParser(prog='PorphyStruct Merger')
parser.add_argument("--folder", help="input folder path")
args = parser.parse_args()

path = args.folder
if path == None:
    path = r"C:\Users\jenso\PowerFolders\Forschung\CSD Data Mining"

# read files
filenames = []
for root, dir, files in os.walk(path):
    for file in fnmatch.filter(files, "*.mol2"):
        filenames.append(os.path.join(root, file))

data = []
for file in filenames:
    metaFile = file + ".meta.json"
    crystal: Crystal
    with open(metaFile, "r") as meta:
        raw = json.load(meta)
        ccdc = raw["Title"].split(".")[0]
        group = raw["Group"]
        if group == "0": 
            group = "Ln"
        crystal = Crystal(ccdc, raw["Class"], raw["Ligand"], raw["Metal"],
                          group, raw["AxialLigand"], raw["CoordNo"],
                          raw["SubstNo"], raw["CoSolv"])
    for root, dir, files in os.walk(os.path.dirname(file)):
        currentAnalysis: Analysis
        lastId = ord('A')
        for analysis in fnmatch.filter(files, crystal.CCDC + "*_analysis.json"):
            currentFile = os.path.join(root, analysis)
            with open(currentFile, "r") as current:
                raw = json.load(current)
                id = currentFile.split("_")[1]
                if(id == "analysis.json"):
                    id = ""
                else:
                    id = chr(lastId)
                    lastId += 1
                sim = raw["Simulation"]
                result = sim["SimulationResult"]
                dom1 = next(x for x in result if x["Key"] == "Doming")["Value"]
                sad1 = next(x for x in result if x["Key"] == "Saddling")["Value"]
                ruf1 = next(x for x in result if x["Key"] == "Ruffling")["Value"]
                wavx1 = next(x for x in result if x["Key"] == "WavingX")["Value"]
                wavy1 = next(x for x in result if x["Key"] == "WavingY")["Value"]
                pro1 = next(x for x in result if x["Key"] == "Propellering")["Value"]
                dom2 = next(x for x in result if x["Key"] == "Doming2")["Value"]
                sad2 = next(x for x in result if x["Key"] == "Saddling2")["Value"]
                ruf2 = next(x for x in result if x["Key"] == "Ruffling2")["Value"]
                wavx2 = next(x for x in result if x["Key"] == "WavingX2")["Value"]
                wavy2 = next((x for x in result if x["Key"] == "WavingY2"), {"Value": 0.0})["Value"]
                pro2 = next(x for x in result if x["Key"] == "Propellering2")["Value"]
                analysis = Analysis(id, raw["AnalysisType"],
                                    raw["OutOfPlaneParameter"]["Value"],
                                    sim["OutOfPlaneParameter"]["Value"],
                                    dom1, sad1, ruf1, wavx1, wavy1, pro1,
                                    dom2, sad2, ruf2, wavx2, wavy2, pro2,
                                    raw["Cavity"]["Value"]
                                    )
                crystal.Analyses.append(analysis)
    data.append(crystal)

rows = []
for crystal in data:
    for analysis in crystal.Analyses:
        row = crystal.__dict__|analysis.__dict__
        del row["Analyses"]
        rows.append(row)
        
df = pd.DataFrame(rows)
df.to_excel(path + r"\Results.xlsx")
print("Done!")