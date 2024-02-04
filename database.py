""" Create or delete the database. """
import argparse

from app import ColorText, DatabaseManager


def create_database(db_manager, db_filename):
    if db_manager.database_file.exists():
        if user_wants_to_continue(f"Delete {db_filename}?"):
            db_manager.delete()
            print(ColorText.message(f"\nOld {db_filename} deleted successfully.", "GREEN"))
        else:
            print(ColorText.message("\nCancelled.", "RED"))
            exit()
    db_manager.create()
    print(ColorText.message(f"\nNew {db_filename} created successfully.", "GREEN"))


def delete_database(db_manager, db_filename):
    if not db_manager.database_file.exists():
        print(ColorText.message(f"\n{db_filename} doesn't exist.", "RED"))
        exit()
    if user_wants_to_continue(f"Delete {db_filename}?"):
        db_manager.delete()
        print(ColorText.message(f"\n{db_filename} deleted successfully.", "GREEN"))
    else:
        print(ColorText.message("\nCancelled.", "RED"))
        exit()


def user_wants_to_continue(question):
    response = input(f"{question} ({ColorText.message('Y', 'BLUE')}/n) ")
    return response == "Y"


def main():
    parser = argparse.ArgumentParser(description="Create or delete the database.")
    parser.add_argument("action", choices=["create", "delete"], help="Create or delete the database.")
    args = parser.parse_args()

    db_manager = DatabaseManager()
    db_filename = db_manager.database_file.name

    if args.action == "create":
        create_database(db_manager, db_filename)
    elif args.action == "delete":
        delete_database(db_manager, db_filename)


if __name__ == "__main__":
    main()
