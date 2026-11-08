import re
from collections import Counter

def read_errors(path):
    
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+\|\s+(\w+)\s+\|\s+(.*)$')
    malformed_count = 0

    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if not match:
                malformed_count += 1
                continue
            timestamp, level, message = match.groups()
            if level == "ERROR":
                yield (line_num, timestamp, message)

def summarize_errors(path):
    error_counts = Counter()
    for _, timestamp, _ in read_errors(path):
        date_str = timestamp.split()[0]
        error_counts[date_str] += 1
    return dict(error_counts)