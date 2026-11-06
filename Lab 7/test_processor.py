
from hypothesis import given, strategies as st
from processor import (
    parse_transit_corridor,
    lookup_concession_discount,
    compute_passenger_density
)


@given(st.text() | st.none())
def test_parse_transit_corridor_no_unexpected_crash(s):
    try:
        result = parse_transit_corridor(s)
        assert isinstance(result, str)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_lookup_concession_discount_safe(s):
    try:
        result = lookup_concession_discount(s)
        assert isinstance(result, float)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_compute_passenger_density_safe(s):
    try:
        result = compute_passenger_density(s)
        assert isinstance(result, float)
    except ValueError:
        pass
