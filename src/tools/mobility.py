from database.db import create_mobility_request


def request_mobility_dispatch_async(
    passenger,
    flight,
    origin_gate,
    destination_gate,
    assistance_type,
    reason
):

    request_id = create_mobility_request(
        passenger,
        flight,
        origin_gate,
        destination_gate,
        assistance_type,
        reason
    )

    return {
        "request_id": request_id,
        "status": "PENDING_HUMAN_APPROVAL",
        "message": (
            "Assistance requested. "
            "Waiting for coordinator confirmation."
        )
    }

