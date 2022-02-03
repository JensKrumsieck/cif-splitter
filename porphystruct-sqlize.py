import json
from typing import Union
import fnmatch
import os
import re
import sqlalchemy as sql
from sqlalchemy import INTEGER, Float, ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

try:
    os.remove("porphystruct.db")
except:
    print()

engine = sql.create_engine("sqlite:///porphystruct.db")
conn = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)

# region CONSTANTS
table_cifs = "crystal"
table_reference = "reference"
table_analysis = "analysis"
table_structure = "structure"

json_Simulation = "Simulation"
json_Result = "SimulationResult"
json_Doop = "OutOfPlaneParameter"
# endregion

# region DICTIONARIES
min_basis = {
    "Doming": "dom",
    "Saddling": "sad",
    "Ruffling": "ruf",
    "WavingX": "wavx",
    "WavingY": "wavy",
    "Propellering": "pro"
}

ext_basis = {
    "Doming": "dom1",
    "Saddling": "sad1",
    "Ruffling": "ruf1",
    "WavingX": "wavx1",
    "WavingY": "wavy1",
    "Propellering": "pro1",
    "Doming2": "dom2",
    "Saddling2": "sad2",
    "Ruffling2": "ruf2",
    "WavingX2": "wavx2",
    "WavingY2": "wavy2",
    "Propellering2": "pro2"
}
# endregion

test_path = f"D:\Desktop\HomeOffice\Corrole"
path = test_path  # use argparse later
verbose = 1

# region ORM DEFS


class Reference(Base):
    __tablename__ = table_reference
    id = Column(Integer, primary_key=True)
    doi = Column(String, unique=True)
    crystals = relationship("Crystal", back_populates=table_reference)


class Crystal(Base):
    __tablename__ = table_cifs
    id = Column(Integer, primary_key=True)
    ccdc = Column(String, unique=True)
    reference_id = Column(Integer, ForeignKey(
        table_reference+'.id'), nullable=True)
    reference = relationship("Reference", back_populates=table_cifs+"s")
    structure_id = Column(Integer, ForeignKey(
        table_structure+'.id'), nullable=True)
    structure = relationship("Structure", back_populates=table_cifs)
    analysis = relationship("Analysis", back_populates=table_cifs)


class Structure(Base):
    __tablename__ = table_structure
    id = Column(Integer, primary_key=True)
    formula = Column(String)
    ligand = Column(String)
    metal = Column(String)
    group = Column(String)
    coordination_number = Column(INTEGER)
    axial = Column(String)
    co_solvate = Column(String)
    crystal = relationship("Crystal", back_populates=table_structure)


class Analysis(Base):
    __tablename__ = table_analysis
    id = Column(Integer, primary_key=True)
    doop_exp = Column(Float)
    dom = Column(Float)
    sad = Column(Float)
    ruf = Column(Float)
    wavx = Column(Float)
    wavy = Column(Float)
    pro = Column(Float)
    doop_sim = Column(Float)
    crystal_id = Column(Integer, ForeignKey(table_cifs+'.id'))
    crystal = relationship("Crystal", back_populates=table_analysis)


Base.metadata.create_all(engine)
# endregion

# region FUNCS


def is_ext(decoded):
    return len(decoded[json_Simulation][json_Result]) > 6


def get_crystal(ccdc: str, session) -> Crystal:
    res = session.query(Crystal).filter_by(ccdc=ccdc).first()
    return res


def basename(cif) -> str:
    return os.path.basename(cif).split(".")[0]


def find_first(pattern, data) -> Union[str, None]:
    item = re.findall(pattern, data)
    if len(item) == 0:
        item = None
    else:
        item = item[0]
    return item


def extract_cif_data(cif):
    session = Session()
    formula_pattern = r"_chemical_formula_sum *'([A-Za-z0-9\W]*)'"
    doi_pattern = r"_citation_year\W*.* (10.\d{4}\/[A-Za-z0-9.\-:;<>()]*)"

    with open(cif, "r") as data:
        data = data.read()

        formula = find_first(formula_pattern, data)
        if(formula is not None):
            formula = formula.replace(" ", "")
        doi = find_first(doi_pattern, data)

        structure = Structure(formula=formula)
        ccdc = basename(cif)
        crystal = Crystal(ccdc=ccdc)
        if doi != None:
            res = session.query(Reference).filter_by(doi=doi).first()
            if(res == None):
                ref = Reference(doi=doi)
                crystal.reference = ref
                session.add(ref)
            else:
                crystal.reference = res
        if structure != None:
            crystal.structure = structure
            session.add(structure)
        session.add(crystal)
    session.commit()
# endregion


cifs = []
analysis = []
for root, dir, files in os.walk(path):
    for file in fnmatch.filter(files, "*.cif"):
        cifs.append(os.path.join(root, file))
    for file in fnmatch.filter(files, "*_analysis.json"):
        analysis.append(os.path.join(root, file))

for cif in cifs:
    ccdc = basename(cif)
    try:
        extract_cif_data(cif)
    except:
        if verbose != 0:
            print(f"Crystals {ccdc} already loaded!  Skipping...")

for an in analysis:
    file = basename(an).split("_")
    ccdc = file[0]
    suffix = ""
    if len(file) > 2:
        suffix = file[1]
    if suffix == "compl":
        ccdc += suffix
        suffix = ""

    session = Session()
    parent = get_crystal(ccdc, session)

    with open(an, "r") as handle:
        decoded = json.load(handle)
        doop_exp = decoded[json_Doop]["Value"]
        doop_sim = decoded[json_Simulation][json_Doop]["Value"]
        res = decoded[json_Simulation][json_Result]
        data = {}
        if is_ext(decoded):
            for value in res:
                data[ext_basis[value["Key"]]] = value["Value"]
        else:
            for value in res:
                data[min_basis[value["Key"]]] = value["Value"]
            insert = Analysis(doop_exp=doop_exp,
                              doop_sim=doop_sim,
                              dom=data["dom"],
                              sad=data["sad"],
                              ruf=data["ruf"],
                              wavx=data["wavx"],
                              wavy=data["wavy"],
                              pro=data["pro"],
                              crystal=parent)
            session.add(insert)
    session.commit()
