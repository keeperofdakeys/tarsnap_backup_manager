#!/usr/bin/env python3

def main():
    backups = []
    for backup_str in backup_names:
        try:
            (name, date) = BackupEntry.parse_name(backup_str)
        except InvalidBackupNameException:
            continue
        backups.append(BackupEntry(name,date))

    backups.sort()

