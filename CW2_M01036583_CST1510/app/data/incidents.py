# app/data/incidents.py
# FINAL FIXED VERSION — NO MORE ERRORS

import pandas as pd
from app.data.db import connect_database   # ← This is a FUNCTION, not a class!

def get_all_incidents():
    conn = None
    try:
        conn = connect_database()   # ← CALL THE FUNCTION, don't do .connect()
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

def insert_incident(date, incident_type, severity, status, description, reported_by="unknown"):
    conn = None
    try:
        conn = connect_database()   # ← Correct way
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cyber_incidents 
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(date), incident_type, severity, status, description, reported_by))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Insert failed: {e}")
        return None
    finally:
        if conn:
            conn.close()
