import csv

def read_csv_files(paths):
    rows = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows.extend(reader)
    return rows