from dataclasses import dataclass, field
from . import Analysis


@dataclass
class Crystal:
    CCDC: str
    Class: str
    Ligand: str
    Metal: str
    Group: str
    AxialLigand: str
    CoordNo: int
    SubstNo: int
    CoSolv: str
    Analyses:list[Analysis] = field(default_factory=list)
