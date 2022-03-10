
from matplotlib import pyplot as plt
from util.analysis import groupAnalysis, perc_selector, perc_ext_selector, perc_min_selector
from util.merge import merge
from util.plotting import cm_to_inch, export_with_stackedbar_cavity, export_with_stackedbar_doop,  export_with_stackedbars, save_plot
from util.scatterpie import make_scatter_pie
from util.scatter import scatter, signed_mode
from util.settings import doop_axis_label
from util.datasource import dataSourceLoop, corroles_free, corroles_transition
import matplotlib
# plot styles
matplotlib.use('Agg')
plt.style.use(['science', 'nature', 'no-latex'])
plt.rcParams["figure.figsize"] = (cm_to_inch(16), cm_to_inch(13))
plt.rcParams["figure.dpi"] = 1200
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.titlesize"] = 9
plt.rcParams["xtick.labelsize"] = 9
plt.rcParams["ytick.labelsize"] = 9
plt.rcParams["font.family"] = "Arial"

# Key = DataFrame Series : (FileName, Print Legend)
analysisTypes = {
    "Group": ("Group", False),
    "No_Subs": ("substituents", False),
    "Coord_No": ("coordNo", True),
    "category": ("category", True),
    "M": ("metals", True)
}

# loops
for datasource in dataSourceLoop:
    fig, ax = make_scatter_pie(datasource.dataFrame)
    save_plot(datasource.outputFolder + "_periodic_table")
    export_with_stackedbar_doop(datasource.dataFrame,
                                [.2, .4, .6, 1, 1000],
                                datasource.outputFolder + "_doop")
    export_with_stackedbar_doop(datasource.dataFrame,
                                [.2, .4, .6, .8, 1, 1.5, 2, 1000],
                                datasource.outputFolder + "_doop_wide")
    export_with_stackedbar_doop(datasource.dataFrame,
                                [.6, .7, .8, .9, 1, 1.2, 1.8, 1000],
                                datasource.outputFolder + "_doop_wide_v2")
    export_with_stackedbar_cavity(datasource.dataFrame,
                                  [6, 6.5, 6.75, 7.00, 7.25, 7.5, 7.75, 8.0, 8.5, 1000],
                                  datasource.outputFolder + "_cavity")
    for analysis in analysisTypes:
        export_with_stackedbars(datasource.dataFrame,
                                analysis,
                                datasource.outputFolder + "_" + analysisTypes[analysis][0],
                                True, analysisTypes[analysis][1])
# additional doop plots
export_with_stackedbar_doop(corroles_free.dataFrame.query("`δoop (min) %` < .03"),
                            [.6, .7, .8, .9, 1, 1.2, 1.8, 1000],
                            "corroles/corroles/freebases_doop_min",
                            perc_min_selector, .6)
export_with_stackedbar_doop(corroles_free.dataFrame.query("`δoop (min) %` < .03"),
                            [.6, .7, .8, .9, 1, 1.2, 1.8, 1000],
                            "corroles/corroles/freebases_doop_ext")

# group 4-5 by Metal
export_with_stackedbars(corroles_transition.query(
    "Group == 4 or Group == 5"), "M", "corroles/corroles/transition_g4g5_metals")

# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = corroles_transition.query(f"Group == {group}")

    export_with_stackedbars(
        group_dataset, "M", f"corroles/corroles/corroles/transition_g{group}_metals")

    # group by doop
    export_with_stackedbar_doop(
        group_dataset, [.2, .4, .6, 1, 10000], f"corroles/corroles/transition_g{group}_doop")
    # group by coord number
    export_with_stackedbars(group_dataset, "Coord_No",
                            f"corroles/corroles/transition_g{group}_coordNo")

# # region SELECTED MAINGROUP COMPLEXES
# mgcn4 = corroles_maingroup.query("Coord_No == 4")
# mgcn5 = corroles_maingroup.query("Coord_No == 5")
# mgcn6 = corroles_maingroup.query("Coord_No == 6")
# phos_6c = mgcn6.query("M == 'P'")[perc_selector].mean()
# phos_6c["M"] = "P"
# gall_6c = mgcn6.query("M == 'Ga'")[perc_selector].mean()
# gall_6c["M"] = "Ga"
# germ_5c = mgcn5.query("M == 'Ge'")[perc_selector].mean()
# germ_5c["M"] = "Ge"
# tin_5c = mgcn5.query("M == 'Sn'")[perc_selector].mean()
# tin_5c["M"] = "Sn"
# sel_comp = pd.DataFrame([phos_6c, gall_6c, germ_5c, tin_5c])
# export_with_stackedbars(
#     sel_comp, "M", "corroles/metals_maingroup_selectedMetals", False)
# # endregion

# # region Iron Corroles
# IronCorroles = corroles_transition.query("M == 'Fe'")
# export_with_stackedbars(IronCorroles, "Ligand",
#                         "corroles/metals_transition_iron_ligands")
# export_with_stackedbars(IronCorroles, "Coord_No",
#                         "corroles/metals_transition_iron_coordNo")
# # endregion

# # region copper corroles
# CopperCorroles = corroles_transition.query("M == 'Cu'")
# export_with_stackedbar_doop(
#     CopperCorroles,  [.6, 0.8, 1, 1.5, 1000], "corroles/metals_transition_copper_doop", perc_ext_selector)

# export_with_stackedbar_doop(
#     CopperCorroles,  [.6, 0.8, 1, 1.5, 2, 1000], "corroles/metals_transition_copper_doop_wider", perc_ext_selector)
# # # endregion

# # region cobalt corroles
# CobaltCorroles = corroles_transition.query("M == 'Co'")
# export_with_stackedbars(CobaltCorroles, "Coord_No",
#                         "corroles/metals_transition_cobalt_coordNo")
# # endregion

# # region manganese corroles
# ManganeseCorroles = corroles_transition.query("M == 'Mn'")
# NeutralLigands = ["OPPh3", "H2O", "DMF", "Ph", "EtOH", "Br-Ph", "MeOH"]
# NeutralMnCors = ManganeseCorroles.query(
#     "Coord_No > 4").query("Axial.isin(@NeutralLigands)")
# AnionicMnCors = ManganeseCorroles.query(
#     "Coord_No > 4").query("~Axial.isin(@NeutralLigands)")
# NeutralAnalysis = groupAnalysis(NeutralMnCors, "M")
# NeutralAnalysis["title"] = "Neutral Ligands"
# count_n = NeutralMnCors.shape[0]
# AnionicAnalysis = groupAnalysis(AnionicMnCors, "M")
# AnionicAnalysis["title"] = "Anionic Ligands"
# count_a = AnionicMnCors.shape[0]
# Ligands = pd.concat([NeutralAnalysis, AnionicAnalysis])
# Ligands["structures"] = [count_n, count_a]
# export_with_stackedbars(
#     Ligands, "title", "corroles/metals_transition_manganese_axial", False)

# MnpFTPC = corroles_transition.query("M == 'Mn' and Ligand == 'pFTPC'")
# export_with_stackedbars(
#     MnpFTPC, "Axial", "corroles/metals_transition_mnpftpc_axial", False, True)
# # endregion

# # region 3d/4d/5d
# m3d = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
# m4d = ["Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"]
# m5d = ["La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"]
# d3compl = corroles_transition.query("M.isin(@m3d)")
# d4compl = corroles_transition.query("M.isin(@m4d)")
# d5compl = corroles_transition.query("M.isin(@m5d)")
# d3compl = d3compl.assign(title="3d")
# d4compl = d4compl.assign(title="4d")
# d5compl = d5compl.assign(title="5d")
# export_with_stackedbars(
#     pd.concat([d3compl, d4compl, d5compl]), "title", "corroles/metals_transition_dwise")
# # endregion

# # region 10hetero n
# export_with_stackedbars(heterocorroles, "10_Pos", "10-hetero/all_heteroatom", True, True)
# # endregion

# # one could improve colors later....
# scatter_colors = ["#222222", "#F3C300", "#875691", "#F38500", "#A1CBF1",
#                   "#BF0032", "#008855", "#0067A6", "#C3B381", "#818180",
#                   "#E58FAB", "#892C16", "#F99378", "#F1A300", "#604E97",
#                   "#DDD300", "#2A3C26"]

# groups = ["No_Subs", "Group"]
# modes = ["dom", "sad", "ruf", "wav x", "wav y"]
# colors = {0: scatter_colors[0], 1: scatter_colors[1], 2: scatter_colors[2], 3: scatter_colors[3], 4: scatter_colors[4], 5: scatter_colors[5],
#           6: scatter_colors[6], 7: scatter_colors[7], 8: scatter_colors[8], 9: scatter_colors[9], 10: scatter_colors[10], 11: scatter_colors[11],
#           12: scatter_colors[12],  13: scatter_colors[13], 14: scatter_colors[14], 15: scatter_colors[15], "Ln": scatter_colors[16]}
# categories = {
#     "Hauptgruppen Corrole": scatter_colors[0],
#     "Übergangsmetall Corrole": scatter_colors[1],
#     "Freie Corrol Basen": scatter_colors[2],
#     "N-Confused Corrole": scatter_colors[3],
#     "Isocorrole": scatter_colors[4],
#     "10-Heterocorrole": scatter_colors[5],
#     "N-Heterocorrole": scatter_colors[6],
#     "Corrolazine": scatter_colors[7],
#     "N-Subst. Corrole": scatter_colors[8],
#     "Norcorrole": scatter_colors[9]
# }

# for analysis in groups:
#     for mode in modes:
#         scatter(corroles_all, colors, analysis,
#                 lambda x: x[mode + " 1"].abs(), f"|{mode} 1| /Å",
#                 lambda y: signed_mode(y, mode), f"{mode} 2 x sign({mode} 1) /Å",
#                 f"corroles/all_scatter_{mode}_{analysis}")
#     scatter(corroles_all, colors, analysis,
#             lambda x: x["wav x comp"], "wav x /Å",
#             lambda y: y["wav y comp"], "wav y /Å",
#             f"corroles/all_scatter_wavxy_{analysis}")
# prefix = {
#     "anything": allData_corroles,
#     "anything_with_norcorroles": allData_corroleAndNor
# }

# for filename in prefix:
#     data = prefix[filename]
#     for analysis in groups:
#         for mode in modes:
#             scatter(data, colors, analysis,
#                     lambda x: x[mode + " 1"].abs(), f"|{mode} 1| /Å",
#                     lambda y: signed_mode(y, mode), f"{mode} 2 x sign({mode} 1) /Å",
#                     f"{filename}_scatter_{mode}_{analysis}")
#             scatter(data, colors, analysis,
#                     lambda x: x[mode + " comp"], f"{mode} /Å",
#                     lambda y: y["Cavity"], f"N4 Cavity /Å²",
#                     f"{filename}_scatter_{mode}_vs_cavity_{analysis}")

#         scatter(data, colors, analysis,
#                 lambda x: x["wav x comp"], "wav x /Å",
#                 lambda y: y["wav y comp"], "wav y /Å",
#                 f"{filename}_scatter_wavxy_{analysis}")

#     for mode in modes:
#         scatter(data, categories, "category",
#                 lambda x: x[mode + " 1"].abs(), f"|{mode} 1| /Å",
#                 lambda y: signed_mode(y, mode), f"{mode} 2 x sign({mode} 1) /Å",
#                 f"{filename}_scatter_{mode}_category")
#         scatter(data, categories, "category",
#                 lambda x: x[mode + " comp"], f"{mode} /Å",
#                 lambda y: y["Cavity"], f"N4 Cavity /Å²",
#                 f"{filename}_scatter_{mode}_vs_cavity_category")
#     scatter(data, categories, "category",
#             lambda x: x["wav x comp"], "wav x /Å",
#             lambda y: y["wav y comp"], "wav y /Å",
#             f"{filename}_scatter_wavxy_category")
#     scatter(data, categories, "category",
#             lambda x: x["Doop (exp.)"], doop_axis_label,
#             lambda y: y["Cavity"], f"N4 Cavity /Å²",
#             f"{filename}_scatter_Doop_vs_cavity_category")

# # b1 vs a2 plot
# b1 = allData_corroles["dom 1"].pow(2) + allData_corroles["dom 2"].pow(2) + allData_corroles["ruf 1"].pow(2) + \
#     allData_corroles["ruf 2"].pow(2) + allData_corroles["wav x 1"].pow(2) + allData_corroles["wav x 2"].pow(2)
# a2 = allData_corroles["sad 1"].pow(2) + allData_corroles["sad 2"].pow(2) + allData_corroles["wav y 1"].pow(2) + \
#     allData_corroles["wav y 2"].pow(2) + allData_corroles["pro 1"].pow(2) + allData_corroles["pro 2"].pow(2)
# b1 = np.sqrt(b1)
# a2 = np.sqrt(a2)
# allData_corroles["B1"] = b1
# allData_corroles["A2"] = a2
# scatter(allData_corroles, categories, "category",
#         lambda x: x["B1"], "b1 /Å",
#         lambda y: y["A2"], "a2 /Å",
#         "anything_scatter_B1A2_category")

# selectedTM = ["Ni", "Cu", "Fe", "Co", "H", "Mn", "Pd", "P"]
# for m in selectedTM:
#     export_with_stackedbars(allData_corroles.query("M == @m"), "category", f"CoordCenters/anything_{m}")
