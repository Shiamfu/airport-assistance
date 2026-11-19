def check_connection_feasibility(
    boarding_minutes,
    transfer_minutes,
    extra_requirements=False
):
    if boarding_minutes < 0 or transfer_minutes < 0:
        return {
            "status": "INVALID",
            "message": "Invalid timing information"
        }

    remaining = boarding_minutes - transfer_minutes

    if remaining < 0:

        return {
            "status": "NOT_FEASIBLE",
            "remaining_minutes": remaining,
            "message": "Estimated transfer exceeds available time"
        }

    if extra_requirements:

        return {
            "status": "URGENT_REVIEW",
            "remaining_minutes": remaining,
            "message": "Additional staff review required"
        }

    if remaining < 10:

        return {
            "status": "TIGHT_CONNECTION",
            "remaining_minutes": remaining,
            "message": "Connection requires urgent review"
        }

    return {
        "status": "POTENTIALLY_FEASIBLE",
        "remaining_minutes": remaining,
        "message": "Estimated transfer fits available time"
    }

