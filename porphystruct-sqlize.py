from typing import Union
import fnmatch
import os
import re
import sqlalchemy as sql
from sqlalchemy import ForeignKey, Integer, String, Column, select
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = sql.create_engine("sqlite:///porphystruct.db")
conn = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)

# region CONSTANTS
table_cifs = "crystal"
table_reference = "reference"
table_analysis = "analysis"
table_structure = "structure"
# endregion

test_path = f"D:\Desktop\HomeOffice\Corrole"
path = test_path  # use argparse later

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


class Structure(Base):
    __tablename__ = table_structure
    id = Column(Integer, primary_key=True)
    formula = Column(String)
    ligand = Column(String)
    crystal = relationship("Crystal", back_populates=table_structure)


Base.metadata.create_all(engine)
# endregion

# region FUNCS


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
        ccdc = os.path.basename(cif).split(".")[0]
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
for root, dir, files in os.walk(path):
    for file in fnmatch.filter(files, "*.cif"):
        cifs.append(os.path.join(root, file))

for cif in cifs:
    extract_cif_data(cif)
