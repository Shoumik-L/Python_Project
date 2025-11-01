import os
import csv
import re

def generate_id(filename):
    """Generates the next ID even if it has prefixes like D001 or W010."""
    if not os.path.exists(filename):
        return 1

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        rows = list(reader)
        if not rows:
            return 1

        last_id = rows[-1][0]

        # Try to extract number part (like 'W010' -> 10)
        match = re.search(r'(\d+)$', last_id)
        if match:
            return int(match.group(1)) + 1
        else:
            # if no number found, fallback
            return 1
