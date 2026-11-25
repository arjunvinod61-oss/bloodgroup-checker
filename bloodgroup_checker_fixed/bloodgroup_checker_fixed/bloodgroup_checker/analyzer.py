"""Educational ABO/Rh red-cell compatibility rules.

This module is not a clinical transfusion decision system. Actual transfusions
require validated blood typing, antibody screening and serologic crossmatching.
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple
from bloodgroup_checker.models import BloodGroupProfile, BloodType, RhType, EXTENDED_ANTIGENS

@dataclass
class CompatibilityResult:
    is_compatible: bool
    risk_level: str
    reason: str
    detected_antibodies: List[str]
    additional_notes: List[str]

class BloodGroupAnalyzer:
    """Rule-based educational ABO/Rh red-cell compatibility reference."""
    def __init__(self):
        self.extended_systems = EXTENDED_ANTIGENS

    def check_abo_compatibility(self, donor: BloodGroupProfile, recipient: BloodGroupProfile) -> CompatibilityResult:
        errors, antibodies, notes = [], [], []
        abo_allowed = {
            BloodType.O: {BloodType.O, BloodType.A, BloodType.B, BloodType.AB},
            BloodType.A: {BloodType.A, BloodType.AB},
            BloodType.B: {BloodType.B, BloodType.AB},
            BloodType.AB: {BloodType.AB},
        }
        if recipient.abo not in abo_allowed[donor.abo]:
            errors.append(f"ABO-incompatible for red-cell transfusion: {donor.abo.value} donor to {recipient.abo.value} recipient")
            if recipient.abo == BloodType.A:
                antibodies.append("anti-B")
            elif recipient.abo == BloodType.B:
                antibodies.append("anti-A")
            elif recipient.abo == BloodType.O:
                if donor.abo in (BloodType.A, BloodType.AB):
                    antibodies.append("anti-A")
                if donor.abo in (BloodType.B, BloodType.AB):
                    antibodies.append("anti-B")
        # RhD rule applies regardless of ABO group.
        if recipient.rh == RhType.NEGATIVE and donor.rh == RhType.POSITIVE:
            errors.append("RhD-incompatible for a RhD-negative recipient")
            notes.append("RhD-negative people are not assumed to have anti-D; sensitization can occur after exposure.")
        compatible = not errors
        return CompatibilityResult(
            is_compatible=compatible,
            risk_level="EDUCATIONAL_MATCH" if compatible else "INCOMPATIBLE",
            reason="ABO/RhD rules indicate a compatible red-cell pairing" if compatible else "; ".join(errors),
            detected_antibodies=antibodies,
            additional_notes=notes + ["This simplified rule check is not a transfusion authorization."]
        )

    def check_extended_compatibility(self, donor: BloodGroupProfile, recipient: BloodGroupProfile) -> Dict:
        """Do not infer clinical extended-antigen compatibility from incomplete profiles."""
        supplied = [name for name in ("kell","duffy","kidd","diego","mns","p","lewis")
                    if getattr(donor, name) is not None or getattr(recipient, name) is not None]
        return {
            "assessment": "NOT_CLINICALLY_ASSESSED",
            "systems_with_data": supplied,
            "message": "Extended antigen compatibility requires validated antigen typing and antibody-screen/crossmatch data."
        }

    def is_universal_donor(self, profile: BloodGroupProfile) -> Tuple[bool, str]:
        ok = profile.abo == BloodType.O and profile.rh == RhType.NEGATIVE
        return ok, "O− is the usual universal red-cell donor type (simplified ABO/Rh reference)." if ok else "Not the universal red-cell donor type."

    def is_universal_recipient(self, profile: BloodGroupProfile) -> Tuple[bool, str]:
        ok = profile.abo == BloodType.AB and profile.rh == RhType.POSITIVE
        return ok, "AB+ is the usual universal red-cell recipient type (simplified ABO/Rh reference)." if ok else "Not the universal red-cell recipient type."

    def get_compatibility_matrix(self, donor_profile: BloodGroupProfile) -> Dict[str, List[str]]:
        compatible, incompatible = [], []
        for abo in BloodType:
            for rh in RhType:
                profile = BloodGroupProfile(abo=abo, rh=rh)
                result = self.check_abo_compatibility(donor_profile, profile)
                key = f"{abo.value}{rh.value}"
                (compatible if result.is_compatible else incompatible).append(key)
        return {"compatible": compatible, "incompatible": incompatible}

    def calculate_risk_score(self, donor: BloodGroupProfile, recipient: BloodGroupProfile) -> Dict:
        result = self.check_abo_compatibility(donor, recipient)
        return {
            "risk_score": 0 if result.is_compatible else 100,
            "risk_level": "RULES_COMPATIBLE" if result.is_compatible else "INCOMPATIBLE",
            "factors": [] if result.is_compatible else [result.reason],
            "recommendation": "Educational rule match only; laboratory testing is still required."
        }

    def emergency_compatibility(self, donor_profiles: List[BloodGroupProfile]) -> Dict:
        universal = next((p for p in donor_profiles if self.is_universal_donor(p)[0]), None)
        return {"universal_red_cell_donor": universal, "note": "Not an emergency-release recommendation. Follow local transfusion protocols."}

def _parse_group(abo, rh):
    return BloodGroupProfile(abo=BloodType(str(abo).upper()), rh=RhType(str(rh).strip()))

def check_compatibility(donor_abo: str, donor_rh: str, recipient_abo: str, recipient_rh: str, extended_match: bool = False) -> Dict:
    donor, recipient = _parse_group(donor_abo, donor_rh), _parse_group(recipient_abo, recipient_rh)
    analyzer = BloodGroupAnalyzer()
    result = analyzer.check_abo_compatibility(donor, recipient)
    output = {
        "donor": f"{donor.abo.value}{donor.rh.value}",
        "recipient": f"{recipient.abo.value}{recipient.rh.value}",
        "compatible": result.is_compatible,
        "risk_level": result.risk_level,
        "reason": result.reason,
        "antibodies_detected": result.detected_antibodies,
        "additional_notes": result.additional_notes,
    }
    if extended_match:
        output["extended_check"] = analyzer.check_extended_compatibility(donor, recipient)
    return output

def get_universal_status(abo: BloodType = None, rh: RhType = None, blood_type: str = None, rh_str: str = None) -> Dict:
    if abo is not None and rh is not None:
        profile = BloodGroupProfile(abo=abo, rh=rh)
    elif blood_type is not None and rh_str is not None:
        profile = _parse_group(blood_type, rh_str)
    else:
        raise ValueError("Provide either (abo, rh) or (blood_type, rh_str).")
    analyzer = BloodGroupAnalyzer()
    donor, donor_msg = analyzer.is_universal_donor(profile)
    recipient, recipient_msg = analyzer.is_universal_recipient(profile)
    return {
        "blood_type": f"{profile.abo.value}{profile.rh.value}",
        "universal_red_cell_donor": donor,
        "universal_red_cell_recipient": recipient,
        "universal_plasma_donor": profile.abo == BloodType.AB,
        "messages": {"red_cell_donor": donor_msg, "red_cell_recipient": recipient_msg}
    }
