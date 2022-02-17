from matplotlib import pyplot as plt
import pandas as pd
from util.analysis import groupAnalysis, perc_selector, perc_ext_selector, perc_min_selector
from util.merge import merge
from util.plotting import cm_to_inch, export_with_stackedbar_doop,  export_with_stackedbars, save_plot
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
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.titlesize"] = 9
plt.rcParams["xtick.labelsize"] = 9
plt.rcParams["ytick.labelsize"] = 9
plt.rcParams["font.family"] = "Arial"

# groupwise all
export_with_stackedbars(df, "Group", "metals_all_overview", False, True)
# substituents all
export_with_stackedbars(df, "No_Subs", "metals_all_substituents", True, True)
# ligands all, no plot
groupAnalysis(df, "Ligand").to_excel("out/metals_all_ligands.xlsx")
# all doop
export_with_stackedbar_doop(
    df, [.2, .4, .6, .8, 1, 1.2, 1000], "metals_all_doop")
# coord no all
export_with_stackedbars(df, "Coord_No", "metals_all_coordNo")

# maingroup by CN
export_with_stackedbars(mainGroup, "Coord_No", "metals_maingroup_coordNo")
# maingroup doop
export_with_stackedbar_doop(
    mainGroup, [.2, .4, .6, 1, 1000], "metals_maingroup_doop")

# groupwise transition
export_with_stackedbars(transitionAndLn, "Group",
                        "metals_transition_overview", True, True)

# transition doop
export_with_stackedbar_doop(
    transitionAndLn, [.2, .4, .6, 1, 1000], "metals_transition_doop")
# transition by substituents
export_with_stackedbars(transitionAndLn, "No_Subs",
                        "metals_transition_substituents", True, True)
# transition by CN
export_with_stackedbars(transitionAndLn, "Coord_No",
                        "metals_transition_coordNo")

# group 4-5 by Metal
export_with_stackedbars(transition.query(
    "Group == 4 or Group == 5"), "M", "metals_transition_g4g5_metals")

# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = transition.query(f"Group == {group}")

    export_with_stackedbars(
        group_dataset, "M", f"metals_transition_g{group}_metals")

    # group by doop
    export_with_stackedbar_doop(
        group_dataset, [.2, .4, .6, 1, 10000], f"metals_transition_g{group}_doop")
    # group by coord number
    export_with_stackedbars(group_dataset, "Coord_No",
                            f"metals_transition_g{group}_coordNo")

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
export_with_stackedbars(
    sel_comp, "M", "metals_maingroup_selectedMetals", False)
# endregion

# region Iron Corroles
IronCorroles = transition.query("M == 'Fe'")
export_with_stackedbars(IronCorroles, "Ligand",
                        "metals_transition_iron_ligands")
export_with_stackedbars(IronCorroles, "Coord_No",
                        "metals_transition_iron_coordNo")
# endregion

# region copper corroles
CopperCorroles = transition.query("M == 'Cu'")
export_with_stackedbar_doop(
    CopperCorroles,  [.6, 0.8, 1, 1.5, 1000], "metals_transition_copper_doop", perc_ext_selector)

export_with_stackedbar_doop(
    CopperCorroles,  [.6, 0.8, 1, 1.5, 2, 1000], "metals_transition_copper_doop_wider", perc_ext_selector)
# # endregion

# region cobalt corroles
CobaltCorroles = transition.query("M == 'Co'")
export_with_stackedbars(CobaltCorroles, "Coord_No",
                        "metals_transition_cobalt_coordNo")
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
export_with_stackedbars(
    Ligands, "title", "metals_transition_manganese_axial", False)

MnpFTPC = transition.query("M == 'Mn' and Ligand == 'pFTPC'")
export_with_stackedbars(
    MnpFTPC, "Axial", "metals_transition_mnpftpc_axial", False, True)
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
    pd.concat([d3compl, d4compl, d5compl]), "title", "metals_transition_dwise")
# endregion

# print periodic table
big_df = merge(paths + freeBases)
fig, ax = make_scatter_pie(big_df)
save_plot("periodic_table_corroles")

# FREEBASE
free = big_df.query("M == 'H'")
free_min_feasible = free.query("`δoop (min) %` < .03")
export_with_stackedbar_doop(
    free_min_feasible, [.6, .7, .8, .9, 1, 1.2, 1.8, 1000], "freebases_doop_min", perc_min_selector, .6)

export_with_stackedbar_doop(
    free,  [.6, .7, .8, .9, 1, 1.2, 1.8, 1000], "freebases_doop_ext")

# free base and metals doop
export_with_stackedbar_doop(
    big_df, [.2, .4, .6, .8, 1, 1.5, 2, 1000], "all_doop")

# free base and metals group
export_with_stackedbars(big_df, "Group", "all_overview")

# free base and metals subs
export_with_stackedbars(big_df, "No_Subs", "all_substituents")
