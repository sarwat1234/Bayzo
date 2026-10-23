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
            unit TEXT NOT NULL,
            description TEXT NOT NULL
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
            status TEXT NOT NULL DEFAULT 'booked',
            FOREIGN KEY (service_id) REFERENCES services (id),
            FOREIGN KEY (bay_id) REFERENCES bays (id)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL UNIQUE,
            description TEXT NOT NULL,
            subtotal_cents INTEGER NOT NULL,
            tax_cents INTEGER NOT NULL,
            total_cents INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'unpaid',
            created_at TEXT NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES bookings (id)
        )
        """
    )
    if connection.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
        connection.executemany(
            "INSERT INTO services (name, price, unit, description) VALUES (?, ?, ?, ?)",
            [
                ("Basic Bay", 25, "hour", "A bay with a lift and a standard tool set."),
                ("Guided Bay", 45, "hour", "Everything in Basic, plus a mechanic helping you through the job."),
                ("Specialty Tools", 10, "day", "Borrow tools like torque wrenches and diagnostic scanners."),
            ],
        )
    if connection.execute("SELECT COUNT(*) FROM bays").fetchone()[0] == 0:
        connection.executemany(
            "INSERT INTO bays (name) VALUES (?)",
            [("Bay 1",), ("Bay 2",), ("Bay 3",)],
        )
    connection.commit()
    connection.close()