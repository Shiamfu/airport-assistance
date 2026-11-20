from database.db import create_crime_report

CATEGORIES = [
    "theft",
    "assault",
    "harassment",
    "suspicious_person_or_item",
    "lost_or_stolen_documents",
    "other"
]

EMERGENCY_NOTICE = (
    "If anyone is in immediate danger, alert the nearest "
    "uniformed airport staff or call the local emergency "
    "number now. Do not wait for this report to be reviewed."
)


def submit_crime_report(
    category,
    location,
    description,
    reporter="Anonymous",
    in_progress=False
):

    if category not in CATEGORIES:
        category = "other"

    report_id = create_crime_report(
        reporter or "Anonymous",
        category,
        location,
        description,
        in_progress
    )

    return {
        "request_id": report_id,
        "request_type": "crime",
        "status": "PENDING_HUMAN_APPROVAL",
        "message": (
            "Report filed. Waiting for security "
            "coordinator review."
        ),
        "emergency_notice": EMERGENCY_NOTICE
    }

