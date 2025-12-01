from pathlib import Path

import pandas as pd

from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import (
    register_user,
    login_user,
    migrate_users_from_file,   # ← you had a typo in the import
)
from app.data.incidents import insert_incident, get_all_incidents


def main() -> None:
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    try:
        create_all_tables(conn)
        print("Database tables ready")
    finally:
        conn.close()


    # 2. Migrate legacy users (from CSV/JSON/etc.)

    print("\nMigrating users …")
    migrate_users_from_file()
    print("User migration completed")


    # 3. Test authentication
    print("\nTesting registration & login …")
    success, msg = register_user("alice", "SecurePass123!", role="analyst")
    print(f"Register alice → {msg}")

    success, msg = login_user("alice", "SecurePass123!")
    print(f"Login alice    → {msg if success else 'Failed: ' + msg}")

    # 4. Test incident creation
    print("\nCreating a new incident …")
    incident_id = insert_incident(
        reported_date="2024-11-05",
        incident_type="Phishing",
        severity="High",
        status="Open",
        description="Suspicious email detected",
        reported_by="alice",
    )

    if incident_id:
        print(f"Created incident #{incident_id}")
    else:
        print("Incident creation failed")

    # 5. Query all incidents
    print("\nFetching all incidents …")
    df: pd.DataFrame = get_all_incidents()

    if not df.empty:
        print(f"Total incidents in database: {len(df)}")
        # Pretty-print the first few rows
        print(df.head().to_string(index=False))
    else:
        print("No incidents found.")

if __name__ == "__main__":
    main()