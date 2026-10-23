from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import get_connection, setup_database

app = FastAPI(title="Bayzo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

setup_database()

CLOSING_HOUR = 20


class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=1)
    customer_email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    service_id: int
    bay_id: int
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


@app.get("/bays")
def list_bays():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM bays").fetchall()
    connection.close()
    return [dict(row) for row in rows]


@app.post("/bookings", status_code=201)
def create_booking(booking: BookingRequest):
    start = booking.start_hour
    end = start + booking.duration_hours
    if end > CLOSING_HOUR:
        raise HTTPException(status_code=400, detail="Bookings must end by 8 PM")

    connection = get_connection()
    try:
        # Lock the database so no one else can write until we finish
        connection.execute("BEGIN IMMEDIATE")

        service = connection.execute(
            "SELECT id FROM services WHERE id = ?", (booking.service_id,)
        ).fetchone()
        if service is None:
            raise HTTPException(status_code=404, detail="Service not found")

        bay = connection.execute(
            "SELECT id FROM bays WHERE id = ?", (booking.bay_id,)
        ).fetchone()
        if bay is None:
            raise HTTPException(status_code=404, detail="Bay not found")

        conflict = connection.execute(
            """
            SELECT id FROM bookings
            WHERE bay_id = ?
              AND booking_date = ?
              AND start_hour < ?
              AND (start_hour + duration_hours) > ?
            """,
            (booking.bay_id, booking.booking_date.isoformat(), end, start),
        ).fetchone()
        if conflict is not None:
            raise HTTPException(
                status_code=409, detail="That bay is already booked at that time"
            )

        cursor = connection.execute(
            """
            INSERT INTO bookings
                (customer_name, customer_email, service_id, bay_id,
                 booking_date, start_hour, duration_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                booking.customer_name,
                booking.customer_email,
                booking.service_id,
                booking.bay_id,
                booking.booking_date.isoformat(),
                start,
                booking.duration_hours,
            ),
        )
        connection.commit()
        row = connection.execute(
            "SELECT * FROM bookings WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)
    except HTTPException:
        connection.rollback()
        raise
    finally:
        connection.close()


@app.get("/bookings")
def list_bookings():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM bookings").fetchall()
    connection.close()
    return [dict(row) for row in rows]