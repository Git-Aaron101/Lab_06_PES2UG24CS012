import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles


def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_commute_manifest("not-a-list", 2.0)
    with pytest.raises(ValueError):
        process_commute_manifest([], -1.0)


def test_inactive_and_unknown_routes_are_skipped_or_rejected():
    result = process_commute_manifest([
        {"route_active": False, "route_type": "local", "commuters": [{"zones": 2}]},
        {"route_active": True, "route_type": "unknown", "commuters": []},
    ], 2.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


@pytest.mark.parametrize("route_type,expected", [("local", 4.5), ("express", 8.0), ("shuttle", 6.0)])
def test_route_types_and_regular_fare(route_type, expected):
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": route_type,
        "commuters": [{"zones": 2, "type": "regular"}],
    }], 2.0)
    assert result["total_fare"] == expected
    assert result["status"] == "COMPLETED"


def test_student_senior_and_default_commuter_fields():
    result = process_commute_manifest([{
        "route_active": True,
        "commuters": [
            {"zones": 2, "type": "student"},
            {"zones": 2, "type": "senior"},
            {},
        ],
    }], 2.0)
    assert result["total_fare"] == 7.7


def test_invalid_zones_blacklisted_and_priority_fee():
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "local",
        "priority_boarding": True,
        "commuters": [
            {"zones": 0},
            {"zones": 1, "blacklisted": True},
            {"zones": 1},
        ],
    }], 3.0)
    assert result == {"total_fare": 6.5, "status": "COMPLETED"}


def test_blacklisted_express_cancels_manifest_fare():
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "express",
        "priority_boarding": False,
        "commuters": [{"zones": 2}, {"zones": 1, "blacklisted": True}, {"zones": 2}],
    }], 2.0)
    assert result["total_fare"] == 0.0
    assert result["status"] == "ZERO_RIDERSHIP"


def test_audit_rejection_after_more_than_four_rejected_rides():
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 0} for _ in range(5)],
    }], 2.0)
    assert result == {"total_fare": 0.0, "status": "AUDIT_REJECTED"}


def test_zero_riders_and_priority_fee_can_produce_completed_fare():
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "local",
        "priority_boarding": True,
        "commuters": [],
    }], 2.0)
    assert result == {"total_fare": 2.0, "status": "COMPLETED"}


def test_turnstile_no_data_and_operational():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"
    assert inspect_smartcard_turnstiles([[0, 1, 3], [4, 2, 1]]) == "OPERATIONAL"


def test_turnstile_failure_streak_jams():
    assert inspect_smartcard_turnstiles([[4, 5]]) == "TURNSTILE_JAM"


def test_turnstile_failure_streak_resets_and_devices_are_checked_separately():
    assert inspect_smartcard_turnstiles([[4, 3, 5], [4], [5]]) == "OPERATIONAL"
