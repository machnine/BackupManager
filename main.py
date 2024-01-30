""" main """
import logging

from app.backup_manager import BackupManager
from app.setting import Setting

if __name__ == "__main__":
    # set up logging to file
    logging.basicConfig(
        filename=Setting().log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    BackupManager().run_backups()
