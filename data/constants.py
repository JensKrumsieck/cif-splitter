modes = ["Doming", "Saddling", "Ruffling", "WavingX", "WavingY", "Propellering"]
analysisColumns = [m + "1" for m in modes] + [m + "2" for m in modes]
compColumns = [m + " comp" for m in modes]
percColumns = [m+"%" for m in analysisColumns]
percCompColumns = [m+"%" for m in compColumns]

colors_min = ["#999999", "#666699", "#3BC371", "#FEC211", "#336699", "#EF0000"]
colors_ext = ["#99867A", "#6B67BC", "#009999",
              "#CC6600", "#6699CC", "#FF6666"]
doop_axis_label = "$\mathregular{D_{oop}}$ /Å"
cavity_axis_label = "Cavity /Å"

scatter_colors = ["#222222", "#F3C300", "#875691", "#F38500", "#A1CBF1",
                  "#BF0032", "#008855", "#0067A6", "#C3B381", "#818180",
                  "#E58FAB", "#892C16", "#F99378", "#F1A300", "#604E97",
                  "#DDD300", "#2A3C26"]
scatter_colors_to_group = {0: scatter_colors[0], 1: scatter_colors[1], 2: scatter_colors[2], 3: scatter_colors[3], 4: scatter_colors[4], 5: scatter_colors[5],
                           6: scatter_colors[6], 7: scatter_colors[7], 8: scatter_colors[8], 9: scatter_colors[9], 10: scatter_colors[10], 11: scatter_colors[11],
                           12: scatter_colors[12],  13: scatter_colors[13], 14: scatter_colors[14], 15: scatter_colors[15], "Ln": scatter_colors[16]}

x_axis_labels = {
    "Coord_No": "Koordinationszahl",
    "Group": "Gruppe",
    "M": "",
    "Ligand": "Ligand",
    "No_Subs": "Anzahl Substituenten",
    "title": "",
    "Axial": "",
    "category": "",
    "10_Pos": "Heteroatom",
    "Cavity": "N4 Cavity"
}