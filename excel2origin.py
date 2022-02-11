import fnmatch
import os
import originpro as op
import pandas as pd

### CRUNCH ALL XLSX FILES IN OUT TO ORIGIN! ###
path = "out/"
data = []
for root, dir, files in os.walk(path):
    for file in fnmatch.filter(files, "*.xlsx"):
        data.append(os.path.join(root, file))

for analysis in data:
    df = pd.read_excel(analysis)
    wks = op.new_sheet("w", os.path.basename(analysis))
    wks.from_df(df)
op.set_show(True)  # active origin
