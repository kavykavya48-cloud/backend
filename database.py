import sqlite3


DATABASE_NAME = "resqnet.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergencies (
            emergency_id TEXT PRIMARY KEY,
            emergency_type TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            status TEXT NOT NULL
        )
    """)

    # Add priority column if it doesn't already exist
    cursor.execute("""
        PRAGMA table_info(emergencies)
    """)

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "priority" not in columns:

        cursor.execute("""
            ALTER TABLE emergencies
            ADD COLUMN priority TEXT NOT NULL DEFAULT 'MEDIUM'
        """)

    connection.commit()
    connection.close()


def save_emergency(
    emergency_id,
    emergency_type,
    description,
    location,
    status,
    priority="HIGH"
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO emergencies (
            emergency_id,
            emergency_type,
            description,
            location,
            status,
            priority
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        emergency_id,
        emergency_type,
        description,
        location,
        status,
        priority
    ))

    connection.commit()
    connection.close()


def get_all_emergencies():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            emergency_id,
            emergency_type,
            description,
            location,
            status,
            priority
        FROM emergencies
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows