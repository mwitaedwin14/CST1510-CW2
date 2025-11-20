import pandas as pd
from app.data.db
import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new accident."""
    conn = connect_database.connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by)
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id