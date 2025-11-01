import csv
import os

def read_data(filename):
    data = []
    if os.path.exists(filename):
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def write_data(filename, fieldnames, data):
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_data(filename, fieldnames, new_row):
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)
