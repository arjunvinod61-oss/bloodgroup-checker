import pytest
from bloodgroup_checker import check_compatibility, get_universal_status, BloodType, RhType
from bloodgroup_checker.database import get_blood_group_database

@pytest.mark.parametrize("donor,recipient,expected", [
    ("O-","O-",True),("O-","AB+",True),("A-","A+",True),
    ("B+","AB+",True),("AB-","AB+",True),("A+","B+",False),
    ("O+","O-",False),("AB+","O+",False),("B-","A-",False),
    ("AB+","AB-",False),("O+","A-",False),
])
def test_red_cell_compatibility(donor,recipient,expected):
    got=check_compatibility(donor[:-1],donor[-1],recipient[:-1],recipient[-1])
    assert got["compatible"] is expected

def test_rhd_rule_applies_to_ab_recipient_too():
    assert not check_compatibility("AB","+","AB","-")["compatible"]

def test_rh_negative_does_not_mean_natural_anti_d():
    assert check_compatibility("O","-","A","+")["compatible"]

def test_universal_status_names():
    o=get_universal_status(blood_type="O",rh_str="-")
    ab=get_universal_status(blood_type="AB",rh_str="+")
    assert o["universal_red_cell_donor"] is True
    assert ab["universal_red_cell_recipient"] is True
    assert ab["universal_plasma_donor"] is True

def test_population_frequency_case():
    db=get_blood_group_database()
    assert db.get_population_frequency("O-","North_European")["frequency"] > 0
    assert db.get_population_frequency("A+","East_Asian")["frequency"] > 0

def test_invalid_group_rejected():
    with pytest.raises(ValueError):
        check_compatibility("X","+","A","+")


def test_antibody_explanation_for_o_recipient_is_specific():
    a_to_o = check_compatibility("A", "+", "O", "+")
    assert a_to_o["antibodies_detected"] == ["anti-A"]
    ab_to_o = check_compatibility("AB", "+", "O", "+")
    assert set(ab_to_o["antibodies_detected"]) == {"anti-A", "anti-B"}
