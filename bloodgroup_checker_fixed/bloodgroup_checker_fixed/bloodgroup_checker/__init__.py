#!/usr/bin/env python3
"""
Blood Group Compatibility Checker Library

A comprehensive Python library for blood group compatibility analysis using public databases.

Features:
- ABO and Rh factor compatibility checking
- Extended blood group systems (Kell, Duffy, Kidd, Diego, MNS, P, Lewis)
- Emergency compatibility assessment
- Virtual blood bank simulation
- Population frequency analysis
- Clinical decision support algorithms
- Disease association data

All data sourced from public databases:
- ISBT Blood Group Antigen Facts Book
- WHO Blood Group Reference
- PubMed Central
"""

from bloodgroup_checker.models import (
    BloodGroupProfile,
    BloodType,
    RhType,
    ABO_ANTIBODIES,
    RH_ANTIBODIES,
    EXTENDED_ANTIGENS,
    UNIVERSAL_PATIENTS
)

from bloodgroup_checker.analyzer import (
    BloodGroupAnalyzer,
    CompatibilityResult,
    check_compatibility,
    get_universal_status
)

from bloodgroup_checker.database import (
    BloodGroupDatabase,
    get_blood_group_database
)

__all__ = [
    # Models
    "BloodGroupProfile",
    "BloodType",
    "RhType",
    "ABO_ANTIBODIES",
    "RH_ANTIBODIES",
    "EXTENDED_ANTIGENS",
    "UNIVERSAL_PATIENTS",

    # Analyzer
    "BloodGroupAnalyzer",
    "CompatibilityResult",
    "check_compatibility",
    "get_universal_status",

    # Database
    "BloodGroupDatabase",
    "get_blood_group_database",
]

__version__ = "1.0.0"