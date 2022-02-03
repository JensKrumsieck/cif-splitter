
import argparse
from itertools import dropwhile, takewhile
import os
import re
import sys

### ARGPARSE ###
parser = argparse.ArgumentParser(prog='CIF Splitter')
parser.add_argument("file", help="specify multi structural cif file")
parser.add_argument("-d", "--nodel", action='store_true',  help="do not delete output folder")
args = parser.parse_args()
### END ARGPARSE ###

### VARIABLES ###
commentBlock = """
####################################################################### 
# 
# This file contains crystal structure data downloaded from the 
# Cambridge Structural Database (CSD) hosted by the Cambridge 
# Crystallographic Data Centre (CCDC).
# 
# Full information about CCDC data access policies and citation 
# guidelines are available at http://www.ccdc.cam.ac.uk/access/V1 
# 
# Audit and citation data items may have been added by the CCDC. 
# Please retain this information to preserve the provenance of 
# this file and to allow appropriate attribution of the data. 
# 
#######################################################################
"""
ccdcNo = "_database_code_depnum_ccdc_archive"
regex = r"^_database_code_depnum_ccdc_archive 'CCDC\W(\d*)'$"
path = os.getcwd()
dir = path + "/out"
### END VARIABLES ###

try:
    with open(args.file, 'r') as file:
        data = file.read().split(commentBlock)
        print(len(data))  # number of files
        if(not args.nodel):
            if os.path.exists(dir):
                os.rmdir(dir)
            os.mkdir(dir)
        for cif in data:
            lines = cif.splitlines()
            res = 0
            for i in range(len(lines)):
                if lines[i].startswith(ccdcNo):
                    res = i
                    break
            match = re.match(regex, lines[i])
            save = match.group(1) + ".cif"
            with open(dir+"/"+save, "w") as newCif:
                newCif.writelines(cif)

except IOError:
    print("file not found at " + args.file)
    sys.exit(1)  # exit with failure
### END PARSING ###
