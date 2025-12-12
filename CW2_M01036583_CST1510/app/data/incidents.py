# app/data/incidents.py


import pandas as pd
from app.data.db import connect_database

def get_all_incidents():
    conn = None
    try:
        conn = connect_database()
        df = pd.read_sql_query(
            "SELECT * FROM cyber_incidents ORDER BY id DESC",
            conn
        )
        return df
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
    finally:
        if conn:                    # ← Properly close connection
            conn.close()

# In insert_incident function
def insert_incident(incident):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (incident.date, incident.type, incident.severity, incident.status, incident.description, incident.reporter))
    conn.commit()
    conn.close()
