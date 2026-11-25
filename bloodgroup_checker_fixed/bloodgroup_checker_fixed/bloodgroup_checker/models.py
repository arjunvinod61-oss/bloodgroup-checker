"""
Blood Group Antigen and System Definitions

Based on ISBT Blood Group Antigen Facts Book and WHO standards.
Data sourced from public genomic and transfusion medicine databases.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple
import json


class BloodType(Enum):
    """ABO blood types."""
    A = "A"
    B = "B"
    AB = "AB"
    O = "O"


class RhType(Enum):
    """Rh factor types."""
    POSITIVE = "+"
    NEGATIVE = "-"


@dataclass
class BloodGroupProfile:
    """Complete blood group profile including extended antigens."""
    abo: BloodType
    rh: RhType
    kell: Optional[Dict] = None  # {present: bool, variants: Set[str]}
    duffy: Optional[Dict] = None
    kidd: Optional[Dict] = None
    diego: Optional[Dict] = None
    mns: Optional[Dict] = None
    p: Optional[Dict] = None
    lewis: Optional[Dict] = None
    microvariants: Optional[Set[str]] = None

    def to_dict(self) -> dict:
        """Convert profile to dictionary."""
        result = {
            "abo": self.abo.value,
            "rh": self.rh.value,
        }
        if self.kell:
            result["kell"] = self.kell
        if self.duffy:
            result["duffy"] = self.duffy
        if self.kidd:
            result["kidd"] = self.kidd
        if self.diego:
            result["diego"] = self.diego
        if self.mns:
            result["mns"] = self.mns
        if self.p:
            result["p"] = self.p
        if self.lewis:
            result["lewis"] = self.lewis
        if self.microvariants:
            result["microvariants"] = list(self.microvariants)
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'BloodGroupProfile':
        """Create profile from dictionary."""
        return cls(
            abo=BloodType(data["abo"]),
            rh=RhType(data["rh"]),
            kell=data.get("kell"),
            duffy=data.get("duffy"),
            kidd=data.get("kidd"),
            diego=data.get("diego"),
            mns=data.get("mns"),
            p=data.get("p"),
            lewis=data.get("lewis"),
            microvariants=set(data.get("microvariants", [])) if data.get("microvariants") else None
        )


# Antibody production rules based on ABO/Rh system
# Data from WHO Blood Group Antigen Facts Book

ABO_ANTIBODIES = {
    BloodType.A: {"anti_B": True, "anti_A": False, "natural": True},
    BloodType.B: {"anti_A": True, "anti_B": False, "natural": True},
    BloodType.AB: {"anti_A": False, "anti_B": False, "natural": True},
    BloodType.O: {"anti_A": True, "anti_B": True, "natural": True},
}

RH_ANTIBODIES = {
    RhType.POSITIVE: {"anti_D": False, "natural": False},
    RhType.NEGATIVE: {"anti_D": False, "natural": False},
}

# Extended antigen definitions
# ISBT nomenclature for extended blood group systems

EXTENDED_ANTIGENS = {
    "KELL": {
        "system": "KELL",
        "genes": ["KEL"],
        "phenotype": ["K", "k", "Kpa", "Kpb"],
        "antibody": ["anti-K"],
        "prevalence": {"K": 0.01, "k": 0.85, "Kpa": 0.07, "Kpb": 0.07},
        "clinical": "KEL deficiency may cause mild anemia"
    },
    "DUFFY": {
        "system": "DUFFY",
        "genes": ["FY"],
        "phenotype": ["Fya", "Fyb", "FY*A.01", "FY*B.07"],
        "antibody": ["anti-Fya", "anti-Fyb"],
        "prevalence": {"Fya": 0.65, "Fyb": 0.35},
        "clinical": "Duffy negative confers malaria resistance"
    },
    "KIDD": {
        "system": "KIDD",
        "genes": ["KPA", "KID"],
        "phenotype": ["Kpa", "Kpb", "Jka", "Jkb"],
        "antibody": ["anti-Kpa", "anti-Kpb", "anti-Jka", "anti-Jkb"],
        "prevalence": {"Jka": 0.75, "Jkb": 0.85},
        "clinical": "Common cause of transfusion reactions"
    },
    "DIEGO": {
        "system": "DIEGO",
        "genes": ["DIE"],
        "phenotype": ["Dia", "Dib"],
        "antibody": ["anti-Dia", "anti-Dib"],
        "prevalence": {"Dia": 0.95, "Dib": 0.95},
        "clinical": "Anti-Dia associated with HE defect"
    },
    "MNS": {
        "system": "MNS",
        "genes": ["GY"],
        "phenotype": ["M", "N", "S", "s"],
        "antibody": ["anti-M", "anti-N", "anti-S", "anti-s"],
        "prevalence": {"M": 0.75, "N": 0.25},
        "clinical": "Autoantibodies in warm AIHA"
    },
    "P": {
        "system": "P",
        "genes": ["P"],
        "phenotype": ["P1", "P", "p"],
        "antibody": ["anti-P1", "anti-P1M", "anti-P"],
        "prevalence": {"P1": 0.90, "p": 0.10},
        "clinical": "P1/Kidd antibody association"
    },
    "LEWIS": {
        "system": "LEWIS",
        "genes": ["FUT3", "FUT2"],
        "phenotype": ["Lea", " Leb"],
        "antibody": [],
        "prevalence": {"Lea": 0.50, "Leb": 0.50},
        "clinical": "Secretor status determination"
    }
}

# Universal donor/recipient designations
UNIVERSAL_PATIENTS = {
    "O_negative": "Universal red cell recipient incompatible, Universal plasma donor",
    "AB_positive": "Universal plasma recipient, Universal red cell donor",
    "O_positive": "Universal red cell donor for Rh+ patients",
    "A_negative": "Universal red cell recipient for A/B types only"
}

# Population frequencies by ethnicity (approximate, from public databases)
POPULATION_FREQUENCIES = {
    "North_European": {
        "O": {"positive": 0.42, "negative": 0.13},
        "A": {"positive": 0.23, "negative": 0.06},
        "B": {"positive": 0.07, "negative": 0.02},
        "AB": {"positive": 0.03, "negative": 0.01}
    },
    "East_Asian": {
        "O": {"positive": 0.45, "negative": 0.09},
        "A": {"positive": 0.35, "negative": 0.07},
        "B": {"positive": 0.17, "negative": 0.04},
        "AB": {"positive": 0.03, "negative": 0.01}
    },
    "West_African": {
        "O": {"positive": 0.46, "negative": 0.09},
        "A": {"positive": 0.42, "negative": 0.08},
        "B": {"positive": 0.10, "negative": 0.02},
        "AB": {"positive": 0.02, "negative": 0.01}
    },
    "Hispanic": {
        "O": {"positive": 0.51, "negative": 0.12},
        "A": {"positive": 0.32, "negative": 0.07},
        "B": {"positive": 0.13, "negative": 0.03},
        "AB": {"positive": 0.04, "negative": 0.01}
    }
}