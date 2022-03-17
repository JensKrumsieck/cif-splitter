from calendar import c
import os
import pandas as pd
from util.merge import merge


class DataSource:
    def __init__(self, inputFileName="", outputFolder="", categoryName=""):
        if(inputFileName == ""):
            return
        self.inputFileName = inputFileName
        self.outputFolder = outputFolder
        self.categoryName = categoryName
        self.dataFrame = merge([inputFileName]).assign(category=self.categoryName)
        self.makeFolder()
        self.inputFileName += "/all"

    inputFileName: str
    outputFolder: str
    categoryName: str
    dataFrame: pd.DataFrame

    def makeFolder(self):
        if not os.path.exists(f"out/{self.outputFolder}"):
            os.makedirs(f"out/{self.outputFolder}", exist_ok=True)


def create(outputfolder: str, dataFrame: pd.DataFrame) -> DataSource:
    datasrc = DataSource()
    datasrc.outputFolder = outputfolder
    datasrc.dataFrame = dataFrame
    return datasrc


root = r"D:\PowerFolders\Forschung\PorphyStruct Results\\"
if not os.path.exists(root): # we are not at home
    root = r"C:\Users\jenso\PowerFolders\Forschung\PorphyStruct Results\\"
corroles_transition = DataSource(root + r"Corrole\TransitionMetals.xlsx",
                                 "corroles/corroles/transition metals/",
                                 "Übergangsmetall Corrole")
corroles_main = DataSource(root + r"Corrole\MainGroup.xlsx",
                           "corroles/corroles/maingroup/",
                           "Hauptgruppen Corrole")
corroles_free = DataSource(root + r"Corrole\FreeBases.xlsx",
                           "corroles/corroles/freebase/",
                           "Freie Corrol Basen")
corroles_fBlock = DataSource(root + r"Corrole\fBlock.xlsx",
                             "corroles/corroles/f-block/",
                             "f-Block Corrole")
corroles_iso = DataSource(root + r"Isocorrole/Isocorroles.xlsx",
                          "corroles/isocorroles/",
                          "Isocorrole")
corroles_hetero = DataSource(root + r"Heterocorrole\Heterocorroles.xlsx",
                             "corroles/hetero/10-hetero/",
                             "10-Heterocorrole")
corroles_nHetero = DataSource(root + r"CoreHeterocorrole\CoreHeterocorroles.xlsx",
                              "corroles/hetero/n-hetero/",
                              "N-Heterocorrole")
corroles_nconfused = DataSource(root + r"NConfusedCorrole\NConfused.xlsx",
                                "corroles/n-confused/",
                                "N-Confused Corrole")
corroles_nSubst = DataSource(root + r"NRCorroles\NRCorroles.xlsx",
                             "corroles/hetero/n-substituted/",
                             "N-subst. Corrole")
corroles_corrolazines = DataSource(root + r"Corrolazine\Corrolazines.xlsx",
                                   "corroles/hetero/corrolazines/",
                                   "Corrolazine")
norcorroles = DataSource(root + r"Norcorrole\Norcorrole.xlsx",
                         "norcorroles",
                         "Norcorrole")

corroles_df = create("corroles/corroles/d_f_block",
                     pd.concat([corroles_fBlock.dataFrame,
                                corroles_transition.dataFrame], ignore_index=True))
corroles_metallo = create("corroles/corroles/metallo",
                          pd.concat([corroles_df.dataFrame,
                                     corroles_main.dataFrame], ignore_index=True))
corroles = create("corroles/corroles/all",
                  pd.concat([corroles_metallo.dataFrame,
                             corroles_free.dataFrame], ignore_index=True))
heterocorroles_all = create("corroles/hetero/all",
                            pd.concat([corroles_hetero.dataFrame,
                                       corroles_corrolazines.dataFrame,
                                       corroles_nHetero.dataFrame,
                                       corroles_nSubst.dataFrame], ignore_index=True))
corroles_all = create("corroles/any",
                      pd.concat([corroles.dataFrame,
                                 heterocorroles_all.dataFrame,
                                 corroles_nconfused.dataFrame,
                                 corroles_iso.dataFrame], ignore_index=True))
anything = create("any", pd.concat([corroles_all.dataFrame, norcorroles.dataFrame], ignore_index=True))


dataSourceLoop = [anything,  # corroles and norcorroles
                  corroles,  # all corroles, hetero, etc-
                  corroles_all,  # all usual corroles
                  corroles_metallo, corroles_df, corroles_main, corroles_fBlock, corroles_transition,  # complexes
                  corroles_free,  # free bases
                  heterocorroles_all,  # all hetero like
                  corroles_hetero, corroles_corrolazines, corroles_nHetero, corroles_nSubst,  # all heterocorroles
                  corroles_iso,  # isocorroles
                  corroles_nconfused,  # nconfused
                  norcorroles  # norcorroles
                  ]
