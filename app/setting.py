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


class ColorText:
    """Color class for printing colored text in terminal."""

    colors = {
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "RESET": "\033[0m",
    }

    @classmethod
    def message(cls, message: str, color: str = "RESET"):
        """Print message with color."""
        RESET = cls.colors["RESET"]
        color = cls.colors[color.upper()]
        return f"{color}{message}{RESET}"
