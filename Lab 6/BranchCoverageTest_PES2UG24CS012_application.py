import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles


def test_input_validation_true_and_false_paths():
    with pytest.raises(ValueError):
        process_commute_manifest(None, 1.0)
    with pytest.raises(ValueError):
        process_commute_manifest([], -0.01)
    assert process_commute_manifest([], 0.0)["status"] == "ZERO_RIDERSHIP"


def test_route_active_and_route_type_branches():
    result = process_commute_manifest([
        {"route_active": False},
        {"route_active": True, "route_type": "express", "commuters": [{"zones": 1}]},
        {"route_active": True, "route_type": "shuttle", "commuters": [{"zones": 1}]},
        {"route_active": True, "route_type": "local", "commuters": [{"zones": 1}]},
        {"route_active": True, "route_type": "unknown", "commuters": []},
    ], 0.0)
    assert result["total_fare"] == 15.5
    assert result["status"] == "COMPLETED"


def test_commuter_zone_and_blacklist_branches():
    # Invalid zones; non-express blacklisted card; valid regular passenger.
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "local",
        "commuters": [
            {"zones": 0},
            {"zones": 1, "blacklisted": True},
            {"zones": 1, "blacklisted": False, "type": "regular"},
        ],
    }], 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_blacklisted_express_breaks_out_of_commuter_loop():
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "express",
        "commuters": [{"zones": 1}, {"zones": 1, "blacklisted": True}, {"zones": 1}],
    }], 0.0)
    assert result["total_fare"] == 0.0


@pytest.mark.parametrize("passenger_type,expected", [("student", 1.5), ("senior", 2.1), ("regular", 3.5), ("other", 3.5)])
def test_passenger_type_decision_branches(passenger_type, expected):
    result = process_commute_manifest([{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 1, "type": passenger_type}],
    }], 0.0)
    assert result["total_fare"] == expected


def test_priority_boarding_true_and_false():
    manifests = [
        {"route_active": True, "route_type": "local", "priority_boarding": True, "commuters": []},
        {"route_active": True, "route_type": "local", "priority_boarding": False, "commuters": [{"zones": 1}]},
    ]
    assert process_commute_manifest(manifests, 2.0)["total_fare"] == 5.5


def test_rejected_rides_threshold_both_sides():
    exactly_four = [{"route_active": True, "route_type": "unknown"} for _ in range(4)]
    more_than_four = [{"route_active": True, "route_type": "unknown"} for _ in range(5)]
    assert process_commute_manifest(exactly_four, 0.0)["status"] == "ZERO_RIDERSHIP"
    assert process_commute_manifest(more_than_four, 0.0)["status"] == "AUDIT_REJECTED"


def test_zero_fare_and_nonzero_fare_status_branches():
    assert process_commute_manifest([], 0.0)["status"] == "ZERO_RIDERSHIP"
    assert process_commute_manifest([{
        "route_active": True, "route_type": "local", "commuters": [{"zones": 1}]
    }], 0.0)["status"] == "COMPLETED"


def test_turnstile_empty_and_nonempty_branches():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"
    assert inspect_smartcard_turnstiles([[1, 2, 3]]) == "OPERATIONAL"


def test_turnstile_failure_threshold_and_streak_reset():
    # 3 is not a failure; 4 is. A reading <= 3 resets a streak.
    assert inspect_smartcard_turnstiles([[4, 3, 5]]) == "OPERATIONAL"
    assert inspect_smartcard_turnstiles([[4, 4]]) == "TURNSTILE_JAM"


def test_turnstile_streak_is_per_device():
    # One failure at the end of device 1 must not combine with device 2.
    assert inspect_smartcard_turnstiles([[4], [5]]) == "OPERATIONAL"
