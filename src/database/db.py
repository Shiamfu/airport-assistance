import sqlite3

DB_NAME = ("swagon.sqlite")


def connect():
    return sqlite3.connect(
        DB_NAME,
        timeout=10
    )


def initialise_database():

    con = connect()

    con.execute("""
        CREATE TABLE IF NOT EXISTS mobility_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger TEXT,
            flight TEXT,
            origin_gate TEXT,
            destination_gate TEXT,
            assistance_type TEXT,
            reason TEXT,
            status TEXT DEFAULT 'PENDING',
            coordinator TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            details TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    con.close()

    initialise_incident_tables()


def create_mobility_request(
    passenger,
    flight,
    origin,
    destination,
    assistance,
    reason
):

    con = connect()

    cursor = con.execute("""
        INSERT INTO mobility_requests
        (passenger, flight, origin_gate,
         destination_gate, assistance_type, reason)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        passenger,
        flight,
        origin,
        destination,
        assistance,
        reason
    ))

    request_id = cursor.lastrowid

    con.commit()
    con.close()

    return request_id


def get_requests():

    con = connect()

    rows = con.execute("""
        SELECT * FROM mobility_requests
        ORDER BY created_at DESC
    """).fetchall()

    con.close()

    return rows


def get_request(request_id):

    con = connect()

    row = con.execute("""
        SELECT * FROM mobility_requests
        WHERE id = ?
    """, (request_id,)).fetchone()

    con.close()

    return row


def update_request(request_id, decision, coordinator):

    if decision not in ["APPROVED", "REJECTED"]:
        raise ValueError("Invalid decision")

    con = connect()

    con.execute("""
        UPDATE mobility_requests
        SET status = ?,
            coordinator = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND status = 'PENDING'
    """, (decision, coordinator, request_id))

    con.commit()
    con.close()


def log_event(event, details):

    con = connect()

    con.execute("""
        INSERT INTO agent_logs (event, details)
        VALUES (?, ?)
    """, (event, str(details)))

    con.commit()
    con.close()


def get_logs():

    con = connect()

    rows = con.execute("""
        SELECT * FROM agent_logs
        ORDER BY created_at DESC
    """).fetchall()

    con.close()

    return rows



# ---------------------------------------------------------------
# Crime reports and medical assistance
# ---------------------------------------------------------------

CRIME_COLUMNS = [
    "ID", "Reporter", "Category", "Location", "Description",
    "In progress", "Status", "Coordinator", "Created", "Updated"
]

MEDICAL_COLUMNS = [
    "ID", "Patient", "Location", "Condition", "Urgency",
    "Assistance", "Status", "Coordinator", "Created", "Updated"
]

URGENCY_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

# status -> statuses a coordinator may move it to
CRIME_TRANSITIONS = {
    "PENDING": {"ACKNOWLEDGED", "ESCALATED"},
    "ACKNOWLEDGED": {"ESCALATED", "CLOSED"},
    "ESCALATED": {"CLOSED"},
}

MEDICAL_TRANSITIONS = {
    "PENDING": {"DISPATCHED", "UNABLE_TO_DISPATCH"},
    "DISPATCHED": {"RESOLVED"},
}


def initialise_incident_tables():

    con = connect()

    con.execute("""
        CREATE TABLE IF NOT EXISTS crime_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporter TEXT,
            category TEXT,
            location TEXT,
            description TEXT,
            in_progress INTEGER DEFAULT 0,
            status TEXT DEFAULT 'PENDING',
            coordinator TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS medical_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT,
            location TEXT,
            condition TEXT,
            urgency TEXT,
            assistance_type TEXT,
            status TEXT DEFAULT 'PENDING',
            coordinator TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    con.close()


def create_crime_report(
    reporter,
    category,
    location,
    description,
    in_progress=False
):

    con = connect()

    cursor = con.execute("""
        INSERT INTO crime_reports
        (reporter, category, location, description, in_progress)
        VALUES (?, ?, ?, ?, ?)
    """, (
        reporter,
        category,
        location,
        description,
        1 if in_progress else 0
    ))

    report_id = cursor.lastrowid

    con.commit()
    con.close()

    return report_id


def get_crime_reports():

    con = connect()

    rows = con.execute("""
        SELECT * FROM crime_reports
        ORDER BY created_at DESC, id DESC
    """).fetchall()

    con.close()

    return rows


def get_crime_report(report_id):

    con = connect()

    row = con.execute("""
        SELECT * FROM crime_reports WHERE id = ?
    """, (report_id,)).fetchone()

    con.close()

    return row


def update_crime_report(report_id, new_status, coordinator):

    row = get_crime_report(report_id)

    if row is None:
        raise ValueError("Report not found")

    if new_status not in CRIME_TRANSITIONS.get(row[6], set()):
        raise ValueError(
            f"Cannot move from {row[6]} to {new_status}"
        )

    con = connect()

    con.execute("""
        UPDATE crime_reports
        SET status = ?, coordinator = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND status = ?
    """, (new_status, coordinator, report_id, row[6]))

    con.commit()
    con.close()


def create_medical_request(
    patient,
    location,
    condition,
    urgency,
    assistance_type
):

    if urgency not in URGENCY_LEVELS:
        raise ValueError("Invalid urgency")

    con = connect()

    cursor = con.execute("""
        INSERT INTO medical_requests
        (patient, location, condition, urgency, assistance_type)
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient,
        location,
        condition,
        urgency,
        assistance_type
    ))

    request_id = cursor.lastrowid

    con.commit()
    con.close()

    return request_id


def get_medical_requests():

    con = connect()

    rows = con.execute("""
        SELECT * FROM medical_requests
        ORDER BY created_at DESC, id DESC
    """).fetchall()

    con.close()

    return rows


def get_medical_request(request_id):

    con = connect()

    row = con.execute("""
        SELECT * FROM medical_requests WHERE id = ?
    """, (request_id,)).fetchone()

    con.close()

    return row


def update_medical_request(request_id, new_status, coordinator):

    row = get_medical_request(request_id)

    if row is None:
        raise ValueError("Request not found")

    if new_status not in MEDICAL_TRANSITIONS.get(row[6], set()):
        raise ValueError(
            f"Cannot move from {row[6]} to {new_status}"
        )

    con = connect()

    con.execute("""
        UPDATE medical_requests
        SET status = ?, coordinator = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND status = ?
    """, (new_status, coordinator, request_id, row[6]))

    con.commit()
    con.close()
