""" Create or destroy the database. """
import argparse

from app.database_manager import DatabaseManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create or destroy the database.")
    parser.add_argument("action", choices=["create", "destroy"], help="Create or destroy the database.")
    args = parser.parse_args()

    db_manager = DatabaseManager()

    if args.action == "create":
        # if database exists ask if drop it and create a new one
        if (
            db_manager.database_file.exists()
            and input(f"{db_manager.database_file} already exists. Do you want to drop it and create a new one? (Y/n)")
            != "Y"
        ):
            exit()
        else:
            db_manager.destroy()
        db_manager.create()
    elif args.action == "destroy":
        # confirm before destroying the database
        if (
            db_manager.database_file.exists()
            and input(f"Are you sure you want to destroy {db_manager.database_file}? (Y/n) ") != "Y"
        ):
            exit()
        else:
            db_manager.destroy()
