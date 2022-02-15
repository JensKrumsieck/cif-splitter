from matplotlib import figure, pyplot as plt
import pandas as pd
from util.analysis import doopAnalysis, groupAnalysis, perc_selector, perc_ext_selector
from util.element import df_periodic_table
from util.merge import merge
from util.scatterpie import make_scatter_pie

### THE AWESOME MOMENT WHEN SCRIPTS WRITE YOUR THESIS 😎 ###
### ENTER PATHS OF UBERMERGED XLSX FILES HERE! ####
### UBERMERGE.py RESULTS CAN BE USED, YOU NEED TO ENTER LIGAND,AXIAL,... INFO BY HAND! ###
paths = [r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\TransitionMetals.xlsx",
         r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\MainGroup.xlsx",
         r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\fBlock.xlsx"]
freeBases = [
    r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\Corrole\FreeBases.xlsx"]

df = merge(paths)
nonLa = df.query("Group != 'Ln'")
mainGroup = nonLa.query("Group < 3 or Group > 12")
lanthanoids = df.query("Group == 'Ln'")
transition = nonLa.query("Group > 3 and Group < 13")

# sanity check
assert len(transition) + len(mainGroup) + \
    len(lanthanoids) == len(df), "Oh no something is missing!"

# groupwise all
groupAnalysis(df, "Group").to_excel("out/all_overview.xlsx")
# substituents all
groupAnalysis(df, "No_Subs").to_excel("out/all_substituents.xlsx")
# ligands all
groupAnalysis(df, "Ligand").to_excel("out/all_ligands.xlsx")
# coord no all
groupAnalysis(df, "Coord_No").to_excel("out/all_coordNo.xlsx")
# maingroup by CN
groupAnalysis(mainGroup, "Coord_No").to_excel("out/maingroup_coordNo.xlsx")
# maingroup doop
doopAnalysis(mainGroup, [.2, .4, .6, 1, 1000]
             ).to_excel("out/maingroup_doop.xlsx")
# groupwise transition
groupAnalysis(pd.concat([transition, lanthanoids]),
              "Group").to_excel("out/transition_overview.xlsx")
# transition doop
doopAnalysis(pd.concat([transition, lanthanoids]),
             [.2, .4, .6, 1, 1000]).to_excel("out/transition_doop.xlsx")
# transition by substituents
groupAnalysis(pd.concat([transition, lanthanoids]), "No_Subs").to_excel(
    "out/transition_substituents.xlsx")
# transition by CN
groupAnalysis(pd.concat([transition, lanthanoids]),
              "Coord_No").to_excel("out/transition_coordNo.xlsx")
# group 4-5 by Metal
groupAnalysis(transition.query("Group == 4 or Group == 5"),
              "M").to_excel("out/transition_g4g5_metals.xlsx")
# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = transition.query(f"Group == {group}")
    groupAnalysis(group_dataset, "M").to_excel(
        f"out/transition_g{group}_metals.xlsx")
    # group by doop
    doopAnalysis(group_dataset, [.2, .4, .6, 1, 10000]).to_excel(
        f"out/transition_g{group}_doop.xlsx")
    # group by coord number
    groupAnalysis(group_dataset, "Coord_No").to_excel(
        f"out/transition_g{group}_coordNo.xlsx")

# region SELECTED MAINGROUP COMPLEXES
mgcn4 = mainGroup.query("Coord_No == 4")
mgcn5 = mainGroup.query("Coord_No == 5")
mgcn6 = mainGroup.query("Coord_No == 6")
phos_6c = mgcn6.query("M == 'P'")[perc_selector].mean()
gall_6c = mgcn6.query("M == 'Ga'")[perc_selector].mean()
germ_5c = mgcn5.query("M == 'Ge'")[perc_selector].mean()
tin_5c = mgcn5.query("M == 'Sn'")[perc_selector].mean()
metals = ["P", "Ga", "Ge", "Sn"]
lens = [len(mgcn6.query("M == 'P'")), len(mgcn6.query("M == 'Ga'")),
        len(mgcn5.query("M == 'Ge'")), len(mgcn5.query("M == 'Sn'"))]
sel_comp = pd.DataFrame([phos_6c, gall_6c, germ_5c, tin_5c])
sel_comp["M"] = metals
sel_comp["structures"] = lens
sel_comp.to_excel("out/maingroup_selectedMetals.xlsx")
# endregion

# region Iron Corroles
IronCorroles = transition.query("M == 'Fe'")
groupAnalysis(IronCorroles, "Ligand").to_excel(
    "out/transition_iron_ligands.xlsx")
groupAnalysis(IronCorroles, "Coord_No").to_excel(
    "out/transition_iron_coordNo.xlsx")
# endregion

# region copper corroles
CopperCorroles = transition.query("M == 'Cu'")
ranges = [.5, .7, 1, 1000]
doopAnalysis(CopperCorroles, ranges, "range", perc_ext_selector).to_excel(
    "out/transition_copper_doop.xlsx")
# endregion

# region cobalt corroles
CobaltCorroles = transition.query("M == 'Co'")
groupAnalysis(CobaltCorroles, "Coord_No").to_excel(
    "out/transition_cobalt_coordNo.xlsx")
# endregion

# region manganese corroles
ManganeseCorroles = transition.query("M == 'Mn'")
NeutralLigands = ["OPPh3", "H2O", "DMF", "Ph", "EtOH", "Br-Ph", "MeOH"]
NeutralMnCors = ManganeseCorroles.query(
    "Coord_No > 4").query("Axial.isin(@NeutralLigands)")
AnionicMnCors = ManganeseCorroles.query(
    "Coord_No > 4").query("~Axial.isin(@NeutralLigands)")
NeutralAnalysis = groupAnalysis(NeutralMnCors, "M")
NeutralAnalysis["title"] = "Neutral Ligands"
AnionicAnalysis = groupAnalysis(AnionicMnCors, "M")
AnionicAnalysis["title"] = "Anionic Ligands"
pd.concat([NeutralAnalysis, AnionicAnalysis]).to_excel(
    "out/transition_manganese_axial.xlsx")

MnpFTPC = transition.query("M == 'Mn' and Ligand == 'pFTPC'")
groupAnalysis(MnpFTPC, "Axial").to_excel(
    "out/transition_mnpftpc_axial.xlsx")
# endregion

# region 3d/4d/5d
m3d = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
m4d = ["Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"]
m5d = ["La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"]
d3compl = transition.query("M.isin(@m3d)")
d4compl = transition.query("M.isin(@m4d)")
d5compl = transition.query("M.isin(@m5d)")
d3compl["title"] = "3D"
d4compl["title"] = "4D"
d5compl["title"] = "5D"
groupAnalysis(pd.concat([d3compl, d4compl, d5compl]),
              "title").to_excel("out/transition_dwise.xlsx")
# endregion

big_df = merge(paths + freeBases)
plt.style.use(['science', 'nature', 'no-latex'])
fig, ax = make_scatter_pie(big_df)
plt.savefig("out/periodic.svg", dpi=1000)
