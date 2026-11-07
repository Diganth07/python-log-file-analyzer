"""Summarize common plain-text log files using only Python's standard library."""

import argparse
import re
from collections import Counter
from pathlib import Path

LEVELS = ("CRITICAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG")
LEVEL_PATTERN = re.compile(r"\b(CRITICAL|ERROR|WARNING|WARN|INFO|DEBUG)\b", re.IGNORECASE)


def analyze(path: Path) -> tuple[int, Counter[str], Counter[str]]:
    counts: Counter[str] = Counter()
    messages: Counter[str] = Counter()
    total = 0
    with path.open(encoding="utf-8", errors="replace") as log:
        for line in log:
            total += 1
            match = LEVEL_PATTERN.search(line)
            level = match.group(1).upper() if match else "OTHER"
            counts[level] += 1
            message = line.strip()
            if match:
                message = message[match.end():].strip(" :-\t")
            if message:
                messages[message] += 1
    return total, counts, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize levels and repeated messages in a log file.")
    parser.add_argument("file", type=Path, help="Path to a plain-text log file")
    parser.add_argument("--top", type=int, default=5, help="Number of frequent messages to show")
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top must be zero or greater")
    if not args.file.is_file():
        parser.error(f"not a file: {args.file}")

    total, counts, messages = analyze(args.file)
    print(f"\nLog summary: {args.file}")
    print(f"Total lines: {total}")
    print("\nLines by level:")
    for level in (*LEVELS, "OTHER"):
        if counts[level]:
            print(f"  {level:<10} {counts[level]}")
    if args.top:
        print(f"\nTop {min(args.top, len(messages))} messages:")
        for message, count in messages.most_common(args.top):
            print(f"  {count:>4}x  {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
