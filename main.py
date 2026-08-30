from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from emergency import EmergencyReport, EmergencyResponse
from datetime import datetime
from database import create_table, save_emergency, get_all_emergencies
import sqlite3


app = FastAPI(
    title="ResQNet API",
    description="Smart emergency response coordination backend",
    version="1.0.0"
)

create_table()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "project": "ResQNet",
        "message": "ResQNet backend is running!",
        "status": "online"
    }


@app.post("/emergencies", response_model=EmergencyResponse)
def create_emergency(report: EmergencyReport):

    emergency_id = "RQ-" + datetime.now().strftime("%Y%m%d%H%M%S")

    # Automatically assign priority
    emergency_type = report.emergency_type.strip().lower()
    if emergency_type in ["medical", "fire", "accident"]:
        priority = "HIGH"

    elif report.emergency_type == "public safety":
        priority = "MEDIUM"

    else:
        priority = "LOW"

    save_emergency(
        emergency_id=emergency_id,
        emergency_type=report.emergency_type,
        description=report.description,
        location=report.location,
        status="REPORTED",
        priority=priority
    )

    return EmergencyResponse(
        emergency_id=emergency_id,
        emergency_type=report.emergency_type,
        description=report.description,
        location=report.location,
        status="REPORTED"
    )


@app.get("/emergencies")
def get_emergencies():

    rows = get_all_emergencies()

    emergencies = []

    for row in rows:

        emergencies.append({
            "emergency_id": row[0],
            "emergency_type": row[1],
            "description": row[2],
            "location": row[3],
            "status": row[4],
            "priority": row[5]
        })

    return emergencies


@app.put("/emergencies/{emergency_id}/status")
def update_emergency_status(
    emergency_id: str,
    status: str
):

    connection = sqlite3.connect("resqnet.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE emergencies
        SET status = ?
        WHERE emergency_id = ?
        """,
        (status, emergency_id)
    )

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        return {
            "message": "Emergency not found"
        }

    connection.close()

    return {
        "emergency_id": emergency_id,
        "status": status,
        "message": "Emergency status updated successfully"
    }