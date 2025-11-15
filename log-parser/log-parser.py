import re
import json
import argparse
from pathlib import Path

log_pattern = re.compile(r"^(?P<timestamp>\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*-\s*(?P<level>\w+)\s*-\s*(?P<message>.+)$")

def read_log_file(filepath: str):
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {filepath}")
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line: 
                yield line

def parse_log_entry(line: str, pattern: re.Pattern) -> dict | None:
    match = pattern.match(line)
    if match: 
        return match.groupdict()
    return None

def parse_log_file(filepath, pattern):
    for line in read_log_file(filepath):
        parsed_data = parse_log_entry(line, pattern)
        if parsed_data: 
            yield parsed_data
            
def filter_entries(entries, level=None, contains=None):
    
    for entry in entries:
        if level and entry.get("level") != level:
            continue
        if contains and contains not in entry.get("message", ""):
            continue
        yield entry
        
def summarize_entries(entries):
    stats = {
        "total": 0,
        "by_level": {},
        "first_timestamp": None,
        "last_timestamp": None,
    }
    
    for entry in entries:
        stats["total"] += 1
        
        level = entry.get("level", "UNKNOWN")
        stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
        
        ts = entry.get("timestamp")
        if ts:
            if stats["first_timestamp"] is None:
                stats["first_timestamp"] = ts
            stats["last_timestamp"] = ts
            
    return stats

def main():
    parser = argparse.ArgumentParser(description="simple log parser.")
    parser.add_argument("logfile", help="path to the log file to parser")
    parser.add_argument("--contains", help="filter messages that contain this text")
    parser.add_argument("--level", help="filter by log level (INFO, ERROR)")
    parser.add_argument("--summary", action="store_true", help="print summary instead of raw entries")
    args = parser.parse_args()

    entries = parse_log_file(args.logfile, log_pattern)
    
    entries = filter_entries(entries, level=args.level, contains=args.contains)
    
    if args.summary:
        stats = summarize_entries(entries)
        print(json.dumps(stats, indent=2))
    else:
        for entry in entries: 
            print(json.dumps(entry))

if __name__ == "__main__":
    main()