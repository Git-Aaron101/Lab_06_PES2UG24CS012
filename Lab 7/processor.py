
def parse_transit_corridor(corridor_code):
    if not isinstance(corridor_code, str):
        raise ValueError("Corridor code must be a string")

    parts = corridor_code.strip().split('-')

    if len(parts) != 3:
        raise ValueError("Corridor must contain origin, destination and zones")

    orig, dest, zones_str = parts

    if not orig.strip() or not dest.strip():
        raise ValueError("Origin and destination cannot be empty")

    try:
        zones = int(zones_str)
    except ValueError:
        raise ValueError("Zones must be a valid integer")

    if zones <= 0:
        raise ValueError("Zones must be positive")

    base_fare = 2.50 + (zones * 0.75)
    return f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${base_fare:.2f}"


def lookup_concession_discount(category_name):
    if not isinstance(category_name, str):
        raise ValueError("Category must be a string")

    category = category_name.strip().upper()

    discounts = {
        "STANDARD": 1.00,
        "STUDENT": 0.50,
        "SENIOR": 0.35,
        "MILITARY": 0.20,
        "CHILD": 0.00
    }

    if category not in discounts:
        raise ValueError("Unknown concession category")

    return discounts[category]


def compute_passenger_density(occupancy_ratio_str):
    if not isinstance(occupancy_ratio_str, str):
        raise ValueError("Occupancy ratio must be a string")

    parts = occupancy_ratio_str.split('/')

    if len(parts) != 2:
        raise ValueError("Input must be in passengers/km format")

    try:
        passengers = float(parts[0])
        km = float(parts[1])
    except ValueError:
        raise ValueError("Passengers and kilometres must be numeric")

    if not (float('-inf') < passengers < float('inf')):
        raise ValueError("Passengers must be finite")

    if not (float('-inf') < km < float('inf')):
        raise ValueError("Kilometres must be finite")

    if passengers < 0:
        raise ValueError("Passengers cannot be negative")

    if km <= 0:
        raise ValueError("Kilometres must be positive")

    density = passengers / km
    return round(density, 2)


def main():
    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    print(parse_transit_corridor(c_input))

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    print("Multiplier:", lookup_concession_discount(cat_input))

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    print("Density:", compute_passenger_density(d_input))


if __name__ == "__main__":
    main()
