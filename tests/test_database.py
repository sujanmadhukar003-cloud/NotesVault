import unittest

from database import get_db_connection


class DatabaseFallbackTests(unittest.TestCase):
    def test_sqlite_fallback_works(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 AS one")
        self.assertEqual(cursor.fetchone(), (1,))
        conn.close()


if __name__ == "__main__":
    unittest.main()
