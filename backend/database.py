import sqlite3

DB_FILE = "bayzo.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            unit TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            service_id INTEGER NOT NULL,
            bay_id INTEGER NOT NULL,
            booking_date TEXT NOT NULL,
            start_hour INTEGER NOT NULL,
            duration_hours INTEGER NOT NULL,
            FOREIGN KEY (service_id) REFERENCES services (id),
            FOREIGN KEY (bay_id) REFERENCES bays (id)
        )
        """
    )
    if connection.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
        connection.executemany(
            "INSERT INTO services (name, price, unit) VALUES (?, ?, ?)",
            [
                ("Basic Bay", 25, "hour"),
                ("Guided Bay", 45, "hour"),
                ("Specialty Tools", 10, "day"),
            ],
        )
    if connection.execute("SELECT COUNT(*) FROM bays").fetchone()[0] == 0:
        connection.executemany(
            "INSERT INTO bays (name) VALUES (?)",
            [("Bay 1",), ("Bay 2",), ("Bay 3",)],
        )
    connection.commit()
    connection.close()