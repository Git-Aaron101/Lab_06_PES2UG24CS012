def parse_transit_corridor(corridor_code):
    orig, dest, zones_str = corridor_code.strip().split('-')
    zones = int(zones_str)
    base_fare = 2.50 + (zones * 0.75)
    return f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${base_fare:.2f}"

def lookup_concession_discount(category_name):
    category = category_name.strip().upper()
    discounts = {
        "STANDARD": 1.00,
        "STUDENT": 0.50,
        "SENIOR": 0.35,
        "MILITARY": 0.20,
        "CHILD": 0.00
    }
    return discounts[category]

def compute_passenger_density(occupancy_ratio_str):
    passengers_str, km_str = occupancy_ratio_str.split('/')
    passengers = float(passengers_str)
    km = float(km_str)
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