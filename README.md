# porphystruct-scripts

This repository contains my companion scripts for data analysis using [PorphyStruct](https://github.com/JensKrumsieck/PorphyStruct).

The JupyterNotebooks are used to create all figures contained in my doctoral thesis. The data created by the [PorphyStruct](https://github.com/JensKrumsieck/PorphyStruct) batchprocessing function can be merged in to a single XLSX file which can be used for further analysis. 
For this to work all files have to be classified with my [File Classifier](https://github.com/JensKrumsieck/FileClassification). 

These scripts are created for my analyses, so they will not work out of the box. However you can take a look at the excel file appended to the [SI of my thesis](https://data.mendeley.com/datasets/dpc3v9tvsm/1).

## Steps to reproduce
1. With CSD Conquest all files matching the structural motifs of Corroles, Norcorroles, Porphycenes and Corrphycenes were downloaded as mol2-Files
2. With the FileClassification Tool, all Files were classified and than validated by hand.
3. PorphyStruct (V 2.0) Batch Processing was used with the extended Basis to generate Data
4. Data was merged into Excel file using the PorphyStruct Python Scripts

## Example image
Example tSNE Analysis created with these scripts:
![tsne_all_dominant](https://github.com/JensKrumsieck/porphystruct-scripts/assets/4296194/88c0e3ff-f46c-45ed-bff2-2691f1934201)
