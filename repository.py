import sqlite3
from contextlib import closing


class ContactRepository:
    def __init__(self, database_path: str = "data/contacts.db"):
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._initialize()

    def _initialize(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    mobile TEXT,
                    landline TEXT,
                    address TEXT,
                    notes TEXT
                )
                """
            )
            self.connection.commit()

    def create(
        self,
        first_name,
        last_name,
        mobile,
        landline,
        address,
        notes,
    ):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                """
                INSERT INTO contacts
                (
                    first_name,
                    last_name,
                    mobile,
                    landline,
                    address,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    first_name,
                    last_name,
                    mobile,
                    landline,
                    address,
                    notes,
                ),
            )
            self.connection.commit()
            return cursor.lastrowid

    def update(
        self,
        contact_id,
        first_name,
        last_name,
        mobile,
        landline,
        address,
        notes,
    ):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                """
                UPDATE contacts
                SET
                    first_name=?,
                    last_name=?,
                    mobile=?,
                    landline=?,
                    address=?,
                    notes=?
                WHERE id=?
                """,
                (
                    first_name,
                    last_name,
                    mobile,
                    landline,
                    address,
                    notes,
                    contact_id,
                ),
            )
            self.connection.commit()

    def remove(self, contact_id):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM contacts WHERE id=?",
                (contact_id,),
            )
            self.connection.commit()

    def remove_all(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM contacts")
            self.connection.commit()

    def fetch(self, contact_id):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT * FROM contacts WHERE id=?",
                (contact_id,),
            )
            return cursor.fetchone()

    def fetch_all(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM contacts
                ORDER BY last_name, first_name
                """
            )
            return cursor.fetchall()

    def search(self, keyword):
        expression = f"%{keyword}%"

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM contacts
                WHERE
                    first_name LIKE ?
                    OR last_name LIKE ?
                    OR mobile LIKE ?
                    OR landline LIKE ?
                    OR address LIKE ?
                    OR notes LIKE ?
                ORDER BY last_name, first_name
                """,
                (
                    expression,
                    expression,
                    expression,
                    expression,
                    expression,
                    expression,
                ),
            )
            return cursor.fetchall()

    def total(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT COUNT(*) FROM contacts")
            return cursor.fetchone()[0]

    def close(self):
        self.connection.close()