import unittest

from tools.flight import get_flight_and_gate_status
from tools.routing import calculate_terminal_transfer_time

from safety.check import check_connection_feasibility


class SwagonTests(unittest.TestCase):

    # 1. Valid flight
    def test_valid_flight(self):
        result = get_flight_and_gate_status("DXB402")

        self.assertIn("flight_information", result)

    # 2. Invalid flight
    def test_invalid_flight(self):
        result = get_flight_and_gate_status("UNKNOWN")

        self.assertIn("error", result)

    # 3. Wheelchair transfer
    def test_wheelchair_route(self):
        result = calculate_terminal_transfer_time(
            "C12",
            "B14",
            "wheelchair",
            True
        )

        self.assertIn("total_estimated_minutes", result)

    # 4. Normal walking
    def test_walking_route(self):
        result = calculate_terminal_transfer_time(
            "C12",
            "B14",
            "walking"
        )

        self.assertIn("distance_m", result)

    # 5. Unknown route
    def test_unknown_route(self):
        result = calculate_terminal_transfer_time(
            "C12",
            "Z99",
            "walking"
        )

        self.assertIn("error", result)

    # 6. Wheelchair inaccessible route
    def test_inaccessible_route(self):
        result = calculate_terminal_transfer_time(
            "C15",
            "A08",
            "wheelchair"
        )

        self.assertIn("error", result)

    # 7. Connection too short
    def test_not_feasible(self):
        result = check_connection_feasibility(
            20,
            30
        )

        self.assertEqual(
            result["status"],
            "NOT_FEASIBLE"
        )

    # 8. Tight connection
    def test_tight_connection(self):
        result = check_connection_feasibility(
            35,
            30
        )

        self.assertEqual(
            result["status"],
            "TIGHT_CONNECTION"
        )

    # 9. Potentially feasible connection
    def test_potentially_feasible(self):
        result = check_connection_feasibility(
            60,
            30
        )

        self.assertEqual(
            result["status"],
            "POTENTIALLY_FEASIBLE"
        )

    # 10. Invalid timing
    def test_invalid_timing(self):
        result = check_connection_feasibility(
            -10,
            30
        )

        self.assertEqual(
            result["status"],
            "INVALID"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

