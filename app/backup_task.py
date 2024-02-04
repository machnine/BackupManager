""" Get tasks from db """
import json
import logging
import sqlite3

from .setting import Setting


class BackupTask:
    """Backup task class"""

    VALID_TASK_TYPES = {"mssql", "file"}
    VALID_SCHEDULE_TYPES = {"daily", "weekly", "monthly"}

    def __init__(
        self, task_name, task_type, schedule_type, enabled, task_id=None, source: dict = None, destination=None
    ):
        """Initialize a new BackupTask instance."""

        # Validate the task type and schedule type
        self.validate_task_type(task_type)
        self.validate_schedule_type(schedule_type)

        self.task_id = task_id
        self.task_name = task_name.lower()
        self.task_type = task_type.lower()
        self.schedule_type = schedule_type.lower()
        self.enabled = enabled
        self.source = source or {}
        self.destination = destination

    @staticmethod
    def validate_task_type(task_type):
        """Validate the task type."""
        if task_type.lower() not in BackupTask.VALID_TASK_TYPES:
            raise ValueError("Invalid task_type, must be 'mssql' or 'file'")

    @staticmethod
    def validate_schedule_type(schedule_type):
        """Validate the schedule type."""
        if schedule_type.lower() not in BackupTask.VALID_SCHEDULE_TYPES:
            raise ValueError("Invalid schedule_type, must be 'daily', 'weekly', or 'monthly'")

    def save(self):
        """Save the task to the database."""
        try:
            with sqlite3.connect(Setting().database) as conn:
                cursor = conn.cursor()
                self.insert_task(cursor)
        except Exception as e:
            logging.error("Error saving BackupTask to database: %s", e)

    def insert_task(self, cursor):
        """Insert the common task information into the database."""
        cursor.execute(
            """
            INSERT INTO tasks (task_name, task_type, schedule_type, source, destination, enabled)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                self.task_name,
                self.task_type,
                self.schedule_type,
                self.source,
                self.destination,
                self.enabled,
            ),
        )
        self.task_id = cursor.lastrowid

    @classmethod
    def get_all(cls, active_only=True):
        """Retrieve all tasks from the database, optionally filtering by active status."""
        tasks = []
        with sqlite3.connect(Setting().database) as conn:
            cursor = conn.cursor()
            condition = "WHERE enabled = 1" if active_only else ""
            cursor.execute(f"""SELECT * FROM tasks {condition}""")
            rows = cursor.fetchall()
            fields = [f[0] for f in cursor.description]
            for row in rows:
                task_data = dict(zip(fields, row))
                task_data["source"] = json.loads(task_data["source"])
                tasks.append(cls(**task_data))
        return tasks

    @classmethod
    def get_by_id(cls, task_id):
        """Retrieve a task by its id."""
        with sqlite3.connect(Setting().database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM tasks WHERE task_id = {task_id}""")
            row = cursor.fetchone()
            fields = [f[0] for f in cursor.description]
            task_data = dict(zip(fields, row))
            task_data["source"] = json.loads(task_data["source"])
            return cls(**task_data)

    @classmethod
    def delete_by_id(cls, task_id):
        """Delete a task by its id."""
        with sqlite3.connect(Setting().database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""DELETE FROM tasks WHERE task_id = {task_id}""")
            conn.commit()

    def __str__(self):
        """String representation of the BackupTask."""
        # self.task_type has fixed length of 6 characters
        return f"BackupTask: {self.task_id}\t{self.task_type}\t{self.schedule_type}\t{'A' if self.enabled else '-'}\t'{self.task_name}'"

    def __repr__(self):
        """Representation of the BackupTask."""
        return str(self)
