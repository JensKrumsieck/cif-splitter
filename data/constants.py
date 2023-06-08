modes = ["Doming", "Saddling", "Ruffling", "WavingX", "WavingY", "Propellering"]
analysisColumns = [m + "1" for m in modes] + [m + "2" for m in modes]
compColumns = [m + " comp" for m in modes]
sumColumns = [m + " summed" for m in modes]
percColumns = [m+"%" for m in analysisColumns]
percCompColumns = [m+"%" for m in compColumns]
percSumColumns = [m+"%" for m in sumColumns]

colors_min = ["#999999", "#666699", "#3BC371", "#FEC211", "#336699", "#EF0000"]
colors_ext = ["#99867A", "#6B67BC", "#009999",
              "#CC6600", "#6699CC", "#FF6666"]
colors_additional = ["#73655d", "#4f4c8a", "#014747",
                     "#a35202", "#4a6f94", "#b54848"
                     ]
doop_axis_label = "$\mathregular{D_{oop}}$ /Å"
cavity_axis_label = " $\mathregular{N_{4}}$-Kavität /$\mathregular{Å^{2}}$"
dist_metal_n4 = "Abstand Metall - $\mathregular{N_{4}}$-Kavität /Å"

scatter_colors = ["#222222", "#F3C300", "#875691", "#F38500", "#A1CBF1",
                  "#BF0032", "#008855", "#0067A6", "#C3B381", "#818180",
                  "#E58FAB", "#892C16", "#F99378", "#F1A300", "#604E97",
                  "#DDD300", "#2A3C26"]
scatter_colors_to_group = {0: scatter_colors[0], 1: scatter_colors[1], 2: scatter_colors[2], 3: scatter_colors[3], 4: scatter_colors[4], 5: scatter_colors[5],
                           6: scatter_colors[6], 7: scatter_colors[7], 8: scatter_colors[8], 9: scatter_colors[9], 10: scatter_colors[10], 11: scatter_colors[11],
                           12: scatter_colors[12],  13: scatter_colors[13], 14: scatter_colors[14], 15: scatter_colors[15], "Ln": scatter_colors[16]}

x_axis_labels = {
    "CoordNo": "Koordinationszahl",
    "CoordNo_": "Koordinationszahl",
    "Group": "Gruppe",
    "Metal": "",
    "Ligand": "Ligand",
    "SubstNo": "Anzahl Substituenten",
    "title": "",
    "AxialLigand": "",
    "category": "",
    "10_Pos": "Heteroatom",
    "Cavity": "N4 Cavity",
    "CoSolv": "Kokristallisat"
}


colors_to_subgroup ={
    "freie Corrol Basen": "#999999",
    "Hauptgruppenelementcorrole": "#666999",
    "Übergangsmetallcorrole": "#3BC371",
    "Kupfercorrole": "#76D69C",
    "f-Block-Corrole": "#9EE2BA",
    "10-Isocorrole": "#FEC211",
    "5-Isocorrole": "#FED558",
    "sonstige Isocorrole" : "#FFE188",
    "Norrol": "#336699",
    "A-confused": "#6699CC",
    "B-confused": "#9387DB",
    "10-Heterocorrole" : "#EF0000",
    "N-Heterocorrole": "#FF4444",
    "Corrolazine": "#FF7D7D",
    "$N_A$ substituiert": "#CC6600",
    "$N_B$ substituiert": "#FF9933",
    "$N_A$,$N_B$-verbrückt": "#FFB76F",
    "$N_A$,$N_B$-disubst.": "#FFD6AC",
    "4-fach subst.": "#CC9900"
}

colors_classes = ['#999999', '#666999', '#3BC371', '#76D69C', '#CC6600', '#FF9933', '#FEC211', '#FED558', '#FFE188', '#336699', '#6699CC', '#EF0000','#FF4444', '#FF7D7D', '#CC6600', '#FF9933', '#FFB76F', '#FFD6AC', '#CC9900']
classlist = ["Corrole", "Isocorrole", "Heterocorrole", "Corrolazine", "NR-Corrole", "NConfused-Corrole",
                "Norcorrole", "Isonorcorrole", "Norcorrolazine", 
                "Porphycene", "NR-Porphycene",
                "Corrphycene", "Heterocorrphycene"]