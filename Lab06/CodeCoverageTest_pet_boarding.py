
import pytest

from pet_boarding import boarding_fee, admission_ok, checkout_status


# ==========================================
# BOARDING FEE TEST CASES
# ==========================================

def test_unknown_pet_type():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("parrot", 5, False)


def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("dog", -1, False)


def test_within_included_days():
    assert boarding_fee("dog", 1, False) == 0



def test_premium_dog():
    assert boarding_fee("dog", 5, True) == 60


def test_cat_more_than_ten_extra_days():
    assert boarding_fee("cat", 14, False) == 330


def test_premium_rabbit():
    assert boarding_fee("rabbit", 5, True) == 20


def test_cat_extra_days():
    assert boarding_fee("cat", 5, False) == 40


def test_cat_more_than_ten_extra_days():
    assert boarding_fee("cat", 14, False) == 330


def test_dog_more_than_ten_extra_days():
    assert boarding_fee("dog", 14, False) == 540


# ==========================================
# ADMISSION TEST CASES
# ==========================================

def test_senior_pet_admission():
    assert admission_ok(10, 3, True) is True


def test_senior_pet_insufficient_vaccinations():
    assert admission_ok(10, 2, True) is False


def test_young_pet_rejected():
    assert admission_ok(0.5, 3, False) is False


def test_adult_pet_admission():
    assert admission_ok(4, 2, False) is True


def test_adult_pet_insufficient_vaccinations():
    assert admission_ok(4, 1, False) is False


# ==========================================
# CHECKOUT STATUS TEST CASES
# ==========================================

def test_checkout_open():
    assert checkout_status(30, True, False) == "open"


def test_checkout_late():
    assert checkout_status(5, False, False) == "late"


def test_checkout_closed():
    assert checkout_status(-1, False, False) == "closed"


def test_weekend_checkout():
    assert checkout_status(35, False, True) == "open"
