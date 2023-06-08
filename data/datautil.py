import pandas as pd

NHetero_O = ["21O", "22O", "21-O", "22-O"]
NHetero_C = ["21C", "22C", "21-C", "22-C"]
XHetero_S = ["(10-S)"]
XHetero_Se = ["(10-Se)"]
XHetero_O = ["(10-O)"]
XHetero_N = ["(10-N-Tol)", "(10-NBz)", "(10-NH)", "(10-NCH2Ph)",
            "(10-NC=OCH3)"]
XHetero_Si = ["(10-Si"]
XHetero_B = ["(10-B"]
XHetero_P = ["(10-P"]
XIso = ["10,10", "10-Ph/OH", "10-Ph/OEt", "10-Tol/OH", 
    "10-Spiro", "10-H/Dimer", "10-=O", "10-O-BArF", "10-OMe/Pyr", 
    "10-Me2", "10-C=O", "10H/Dimer", "10-Tol/Et", "10-OMePh/Pyr"]
VIso = ["5,5", "5-Me2", "5-Ph/OH", "5-Tol/OH", "5-OMePh/OH",
    "5=O", "5-=O", "5-OMePh/Pyr", "5- Me2"]
IXIso = ["9,11-Me", "9-Me", "1,19-Me", "1-C(OMe)2"]

subclasses = ["N-Heterocorrole", "10-Heterocorrole", "Corrolazine", "5-Isocorrole", "10-Isocorrole"]

def applyHICSubclass(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe["Subclass"] = dataframe.apply(
        lambda x:
        "N-Heterocorrole" if x["Class"] == "Heterocorrole" 
                            and (any(item in x["Ligand"] for item in NHetero_C) 
                                or any(item in x["Ligand"] for item in NHetero_O))
        else "10-Heterocorrole" if x["Class"] == "Heterocorrole" 
                            and (any(item in x["Ligand"] for item in XHetero_B) 
                            or any(item in x["Ligand"] for item in XHetero_N)
                            or any(item in x["Ligand"] for item in XHetero_P)
                            or any(item in x["Ligand"] for item in XHetero_Si)
                            or any(item in x["Ligand"] for item in XHetero_O)
                            or any(item in x["Ligand"] for item in XHetero_Se)
                            or any(item in x["Ligand"] for item in XHetero_S))
        else "10-Isocorrole" if x["Class"] == "Isocorrole"
                            and (any(item in x["Ligand"] for item in XIso))
        else "5-Isocorrole" if x["Class"] == "Isocorrole"
                            and (any(item in x["Ligand"] for item in VIso))
        else "sonstige Isocorrole" if x["Class"] == "Isocorrole"
                            and (any(item in x["Ligand"] for item in IXIso))
        else "Corrolazine" if x["Class"] == "Corrolazine"
        else "Nope"
    ,axis = 1
    )
    return dataframe

def getHeteroAtom(df: pd.DataFrame) -> pd.DataFrame:
    df["Heteroatom"] = df.apply(lambda x:
        "O" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_O)
            or any(item in x["Ligand"] for item in NHetero_O))
        else "N" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_N))
        else "S" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_S))        
        else "Se" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_Se))
        else "C" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in NHetero_C))   
        else "B" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_B))   
        else "P" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_P)) 
        else "Si" if "Heterocorrole" in x["Subclass"] and
            (any(item in x["Ligand"] for item in XHetero_Si))    
        else ""   
    ,axis = 1)
    return df
    
Me25 = ["5,5-Me2", "5-Me2", "5- Me2"]
Me210 = ["10,10-Me2", "10-Me2"]
OMePy5 = ["5-OMePh/Pyr"]
OMePy10 = ["10-OMePh/Pyr"]
ArOH5 = ["5-OMePh/OH", "5-Tol/OH", "5,5-OH/Tol", "5,5-(OH/tBuPh)", "5-Ph/OH", "5,5-OH,Tol"]
ArOH10 = ["10,10-O,Tol", "10-Tol/OH", "10-Ph/OH"]
Oxo5 = ["5=O"]
Oxo10 = ["10-=O", "10=O", "10-O-BArF", "10-C=O"]
Dimer10 = ["10H/Dimer", "10-Spiro"]
ArOEt10 = ["10-Ph/OEt"]
ArAlkyl10 = ["10-Tol/Et"]
def getIsoSubstituent(df: pd.DataFrame) -> pd.DataFrame:
    df["Iso"] = df.apply(lambda x:
        "$5,5-Me_2$" if "5-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in Me25))
        else "$5,5-Ar/Pyr$" if "5-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in OMePy5))
        else "$5,5-Ar/OH$" if "5-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in ArOH5))
        else "$5-Oxo$" if "5-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in Oxo5))
        else "$10,10-Me_2$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in Me210))
        else "$10,10-Ar/Pyr$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in OMePy10))
        else "$10,10-Ar/OH$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in ArOH10))
        else "$10-Oxo$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in Oxo10))
        else "$10,10-Ar/OAlkyl$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in ArOEt10))        
        else "$10,10-Ar/Alkyl$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in ArAlkyl10))                    
        else "$10-Dimer$" if "10-Isocorrol" in x["Subclass"] and
            (any(item in x["Ligand"] for item in Dimer10))
        else ""    
    ,axis = 1)
    return df


N21At1 = ["BOBYAU", "BOBYEY", "DEJGUW", "DEJHAD", "HOCNOF", "HOCNUL", "OTIGIJ", "OTOSIB", "UVUDUL"]
N21At1_Dimers = ["DEJHEH", "DEJHIL", "DEJHOR"]
N21At1_Isocorrol = ["EHARUC"]
N21At2 = ["EHASAJ", "UVUDOF"]
N21At2_Dimers = ["URIFAF", "URIFEJ", "YEZLEX"]
N21At1_N24At19 = ["LURDAG"]
N22At7 = ["UVUDIZ", "YEZKUM"]

def getConfusedSubclass(df: pd.DataFrame) -> pd.DataFrame:
    df["Confusion"] = df.apply(lambda x:
        "Norrol" if any(item in x["CCDC"] for item in N21At1)
        else "Norrol-Dimere" if any(item in x["CCDC"] for item in N21At1_Dimers)
        else "Isonorrol" if any(item in x["CCDC"] for item in N21At1_Isocorrol)
        else "N^Norrol" if any(item in x["CCDC"] for item in N21At1_N24At19)
        else "A-confused" if any (item in x["CCDC"] for item in N21At2)
        else "A-confused-Dimere" if any(item in x["CCDC"] for item in N21At2_Dimers)
        else "B-confused" if any(item in x["CCDC"] for item in N22At7)
         else ""
    ,axis =1)
    return df

NA_Methyl = ["MCORRH"]
NB_Methyl = ["RHMCOR"]
NA_NB_Methyl = ["APIXII", "APIYOP"]
NA_NB_CO = ["BAWHOX", "DADJOI", "WEWROG", "WEWRUM", "WEWSAT", "ZENJIO", "ZENJOU", "ZENJUA"]
NA_NB_CH2 = ["NILYIT"]
NB_Bz = ["LISYAO", "MOLPEI", "MOLPIM", "MOLPOS", "UCEXOR"]
NA_Bz = ["MOLNUW", "MOLPAE", "MOLPUY", "MOLQAF", "NEMCOY", "QONXUM"]
AllN = ["XABFOW"]
def getNSubst(df: pd.DataFrame) -> pd.DataFrame:
    df["NSubst"] = df.apply(lambda x:
        "$N_A$-Methyl" if any(item in x["CCDC"] for item in NA_Methyl)
        else "$N_A$-Me-Ar" if any(item in x["CCDC"] for item in NA_Bz)
        else "$N_B$-Methyl" if any(item in x["CCDC"] for item in NB_Methyl)
        else "$N_B$-Me-Ar" if any(item in x["CCDC"] for item in NB_Bz)        
        else "$N_B$-Me & $N_A$-Me" if any(item in x["CCDC"] for item in NA_NB_Methyl)
        else "$N_A$-CO-$N_B$" if any(item in x["CCDC"] for item in NA_NB_CO)
        else "$N_A$-$CH_2$-$N_B$" if any(item in x["CCDC"] for item in NA_NB_CH2)
        else "4-fach subst." if any (item in x["CCDC"] for item in AllN)
        else ""
    ,axis = 1)
    return df

def applyNRSubclasses(df: pd.DataFrame)-> pd.DataFrame:
    df = getNSubst(df)
    df["NSubst"] = df.apply(
    lambda x:
    "$N_A$,$N_B$-verbrückt" if (x["NSubst"] == "$N_A$-CO-$N_B$" or x["NSubst"] == "$N_A$-$CH_2$-$N_B$")
    else "$N_A$,$N_B$-disubst." if x["NSubst"] == "$N_B$-Me & $N_A$-Me"
    else "$N_A$ substituiert" if (x["NSubst"].startswith("$N_A"))
    else "$N_B$ substituiert" if x["NSubst"].startswith("$N_B")
    else x["NSubst"]
    ,axis=1)
    return df

def applyAllSubclasses(df:pd.DataFrame) -> pd.DataFrame:
    df = applyHICSubclass(df) # hetero and isocorroles in df["Subclass"]
    df = applyNRSubclasses(df) # nr subst in df["NSubst"]
    df = getConfusedSubclass(df) # nconfusion in df["Confusion"]
    df["Subclass"] = df.apply(lambda x:
        x["NSubst"] if x["Subclass"] == "Nope" and  x["NSubst"] != ""
        else "Norrol" if x["Confusion"]== "Isonorrol" or x["Confusion"] == "N^Norrol"
        else x["Confusion"] if x["Subclass"] == "Nope" and  x["Confusion"] != ""
        else "freie Corrol Basen" if x["Subclass"] == "Nope" and x["Metal"] == "H"
        else "Übergangsmetallcorrole" if x["Subclass"] == "Nope" and x["Group"] in ["3", "4","5","6","7","8","9","10","11","12"]
        else "f-Block-Corrole" if x["Subclass"] == "Nope" and x["Group"] == "Ln"
        else "Hauptgruppenelementcorrole" if x["Subclass"] == "Nope"
        else x["Subclass"]
    ,axis = 1)
    df["Subclass"] = df["Subclass"].replace(regex=r"-Dimere", value="")
    return df