import sqlite3

DB_NAME = "skylink.sqlite"


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

