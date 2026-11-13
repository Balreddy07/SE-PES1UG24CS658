
from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee


# Test 1: Fuzz testing parse_booking()
@given(st.one_of(st.text(), st.none()))
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with input {s!r}: {e}"


# Test 2: Fuzz testing stay_average()
@given(st.one_of(st.text(), st.none()))
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:
        assert False, f"stay_average crashed with input {s!r}: {e}"


# Test 3: Fuzz testing payable_fee()
@given(st.one_of(st.text(), st.none()))
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with input {s!r}: {e}"
