import json

DATA_PATH = "data/terminals.json"


def load_data():

    with open(DATA_PATH, "r") as file:
        return json.load(file)


def calculate_terminal_transfer_time(
    origin_gate,
    destination_gate,
    mobility_mode="walking",
    family_travelling=False
):
    data = load_data()

    routes = data["routes"]

    route = None

    for item in routes:
        if (
            item["from"] == origin_gate
            and item["to"] == destination_gate
        ):
            route = item
            break

        if (
            item["to"] == origin_gate
            and item["from"] == destination_gate
        ):
            route = item
            break

    if not route:
        return {
            "error": "No verified route available"
        }

    if (
        mobility_mode == "wheelchair"
        and not route["wheelchair_accessible"]
    ):
        return {
            "error": "Route is not wheelchair accessible"
        }

    distance = route["distance_m"]

    if mobility_mode == "wheelchair":

        speed = data["mobility"][
            "wheelchair_speed_m_per_min"
        ]

        buffer = data["mobility"][
            "wheelchair_safety_buffer_minutes"
        ]

    else:

        speed = data["mobility"][
            "walking_speed_m_per_min"
        ]

        buffer = 0

    if family_travelling:

        buffer += data["mobility"][
            "family_safety_buffer_minutes"
        ]

    travel_minutes = distance / speed

    total_minutes = round(
        travel_minutes + buffer
    )

    return {
        "origin": origin_gate,
        "destination": destination_gate,
        "distance_m": distance,
        "mobility_mode": mobility_mode,
        "travel_minutes": round(travel_minutes, 1),
        "safety_buffer_minutes": buffer,
        "total_estimated_minutes": total_minutes,
        "route_verified": True,
        "data_type": "SIMULATED"
    }

