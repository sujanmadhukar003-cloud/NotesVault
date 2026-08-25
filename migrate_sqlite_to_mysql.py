import sqlite3
import mysql.connector
from getpass import getpass
from datetime import datetime


SQLITE_DB = "notes.db"

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "notevault"
MYSQL_USER = "root"


def convert_datetime(value):
    """
    Convert SQLite datetime strings into Python datetime objects.
    Leave NULL values as NULL.
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def main():

    mysql_password = getpass("Enter MySQL root password: ")

    print("\nConnecting to SQLite...")

    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_cursor = sqlite_conn.cursor()

    print("Connecting to MySQL...")

    mysql_conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=mysql_password
    )

    mysql_cursor = mysql_conn.cursor()

    print("Connected successfully.\n")

    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------

    tables = [
        "notes",
        "topic_sections",
        "problem_bank",
        "resources",
        "announcements",
        "feedback",
        "unit_resources"
    ]

    for table in tables:

        mysql_cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = mysql_cursor.fetchone()[0]

        if count != 0:
            raise RuntimeError(
                f"Table '{table}' is not empty. "
                f"Migration stopped for safety."
            )

    try:

        # --------------------------------------------------
        # NOTES
        # --------------------------------------------------

        print("Migrating notes...")

        sqlite_cursor.execute("""
            SELECT
                id,
                semester,
                subject,
                unit,
                topic,
                content,
                definition,
                example,
                image_path,
                topic_order
            FROM notes
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        mysql_cursor.executemany("""
            INSERT INTO notes (
                id,
                semester,
                subject,
                unit,
                topic,
                content,
                definition,
                example,
                image_path,
                topic_order
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, rows)

        print(f"  {len(rows)} notes migrated.")


        # --------------------------------------------------
        # TOPIC SECTIONS
        # --------------------------------------------------

        print("Migrating topic sections...")

        sqlite_cursor.execute("""
            SELECT
                id,
                topic_id,
                section_title,
                section_content,
                image_path,
                section_order
            FROM topic_sections
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        # Get all valid topic IDs from MySQL
        mysql_cursor.execute("SELECT id FROM notes")
        valid_topic_ids = {
            row[0]
            for row in mysql_cursor.fetchall()
        }

        # Preserve orphan sections, but remove their invalid relationship
        fixed_rows = []

        orphan_sections = 0

        for row in rows:

            section_id = row[0]
            topic_id = row[1]

            if topic_id not in valid_topic_ids:
                topic_id = None
                orphan_sections += 1

            fixed_rows.append((
                section_id,
                topic_id,
                row[2],
                row[3],
                row[4],
                row[5]
            ))

        mysql_cursor.executemany("""
            INSERT INTO topic_sections (
                id,
                topic_id,
                section_title,
                section_content,
                image_path,
                section_order
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, fixed_rows)

        print(f"  {len(fixed_rows)} sections migrated.")
        print(f"  {orphan_sections} orphan sections had topic_id set to NULL.")


        # --------------------------------------------------
        # PROBLEM BANK
        # --------------------------------------------------

        sqlite_cursor.execute("""
            SELECT
                id,
                topic_id,
                problem,
                solution,
                problem_order
            FROM problem_bank
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        fixed_rows = []

        orphan_problems = 0

        for row in rows:

            problem_id = row[0]
            topic_id = row[1]

            if topic_id not in valid_topic_ids:
                topic_id = None
                orphan_problems += 1

            fixed_rows.append((
                problem_id,
                topic_id,
                row[2],
                row[3],
                row[4]
            ))

        mysql_cursor.executemany("""
            INSERT INTO problem_bank (
                id,
                topic_id,
                problem,
                solution,
                problem_order
            )
            VALUES (%s, %s, %s, %s, %s)
        """, fixed_rows)

        print(f"  {len(fixed_rows)} problems migrated.")
        print(f"  {orphan_problems} orphan problems had topic_id set to NULL.")


        # --------------------------------------------------
        # RESOURCES
        # --------------------------------------------------

        print("Migrating resources...")

        sqlite_cursor.execute("""
            SELECT
                id,
                semester,
                subject,
                unit,
                type,
                file_path
            FROM resources
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        mysql_cursor.executemany("""
            INSERT INTO resources (
                id,
                semester,
                subject,
                unit,
                type,
                file_path
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, rows)

        print(f"  {len(rows)} resources migrated.")


        # --------------------------------------------------
        # ANNOUNCEMENTS
        # --------------------------------------------------

        print("Migrating announcements...")

        sqlite_cursor.execute("""
            SELECT
                id,
                title,
                message,
                created_at
            FROM announcements
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        rows = [
            (
                row[0],
                row[1],
                row[2],
                convert_datetime(row[3])
            )
            for row in rows
        ]

        mysql_cursor.executemany("""
            INSERT INTO announcements (
                id,
                title,
                message,
                created_at
            )
            VALUES (%s, %s, %s, %s)
        """, rows)

        print(f"  {len(rows)} announcements migrated.")


        # --------------------------------------------------
        # FEEDBACK
        # --------------------------------------------------

        print("Migrating feedback...")

        sqlite_cursor.execute("""
            SELECT
                id,
                name,
                subject,
                issue_type,
                message,
                created_at
            FROM feedback
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        rows = [
            (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                convert_datetime(row[5])
            )
            for row in rows
        ]

        mysql_cursor.executemany("""
            INSERT INTO feedback (
                id,
                name,
                subject,
                issue_type,
                message,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, rows)

        print(f"  {len(rows)} feedback records migrated.")


        # --------------------------------------------------
        # UNIT RESOURCES
        # --------------------------------------------------

        print("Migrating unit resources...")

        sqlite_cursor.execute("""
            SELECT
                id,
                semester,
                subject,
                unit,
                resource_type,
                title,
                file_path
            FROM unit_resources
            ORDER BY id
        """)

        rows = sqlite_cursor.fetchall()

        mysql_cursor.executemany("""
            INSERT INTO unit_resources (
                id,
                semester,
                subject,
                unit,
                resource_type,
                title,
                file_path
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, rows)

        print(f"  {len(rows)} unit resources migrated.")


        # --------------------------------------------------
        # COMMIT
        # --------------------------------------------------

        mysql_conn.commit()

        print("\nMigration completed successfully!")


    except Exception as e:

        print("\nERROR:")
        print(e)

        print("\nRolling back MySQL transaction...")

        mysql_conn.rollback()

        raise


    finally:

        sqlite_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

        print("\nConnections closed.")


if __name__ == "__main__":
    main()