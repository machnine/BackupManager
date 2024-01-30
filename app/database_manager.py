"""Tasks database manager."""
import sqlite3

from app.setting import Setting


class DatabaseManager:
    """Create and destroy the database."""

    def __init__(self):
        """Initialize the database manager."""
        self.database_file = Setting().database

    def create(self):
        """Create the database."""
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.cursor()
            cursor.execute(self.get_schema_definition())

    def destroy(self):
        """Destroy the tables and view in database."""
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE tasks")

    def get_schema_definition(self):
        """Return the schema definitions."""
        return """
            CREATE TABLE tasks (
                task_id INTEGER PRIMARY KEY,
                task_name TEXT,
                task_type TEXT,
                schedule_type TEXT,
                source TEXT,
                destination TEXT,
                enabled BOOLEAN
            );"""
