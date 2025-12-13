# app/data/datasets.py  ← THIS FIXES YOUR ERROR
import pandas as pd
from app.data.db import connect_database

# For datasets.py
def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df

def insert_dataset(name, category, source, last_updated, record_count, file_size_mb):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    conn.close()