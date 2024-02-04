# BackupManager
## Script for backing up databases and files

## Create database
```bash
python database.py create
```

## Delete database
```bash
python database.py delete
```

## Manage (list/create/delete) backup tasks
```bash
python task.py
```

## Run the backup
```bash
python main.py
```

## NB
- The MSSQL backup uses sqlcmd which can be downloaded from https://github.com/microsoft/go-sqlcmd/releases
- sqlcmd does not have awareness of the computer where this Python script is running from. 'Local' backup destination is located on the machine where the MS SQL server running. If using network locations, make sure appropriate permission is given to the account running the SQL Server instance.