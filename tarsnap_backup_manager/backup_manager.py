#!/usr/bin/env python3

from backup_entry import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

class Bins():
    def __init__(self):
        self.bins = {}

    def append(self, key, entry):
        if not self.bins.has_key(key):
            self.bins[key] = []
        self.bins[key].append(entry)

    def bin_size(self, key):
        if not self.bins.has_key(key):
            return 0
        else:
            return len(self.bins[key])

    def bin_em_range(self, entries, to_remove, limit, end_period, key_func):
        outside_range = False
        while not outside_range and len(entries) > 0:
            elem = entries.pop()
            elem_key = key_func(elem)
            if limit == 0 or self.bin_size(elem_key) < limit:
                self.append(elem_key, elem)
            else:
                to_remove.append(elem)
            if elem.date + end_period > datetime.utcnow():
                outside_range = True


    def bin_em(self, entries, to_remove, classifiers):
        backups = list(entries)
        backups.sort(reverse=True)
        for values in classifiers:
            self.bin_em_range(backups, to_remove, values[0], values[1], values[2])

    def print_em(self):
        for x in self.bins.values():
            for y in x:
                print y.name
        

def main():
    getting_input = True
    backups = []
    to_remove = []
    backup_names = []
    while getting_input:
        try:
            line = raw_input()
        except EOFError:
            getting_input = False
        if line == '':
            getting_input = False
        backup_names.append(line)
    for backup_str in backup_names:
        try:
            backup = BackupEntry.parse_name(backup_str)
        except InvalidBackupNameException:
            continue
        backups.append(backup)
    classifiers = [
            # 1 per year before six months
            (1, relativedelta(months=6), lambda elem: "%s_year_%s" % (elem.type_name, elem.date.year)),
            # 1 per month before one month
            (1, relativedelta(months=1), lambda elem: "%s_month_%s" % (elem.type_name, elem.date.month)),
            (1, relativedelta(weeks=1), lambda elem: "%s_5_days_%s" % (elem.type_name, elem.date.day//5)),
            (0, relativedelta(seconds=0), lambda elem: "%s_last_days" % elem.type_name)
            ]
    bins = Bins()
    bins.bin_em(backups, to_remove, classifiers)
    for x in to_remove:
        print x.name 
    #bins.print_em()

if __name__ == "__main__":
    main()
