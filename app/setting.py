""" Load settings from a JSON file."""
import json
import logging
from pathlib import Path


class Setting:
    """load settings from a JSON file."""

    DEFAULT_LOG_FILE = "backup_manager.log"
    DEFAULT_DATABASE = "backup_tasks.sqlite"

    def __init__(self, settings_file="settings.json"):
        self.parent_dir = Path(__file__).resolve().parent
        self.settings_file = self.parent_dir / settings_file
        self.log_file, self.database = self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                settings = json.load(file)
            log_file = settings.get("log_file", self.DEFAULT_LOG_FILE)
            database = settings.get("database", self.DEFAULT_DATABASE)
            return self.parent_dir.parent / log_file, self.parent_dir.parent / database
        except FileNotFoundError:
            logging.error("Failed to load configuration: %s not found", self.settings_file)
        except Exception as e:
            logging.error("Failed to load configuration: %s", e)
        return None, None
