"""
This application is a backup manager that runs backups for multiple applications. 
"""
import logging
import shutil
import subprocess
import threading
from datetime import datetime
from pathlib import Path

from .backup_task import BackupTask

RETENTION_COUNT = 7  # Number of daily backups to keep


class BackupManager:
    """Backup manager."""

    def __init__(self):
        self.tasks = BackupTask.get_all()
        self.date_stamp = datetime.now().strftime("%Y%m%d%H%M%S")

    def is_backup_due(self, task):
        """
        Check if a backup is due to run for the given task.
        """
        if task.schedule_type == "daily":
            return True
        elif task.schedule_type == "weekly" and datetime.today().weekday() == 0:
            return True
        elif task.schedule_type == "monthly" and datetime.today().day == 1:
            return True
        return False

    def perform_backup(self, task):
        """Perform a backup for the given task."""
        backup_methods = {"mssql": self.mssql_backup, "file": self.file_backup}
        try:
            backup_methods[task.task_type](task)
            # remove old copies of daily backups
            if task.schedule_type == "daily":
                self.cleanup_old_backups(task.destination)
        except KeyError:
            logging.error("Unknown task type for task %s", task.task_name)
        except Exception as e:
            logging.error("Error performing [%s] backup task %s: %s", task.task_type, task.task_name, e)

    def run_backups(self):
        """Run all due backups."""
        threads = [
            threading.Thread(target=self.perform_backup, args=(task,))
            for task in self.tasks
            if self.is_backup_due(task)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def file_backup(self, task):
        """
        Backup the file with the latest backup information.
        """
        source_path = Path(task.source["source_path"])
        destination_path = Path(task.destination)
        # Create the backup path if it doesn't exist
        destination_path.mkdir(parents=True, exist_ok=True)
        destination_name = source_path.stem + "_" + self.date_stamp

        try:
            self._copy_files(source_path, destination_path, destination_name)
            logging.info("File task [%s] completed successfully", task.task_name)
        except Exception as e:
            logging.error("File task [%s] failed: %s", task.task_name, e)

    def _copy_files(self, source, destination, dest_name):
        """Helper function to copy files or directories."""
        if source.is_dir():
            shutil.copytree(source, destination / dest_name)
        else:
            destination_file = destination / (dest_name + source.suffix)
            shutil.copy2(source, destination_file)

    def mssql_backup(self, task):
        """Backup the MSSQL database directly to the network location."""
        backup_file = task.source["database"] + "_" + self.date_stamp + ".bak"
        backup_path = Path(task.destination) / backup_file
        backup_command = self._construct_mssql_backup_command(task, backup_path)

        try:
            subprocess.run(backup_command, check=True, shell=True)
            logging.info("Database backup for task %s completed successfully.", task.task_name)
        except Exception as e:
            logging.error("Database backup for task %s failed: %s", task.task_name, e)

    def _construct_mssql_backup_command(self, task, backup_file):
        """
        Construct the MSSQL backup command.
        """
        server = task.source["server"]
        database = task.source["database"]
        username = task.source["username"]
        password = task.source["password"]
        sqlcmd = (
            f'sqlcmd -S {server} -U {username} -P "{password}" '
            f"-Q \"BACKUP DATABASE {database} TO DISK = '{backup_file}' WITH FORMAT\""
        )
        return sqlcmd

    def cleanup_old_backups(self, destination_path):
        """Keep only the latest RETENTION_COUNT backup files/folders in the destination path."""
        destination = Path(destination_path)
        if not destination.exists():
            logging.warning("Destination path %s does not exist. Backup Manager is not able to delete older files", destination_path)
            return

        # List all files and directories in the destination directory
        all_backups = list(destination.iterdir())

        # Sort backups by their creation time (or modified time), oldest first
        all_backups.sort(key=lambda x: x.stat().st_mtime)

        # If the number of backups exceeds the retention count, delete the oldest
        for backup in all_backups[:-RETENTION_COUNT]:
            try:
                if backup.is_dir():
                    shutil.rmtree(backup)
                else:
                    backup.unlink()
                logging.info("Deleted old backup: %s", backup)
            except Exception as e:
                logging.error("Failed to delete old backup %s: %s", backup, e)
