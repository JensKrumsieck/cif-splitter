# porphystruct-scripts
This Repository contains my companion scripts to [PorphyStruct](https://github.com/JensKrumsieck/PorphyStruct). Feel free to use, steal some code or do whatever you like 😎

## ubermerge.py
Ubermerge merges data from both minimal and extended basis into one excel file. Special Folder Structure needed :
/[metal]/[min/ext]/[PorphyStruct-Files]
Metal info is extracted from folder name, you need to export .json Output (which is done automatically when using Batch Processing)

use:
```Shell
python ubermerge.py [FOLDER]
```

Parameters
`FOLDER` > Selected Folder

## cif-split.py
This script accelerates CCDC mining. You can click "Download selected" in CCDC and get a CIF file with up to 30 structures which PorphyStruct can not separate. cif-split.py separates this cif file to its containing cif files using the ccdc number as filename.

use:
```Shell
python cif-split.py [FILENAME] -d
```

Parameters
`FILENAME` > The multi-cif file
`-d`/`--nodel` do not delete output folder
