from fastapi import FastAPI, HTTPException

from database import get_connection, setup_database

app = FastAPI(title="Bayzo API")

setup_database()


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