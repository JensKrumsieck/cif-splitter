import pandas as pd
from plotutil import periodictable

def createElectronData(df: pd.DataFrame) -> pd.DataFrame:
    # assign d-electron count            
    df["D"] = df.apply(
            lambda x: 
            "3d" if x["Metal"] in periodictable.m3d
            else "4d" if x["Metal"] in periodictable.m4d
            else "5d" if x["Metal"] in periodictable.m5d
            else "-"
            ,axis=1
       )
    df["d-electrons"] = df.apply(
        lambda x:     
        #d0 => Ti(IV), Zr(IV), Hf(IV), Ta(V), Mo(VI), W(VI), La(III)
        "0" if x["Metal"] in ["Ti", "Zr", "Hf"]
        else "0" if x["Metal"] == "La"
        else "0" if x["Metal"] == "Ta"
        else "0" if x["Metal"] in ["Mo", "W"] and x["AxialLigand"] in ["Corrole-Dimer", "2nd Corrole", "μ-O3-Dimer"]
        #d1 => Cr(V), Mo(V), W(V)
        else "1" if x["Metal"] in ["Mo", "Cr", "W"] and x["AxialLigand"] in ["O", "NMes", "NpTos", "Cl2"]
        #d2 => Mn(V), Tc(V), Re(V), Mo(IV), Os(VI)
        else "2" if x["Metal"] == "Mo" and x["AxialLigand"] in ["O-Mg(THF4)-Dimer", "Cp", "Cp*"]
        else "2" if x["Metal"] == "Os" and x["AxialLigand"] == "NPtCl3"
        else "2" if x["Metal"] in ["Mn", "Tc", "Re"] and x["AxialLigand"] in ["O", "N", "NMes"]
        #d3 => Cr(III), Mn(IV)
        else "3" if x["Metal"] == "Cr" and x["AxialLigand"] == "Py2"
        else "3" if x["Metal"] == "Mn" and x["AxialLigand"] == "OH" # nach A. Ghosh sind X- und Ar- Mn(III) Rad
        #d4 => Fe(IV), Os(IV), Ru(IV), Mn(III), Re(III)
        else "4" if x["Metal"] in ["Fe", "Os", "Ru"] and x["AxialLigand"] in ["N", "Ph", "Me", "OH"]
        else "4" if x["Metal"] in ["Mn", "Re"] and x["AxialLigand"] in ["", "Re-Corrole", "EtOH", "CHONMe2", "Py2", "H2O", "(H2O)2", "OCH2NMe2", "OCHNMe2", "MeOH", "OPPh3", "EtOAc", "OS(Me/Ph)"]
        else "4" if x["Metal"] == "Mn" and x["AxialLigand"] in ["Cl", "I", "Br", "Ph", "Br-Ph"]
        #d5 => Fe(III), Ru(III), Os(III)
        else "5" if x["Metal"] in ["Fe", "Ru", "Os"] and x["AxialLigand"] in ["", "Os-Corrole-Dimer", "Ru-Corrole", "Ru-Corrole-Dimer", "Py", "Py2", "(Py)2", "MeCN", "H2O"]
        else "5" if x["Metal"] == "Fe" and x["AxialLigand"] in ["Cl", "F", "μ-O", "Triflate"]
        #d6 => Co(III), Rh(III), Ir(III), Fe(II)
        else "6" if x["Metal"] in ["Co", "Rh", "Ir"]
        else "6" if x["Metal"] == "Fe" and "+" in x["CoSolv"]
        #d7 => -
        #d8 => Ni(II), Pd(II), Pt(II)
        else "8" if x["Metal"] in ["Ni", "Pd", "Pt"]
        #d9 => Cu(II), Ag(II), Au(II)
        else "9" if x["Metal"] in ["Cu", "Ag", "Au"] and x["AxialLigand"] == ""
        #d10 => Zn(II), Au(I)
        else "10" if x["Metal"] == "Zn"
        #else "10" if x["Metal"] == "Au" and x["AxialLigand"] == "PPh3" #(nicht N4 gebunden)
        else "f-Block" if x["Group"] == "Ln"
        else "HG" if x["D"] == "-" and x["Metal"] != "H"
        else "H" if x["Metal"] == "H"
        else ""
        ,axis=1
    )
    return df