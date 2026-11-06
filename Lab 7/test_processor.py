from hypothesis import given, strategies as st
from processor import parse_transit_corridor, lookup_concession_discount, compute_passenger_density

@given(st.text() | st.none())
def test_parse_transit_corridor_no_crash(s):
    #To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_lookup_concession_discount_safe(s):
    #To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_compute_passenger_density_safe(s):
    #To-Do:Using try and except complete this function.
    pass