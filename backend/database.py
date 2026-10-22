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
    count = connection.execute("SELECT COUNT(*) FROM services").fetchone()[0]
    if count == 0:
        connection.executemany(
            "INSERT INTO services (name, price, unit) VALUES (?, ?, ?)",
            [
                ("Basic Bay", 25, "hour"),
                ("Guided Bay", 45, "hour"),
                ("Specialty Tools", 10, "day"),
            ],
        )
    connection.commit()
    connection.close()