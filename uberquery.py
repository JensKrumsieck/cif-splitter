from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from util.analysis import groupAnalysis, perc_selector, perc_ext_selector, perc_min_selector
from util.merge import merge
from util.plotting import cm_to_inch, export_with_stackedbar_doop,  export_with_stackedbars, save_plot
from util.scatterpie import make_scatter_pie
from util.settings import colors_min, colors_ext

# plot styles
plt.style.use(['science', 'nature', 'no-latex'])
plt.rcParams["figure.figsize"] = (cm_to_inch(16), cm_to_inch(13))
plt.rcParams["figure.dpi"] = 1200
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.titlesize"] = 9
plt.rcParams["xtick.labelsize"] = 9
plt.rcParams["ytick.labelsize"] = 9
plt.rcParams["font.family"] = "Arial"


### THE AWESOME MOMENT WHEN SCRIPTS WRITE YOUR THESIS 😎 ###
### ENTER PATHS OF UBERMERGED XLSX FILES HERE! ####
### UBERMERGE.py RESULTS CAN BE USED, YOU NEED TO ENTER LIGAND,AXIAL,... INFO BY HAND! ###
path_corroles = [r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\TransitionMetals.xlsx",
                 r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\MainGroup.xlsx",
                 r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\fBlock.xlsx",
                 r"D:\PowerFolders\Forschung\PorphyStruct Results\Corrole\FreeBases.xlsx"]

path_nConfused = [r"D:\Powerfolders\Forschung\PorphyStruct Results\NConfusedCorrole\NConfused.xlsx"]
path_isocorroles = [r"D:\Powerfolders\Forschung\PorphyStruct Results\Isocorrole\Isocorroles.xlsx"]
path_heterocorroles = [r"D:\Powerfolders\Forschung\PorphyStruct Results\Heterocorrole\Heterocorroles.xlsx"]
path_nHeterocorroles = [r"D:\Powerfolders\Forschung\PorphyStruct Results\CoreHeterocorrole\CoreHeterocorroles.xlsx"]
path_corrolazines = [r"D:\Powerfolders\Forschung\PorphyStruct Results\Corrolazine\Corrolazines.xlsx"]
path_nSubstCorroles = [r"D:\Powerfolders\Forschung\PorphyStruct Results\NRCorroles\NRCorroles.xlsx"]

corroles_all = merge(path_corroles)  # all corroles
corroles_metals = corroles_all.query("M != 'H'")  # all metal corroles
nonLa = corroles_metals.query("Group != 'Ln'")  # non Ln Corroles for querying
corroles_maingroup = nonLa.query("Group < 3 or Group > 12").assign(category="Hauptgruppen Corrole")  # main group corroles
corroles_fBlock = corroles_metals.query("Group == 'Ln'")  # fBlock Corroles
corroles_transition = nonLa.query("Group > 3 and Group < 13")  # transition metals without fBlock
corroles_dfBlock = pd.concat([corroles_transition, corroles_fBlock]).assign(category="Übergangsmetall Corrole")  # f and d Block corroles
corroles_freeBase = corroles_all.query("M == 'H'").assign(category="Freie Corrol Basen")  # free base corroles
nConfusedCorroles = merge(path_nConfused).assign(category="N-Confused Corrole")  # N confused corroles
isocorroles = merge(path_isocorroles).assign(category="Isocorrole")  # isocorroles
heterocorroles = merge(path_heterocorroles).assign(category="10-Heterocorrole")  # 10-heterocorroles
nHeterocorroles = merge(path_nHeterocorroles).assign(category="N-Heterocorrole")  # core modified heterocorroles
corrolazines = merge(path_corrolazines).assign(category="Corrolazine")  # corrolazines aka triazacorroles
nSubstCorroles = merge(path_nSubstCorroles).assign(category="N-Subst. Corrole")  # Corroles with subsititutions at N4

allData = pd.concat([corroles_maingroup, corroles_dfBlock, corroles_freeBase, nConfusedCorroles,
                     isocorroles, heterocorroles, nHeterocorroles, corrolazines, nSubstCorroles])

analyses = ["Group", "No_Subs", "Coord_No"]
filenames = {"Group": "overview",
             "No_Subs": "substituents",
             "Coord_No": "coordNo"}

filenames_corroles = {
    "corroles_all": corroles_all,
    "corroles_freebases": corroles_freeBase,
    "corroles_metals_all": corroles_metals,
    "corroles_metals_maingroup": corroles_maingroup,
    "corroles_metals_transition": corroles_dfBlock
}
filenames_special = {
    "10-hetero": heterocorroles,
    "N-hetero": nHeterocorroles,
    "confused": nConfusedCorroles,
    "corrolazines": corrolazines,
    "N-Substituted": nSubstCorroles,
    "isocorroles": isocorroles,
}
df_to_name = filenames_corroles | filenames_special | {"anything": allData}

print_legend = {
    "Group": True,
    "No_Subs": True,
    "Coord_No": False
}
# ligand stats
groupAnalysis(corroles_all, "Ligand").to_excel(
    "out/corroles_all_ligands.xlsx")

# print periodic table
fig, ax = make_scatter_pie(corroles_all)
save_plot("periodic_table_corroles")

fig, ax = make_scatter_pie(allData)
save_plot("periodic_table_anything")

# by category
export_with_stackedbars(allData, "category", "anything_category", True, True)

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
for key in filenames_special:
    export_with_stackedbars(filenames_special[key], "M", f"{key}_metals")

# additional doop plots
export_with_stackedbar_doop(corroles_freeBase.query("`δoop (min) %` < .03"),
                            [.6, .7, .8, .9, 1, 1.2, 1.8, 1000], "corroles_freebases_doop_min", perc_min_selector, .6)
export_with_stackedbar_doop(corroles_freeBase,
                            [.6, .7, .8, .9, 1, 1.2, 1.8, 1000], "corroles_freebases_doop_ext")

# group 4-5 by Metal
export_with_stackedbars(corroles_transition.query(
    "Group == 4 or Group == 5"), "M", "corroles_metals_transition_g4g5_metals")

# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = corroles_transition.query(f"Group == {group}")

    export_with_stackedbars(
        group_dataset, "M", f"corroles_metals_transition_g{group}_metals")

    # group by doop
    export_with_stackedbar_doop(
        group_dataset, [.2, .4, .6, 1, 10000], f"corroles_metals_transition_g{group}_doop")
    # group by coord number
    export_with_stackedbars(group_dataset, "Coord_No",
                            f"corroles_metals_transition_g{group}_coordNo")

# region SELECTED MAINGROUP COMPLEXES
mgcn4 = corroles_maingroup.query("Coord_No == 4")
mgcn5 = corroles_maingroup.query("Coord_No == 5")
mgcn6 = corroles_maingroup.query("Coord_No == 6")
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
IronCorroles = corroles_transition.query("M == 'Fe'")
export_with_stackedbars(IronCorroles, "Ligand",
                        "corroles_metals_transition_iron_ligands")
export_with_stackedbars(IronCorroles, "Coord_No",
                        "corroles_metals_transition_iron_coordNo")
# endregion

# region copper corroles
CopperCorroles = corroles_transition.query("M == 'Cu'")
export_with_stackedbar_doop(
    CopperCorroles,  [.6, 0.8, 1, 1.5, 1000], "corroles_metals_transition_copper_doop", perc_ext_selector)

export_with_stackedbar_doop(
    CopperCorroles,  [.6, 0.8, 1, 1.5, 2, 1000], "corroles_metals_transition_copper_doop_wider", perc_ext_selector)
# # endregion

# region cobalt corroles
CobaltCorroles = corroles_transition.query("M == 'Co'")
export_with_stackedbars(CobaltCorroles, "Coord_No",
                        "corroles_metals_transition_cobalt_coordNo")
# endregion

# region manganese corroles
ManganeseCorroles = corroles_transition.query("M == 'Mn'")
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

MnpFTPC = corroles_transition.query("M == 'Mn' and Ligand == 'pFTPC'")
export_with_stackedbars(
    MnpFTPC, "Axial", "corroles_metals_transition_mnpftpc_axial", False, True)
# endregion

# region 3d/4d/5d
m3d = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
m4d = ["Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"]
m5d = ["La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"]
d3compl = corroles_transition.query("M.isin(@m3d)")
d4compl = corroles_transition.query("M.isin(@m4d)")
d5compl = corroles_transition.query("M.isin(@m5d)")
d3compl = d3compl.assign(title="3D")
d4compl = d4compl.assign(title="4D")
d5compl = d5compl.assign(title="5D")
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
cols = colors_min + colors_ext
categories = {
    "Hauptgruppen Corrole": cols[0],
    "Übergangsmetall Corrole": cols[1],
    "Freie Corrol Basen": cols[2],
    "N-Confused Corrole": cols[3],
    "Isocorrole": cols[4],
    "10-Heterocorrole": cols[5],
    "N-Heterocorrole": cols[6],
    "Corrolazine": cols[7],
    "N-Subst. Corrole": cols[8],
}

for analysis in groups:
    for mode in modes:
        fig, ax = plt.subplots()
        for c in colors:
            data = corroles_all.query("{0} == @c".format(analysis))
            if data.shape[0] > 0:
                ax.scatter(x=data[mode + " 1"].abs(), y=data[mode + " 2"] *
                           np.sign(data[mode + " 1"]), c=colors[c], label=c)
        ax.legend()
        ax.set_xlabel(f"|{mode} 1| /Å")
        ax.set_ylabel(f"{mode} 2 x sign({mode} 1) /Å")
        plt.savefig(f"out/corroles_all_scatter_{mode}_{analysis}.png")

for mode in modes:
    fig, ax = plt.subplots()
    for c in categories:
        data = allData.query("category == @c")
        ax.scatter(x=data[mode + " 1"].abs(), y=data[mode + " 2"] *
                   np.sign(data[mode + " 1"]), c=categories[c], label=c)
    ax.legend()
    ax.set_xlabel(f"|{mode} 1| /Å")
    ax.set_ylabel(f"{mode} 2 x sign({mode} 1) /Å")
    plt.savefig(f"out/anything_scatter_{mode}_category.png")
