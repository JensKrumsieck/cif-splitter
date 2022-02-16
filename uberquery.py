from matplotlib import pyplot as plt
import pandas as pd
from util.analysis import doopAnalysis, groupAnalysis, perc_selector, perc_ext_selector
from util.merge import merge
from util.plotting import cm_to_inch,  export_with_stackedbars, save_plot
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
transitionAndLn = pd.concat([transition, lanthanoids])

# sanity check
assert len(transition) + len(mainGroup) + \
    len(lanthanoids) == len(df), "Oh no something is missing!"

# plot styles
plt.style.use(['science', 'nature', 'no-latex'])
plt.rcParams["figure.figsize"] = (cm_to_inch(16), cm_to_inch(13))
plt.rcParams["figure.dpi"] = 1200
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["axes.titlesize"] = 8
plt.rcParams["xtick.labelsize"] = 8
plt.rcParams["ytick.labelsize"] = 8

# groupwise all
export_with_stackedbars(df, "Group", "all_overview", False, True)
# substituents all
export_with_stackedbars(df, "No_Subs", "all_substituents", True, True)
# ligands all, no plot
groupAnalysis(df, "Ligand").to_excel("out/all_ligands.xlsx")
# coord no all
export_with_stackedbars(df, "Coord_No", "all_coordNo")

# maingroup by CN
export_with_stackedbars(mainGroup, "Coord_No", "maingroup_coordNo")
# maingroup doop
doopAnalysis(mainGroup, [.2, .4, .6, 1, 1000]
             ).to_excel("out/maingroup_doop.xlsx")
# groupwise transition
export_with_stackedbars(transitionAndLn, "Group",
                        "transition_overview", True, True)

# transition doop
doopAnalysis(transitionAndLn,
             [.2, .4, .6, 1, 1000]).to_excel("out/transition_doop.xlsx")
# transition by substituents
export_with_stackedbars(transitionAndLn, "No_Subs",
                        "transition_substituents", True, True)
# transition by CN
export_with_stackedbars(transitionAndLn, "Coord_No", "transition_coordNo")

# group 4-5 by Metal
export_with_stackedbars(transition.query(
    "Group == 4 or Group == 5"), "M", "transition_g4g5_metals")

# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = transition.query(f"Group == {group}")

    export_with_stackedbars(group_dataset, "M", f"transition_g{group}_metals")

    # group by doop
    doopAnalysis(group_dataset, [.2, .4, .6, 1, 10000]).to_excel(
        f"out/transition_g{group}_doop.xlsx")
    # group by coord number
    export_with_stackedbars(group_dataset, "Coord_No",
                            f"transition_g{group}_coordNo")

# region SELECTED MAINGROUP COMPLEXES
mgcn4 = mainGroup.query("Coord_No == 4")
mgcn5 = mainGroup.query("Coord_No == 5")
mgcn6 = mainGroup.query("Coord_No == 6")
phos_6c = mgcn6.query("M == 'P'")[perc_selector].mean()
phos_6c["M"] = "P"
gall_6c = mgcn6.query("M == 'Ga'")[perc_selector].mean()
gall_6c["M"] = "Ga"
germ_5c = mgcn5.query("M == 'Ge'")[perc_selector].mean()
germ_5c["M"] = "Ge"
tin_5c = mgcn5.query("M == 'Sn'")[perc_selector].mean()
tin_5c["M"] = "Sn"
sel_comp = pd.DataFrame([phos_6c, gall_6c, germ_5c, tin_5c])
export_with_stackedbars(sel_comp, "M", "maingroup_selectedMetals", False)
# endregion

# region Iron Corroles
IronCorroles = transition.query("M == 'Fe'")
export_with_stackedbars(IronCorroles, "Ligand", "transition_iron_ligands")
export_with_stackedbars(IronCorroles, "Coord_No", "transition_iron_coordNo")
# endregion

# region copper corroles
CopperCorroles = transition.query("M == 'Cu'")
ranges = [.5, .7, 1, 1000]
doopAnalysis(CopperCorroles, ranges, "range", perc_ext_selector).to_excel(
    "out/transition_copper_doop.xlsx")
# endregion

# region cobalt corroles
CobaltCorroles = transition.query("M == 'Co'")
export_with_stackedbars(CobaltCorroles, "Coord_No",
                        "transition_cobalt_coordNo")
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
count_n = NeutralMnCors.shape[0]
AnionicAnalysis = groupAnalysis(AnionicMnCors, "M")
AnionicAnalysis["title"] = "Anionic Ligands"
count_a = AnionicMnCors.shape[0]
Ligands = pd.concat([NeutralAnalysis, AnionicAnalysis])
Ligands["structures"] = [count_n, count_a]
export_with_stackedbars(Ligands, "title", "transition_manganese_axial", False)

MnpFTPC = transition.query("M == 'Mn' and Ligand == 'pFTPC'")
export_with_stackedbars(MnpFTPC, "Axial", "transition_mnpftpc_axial", False, True)
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
export_with_stackedbars(
    pd.concat([d3compl, d4compl, d5compl]), "title", "transition_dwise")
# endregion

# print periodic table
big_df = merge(paths + freeBases)
fig, ax = make_scatter_pie(big_df)
save_plot("periodic_table_corroles")
