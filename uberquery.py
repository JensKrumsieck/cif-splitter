from unicodedata import category
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from util.analysis import groupAnalysis, perc_selector, perc_ext_selector, perc_min_selector
from util.merge import merge
from util.plotting import cm_to_inch, export_with_stackedbar_doop,  export_with_stackedbars, save_plot
from util.scatterpie import make_scatter_pie

### THE AWESOME MOMENT WHEN SCRIPTS WRITE YOUR THESIS 😎 ###
### ENTER PATHS OF UBERMERGED XLSX FILES HERE! ####
### UBERMERGE.py RESULTS CAN BE USED, YOU NEED TO ENTER LIGAND,AXIAL,... INFO BY HAND! ###
paths = [r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\TransitionMetals.xlsx",
         r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\MainGroup.xlsx",
         r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\fBlock.xlsx"]
freeBases = [
    r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\FreeBases.xlsx"]

nConfused = [
    r"D:\Powerfolders\Forschung\PorphyStruct Results\NConfusedCorrole\NConfused.xlsx"]
iso = [r"D:\Powerfolders\Forschung\PorphyStruct Results\Isocorrole\Isocorroles.xlsx"]
hetero = [
    r"D:\Powerfolders\Forschung\PorphyStruct Results\Heterocorrole\Heterocorroles.xlsx"]
coreHetero = [
    r"D:\Powerfolders\Forschung\PorphyStruct Results\CoreHeterocorrole\CoreHeterocorroles.xlsx"]
corrolazines = [
    r"D:\Powerfolders\Forschung\PorphyStruct Results\Corrolazine\Corrolazines.xlsx"]
nSubst = [
    r"D:\Powerfolders\Forschung\PorphyStruct Results\NRCorroles\NRCorroles.xlsx"]

df = merge(paths)
nonLa = df.query("Group != 'Ln'")
mainGroup = nonLa.query("Group < 3 or Group > 12")
mainGroup = mainGroup.assign(category="Hauptgruppen Corrole")
lanthanoids = df.query("Group == 'Ln'")
transition = nonLa.query("Group > 3 and Group < 13")
transitionAndLn = pd.concat([transition, lanthanoids])
transitionAndLn = transitionAndLn.assign(category="Übergangsmetall Corrole")
allcorroles = merge(paths + freeBases)
free = allcorroles.query("M == 'H'")
free = free.assign(category="Freie Corrol Basen")
free_min_feasible = free.query("`δoop (min) %` < .03")

nConfusedDf = merge(nConfused)
nConfusedDf = nConfusedDf.assign(category="N-Confused Corrole")
isoDf = merge(iso)
isoDf = isoDf.assign(category="Isocorrole")
heteroDf = merge(hetero)
heteroDf = heteroDf.assign(category="10-Heterocorrole")
coreHeteroDf = merge(coreHetero)
coreHeteroDf = coreHeteroDf.assign(category="N-Heterocorrole")
corrolazinesDf = merge(corrolazines)
corrolazinesDf = corrolazinesDf.assign(category="Corrolazine")
nSubstDf = merge(nSubst)
nSubstDf = nSubstDf.assign(category="N-Subst. Corrole")

hugeDf = pd.concat([mainGroup, transitionAndLn, free, nConfusedDf,
                   isoDf, heteroDf, coreHeteroDf, corrolazinesDf, nSubstDf])


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

analyses = ["Group", "No_Subs", "Coord_No"]
filenames = {"Group": "overview",
             "No_Subs": "substituents",
             "Coord_No": "coordNo"}
df_to_name_1 = {
    "corroles_all": allcorroles,
    "corroles_freebases": free,
    "corroles_metals_all": df,
    "corroles_metals_maingroup": mainGroup,
    "corroles_metals_transition": transitionAndLn,
    "anything": hugeDf
}
df_to_name_2 = {
    "10-hetero": heteroDf,
    "N-hetero": coreHeteroDf,
    "confused": nConfusedDf,
    "corrolazines": corrolazinesDf,
    "N-Substituted": nSubstDf,
    "isocorroles": isoDf,
}
df_to_name = df_to_name_1 | df_to_name_2

print_legend = {
    "Group": True,
    "No_Subs": True,
    "Coord_No": False
}
# ligand stats
groupAnalysis(df, "Ligand").to_excel("out/corroles_metals_all_ligands.xlsx")

# print periodic table
fig, ax = make_scatter_pie(allcorroles)
save_plot("periodic_table_corroles")

fig, ax = make_scatter_pie(hugeDf)
save_plot("periodic_table_anything")

export_with_stackedbars(hugeDf, "category", "anything_category", True, True)

# loop analyses
for key in df_to_name:
    if key != "corroles_freebases":
        export_with_stackedbar_doop(
            df_to_name[key], [.2, .4, .6, 1, 1000], f"{key}_doop")
        export_with_stackedbar_doop(
            df_to_name[key], [.2, .4, .6, .8, 1, 1.5, 2, 1000], f"{key}_doop_wider")
    for analysis in analyses:
        export_with_stackedbars(
            df_to_name[key], analysis, f"{key}_{filenames[analysis]}", True, print_legend[analysis])

# special corroloids
for key in df_to_name_2:
    export_with_stackedbars(df_to_name_2[key], "M", f"{key}_metals")

# additional doop plots
export_with_stackedbar_doop(
    free_min_feasible, [.6, .7, .8, .9, 1, 1.2, 1.8, 1000], "corroles_freebases_doop_min", perc_min_selector, .6)
export_with_stackedbar_doop(
    free,  [.6, .7, .8, .9, 1, 1.2, 1.8, 1000], "corroles_freebases_doop_ext")

# group 4-5 by Metal
export_with_stackedbars(transition.query(
    "Group == 4 or Group == 5"), "M", "corroles_metals_transition_g4g5_metals")

# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = transition.query(f"Group == {group}")

    export_with_stackedbars(
        group_dataset, "M", f"corroles_metals_transition_g{group}_metals")

    # group by doop
    export_with_stackedbar_doop(
        group_dataset, [.2, .4, .6, 1, 10000], f"corroles_metals_transition_g{group}_doop")
    # group by coord number
    export_with_stackedbars(group_dataset, "Coord_No",
                            f"corroles_metals_transition_g{group}_coordNo")

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
    sel_comp, "M", "corroles_metals_maingroup_selectedMetals", False)
# endregion

# region Iron Corroles
IronCorroles = transition.query("M == 'Fe'")
export_with_stackedbars(IronCorroles, "Ligand",
                        "corroles_metals_transition_iron_ligands")
export_with_stackedbars(IronCorroles, "Coord_No",
                        "corroles_metals_transition_iron_coordNo")
# endregion

# region copper corroles
CopperCorroles = transition.query("M == 'Cu'")
export_with_stackedbar_doop(
    CopperCorroles,  [.6, 0.8, 1, 1.5, 1000], "corroles_metals_transition_copper_doop", perc_ext_selector)

export_with_stackedbar_doop(
    CopperCorroles,  [.6, 0.8, 1, 1.5, 2, 1000], "corroles_metals_transition_copper_doop_wider", perc_ext_selector)
# # endregion

# region cobalt corroles
CobaltCorroles = transition.query("M == 'Co'")
export_with_stackedbars(CobaltCorroles, "Coord_No",
                        "corroles_metals_transition_cobalt_coordNo")
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
    Ligands, "title", "corroles_metals_transition_manganese_axial", False)

MnpFTPC = transition.query("M == 'Mn' and Ligand == 'pFTPC'")
export_with_stackedbars(
    MnpFTPC, "Axial", "corroles_metals_transition_mnpftpc_axial", False, True)
# endregion

# region 3d/4d/5d
m3d = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
m4d = ["Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"]
m5d = ["La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"]
d3compl = transition.query("M.isin(@m3d)")
d4compl = transition.query("M.isin(@m4d)")
d5compl = transition.query("M.isin(@m5d)")
d3compl.assign(title="3D")
d4compl.assign(title="4D")
d5compl.assign(title="5D")
export_with_stackedbars(
    pd.concat([d3compl, d4compl, d5compl]), "title", "corroles_metals_transition_dwise")
# endregion

# SCATTERPLTS
# TODO WAV: |wav x comp| vs |wav y comp|
groups = ["No_Subs", "Group"]
modes = ["dom", "sad", "ruf", "wav x", "wav y"]
colors = {0: "#ffffff", 1: "#000000", 2: "#9D9D9D", 3: "#333333", 4: "#BE2633", 5: "#E06F8B", 6: "#493C2B",
          7: "#A46422", 8: "#EB8931", 9: "#F7E26B", 10: "#2F484E", 11: "#44891A",
          12: "#A3CE27", 13: "#1B2632", 14: "#005784", 15: "#31A2F2", "Ln": "#B2DCEF"}
for analysis in groups:
    for mode in modes:
        fig, ax = plt.subplots()
        ax.scatter(x=allcorroles[mode + " 1"].abs(), y=allcorroles[mode + " 2"] *
                   np.sign(allcorroles[mode + " 1"]), c=allcorroles[analysis].map(colors))
        ax.legend()
        plt.savefig(f"out/corroles_all_scatter_{mode}_{analysis}.png")
