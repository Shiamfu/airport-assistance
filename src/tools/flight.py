import json
from config import DATA_PATH


def load_data():
    with open(DATA_PATH, "r") as file:
        return json.load(file)


def get_flight_and_gate_status(flight_number):
    data = load_data()

    flight = data["flights"].get(flight_number)

    if not flight:
        return {
            "error": "Flight not found"
        }

    return {
        "flight_number": flight_number,
        "flight_information": flight,
        "airport": data["airport"],
        "data_type": "SIMULATED"
    }

