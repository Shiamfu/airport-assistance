from database.db import create_medical_request, URGENCY_LEVELS

EMERGENCY_NOTICE = (
    "If this is life-threatening, call the local emergency "
    "number or alert the nearest airport staff immediately. "
    "Do not wait for this request to be approved."
)


def request_medical_assistance(
    patient,
    location,
    condition,
    urgency,
    assistance_type="first_responder"
):

    urgency = str(urgency).upper()

    if urgency not in URGENCY_LEVELS:
        return {
            "error": (
                "urgency must be one of: "
                + ", ".join(URGENCY_LEVELS)
            )
        }

    request_id = create_medical_request(
        patient,
        location,
        condition,
        urgency,
        assistance_type
    )

    return {
        "request_id": request_id,
        "request_type": "medical",
        "urgency": urgency,
        "status": "PENDING_HUMAN_APPROVAL",
        "message": (
            "Medical request filed. Waiting for "
            "coordinator confirmation."
        ),
        "emergency_notice": EMERGENCY_NOTICE
    }

