from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import get_connection, setup_database

app = FastAPI(title="Bayzo API")

setup_database()


class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=1)
    customer_email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    service_id: int
    booking_date: date
    start_hour: int = Field(ge=8, le=19)
    duration_hours: int = Field(ge=1, le=8)


@app.get("/services")
def list_services():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM services").fetchall()
    connection.close()
    return [dict(row) for row in rows]


@app.get("/services/{service_id}")
def get_service(service_id: int):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM services WHERE id = ?", (service_id,)
    ).fetchone()
    connection.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return dict(row)


@app.post("/bookings", status_code=201)
def create_booking(booking: BookingRequest):
    connection = get_connection()
    service = connection.execute(
        "SELECT id FROM services WHERE id = ?", (booking.service_id,)
    ).fetchone()
    if service is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Service not found")

    cursor = connection.execute(
        """
        INSERT INTO bookings
            (customer_name, customer_email, service_id,
             booking_date, start_hour, duration_hours)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            booking.customer_name,
            booking.customer_email,
            booking.service_id,
            booking.booking_date.isoformat(),
            booking.start_hour,
            booking.duration_hours,
        ),
    )
    connection.commit()
    new_id = cursor.lastrowid
    row = connection.execute(
        "SELECT * FROM bookings WHERE id = ?", (new_id,)
    ).fetchone()
    connection.close()
    return dict(row)


@app.get("/bookings")
def list_bookings():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM bookings").fetchall()
    connection.close()
    return [dict(row) for row in rows]