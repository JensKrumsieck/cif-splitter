from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class Analysis:
    Id: str
    Type: str
    DoopExp: float
    DoopSim: float
    Doming1: float
    Saddling1: float
    Ruffling1: float
    WavingX1: float
    WavingY1: float
    Propellering1: float
    Doming2: float
    Saddling2: float
    Ruffling2: float
    WavingX2: float
    WavingY2: float
    Propellering2: float
    Cavity: float
    MetalToN4: Optional[float] = 0
    MetalToMean: Optional[float] = 0
