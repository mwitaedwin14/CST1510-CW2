import pandas as pd
from app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    try:
        conn = connect_database.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cyber_incidents
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, incident_type, severity, status, description, reported_by))
        conn.commit()
        incident_id = cursor.lastrowid
        return incident_id
    except Exception as e:
        print(f"Error inserting incident: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_incidents():
    """Get all incidents as DataFrame."""
    try:
        conn = connect_database.connect()
        df = pd.read_sql_query(
            "SELECT * FROM cyber_incidents ORDER BY id DESC",
            conn
        )
        return df
    except Exception as e:
        print(f"Error fetching incidents: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if conn:
            conn.close()