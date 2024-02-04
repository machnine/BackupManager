""" Command line tool for task management """

import argparse
import json

from app import BackupTask, ColorText


def list_tasks():
    tasks = BackupTask.get_all(False)
    print(ColorText.message("\n==== Tasks ====\n", "CYAN"))
    for task in tasks:
        print(task)


def delete_task():
    task_id = input("Please input the task id: ")
    if task := BackupTask.get_by_id(task_id):
        if input(f"Are you sure you want to delete {task}? (Y/n) ") == "Y":
            BackupTask.delete_by_id(task_id)
            print(f"{task} deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print(f"Task id {task_id} not found.")


def add_task():
    print(ColorText.message("\n==== Add a new backup task ====\n", "CYAN"))
    task_name = input("Please input the task name: ")
    schedule_type = input("Please input the schedule type (daily/weekly/monthly): ")
    task_type = input("Please input the task type (file/mssql): ")

    if task_type.lower() == "file":
        source_path = input("Please input the source file path: ")
        source_input = {"source_path": source_path}
    elif task_type.lower() == "mssql":
        server = input("Please input the database server: ")
        database = input("Please input the database name: ")
        username = input("Please input the username: ")
        password = input("Please input the password: ")
        source_input = {"server": server, "database": database, "username": username, "password": password}
    else:
        print("Invalid task type. Must be 'file' or 'mssql'.")
        return

    destination = input("Please input the destination path: ")
    enabled = input("Please input the enabled status (0/1): ")

    try:
        task = BackupTask(
            task_name=task_name,
            task_type=task_type,
            schedule_type=schedule_type,
            source=json.dumps(source_input),
            destination=destination,
            enabled=bool(int(enabled)),
        )
        task.save()
        print(f"{task} added.")
    except ValueError as e:
        print(f"Error adding task: {e}")


def main():
    parser = argparse.ArgumentParser(description="Backup task manager")
    parser.add_argument("-l", "--list", action="store_true", help="list all backup tasks")
    parser.add_argument("-a", "--add", action="store_true", help="add a new backup task")
    parser.add_argument("-d", "--delete", action="store_true", help="delete a backup task")

    args = parser.parse_args()

    if args.list:
        list_tasks()
    elif args.delete:
        delete_task()
    elif args.add:
        add_task()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
