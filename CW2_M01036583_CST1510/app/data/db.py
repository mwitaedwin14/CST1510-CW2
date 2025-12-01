import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database.
       Creates the database file if it doesn't exist.

       Args:
           db_path: Path to the database file
       Returns:
           sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(str(db_path))

def create_users_table(conn):
    """
    Create the users table if it doesn't exist.

    This is a COMPLETE IMPLEMENTATION as an example.
    Study this carefully before implementing the other tables!

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    #SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user', 
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("Users table created successfully!")