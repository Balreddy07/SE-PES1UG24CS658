
import pytest

from pet_boarding import boarding_fee, admission_ok, checkout_status


# ==================================================
# 1. BOARDING FEE - BRANCH COVERAGE
# ==================================================

def test_unknown_pet_branch():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("parrot", 5, False)


def test_valid_pet_branch():
    assert boarding_fee("cat", 3, False) == 0


def test_negative_days_branch():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("dog", -2, False)


def test_valid_days_branch():
    assert boarding_fee("dog", 1, False) == 0


def test_premium_dog_branch():
    assert boarding_fee("dog", 5, True) == 60


def test_non_premium_dog_branch():
    assert boarding_fee("dog", 4, False) == 60


def test_premium_rabbit_branch():
    assert boarding_fee("rabbit", 5, True) == 20


def test_no_extra_days_branch():
    assert boarding_fee("cat", 3, False) == 0


def test_extra_days_branch():
    assert boarding_fee("cat", 5, False) == 40


def test_dog_rate_branch():
    assert boarding_fee("dog", 4, False) == 60


def test_non_dog_rate_branch():
    assert boarding_fee("cat", 5, False) == 40


def test_more_than_ten_extra_days_cat():
    assert boarding_fee("cat", 14, False) == 330


def test_more_than_ten_extra_days_dog():
    assert boarding_fee("dog", 14, False) == 540


def test_ten_or_less_extra_days():
    assert boarding_fee("dog", 12, False) == 300


# ==================================================
# 2. ADMISSION OK - BRANCH COVERAGE
# ==================================================

def test_senior_pet_accepted():
    assert admission_ok(10, 3, True) is True


def test_senior_pet_rejected():
    assert admission_ok(10, 2, True) is False


def test_non_senior_pet_branch():
    assert admission_ok(4, 2, False) is True


def test_young_pet_rejected():
    assert admission_ok(0.5, 3, False) is False


def test_adult_pet_insufficient_vaccinations():
    assert admission_ok(4, 1, False) is False


def test_adult_pet_sufficient_vaccinations():
    assert admission_ok(4, 2, False) is True


# ==================================================
# 3. CHECKOUT STATUS - BRANCH COVERAGE
# ==================================================

def test_long_stay_weekday_open():
    assert checkout_status(30, True, False) == "open"


def test_normal_stay_weekday_open():
    assert checkout_status(15, False, False) == "open"


def test_weekend_cutoff_open():
    assert checkout_status(35, False, True) == "open"

def test_long_stay_weekend_late():
    assert checkout_status(40, True, True) == "late"


def test_normal_stay_late():
    assert checkout_status(5, False, False) == "late"


def test_checkout_closed():
    assert checkout_status(-1, False, False) == "closed"
