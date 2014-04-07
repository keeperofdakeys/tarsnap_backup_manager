#!/usr/bin/env python3

from datetime import datetime

class InvalidBackupNameException(Exception):
        pass

class BackupEntry():
    def __init__(self, name, type_name, date):
        self.name = name
        self.type_name = type_name
        self.date = date
    
    def __lt__(self, other):
        return self.date < other.date
    
    def __le__(self, other):
        return self.date <= other.date
    
    def __eq__(self, other):
        return self.date == other.date
    
    def __gt__(self, other):
        return self.date > other.date
    
    def __ge__(self, other):
        return self.date >= other.date
    
    @staticmethod
    def parse_name(name):
        """Parse a backup name, return name and date parts if valid.
        Otherwise raise InvalidBackupNameException."""
        parts = name.split("_")
        if len(parts) < 4:
            raise InvalidBackupNameException()
        type_name = "_".join(parts[:-3])
        date_str = '_'.join(parts[-3:])
        try:
            date = datetime.strptime(date_str, "%d_%m_%y")
        except ValueError:
            raise InvalidBackupNameException()
        return BackupEntry(name, type_name, date)
