from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from util.analysis import perc_selector, perc_ext_selector, perc_min_selector, modes
from util.plotting import cm_to_inch, export_with_stackedbar_cavity, export_with_stackedbar_doop,  export_with_stackedbars, save_plot
from util.scatterpie import make_scatter_pie
from util.scatter import scatter, signed_mode
from util.settings import doop_axis_label, scatter_colors_to_group
from util.datasource import dataSourceLoop, corroles_free, corroles_transition, norcorroles, anything, corroles_hetero, corroles_main
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
    "Group": ("Group", True),
    "No_Subs": ("substituents", True),
    "Coord_No": ("coordNo", False),
    "category": ("category", False),
    "M": ("metals", False)
}

categories = {
    "Hauptgruppen Corrole": scatter_colors_to_group[0],
    "Übergangsmetall Corrole": scatter_colors_to_group[1],
    "Freie Corrol Basen": scatter_colors_to_group[2],
    "N-Confused Corrole": scatter_colors_to_group[3],
    "Isocorrole": scatter_colors_to_group[4],
    "10-Heterocorrole": scatter_colors_to_group[5],
    "N-Heterocorrole": scatter_colors_to_group[6],
    "Corrolazine": scatter_colors_to_group[7],
    "N-Subst. Corrole": scatter_colors_to_group[8],
    "Norcorrole": scatter_colors_to_group[9],
    "f-Block Corrole": scatter_colors_to_group[10]
}

anything.dataFrame.to_excel("all-data-merged.xlsx")

df = anything.dataFrame.groupby("category").mean()
df.plot.bar(y="Cavity")
save_plot(anything.outputFolder + "__cavities_per_cat")

colors = []
# loops
for datasource in dataSourceLoop:
    # add sum of waving col
    datasource.dataFrame["sum wav"] = datasource.dataFrame["wav x comp"] + datasource.dataFrame["wav y comp"]
    fig, ax = make_scatter_pie(datasource.dataFrame)
    save_plot(datasource.outputFolder + "_periodic_table")  # makes periodic table plot
    # Doop Plots
    export_with_stackedbar_doop(datasource.dataFrame,
                                [.2, .4, .6, 1, 1000],
                                datasource.outputFolder + "_doop")
    export_with_stackedbar_doop(datasource.dataFrame,
                                [.2, .4, .6, .8, 1, 1.5, 2, 1000],
                                datasource.outputFolder + "_doop_wide")
    export_with_stackedbar_doop(datasource.dataFrame,
                                [.6, .7, .8, .9, 1, 1.2, 1.8, 1000],
                                datasource.outputFolder + "_doop_wide_v2")
    # Cavity Plot
    export_with_stackedbar_cavity(datasource.dataFrame,
                                  [6, 6.5, 6.75, 7.00, 7.25, 7.5, 7.75, 8.0, 8.5, 1000],
                                  datasource.outputFolder + "_cavity")
    for analysis in analysisTypes:  # loop over analysis types
        # choose color for scattter plots
        if analysis == "category":
            colors = categories
        else:
            colors = scatter_colors_to_group
        # normal stacked bars plot with doop as height for each analysis and dataframe
        export_with_stackedbars(datasource.dataFrame,
                                analysis,
                                datasource.outputFolder + "_" + analysisTypes[analysis][0],
                                True, analysisTypes[analysis][1])

        # Scatter Plots
        if analysis != "M":  # metals as colors do not make sense
            for mode in modes:
                # mode 1 vs sgn(mode1) x mode2 like Shape of Porphyrins
                scatter(datasource.dataFrame, colors, analysis,
                        lambda x: x[mode + " 1"].abs(), f"|{mode} 1| /Å",
                        lambda y: signed_mode(y, mode), f"{mode} 2 x sign({mode} 1) /Å",
                        f"{datasource.outputFolder}_scatter_{mode}_{analysis}")
                # mode comp vs cavity
                scatter(datasource.dataFrame, colors, analysis,
                        lambda x: x["Cavity"], f"N4 Cavity /Å²",
                        lambda y: y[mode + " comp"], f"{mode} /Å",
                        f"{datasource.outputFolder}_scatter_{mode}_vs_cavity_{analysis}")
            # wavx vs wavy plots
            scatter(datasource.dataFrame, colors, analysis,
                    lambda x: x["wav x comp"], "wav x /Å",
                    lambda y: y["wav y comp"], "wav y /Å",
                    f"{datasource.outputFolder}_scatter_wavxy_{analysis}")
            # sum wav vs cavity
            scatter(datasource.dataFrame, colors, analysis,
                    lambda x: x["Cavity"], f"N4 Cavity /Å²",
                    lambda y: y["sum wav"], "wav x + wav y /Å",
                    f"{datasource.outputFolder}_scatter_wavxy_vs_cavity_{analysis}")
            # doop vs cavity
            scatter(datasource.dataFrame, colors, analysis,
                    lambda x: x["Doop (exp.)"], doop_axis_label,
                    lambda y: y["Cavity"], f"N4 Cavity /Å²",
                    f"{datasource.outputFolder}_scatter_Doop_vs_cavity_{analysis}")
            if datasource != norcorroles and datasource != anything:  # Norcorroles are not C2v, so B1/A2 is not valid!
                # b1 vs a2 plot
                b1 = datasource.dataFrame["dom 1"].pow(2) + datasource.dataFrame["dom 2"].pow(2) + datasource.dataFrame["ruf 1"].pow(2) + \
                    datasource.dataFrame["ruf 2"].pow(2) + datasource.dataFrame["wav x 1"].pow(2) + datasource.dataFrame["wav x 2"].pow(2)
                a2 = datasource.dataFrame["sad 1"].pow(2) + datasource.dataFrame["sad 2"].pow(2) + datasource.dataFrame["wav y 1"].pow(2) + \
                    datasource.dataFrame["wav y 2"].pow(2) + datasource.dataFrame["pro 1"].pow(2) + datasource.dataFrame["pro 2"].pow(2)
                b1 = np.sqrt(b1)
                a2 = np.sqrt(a2)
                datasource.dataFrame["B1"] = b1
                datasource.dataFrame["A2"] = a2
                scatter(datasource.dataFrame, colors, analysis,
                        lambda x: x["B1"], "b1 /Å",
                        lambda y: y["A2"], "a2 /Å",
                        f"{datasource.outputFolder}_scatter_B1A2_{analysis}")
    # doop plots for copper complexes with ext basis
    if datasource.dataFrame.query("M == 'Cu'").index.shape[0] > 0:
        CopperCorroles = datasource.dataFrame.query("M == 'Cu'")
        export_with_stackedbar_doop(
            CopperCorroles,  [.6, 0.8, 1, 1.5, 1000], datasource.outputFolder + "_copper_doop", perc_ext_selector)
        export_with_stackedbar_doop(
            CopperCorroles,  [.6, 0.8, 1, 1.5, 2, 1000], datasource.outputFolder + "_copper_doop_wider", perc_ext_selector)


# additional doop plots
export_with_stackedbar_doop(corroles_free.dataFrame.query("`δoop (min) %` < .03"),
                            [.6, .7, .8, .9, 1, 1.2, 1.8, 1000],
                            "corroles/corroles/freebases_doop_min",
                            perc_min_selector, .6)
export_with_stackedbar_doop(corroles_free.dataFrame.query("`δoop (min) %` < .03"),
                            [.6, .7, .8, .9, 1, 1.2, 1.8, 1000],
                            "corroles/corroles/freebases_doop_ext")

# group 4-5 by Metal
export_with_stackedbars(corroles_transition.dataFrame.query(
    "Group == 4 or Group == 5"), "M", corroles_transition.outputFolder + "_g4g5_metals")
# loop other groups
groups = [6, 7, 8, 9, 10, 11, 12]
for group in groups:
    # group by metal
    group_dataset = corroles_transition.dataFrame.query(f"Group == {group}")

    export_with_stackedbars(
        group_dataset, "M", corroles_transition.outputFolder + f"_g{group}_metals")

    # group by doop
    export_with_stackedbar_doop(
        group_dataset, [.2, .4, .6, 1, 10000], corroles_transition.outputFolder + f"_g{group}_doop")
    # group by coord number
    export_with_stackedbars(group_dataset, "Coord_No",
                            corroles_transition.outputFolder + f"g{group}_coordNo")




selectedTM = ["Ni", "Cu", "Fe", "Co", "H", "Mn", "Pd", "P"]
for m in selectedTM:
    export_with_stackedbars(anything.dataFrame.query("M == @m"), "category", f"any_coordination_center_{m}")

# region 10hetero n
export_with_stackedbars(corroles_hetero.dataFrame, "10_Pos", corroles_hetero.outputFolder + "_heteroatom", True, True)
# endregion

# SELECTED MAINGROUP COMPLEXES (PorphyStruct Paper)
mgcn4 = corroles_main.dataFrame.query("Coord_No == 4")
mgcn5 = corroles_main.dataFrame.query("Coord_No == 5")
mgcn6 = corroles_main.dataFrame.query("Coord_No == 6")
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
    sel_comp, "M", corroles_main.outputFolder + "_selectedMetals", False)

# region 3d/4d/5d
m3d = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
m4d = ["Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"]
m5d = ["La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"]
d3compl = corroles_transition.dataFrame.query("M.isin(@m3d)")
d4compl = corroles_transition.dataFrame.query("M.isin(@m4d)")
d5compl = corroles_transition.dataFrame.query("M.isin(@m5d)")
d3compl = d3compl.assign(title="3d")
d4compl = d4compl.assign(title="4d")
d5compl = d5compl.assign(title="5d")
export_with_stackedbars(
    pd.concat([d3compl, d4compl, d5compl]), "title", corroles_transition.outputFolder + "dwise")
# endregion
