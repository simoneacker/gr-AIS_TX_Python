import random

# Function to generate a random 168-bit AIS Type 1 Message (Position Report)
def generate_ais_type_1(mmsi, latitude, longitude):
    ais_type = "000001"  # Message Type 1 (6 bits)
    repeat_indicator = "00"  # No repeat (2 bits)
    mmsi_bin = format(mmsi, '030b')  # MMSI (30 bits)
    status = "0000"  # Under way using engine (4 bits)
    rot = "00000000"  # Rate of Turn (8 bits)
    sog = "0000000000"  # Speed Over Ground (10 bits)
    position_accuracy = "0"  # Normal accuracy (1 bit)
    longitude_bin = format(int(longitude * 600000) & (2**28-1), '028b')  # Longitude (28 bits)
    latitude_bin = format(int(latitude * 600000) & (2**27-1), '027b')  # Latitude (27 bits)
    cog = "000000000000"  # Course Over Ground (12 bits)
    true_heading = "000000000"  # True Heading (9 bits)
    timestamp = "000000"  # Time stamp (6 bits)
    special_maneuver = "00"  # No special maneuver (2 bits)
    spare = "000"  # Spare bits (3 bits)
    raim_flag = "0"  # No RAIM (1 bit)
    radio_status = "0000000000000000000"  # Radio status (19 bits)

    # Combine into a full 168-bit AIS payload
    full_ais_payload = (
        ais_type + repeat_indicator + mmsi_bin + status + rot + sog + position_accuracy +
        longitude_bin + latitude_bin + cog + true_heading + timestamp + special_maneuver + 
        spare + raim_flag + radio_status
    )

    # Ensure the final payload is exactly 168 bits
    if len(full_ais_payload) != 168:
        raise ValueError(f"Payload length is not 168 bits: {len(full_ais_payload)}")

    return full_ais_payload

# Coordinates for specified locations
locations = {
    "Seattle": (47.6062, -122.3321),
    "LA": (34.0522, -118.2437),
    "San Diego": (32.7157, -117.1654),
    "Frisco TX": (33.1507, -96.8236),
    "WA DC": (38.9072, -77.0369),
    "Miami": (25.7617, -80.1918),
    "Cabo San Lucas": (22.8800, -109.9167),
    "Portland": (45.5152, -122.6784),
    "Vancouver": (49.2827, -123.1207),
    "Kona HI": (19.6480, -155.9980)
}


# Generate 10 AIS Type 1 payloads for the specified locations
ais_payloads = []
for location, coords in locations.items():
    ais_payloads.append(generate_ais_type_1(random.randint(100000000, 999999999), *coords))

# Output the generated AIS payloads as a long comma-delimited string
comma_separated_payloads = ",".join(ais_payloads)

# Display the final result
print(comma_separated_payloads)
